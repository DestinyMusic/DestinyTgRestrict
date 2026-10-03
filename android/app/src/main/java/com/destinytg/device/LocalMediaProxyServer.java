package com.destinytg.device;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.RandomAccessFile;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

final class LocalMediaProxyServer implements AutoCloseable {
    private static final int BUFFER_SIZE = 64 * 1024;
    private static final Pattern RANGE_PATTERN = Pattern.compile("bytes=(\\d*)-(\\d*)");

    private final Context context;
    private final Uri localUri;
    private final String remoteUrl;
    private final String mimeType;
    private final ExecutorService requests = Executors.newCachedThreadPool();
    private ServerSocket serverSocket;
    private Thread acceptThread;
    private volatile boolean running;

    private LocalMediaProxyServer(Context context, Uri localUri,
                                  String remoteUrl, String mimeType) {
        this.context = context.getApplicationContext();
        this.localUri = localUri;
        this.remoteUrl = remoteUrl;
        this.mimeType = mimeType == null || mimeType.isEmpty()
                ? "application/octet-stream" : mimeType;
    }

    static LocalMediaProxyServer forRemoteUrl(Context context, String url, String mimeType)
            throws IOException {
        URI parsed = URI.create(url);
        if (!("http".equalsIgnoreCase(parsed.getScheme())
            || "https".equalsIgnoreCase(parsed.getScheme())) || parsed.getHost() == null) {
            throw new IllegalArgumentException("Only HTTP(S) media URLs are supported");
        }
        return new LocalMediaProxyServer(context, null, url, mimeType);
    }

    static LocalMediaProxyServer forLocalUri(Context context, Uri uri, String mimeType)
            throws IOException {
        if (uri == null) throw new IllegalArgumentException("No local media URI was provided");
        if ("file".equalsIgnoreCase(uri.getScheme())) {
            File file = new File(uri.getPath());
            if (!file.isFile()) throw new IOException("The local media file is unavailable");
        } else {
            try (AssetFileDescriptor descriptor = context.getContentResolver()
                    .openAssetFileDescriptor(uri, "r")) {
                if (descriptor == null) throw new IOException("Cannot open local media source");
            }
        }
        return new LocalMediaProxyServer(context, uri, null, mimeType);
    }

    void start() throws IOException {
        serverSocket = new ServerSocket(0, 16, InetAddress.getByName("127.0.0.1"));
        running = true;
        acceptThread = new Thread(this::acceptRequests, "destiny-local-media-proxy");
        acceptThread.setDaemon(true);
        acceptThread.start();
    }

    String getUrl() {
        if (serverSocket == null) throw new IllegalStateException("Media proxy is not ready");
        return "http://127.0.0.1:" + serverSocket.getLocalPort() + "/media";
    }

    private void acceptRequests() {
        while (running) {
            try {
                Socket socket = serverSocket.accept();
                requests.execute(() -> serve(socket));
            } catch (IOException exception) {
                if (running) close();
            }
        }
    }

    private void serve(Socket socket) {
        try (Socket client = socket;
             BufferedInputStream input = new BufferedInputStream(client.getInputStream());
             BufferedOutputStream output = new BufferedOutputStream(client.getOutputStream())) {
            String requestLine = readLine(input);
            if (requestLine == null) return;
            String[] request = requestLine.split(" ", 3);
            if (request.length < 2) {
                writeResponse(output, 400, "Bad Request", "Content-Length: 0\r\n");
                return;
            }
            boolean head = "HEAD".equalsIgnoreCase(request[0]);
            boolean options = "OPTIONS".equalsIgnoreCase(request[0]);
            if (options) {
                writeResponse(output, 204, "No Content",
                    "Content-Length: 0\r\nAccess-Control-Allow-Private-Network: true\r\n");
                return;
            }
            if (!head && !"GET".equalsIgnoreCase(request[0])) {
                writeResponse(output, 405, "Method Not Allowed",
                    "Allow: GET, HEAD, OPTIONS\r\nContent-Length: 0\r\n");
                return;
            }
            Map<String, String> headers = readHeaders(input);
            String range = headers.getOrDefault("range", "");
            if (remoteUrl != null) serveRemote(output, request[0], range);
            else serveLocal(output, head, range);
        } catch (Exception ignored) {
            // Players close range requests routinely when seeking or changing tracks.
        }
    }

    private void serveRemote(BufferedOutputStream output, String method, String range)
            throws IOException {
        HttpURLConnection connection = null;
        try {
            connection = (HttpURLConnection) URI.create(remoteUrl).toURL().openConnection();
            connection.setConnectTimeout(15000);
            connection.setReadTimeout(30000);
            connection.setInstanceFollowRedirects(true);
            connection.setRequestMethod(method);
            if (!range.isEmpty()) connection.setRequestProperty("Range", range);
            int code = connection.getResponseCode();
            String reason = connection.getResponseMessage();
            StringBuilder headers = new StringBuilder();
            String type = connection.getContentType();
            if (type != null && !type.isEmpty()) headers.append("Content-Type: ")
                    .append(type).append("\r\n");
            long length = connection.getContentLengthLong();
            if (length >= 0) headers.append("Content-Length: ").append(length).append("\r\n");
            appendHeader(connection, headers, "Content-Range");
            appendHeader(connection, headers, "Accept-Ranges");
            writeResponse(output, code, reason == null ? "Media Response" : reason,
                    headers.toString());
            if ("HEAD".equalsIgnoreCase(method) || code == 416) return;
            InputStream body = code >= 400 ? connection.getErrorStream() : connection.getInputStream();
            if (body != null) copy(body, output);
        } finally {
            if (connection != null) connection.disconnect();
        }
    }

