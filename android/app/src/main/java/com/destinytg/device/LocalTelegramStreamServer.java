package com.destinytg.device;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

final class LocalTelegramStreamServer implements AutoCloseable {
    private static final int RANGE_CHUNK_SIZE = 1024 * 1024;
    private static final Pattern RANGE_PATTERN = Pattern.compile("bytes=(\\d*)-(\\d*)");

    private final ExecutorService requests = Executors.newCachedThreadPool();
    private ServerSocket serverSocket;
    private Thread acceptThread;
    private volatile boolean running;
    private String streamId;
    private String fileName;
    private String mimeType;
    private long fileSize;

    void start(String apiId, String apiHash, String session, String telegramLink)
            throws Exception {
        String metadata = Python.getInstance().getModule("destiny_runtime")
                .callAttr("open_telegram_media", apiId, apiHash, session, telegramLink)
                .toString();
        org.json.JSONObject media = new org.json.JSONObject(metadata);
        streamId = media.getString("stream_id");
        fileName = media.optString("file_name", "Telegram media");
        mimeType = media.optString("mime_type", "application/octet-stream");
        fileSize = media.getLong("file_size");
        serverSocket = new ServerSocket(0, 16, InetAddress.getByName("127.0.0.1"));
        running = true;
        acceptThread = new Thread(this::acceptRequests, "destiny-media-http");
        acceptThread.setDaemon(true);
        acceptThread.start();
    }

    String getUrl() {
        if (serverSocket == null) throw new IllegalStateException("Media stream is not ready");
        return "http://127.0.0.1:" + serverSocket.getLocalPort() + "/media/" + streamId;
    }

    String getFileName() {
        return fileName;
    }

    String getMimeType() {
        return mimeType;
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
            String[] requestParts = requestLine.split(" ", 3);
            if (requestParts.length < 2) {
                writeError(output, 400, "Bad Request");
                return;
            }
            boolean headRequest = "HEAD".equalsIgnoreCase(requestParts[0]);
            boolean optionsRequest = "OPTIONS".equalsIgnoreCase(requestParts[0]);
            if (!headRequest && !optionsRequest && !"GET".equalsIgnoreCase(requestParts[0])) {
                writeError(output, 405, "Method Not Allowed");
                return;
            }
            String requestPath = URLDecoder.decode(requestParts[1], "UTF-8");
            if (!requestPath.equals("/media/" + streamId)) {
                writeError(output, 404, "Not Found");
                return;
            }

            String rangeHeader = "";
            String header;
            while ((header = readLine(input)) != null && !header.isEmpty()) {
                int separator = header.indexOf(':');
                if (separator > 0 && "range".equalsIgnoreCase(header.substring(0, separator).trim())) {
                    rangeHeader = header.substring(separator + 1).trim();
                }
            }
            if (optionsRequest) {
                output.write(("HTTP/1.1 204 No Content\r\n"
                        + "Access-Control-Allow-Origin: *\r\n"
                        + "Access-Control-Allow-Methods: GET, HEAD, OPTIONS\r\n"
                        + "Access-Control-Allow-Headers: Range\r\n"
                        + "Access-Control-Allow-Private-Network: true\r\n"
                        + "Access-Control-Max-Age: 600\r\n"
                        + "Content-Length: 0\r\nConnection: close\r\n\r\n")
                        .getBytes(StandardCharsets.US_ASCII));
                output.flush();
                return;
            }

            long start = 0;
            long end = fileSize - 1;
            boolean partial = !rangeHeader.isEmpty();
            if (partial) {
                Matcher range = RANGE_PATTERN.matcher(rangeHeader);
                if (!range.matches()) {
                    writeRangeError(output);
                    return;
                }
                if (range.group(1).isEmpty()) {
                    long suffix = Long.parseLong(range.group(2));
                    start = Math.max(0, fileSize - suffix);
                } else {
                    start = Long.parseLong(range.group(1));
                    if (!range.group(2).isEmpty()) end = Math.min(end, Long.parseLong(range.group(2)));
                }
                if (start >= fileSize || end < start) {
                    writeRangeError(output);
                    return;
                }
            }
            long length = end - start + 1;
            String status = partial ? "206 Partial Content" : "200 OK";
            StringBuilder responseHeaders = new StringBuilder()
                    .append("HTTP/1.1 ").append(status).append("\r\n")
                    .append("Access-Control-Allow-Origin: *\r\n")
                    .append("Access-Control-Allow-Methods: GET, HEAD, OPTIONS\r\n")
                    .append("Access-Control-Allow-Headers: Range\r\n")
                    .append("Access-Control-Allow-Private-Network: true\r\n")
                    .append("Access-Control-Expose-Headers: Accept-Ranges, Content-Range, Content-Length\r\n")
                    .append("Accept-Ranges: bytes\r\n")
                    .append("Content-Type: ").append(mimeType).append("\r\n")
                    .append("Content-Length: ").append(length).append("\r\n")
                    .append("Connection: close\r\n");
            if (partial) {
                responseHeaders.append("Content-Range: bytes ").append(start).append('-')
                        .append(end).append('/').append(fileSize).append("\r\n");
            }
            responseHeaders.append("\r\n");
            output.write(responseHeaders.toString().getBytes(StandardCharsets.US_ASCII));
            output.flush();
            if (headRequest) return;

            long position = start;
            while (position <= end && running) {
                int amount = (int) Math.min(RANGE_CHUNK_SIZE, end - position + 1);
                PyObject result = Python.getInstance().getModule("destiny_runtime")
                        .callAttr("read_telegram_media_range", streamId,
                                String.valueOf(position), String.valueOf(amount));
                byte[] bytes = result.toJava(byte[].class);
                if (bytes.length == 0) break;
                output.write(bytes);
                output.flush();
                position += bytes.length;
            }
        } catch (Exception ignored) {
            // Media players routinely close a range request while seeking or switching tracks.
        }
    }

    private String readLine(BufferedInputStream input) throws IOException {
        StringBuilder line = new StringBuilder();
        int previous = -1;
        int current;
        while ((current = input.read()) != -1) {
            if (previous == '\r' && current == '\n') {
                line.setLength(Math.max(0, line.length() - 2));
                return line.toString();
            }
            line.append((char) current);
            previous = current;
        }
        return line.length() == 0 ? null : line.toString();
    }

    private void writeRangeError(BufferedOutputStream output) throws IOException {
        output.write(("HTTP/1.1 416 Range Not Satisfiable\r\n"
                + "Content-Range: bytes */" + fileSize + "\r\n"
                + "Content-Length: 0\r\nConnection: close\r\n\r\n")
                .getBytes(StandardCharsets.US_ASCII));
        output.flush();
    }

    private void writeError(BufferedOutputStream output, int code, String reason)
            throws IOException {
        output.write(("HTTP/1.1 " + code + " " + reason + "\r\n"
                + "Content-Length: 0\r\nConnection: close\r\n\r\n")
                .getBytes(StandardCharsets.US_ASCII));
        output.flush();
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
        if (streamId != null && Python.isStarted()) {
            try {
                Python.getInstance().getModule("destiny_runtime")
                        .callAttr("close_telegram_media", streamId);
            } catch (Exception ignored) {
                // The embedded runtime may already be shutting down.
            }
        }
    }
}