    private void appendHeader(HttpURLConnection connection, StringBuilder headers, String name) {
        String value = connection.getHeaderField(name);
        if (value != null && !value.isEmpty()) {
            headers.append(name).append(": ").append(value).append("\r\n");
        }
    }

    private void serveLocal(BufferedOutputStream output, boolean head, String range)
            throws IOException {
        long size = localSize();
        long start = 0;
        long end = size - 1;
        boolean partial = !range.isEmpty();
        if (partial) {
            Matcher matcher = RANGE_PATTERN.matcher(range);
            if (!matcher.matches()) {
                writeResponse(output, 416, "Range Not Satisfiable",
                    "Content-Range: bytes */" + size + "\r\nContent-Length: 0\r\n");
                return;
            }
            if (matcher.group(1).isEmpty()) {
                long suffix = Long.parseLong(matcher.group(2));
                start = Math.max(0, size - suffix);
            } else {
                start = Long.parseLong(matcher.group(1));
                if (!matcher.group(2).isEmpty()) {
                    end = Math.min(end, Long.parseLong(matcher.group(2)));
                }
            }
            if (start >= size || end < start) {
                writeResponse(output, 416, "Range Not Satisfiable",
                    "Content-Range: bytes */" + size + "\r\nContent-Length: 0\r\n");
                return;
            }
        }
        long length = end - start + 1;
        StringBuilder headers = new StringBuilder()
                .append("Accept-Ranges: bytes\r\n")
                .append("Content-Type: ").append(mimeType).append("\r\n")
                .append("Content-Length: ").append(length).append("\r\n");
        if (partial) headers.append("Content-Range: bytes ").append(start).append('-')
                .append(end).append('/').append(size).append("\r\n");
        writeResponse(output, partial ? 206 : 200, partial ? "Partial Content" : "OK",
            headers.toString());
        if (head) return;
        if ("file".equalsIgnoreCase(localUri.getScheme())) {
            try (RandomAccessFile file = new RandomAccessFile(localUri.getPath(), "r")) {
                file.seek(start);
                copy(file, output, length);
            }
            return;
        }
        try (ParcelFileDescriptor descriptor = context.getContentResolver()
                .openFileDescriptor(localUri, "r");
             FileInputStream stream = new FileInputStream(descriptor.getFileDescriptor())) {
            stream.getChannel().position(start);
            copy(stream, output, length);
        }
    }

    private long localSize() throws IOException {
        if ("file".equalsIgnoreCase(localUri.getScheme())) {
            return new File(localUri.getPath()).length();
        }
        try (AssetFileDescriptor descriptor = context.getContentResolver()
                .openAssetFileDescriptor(localUri, "r")) {
            if (descriptor == null || descriptor.getLength() < 0) {
                throw new IOException("The local media source does not report its length");
            }
            return descriptor.getLength();
        }
    }

    private void writeResponse(BufferedOutputStream output, int code, String reason,
                               String headers) throws IOException {
        String response = "HTTP/1.1 " + code + " " + reason + "\r\n"
                + "Access-Control-Allow-Origin: *\r\n"
                + "Access-Control-Allow-Methods: GET, HEAD, OPTIONS\r\n"
                + "Access-Control-Allow-Headers: Range\r\n"
                + "Access-Control-Allow-Private-Network: true\r\n"
                + "Access-Control-Expose-Headers: Accept-Ranges, Content-Range, Content-Length\r\n"
                + "Connection: close\r\n" + headers + "\r\n";
        output.write(response.getBytes(StandardCharsets.US_ASCII));
        output.flush();
    }

    private Map<String, String> readHeaders(BufferedInputStream input) throws IOException {
        Map<String, String> headers = new HashMap<>();
        String line;
        while ((line = readLine(input)) != null && !line.isEmpty()) {
            int split = line.indexOf(':');
            if (split > 0) headers.put(line.substring(0, split).trim().toLowerCase(),
                    line.substring(split + 1).trim());
        }
        return headers;
    }

    private String readLine(BufferedInputStream input) throws IOException {
        StringBuilder line = new StringBuilder();
        int previous = -1;
        int current;
        while ((current = input.read()) != -1) {
            line.append((char) current);
            if (previous == '\r' && current == '\n') {
                line.setLength(Math.max(0, line.length() - 2));
                return line.toString();
            }
            previous = current;
        }
        return line.length() == 0 ? null : line.toString();
    }

    private void copy(InputStream input, BufferedOutputStream output) throws IOException {
        try (InputStream body = input) {
            byte[] buffer = new byte[BUFFER_SIZE];
            int count;
            while (running && (count = body.read(buffer)) != -1) {
                output.write(buffer, 0, count);
                output.flush();
            }
        }
    }

    private void copy(RandomAccessFile file, BufferedOutputStream output, long remaining)
            throws IOException {
        byte[] buffer = new byte[BUFFER_SIZE];
        long left = remaining;
        while (running && left > 0) {
            int count = file.read(buffer, 0, (int) Math.min(buffer.length, left));
            if (count < 0) break;
            output.write(buffer, 0, count);
            output.flush();
            left -= count;
        }
    }

    private void copy(InputStream input, BufferedOutputStream output, long remaining)
            throws IOException {
        byte[] buffer = new byte[BUFFER_SIZE];
        long left = remaining;
        while (running && left > 0) {
            int count = input.read(buffer, 0, (int) Math.min(buffer.length, left));
            if (count < 0) break;
            output.write(buffer, 0, count);
            output.flush();
            left -= count;
        }
    }

    @Override
    public void close() {
        running = false;
        if (serverSocket != null) {
            try {
                serverSocket.close();
            } catch (IOException ignored) {
                // Already closed.
            }
            serverSocket = null;
        }
        requests.shutdownNow();
    }
}