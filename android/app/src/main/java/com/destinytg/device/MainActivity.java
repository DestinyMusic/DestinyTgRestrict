package com.destinytg.device;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.graphics.Color;
import android.net.Uri;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.ViewGroup;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import org.json.JSONObject;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.IOException;
import java.io.File;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.RandomAccessFile;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity {
    private static final int FILE_CHOOSER_REQUEST = 41;
    private static final int LOCAL_FILE_REQUEST = 42;
    private final int backgroundColor = Color.rgb(15, 23, 42);
    private final int foregroundColor = Color.rgb(241, 245, 249);
    private static final String PREF_APP_MODE = "appMode";
    private static final String MODE_LOCAL = "LOCAL";
    private static final String MODE_WEB = "WEB";

    private SharedPreferences preferences;
    private LocalLibraryStore localLibrary;
    private LocalSecretsStore secretsStore;
    private boolean embeddedRuntimeReady;
    private LinearLayout content;
    private WebView webView;
    private ValueCallback<Uri[]> fileChooserCallback;
    private String serverAddress = "";
    private String appMode = MODE_LOCAL;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        preferences = getSharedPreferences("destiny-device", MODE_PRIVATE);
        localLibrary = new LocalLibraryStore(this);
        localLibrary.markInterruptedTasks();
        secretsStore = new LocalSecretsStore(this);
        try {
            if (!Python.isStarted()) Python.start(new AndroidPlatform(this));
            Python.getInstance().getModule("destiny_runtime")
                    .callAttr("set_storage_directory", getFilesDir().getAbsolutePath());
            Python.getInstance().getModule("destiny_runtime").callAttr("runtime_status");
            embeddedRuntimeReady = true;
        } catch (RuntimeException exception) {
            embeddedRuntimeReady = false;
        }
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(backgroundColor);
        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        root.addView(content, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));
        setContentView(root);

        showLocalLibrary();
    }

    private void showLocalLibrary() {
        content.removeAllViews();
        content.setPadding(24, 24, 24, 24);

        TextView title = new TextView(this);
        title.setText("On-device library");
        title.setTextColor(foregroundColor);
        title.setTextSize(24);
        content.addView(title, matchWrap());

        TextView description = new TextView(this);
        description.setText(embeddedRuntimeReady
            ? "Embedded Python runtime is active. Files stay in this app's local library."
            : "The embedded local runtime could not start. Files remain available in the on-device library.");
        description.setTextColor(Color.LTGRAY);
        description.setTextSize(15);
        LinearLayout.LayoutParams descriptionParams = matchWrap();
        descriptionParams.topMargin = 8;
        content.addView(description, descriptionParams);

        Button telegramButton = new Button(this);
        telegramButton.setText(secretsStore.get("telegram_session") == null
            ? "Connect Telegram account" : "Telegram account connected");
        telegramButton.setOnClickListener(view -> showTelegramSetup());
        LinearLayout.LayoutParams telegramParams = matchWrap();
        telegramParams.topMargin = 12;
        content.addView(telegramButton, telegramParams);

        Button downloadButton = new Button(this);
        downloadButton.setText("Download Telegram message");
        downloadButton.setEnabled(secretsStore.get("telegram_session") != null);
        downloadButton.setOnClickListener(view -> showTelegramDownload());
        content.addView(downloadButton, matchWrap());

        Button directDownloadButton = new Button(this);
        directDownloadButton.setText("Download direct URL");
        directDownloadButton.setOnClickListener(view -> showDirectUrlDownload());
        content.addView(directDownloadButton, matchWrap());

        Button watchButton = new Button(this);
        watchButton.setText("Add Telegram Watch task");
        watchButton.setEnabled(secretsStore.get("telegram_session") != null);
        watchButton.setOnClickListener(view -> showTelegramWatcherSetup());
        content.addView(watchButton, matchWrap());

        Cursor watchers = localLibrary.getWatchers();
        if (watchers.getCount() > 0) {
            TextView watchersTitle = new TextView(this);
            watchersTitle.setText("Active Watch tasks");
            watchersTitle.setTextColor(foregroundColor);
            watchersTitle.setTextSize(18);
            LinearLayout.LayoutParams watchersTitleParams = matchWrap();
            watchersTitleParams.topMargin = 16;
            content.addView(watchersTitle, watchersTitleParams);
            while (watchers.moveToNext()) {
                long watcherId = watchers.getLong(0);
                String sourceLink = watchers.getString(1);
                String destinationChat = watchers.getString(2);
                long sourceThread = watchers.getLong(8);
                long destinationThread = watchers.getLong(9);
                String watcherStats;
                try {
                    JSONObject stats = new JSONObject(watchers.getString(11));
                    watcherStats = "  detected " + stats.optLong("detected", 0)
                            + " · sent " + stats.optLong("success", 0)
                            + " · skipped " + stats.optLong("skipped", 0)
                            + " · failed " + stats.optLong("failed", 0);
                } catch (Exception ignored) {
                    watcherStats = "";
                }
                LinearLayout watcherRow = new LinearLayout(this);
                watcherRow.setGravity(Gravity.CENTER_VERTICAL);
                TextView watcher = new TextView(this);
                watcher.setText(sourceLink + "  ->  " + destinationChat
                    + (sourceThread == 0 ? "" : "  source topic " + sourceThread)
                    + (destinationThread == 0 ? "" : "  destination topic " + destinationThread)
                        + "  [" + watchers.getString(3) + "]  checkpoint " + watchers.getLong(10)
                        + watcherStats);
                watcher.setTextColor(Color.LTGRAY);
                watcher.setMaxLines(3);
                watcherRow.addView(watcher, new LinearLayout.LayoutParams(0,
                        ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                Button removeWatcher = new Button(this);
                removeWatcher.setText("Stop");
                removeWatcher.setOnClickListener(view -> {
                    localLibrary.removeWatcher(watcherId);
                    if (Python.isStarted()) {
                        new Thread(() -> {
                            try {
                                Python.getInstance().getModule("destiny_runtime")
                                    .callAttr("remove_watcher", sourceLink, destinationChat,
                                        String.valueOf(sourceThread),
                                        String.valueOf(destinationThread));
                            } catch (Exception ignored) {
                                // The persisted watcher is removed even if it was not running.
                            }
                        }, "destiny-remove-watcher").start();
                    }
                    Cursor remaining = localLibrary.getWatchers();
                    boolean noneRemain = remaining.getCount() == 0;
                    remaining.close();
                    if (noneRemain) stopService(new Intent(this, LocalWatcherService.class));
                    showLocalLibrary();
                });
                watcherRow.addView(removeWatcher, new LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
                content.addView(watcherRow, matchWrap());
            }
            Button stopWatchers = new Button(this);
            stopWatchers.setText("Stop all Watch tasks");
            stopWatchers.setOnClickListener(view -> {
                localLibrary.removeAllWatchers();
                stopService(new Intent(this, LocalWatcherService.class));
                showLocalLibrary();
            });
            content.addView(stopWatchers, matchWrap());
        }
        watchers.close();

        Cursor tasks = localLibrary.getTasks();
        if (tasks.getCount() > 0) {
            TextView tasksTitle = new TextView(this);
            tasksTitle.setText("Recent download tasks");
            tasksTitle.setTextColor(foregroundColor);
            tasksTitle.setTextSize(18);
            LinearLayout.LayoutParams tasksTitleParams = matchWrap();
            tasksTitleParams.topMargin = 16;
            content.addView(tasksTitle, tasksTitleParams);
            while (tasks.moveToNext()) {
                TextView task = new TextView(this);
                task.setText(tasks.getString(2) + "  ·  " + tasks.getString(3)
                        + "\n" + tasks.getString(4));
                task.setTextColor(Color.LTGRAY);
                LinearLayout.LayoutParams taskParams = matchWrap();
                taskParams.topMargin = 6;
                content.addView(task, taskParams);
            }
        }
        tasks.close();

        Button importButton = new Button(this);
        importButton.setText("Import files");
        importButton.setOnClickListener(view -> {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("*/*");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION
                    | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
            startActivityForResult(intent, LOCAL_FILE_REQUEST);
        });
        LinearLayout.LayoutParams importParams = matchWrap();
        importParams.topMargin = 16;
        content.addView(importButton, importParams);

        TextView libraryTitle = new TextView(this);
        libraryTitle.setText("Saved on this device");
        libraryTitle.setTextColor(foregroundColor);
        libraryTitle.setTextSize(18);
        LinearLayout.LayoutParams listTitleParams = matchWrap();
        listTitleParams.topMargin = 20;
        content.addView(libraryTitle, listTitleParams);

        Cursor files = localLibrary.getFiles();
        if (files.getCount() == 0) {
            TextView empty = new TextView(this);
            empty.setText("No files imported yet");
            empty.setTextColor(Color.LTGRAY);
            LinearLayout.LayoutParams emptyParams = matchWrap();
            emptyParams.topMargin = 8;
            content.addView(empty, emptyParams);
        } else {
            while (files.moveToNext()) {
                long id = files.getLong(0);
                String name = files.getString(1);
                String uri = files.getString(2);
                String mimeType = files.getString(3);
                LinearLayout row = new LinearLayout(this);
                row.setGravity(Gravity.CENTER_VERTICAL);
                TextView fileName = new TextView(this);
                fileName.setText(name);
                fileName.setTextColor(foregroundColor);
                fileName.setMaxLines(2);
                row.addView(fileName, new LinearLayout.LayoutParams(0,
                        ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                Button openButton = new Button(this);
                openButton.setText("Open");
                openButton.setOnClickListener(view -> openLocalFile(name, uri, mimeType));
                row.addView(openButton, new LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
                Button editButton = new Button(this);
                editButton.setText("Edit");
                editButton.setOnClickListener(view -> openLocalEditor(name, uri, mimeType));
                row.addView(editButton, new LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
                Button removeButton = new Button(this);
                removeButton.setText("Remove");
                removeButton.setOnClickListener(view -> {
                    localLibrary.removeFile(id);
                    showLocalLibrary();
                });
                row.addView(removeButton, new LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
                LinearLayout.LayoutParams rowParams = matchWrap();
                rowParams.topMargin = 8;
                content.addView(row, rowParams);
            }
        }
        files.close();
    }

    private void showTelegramSetup() {
        content.removeAllViews();
        content.setPadding(24, 24, 24, 24);

        TextView title = new TextView(this);
        title.setText("Telegram account");
        title.setTextColor(foregroundColor);
        title.setTextSize(22);
        content.addView(title, matchWrap());

        EditText apiId = addAccountInput("Telegram API ID", secretsStore.get("telegram_api_id"));
        apiId.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText apiHash = addAccountInput("Telegram API hash", secretsStore.get("telegram_api_hash"));
        apiHash.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD);
        EditText phone = addAccountInput("Phone number with country code", secretsStore.get("telegram_phone"));
        phone.setInputType(android.text.InputType.TYPE_CLASS_PHONE);
        EditText code = addAccountInput("Telegram login code", null);
        code.setInputType(android.text.InputType.TYPE_CLASS_NUMBER
                | android.text.InputType.TYPE_NUMBER_VARIATION_PASSWORD);
        EditText password = addAccountInput("Telegram 2-step verification password", null);
        password.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD);

        TextView status = new TextView(this);
        status.setTextColor(Color.LTGRAY);
        LinearLayout.LayoutParams statusParams = matchWrap();
        statusParams.topMargin = 8;
        content.addView(status, statusParams);

        Button sendCode = new Button(this);
        sendCode.setText("Send login code");
        content.addView(sendCode, matchWrap());
        sendCode.setOnClickListener(view -> {
            String id = apiId.getText().toString().trim();
            String hash = apiHash.getText().toString().trim();
            String number = phone.getText().toString().trim();
            if (id.isEmpty() || hash.isEmpty() || number.isEmpty()) {
                status.setText("Enter API ID, API hash, and phone number first.");
                return;
            }
            secretsStore.put("telegram_api_id", id);
            secretsStore.put("telegram_api_hash", hash);
            secretsStore.put("telegram_phone", number);
            runPython("send_login_code", new String[]{id, hash, number}, status,
                    "Telegram code sent. Enter the code above.");
        });

        Button verifyCode = new Button(this);
        verifyCode.setText("Verify code");
        content.addView(verifyCode, matchWrap());
        verifyCode.setOnClickListener(view -> {
            String number = phone.getText().toString().trim();
            String value = code.getText().toString().trim();
            if (number.isEmpty() || value.isEmpty()) {
                status.setText("Enter your phone number and Telegram code.");
                return;
            }
            runPython("verify_login_code", new String[]{number, value}, status,
                    "Telegram account connected.");
        });

        Button verifyPassword = new Button(this);
        verifyPassword.setText("Verify 2-step password");
        content.addView(verifyPassword, matchWrap());
        verifyPassword.setOnClickListener(view -> {
            String value = password.getText().toString();
            if (value.isEmpty()) {
                status.setText("Enter your Telegram 2-step verification password.");
                return;
            }
            runPython("verify_login_password", new String[]{value}, status,
                    "Telegram account connected.");
        });

        Button back = new Button(this);
        back.setText("Back to library");
        back.setOnClickListener(view -> showLocalLibrary());
        content.addView(back, matchWrap());
    }

    private void showTelegramDownload() {
        content.removeAllViews();
        content.setPadding(24, 24, 24, 24);

        TextView title = new TextView(this);
        title.setText("Telegram download");
        title.setTextColor(foregroundColor);
        title.setTextSize(22);
        content.addView(title, matchWrap());

        EditText link = addAccountInput("https://t.me/channel/123", null);
        link.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        EditText startId = addAccountInput("First message ID (blank = linked message)", null);
        startId.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText endId = addAccountInput("Last message ID (blank = first only)", null);
        endId.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText destination = addAccountInput("Destination chat (default: Saved Messages)", "me");
        EditText sourceTopic = addAccountInput("Source topic ID (0 for all topics)", "0");
        sourceTopic.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText destinationTopic = addAccountInput("Destination topic ID (0 for default)", "0");
        destinationTopic.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText mediaTypes = addAccountInput("Media types: video,document,text,audio,photo,voice,animation,sticker",
            "video,document,text,audio,photo,voice,animation,sticker");
        EditText includeKeywords = addAccountInput("Include keywords (comma-separated, optional)", null);
        EditText excludeKeywords = addAccountInput("Exclude keywords (comma-separated, optional)", null);
        EditText cleanupKeywords = addAccountInput("Cleanup tags (comma-separated, optional)", null);
        EditText delay = addAccountInput("Delay per message in seconds (3-3600)", "3");
        delay.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);

        TextView status = new TextView(this);
        status.setTextColor(Color.LTGRAY);
        LinearLayout.LayoutParams statusParams = matchWrap();
        statusParams.topMargin = 12;
        content.addView(status, statusParams);

        long[] activeTaskId = {-1L};
        long[] taskEventOffset = {0L};
        boolean[] taskFinished = {false};
        boolean[] cancellationRequested = {false};
        Handler progressHandler = new Handler(Looper.getMainLooper());
        Button cancelTask = new Button(this);
        cancelTask.setText("Cancel current task");
        cancelTask.setEnabled(false);
        content.addView(cancelTask, matchWrap());
        Runnable progressPoll = new Runnable() {
            @Override
            public void run() {
                if (taskFinished[0] || activeTaskId[0] <= 0) return;
                File progressFile = new File(new File(getFilesDir(), "tasks"),
                        activeTaskId[0] + ".txt");
                if (progressFile.isFile()) {
                    try (BufferedReader reader = new BufferedReader(new FileReader(progressFile))) {
                        String[] parts = reader.readLine().split("\\|", 6);
                        if (parts.length == 6) {
                            String progress = parts[0] + "  " + parts[1] + "/" + parts[2]
                                    + "  downloaded " + parts[3] + ", skipped " + parts[4]
                                    + ", failed " + parts[5];
                            status.setText(progress);
                                localLibrary.updateTask(activeTaskId[0],
                                    cancellationRequested[0] ? "CANCEL_REQUESTED" : parts[0], progress);
                        }
                    } catch (Exception ignored) {
                        // The atomic progress snapshot may be replaced during this read.
                    }
                }
                consumeTaskEvents(activeTaskId[0], taskEventOffset);
                progressHandler.postDelayed(this, 750);
            }
        };
        cancelTask.setOnClickListener(view -> {
            long taskId = activeTaskId[0];
            if (taskId <= 0) return;
            cancellationRequested[0] = true;
            localLibrary.updateTask(taskId, "CANCEL_REQUESTED", "Cancellation requested");
            cancelTask.setEnabled(false);
            status.setText("Cancellation requested; the current transfer may finish first.");
            new Thread(() -> {
                try {
                    Python.getInstance().getModule("destiny_runtime")
                            .callAttr("cancel_download_task", String.valueOf(taskId));
                } catch (Exception ignored) {
                    // The task will still complete or fail through its normal path.
                }
            }, "destiny-cancel-download").start();
        });

        Button start = new Button(this);
        start.setText("Start download");
        start.setOnClickListener(view -> {
            if (activeTaskId[0] > 0 && !taskFinished[0]) {
                status.setText("A download task is already active on this screen.");
                return;
            }
            String apiId = secretsStore.get("telegram_api_id");
            String apiHash = secretsStore.get("telegram_api_hash");
            String session = secretsStore.get("telegram_session");
            String messageLink = link.getText().toString().trim();
            String target = destination.getText().toString().trim();
            if (apiId == null || apiHash == null || session == null) {
                status.setText("Connect a Telegram account first.");
                return;
            }
            if (messageLink.isEmpty()) {
                status.setText("Enter a Telegram message link.");
                return;
            }
            String first = startId.getText().toString().trim();
            String last = endId.getText().toString().trim();
            String delayValue = delay.getText().toString().trim();
            long sourceThreadId;
            long destinationThreadId;
            int delaySeconds;
            try {
                delaySeconds = Integer.parseInt(delayValue.isEmpty() ? "3" : delayValue);
                sourceThreadId = Long.parseLong(sourceTopic.getText().toString().trim());
                destinationThreadId = Long.parseLong(destinationTopic.getText().toString().trim());
                if (delaySeconds < 3 || delaySeconds > 3600
                        || sourceThreadId < 0 || destinationThreadId < 0) {
                    throw new NumberFormatException();
                }
            } catch (NumberFormatException exception) {
                status.setText("Enter valid topic IDs and a delay from 3 to 3600 seconds.");
                return;
            }
            String label = messageLink + (first.isEmpty() ? "" : "  IDs " + first + "-"
                    + (last.isEmpty() ? first : last));
                long taskId = localLibrary.addTask("DOWNLOAD", label);
            activeTaskId[0] = taskId;
            taskEventOffset[0] = 0L;
            taskFinished[0] = false;
            cancellationRequested[0] = false;
            start.setEnabled(false);
            cancelTask.setEnabled(true);
            progressHandler.post(progressPoll);
            runPython("download_messages", new String[]{apiId, apiHash, session, messageLink,
                    first, last, target.isEmpty() ? "me" : target,
                    mediaTypes.getText().toString().trim(),
                    includeKeywords.getText().toString().trim(),
                    excludeKeywords.getText().toString().trim(), String.valueOf(delaySeconds),
                    String.valueOf(sourceThreadId), String.valueOf(destinationThreadId),
                    cleanupKeywords.getText().toString().trim(), String.valueOf(taskId)},
                    status, "Download task finished.", taskId, () -> {
                        consumeTaskEvents(taskId, taskEventOffset);
                        taskFinished[0] = true;
                        activeTaskId[0] = -1;
                        start.setEnabled(true);
                        cancelTask.setEnabled(false);
                        progressHandler.removeCallbacks(progressPoll);
                    });
        });
        content.addView(start, matchWrap());

        Button back = new Button(this);
        back.setText("Back to library");
        back.setOnClickListener(view -> showLocalLibrary());
        content.addView(back, matchWrap());
    }

    private void showDirectUrlDownload() {
        content.removeAllViews();
        content.setPadding(24, 24, 24, 24);

        TextView title = new TextView(this);
        title.setText("Direct download");
        title.setTextColor(foregroundColor);
        title.setTextSize(22);
        content.addView(title, matchWrap());

        EditText address = addAccountInput("https://example.com/media.mp4", null);
        address.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        TextView status = new TextView(this);
        status.setTextColor(Color.LTGRAY);
        LinearLayout.LayoutParams statusParams = matchWrap();
        statusParams.topMargin = 12;
        content.addView(status, statusParams);

        Button start = new Button(this);
        start.setText("Download to this device");
        start.setOnClickListener(view -> {
            String rawAddress = address.getText().toString().trim();
            final URI parsed;
            try {
                parsed = new URI(rawAddress);
                if (parsed.getHost() == null || !("http".equalsIgnoreCase(parsed.getScheme())
                        || "https".equalsIgnoreCase(parsed.getScheme()))) {
                    throw new IllegalArgumentException("Enter a valid direct HTTP(S) URL.");
                }
            } catch (Exception exception) {
                status.setText("Enter a valid direct HTTP(S) URL.");
                return;
            }

            status.setText("Connecting…");
            new Thread(() -> {
                HttpURLConnection connection = null;
                File downloadedFile = null;
                String result;
                try {
                    connection = (HttpURLConnection) parsed.toURL().openConnection();
                    connection.setConnectTimeout(15000);
                    connection.setReadTimeout(30000);
                    connection.setInstanceFollowRedirects(true);
                    int responseCode = connection.getResponseCode();
                    if (responseCode < 200 || responseCode >= 300) {
                        throw new IOException("Server returned HTTP " + responseCode);
                    }

                    String path = parsed.getPath();
                    String fileName = path == null || path.isEmpty()
                            ? "download.bin" : path.substring(path.lastIndexOf('/') + 1);
                    fileName = fileName.replaceAll("[^A-Za-z0-9._-]", "_");
                    if (fileName.isEmpty()) fileName = "download.bin";
                    File downloadDirectory = new File(getFilesDir(), "downloads");
                    if (!downloadDirectory.exists() && !downloadDirectory.mkdirs()) {
                        throw new IOException("Could not create the local download folder");
                    }
                    downloadedFile = new File(downloadDirectory,
                            System.currentTimeMillis() + "-" + fileName);
                    try (InputStream input = connection.getInputStream();
                         FileOutputStream output = new FileOutputStream(downloadedFile)) {
                        byte[] buffer = new byte[16384];
                        int count;
                        while ((count = input.read(buffer)) != -1) {
                            output.write(buffer, 0, count);
                        }
                    }

                    String mimeType = connection.getContentType();
                    if (mimeType == null || mimeType.isEmpty()) {
                        mimeType = "application/octet-stream";
                    }
                    localLibrary.addFile(fileName, Uri.fromFile(downloadedFile).toString(), mimeType);
                    result = "Saved " + fileName + " to this device.";
                } catch (Exception exception) {
                    if (downloadedFile != null) downloadedFile.delete();
                    result = "Download failed: " + exception.getMessage();
                } finally {
                    if (connection != null) connection.disconnect();
                }
                String finalResult = result;
                new Handler(Looper.getMainLooper()).post(() -> status.setText(finalResult));
            }, "destiny-direct-download").start();
        });
        content.addView(start, matchWrap());

        Button back = new Button(this);
        back.setText("Back to library");
        back.setOnClickListener(view -> showLocalLibrary());
        content.addView(back, matchWrap());
    }

    private void showTelegramWatcherSetup() {
        content.removeAllViews();
        content.setPadding(24, 24, 24, 24);

        TextView title = new TextView(this);
        title.setText("Telegram Watch task");
        title.setTextColor(foregroundColor);
        title.setTextSize(22);
        content.addView(title, matchWrap());

        EditText source = addAccountInput("Source channel/chat link", null);
        source.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        EditText destination = addAccountInput("Destination chat (default: Saved Messages)", "me");
        EditText sourceTopic = addAccountInput("Source topic ID (0 for all topics)", "0");
        sourceTopic.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText destinationTopic = addAccountInput("Destination topic ID (0 for default)", "0");
        destinationTopic.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText mediaTypes = addAccountInput("Media types: video,document,text,audio,photo,voice,animation,sticker",
            "video,document,text,audio,photo,voice,animation,sticker");
        EditText includeKeywords = addAccountInput("Include keywords (comma-separated, optional)", null);
        EditText excludeKeywords = addAccountInput("Exclude keywords (comma-separated, optional)", null);
        EditText cleanupKeywords = addAccountInput("Cleanup caption tags (comma-separated, optional)", null);
        EditText delay = addAccountInput("Delay before forwarding (seconds, 3-3600)", "3");
        delay.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);

        TextView status = new TextView(this);
        status.setTextColor(Color.LTGRAY);
        LinearLayout.LayoutParams statusParams = matchWrap();
        statusParams.topMargin = 8;
        content.addView(status, statusParams);

        Button start = new Button(this);
        start.setText("Start Watch task");
        start.setOnClickListener(view -> {
            String sourceLink = source.getText().toString().trim();
            String target = destination.getText().toString().trim();
            if (sourceLink.isEmpty()) {
                status.setText("Enter a Telegram source link.");
                return;
            }
            String mediaFilter = mediaTypes.getText().toString().trim();
            String includeFilter = includeKeywords.getText().toString().trim();
            String excludeFilter = excludeKeywords.getText().toString().trim();
            String cleanupFilter = cleanupKeywords.getText().toString().trim();
            String delayValue = delay.getText().toString().trim();
            int delaySeconds;
            long sourceThreadId;
            long destinationThreadId;
            try {
                delaySeconds = Integer.parseInt(delayValue.isEmpty() ? "3" : delayValue);
                if (delaySeconds < 3 || delaySeconds > 3600) throw new NumberFormatException();
                sourceThreadId = Long.parseLong(sourceTopic.getText().toString().trim());
                destinationThreadId = Long.parseLong(destinationTopic.getText().toString().trim());
                if (sourceThreadId < 0 || destinationThreadId < 0) throw new NumberFormatException();
            } catch (NumberFormatException exception) {
                status.setText("Enter valid topic IDs and a delay from 3 to 3600 seconds.");
                return;
            }
            String destinationChat = target.isEmpty() ? "me" : target;
            localLibrary.addWatcher(sourceLink, destinationChat, mediaFilter, includeFilter,
                    excludeFilter, cleanupFilter, delaySeconds, sourceThreadId, destinationThreadId);
            Intent service = new Intent(this, LocalWatcherService.class);
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                startForegroundService(service);
            } else {
                startService(service);
            }
            status.setText("Filtered Watch task saved. It runs while the foreground service is active.");
        });
        content.addView(start, matchWrap());

        Button back = new Button(this);
        back.setText("Back to library");
        back.setOnClickListener(view -> showLocalLibrary());
        content.addView(back, matchWrap());
    }

    private EditText addAccountInput(String hint, String value) {
        EditText input = new EditText(this);
        input.setSingleLine(true);
        input.setHint(hint);
        if (value != null) input.setText(value);
        LinearLayout.LayoutParams params = matchWrap();
        params.topMargin = 8;
        content.addView(input, params);
        return input;
    }

    private void runPython(String function, String[] args, TextView status, String successMessage) {
        runPython(function, args, status, successMessage, 0);
    }

    private void consumeTaskEvents(long taskId, long[] readOffset) {
        File eventsFile = new File(new File(getFilesDir(), "tasks"), taskId + ".jsonl");
        if (!eventsFile.isFile()) return;
        try (RandomAccessFile events = new RandomAccessFile(eventsFile, "r")) {
            long fileLength = events.length();
            if (readOffset[0] > fileLength) readOffset[0] = 0L;
            events.seek(readOffset[0]);
            while (events.getFilePointer() < fileLength) {
                String line = events.readLine();
                if (line == null) break;
                readOffset[0] = events.getFilePointer();
                if (line.isEmpty()) continue;
                JSONObject event = new JSONObject(line);
                if ("file".equals(event.optString("type"))) {
                    localLibrary.addFile(event.getString("name"),
                            Uri.fromFile(new File(event.getString("path"))).toString(),
                            event.optString("mime_type", "application/octet-stream"));
                }
            }
        } catch (Exception ignored) {
            // The writer may still be appending the current event line.
        }
    }

    private void runPython(String function, String[] args, TextView status, String successMessage,
                           long taskId) {
        runPython(function, args, status, successMessage, taskId, null);
    }

    private void runPython(String function, String[] args, TextView status, String successMessage,
                           long taskId, Runnable completion) {
        status.setText("Connecting to Telegram…");
        new Thread(() -> {
            String result;
            try {
                result = Python.getInstance().getModule("destiny_runtime")
                        .callAttr(function, (Object[]) args).toString();
            } catch (Exception exception) {
                result = "Login failed: " + exception.getMessage();
            }
            String response = result;
            new Handler(Looper.getMainLooper()).post(() -> {
                if (response.contains("TASK_SUMMARY|")) {
                    String summary = "Task finished.";
                    String taskState = "COMPLETE";
                    for (String line : response.split("\\n")) {
                        if (line.startsWith("TASK_SUMMARY|")) {
                            summary = line.substring("TASK_SUMMARY|".length())
                                    .replace("downloaded=", "Downloaded ")
                                    .replace(",skipped=", ", skipped ")
                                    .replace(",failed=", ", failed ")
                                    .replace(",cancelled=", ", cancelled ");
                            if (line.endsWith("cancelled=1")) {
                                taskState = "CANCELLED";
                            } else if (!line.contains("failed=0")) {
                                taskState = line.matches(".*downloaded=0,skipped=.*")
                                        ? "FAILED" : "PARTIAL";
                            }
                        }
                    }
                    if (taskId > 0) {
                        consumeTaskEvents(taskId, new long[]{Long.MAX_VALUE});
                        localLibrary.updateTask(taskId, taskState, summary);
                        new File(new File(getFilesDir(), "tasks"), taskId + ".txt").delete();
                        new File(new File(getFilesDir(), "tasks"), taskId + ".jsonl").delete();
                    }
                    status.setText(summary);
                    if (completion != null) completion.run();
                    return;
                }
                if (response.startsWith("AUTH_OK:")) {
                    secretsStore.put("telegram_session", response.substring("AUTH_OK:".length()));
                    status.setText(successMessage);
                    return;
                }
                if ("PASSWORD_REQUIRED".equals(response)) {
                    status.setText("Telegram requires your 2-step password.");
                    return;
                }
                if (response.startsWith("SUCCESS:")) {
                    status.setText(response.substring("SUCCESS:".length()));
                    return;
                }
                if (response.startsWith("SUCCESS_TEXT:")) {
                    status.setText(response.substring("SUCCESS_TEXT:".length()));
                    return;
                }
                if (response.startsWith("SUCCESS_FILE|")) {
                    String[] parts = response.split("\\|", 4);
                    if (parts.length == 4 && (parts[2].startsWith("audio/")
                            || parts[2].startsWith("video/"))) {
                        localLibrary.addFile(parts[1], Uri.fromFile(new File(parts[3])).toString(), parts[2]);
                        status.setText("Saved to this device and " + parts[1]);
                    } else {
                        status.setText("Telegram message copied to destination.");
                    }
                    return;
                }
                if (taskId > 0) {
                    localLibrary.updateTask(taskId, "FAILED", response);
                    new File(new File(getFilesDir(), "tasks"), taskId + ".txt").delete();
                }
                status.setText(response);
                if (completion != null) completion.run();
            });
        }, "destiny-telegram-auth").start();
    }

    private void openLocalFile(String name, String uriValue, String mimeType) {
        try {
            Uri uri = Uri.parse(uriValue);
            String resolvedMimeType = mimeType == null || mimeType.isEmpty()
                    ? "application/octet-stream" : mimeType;
            if (resolvedMimeType.startsWith("video/") || resolvedMimeType.startsWith("audio/")) {
                Intent theaterIntent = new Intent(this, LocalTheaterActivity.class);
                theaterIntent.setDataAndType(uri, resolvedMimeType);
                theaterIntent.putExtra("displayName", name);
                theaterIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                startActivity(theaterIntent);
                return;
            }
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setDataAndType(uri, resolvedMimeType);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivity(intent);
        } catch (ActivityNotFoundException exception) {
            Toast.makeText(this, "No app can open this file", Toast.LENGTH_SHORT).show();
        }
    }

    private void openLocalEditor(String name, String uriValue, String mimeType) {
        Uri uri = Uri.parse(uriValue);
        Intent editorIntent = new Intent(this, LocalMediaEditorActivity.class);
        editorIntent.setDataAndType(uri, mimeType == null ? "application/octet-stream" : mimeType);
        editorIntent.putExtra("displayName", name);
        editorIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        startActivity(editorIntent);
    }

    private void configureWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setAllowFileAccess(false);
        webView.setBackgroundColor(backgroundColor);
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String scheme = uri.getScheme();
                if ("http".equalsIgnoreCase(scheme) || "https".equalsIgnoreCase(scheme)) {
                    if (sameServer(uri)) return false;
                }
                openExternal(uri);
                return true;
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback,
                                             FileChooserParams params) {
                if (fileChooserCallback != null) fileChooserCallback.onReceiveValue(null);
                fileChooserCallback = callback;
                try {
                    startActivityForResult(params.createIntent(), FILE_CHOOSER_REQUEST);
                    return true;
                } catch (ActivityNotFoundException exception) {
                    fileChooserCallback = null;
                    return false;
                }
            }
        });
    }

    private boolean sameServer(Uri uri) {
        if (serverAddress == null || serverAddress.isEmpty()) return false;
        Uri base = Uri.parse(serverAddress);
        return uri.getHost() != null && uri.getHost().equalsIgnoreCase(base.getHost())
                && effectivePort(uri) == effectivePort(base);
    }

    private boolean isLocalMode() {
        return MODE_LOCAL.equalsIgnoreCase(appMode);
    }

    private int effectivePort(Uri uri) {
        if (uri.getPort() != -1) return uri.getPort();
        return "https".equalsIgnoreCase(uri.getScheme()) ? 443 : 80;
    }

    private void openExternal(Uri uri) {
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, uri));
        } catch (ActivityNotFoundException exception) {
            Toast.makeText(this, "No app can open this link", Toast.LENGTH_SHORT).show();
        }
    }

    private void showSetup() {
        content.removeAllViews();
        content.setPadding(24, 32, 24, 24);

        TextView title = new TextView(this);
        title.setText("Connect to Destiny TG");
        title.setTextColor(foregroundColor);
        title.setTextSize(24);
        title.setGravity(Gravity.CENTER_VERTICAL);
        content.addView(title, matchWrap());

        TextView description = new TextView(this);
        description.setText(isLocalMode()
                ? "Local mode: connect to your LAN server or auto-detect it on your local network."
                : "Web mode: connect to a public or private web deployment.");
        description.setTextColor(Color.LTGRAY);
        description.setTextSize(16);
        LinearLayout.LayoutParams descriptionParams = matchWrap();
        descriptionParams.topMargin = 16;
        content.addView(description, descriptionParams);

        LinearLayout modeRow = new LinearLayout(this);
        modeRow.setOrientation(LinearLayout.HORIZONTAL);
        Button localButton = new Button(this);
        localButton.setText("Local");
        localButton.setEnabled(!isLocalMode());
        localButton.setOnClickListener(view -> {
            appMode = MODE_LOCAL;
            preferences.edit().putString(PREF_APP_MODE, appMode).apply();
            showSetup();
        });
        Button webButton = new Button(this);
        webButton.setText("Web");
        webButton.setEnabled(isLocalMode());
        webButton.setOnClickListener(view -> {
            appMode = MODE_WEB;
            preferences.edit().putString(PREF_APP_MODE, appMode).apply();
            showSetup();
        });
        modeRow.addView(localButton, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        modeRow.addView(webButton, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        content.addView(modeRow, matchWrap());

        EditText addressInput = new EditText(this);
        addressInput.setSingleLine(true);
        addressInput.setHint(isLocalMode() ? "http://192.168.1.20:8080" : "https://your-server.example");
        addressInput.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        addressInput.setText(serverAddress);
        LinearLayout.LayoutParams inputParams = matchWrap();
        inputParams.topMargin = 20;
        content.addView(addressInput, inputParams);

        if (isLocalMode()) {
            Button autoDetect = new Button(this);
            autoDetect.setText("Auto-detect local server");
            autoDetect.setOnClickListener(view -> autoDetectServer(addressInput));
            LinearLayout.LayoutParams autoParams = matchWrap();
            autoParams.topMargin = 12;
            content.addView(autoDetect, autoParams);
        }

        Button connect = new Button(this);
        connect.setText("Connect");
        connect.setOnClickListener(view -> {
            String normalized = normalizeAddress(addressInput.getText().toString());
            if (normalized == null) {
                addressInput.setError("Enter a valid http:// or https:// server address");
                return;
            }
            serverAddress = normalized;
            preferences.edit().putString("serverAddress", serverAddress).apply();
            showDashboard();
        });
        LinearLayout.LayoutParams buttonParams = matchWrap();
        buttonParams.topMargin = 16;
        content.addView(connect, buttonParams);
    }

    private void autoDetectServer(EditText addressInput) {
        List<String> candidates = LocalServerDiscovery.buildCandidateAddresses(addressInput.getText().toString());
        candidates.addAll(getWifiSubnetCandidates());

        if (candidates.isEmpty()) {
            Toast.makeText(this, "No local server candidates found", Toast.LENGTH_SHORT).show();
            return;
        }

        final Handler uiHandler = new Handler(Looper.getMainLooper());
        Toast.makeText(this, "Checking local network for Destiny server…", Toast.LENGTH_SHORT).show();

        new Thread(() -> {
            for (String candidate : candidates) {
                if (probeServer(candidate)) {
                    serverAddress = candidate;
                    preferences.edit().putString("serverAddress", serverAddress).apply();
                    uiHandler.post(() -> {
                        addressInput.setText(serverAddress);
                        showDashboard();
                    });
                    return;
                }
            }
            uiHandler.post(() -> {
                Toast.makeText(this, "No local Destiny server responded. Enter the address manually.", Toast.LENGTH_LONG).show();
            });
        }).start();
    }

    private List<String> getWifiSubnetCandidates() {
        List<String> candidates = new ArrayList<>();
        try {
            WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WifiManager.class);
            if (wifiManager == null) {
                return candidates;
            }
            int ipAddress = wifiManager.getDhcpInfo().ipAddress;
            int gateway = wifiManager.getDhcpInfo().gateway;
            int mask = wifiManager.getDhcpInfo().netmask;
            if (ipAddress == 0 || gateway == 0 || mask == 0) {
                return candidates;
            }

            String subnetBase = buildSubnetBase(gateway, mask);
            if (subnetBase == null) {
                return candidates;
            }

            String[] parts = subnetBase.split("\\.");
            if (parts.length != 4) {
                return candidates;
            }

            for (int host = 1; host <= 32; host++) {
                candidates.add("http://" + parts[0] + "." + parts[1] + "." + parts[2] + "." + host + ":8080");
                candidates.add("http://" + parts[0] + "." + parts[1] + "." + parts[2] + "." + host + ":8000");
            }
        } catch (Exception ignored) {
            // Ignore and rely on manual entry if Wi‑Fi info is unavailable
        }
        return candidates;
    }

    private String buildSubnetBase(int gateway, int mask) {
        int subnet = gateway & mask;
        String[] octets = new String[] {
                String.valueOf((subnet >> 24) & 0xFF),
                String.valueOf((subnet >> 16) & 0xFF),
                String.valueOf((subnet >> 8) & 0xFF),
                String.valueOf(subnet & 0xFF)
        };
        return String.join(".", octets);
    }

    private boolean probeServer(String address) {
        try {
            URL url = new URL(address);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(1500);
            connection.setReadTimeout(1800);
            connection.setInstanceFollowRedirects(true);
            int responseCode = connection.getResponseCode();
            connection.disconnect();
            return responseCode >= 200 && responseCode < 500;
        } catch (IOException ignored) {
            return false;
        }
    }

    private String normalizeAddress(String value) {
        String address = value.trim();
        if (address.isEmpty()) return null;
        if (!address.contains("://")) address = "http://" + address;
        try {
            URI uri = new URI(address);
            String scheme = uri.getScheme();
            if (uri.getHost() == null || !("http".equalsIgnoreCase(scheme)
                    || "https".equalsIgnoreCase(scheme))) return null;
            String path = uri.getRawPath();
            while (path != null && path.endsWith("/") && !path.isEmpty()) {
                path = path.substring(0, path.length() - 1);
            }
            return uri.getScheme() + "://" + uri.getRawAuthority()
                    + (path == null ? "" : path);
        } catch (Exception exception) {
            return null;
        }
    }

    private void showDashboard() {
        content.removeAllViews();
        content.setPadding(0, 0, 0, 0);

        LinearLayout toolbar = new LinearLayout(this);
        toolbar.setGravity(Gravity.CENTER_VERTICAL);
        toolbar.setPadding(8, 4, 8, 4);
        Button server = new Button(this);
        server.setText("Server");
        server.setOnClickListener(view -> showSetup());
        Button reload = new Button(this);
        reload.setText("Reload");
        reload.setOnClickListener(view -> webView.reload());
        toolbar.addView(server, new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        toolbar.addView(reload, new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        content.addView(toolbar, matchWrap());
        if (webView.getParent() != null) ((ViewGroup) webView.getParent()).removeView(webView);
        content.addView(webView, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));
        webView.loadUrl(serverAddress);
    }

    private LinearLayout.LayoutParams matchWrap() {
        return new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == LOCAL_FILE_REQUEST) {
            if (resultCode == RESULT_OK && data != null && data.getData() != null) {
                Uri uri = data.getData();
                try {
                    getContentResolver().takePersistableUriPermission(uri,
                            Intent.FLAG_GRANT_READ_URI_PERMISSION);
                } catch (SecurityException ignored) {
                    // Some document providers do not offer persistable grants.
                }
                String name = uri.getLastPathSegment();
                String mimeType = getContentResolver().getType(uri);
                try (Cursor cursor = getContentResolver().query(uri,
                        new String[]{android.provider.OpenableColumns.DISPLAY_NAME},
                        null, null, null)) {
                    if (cursor != null && cursor.moveToFirst()) {
                        name = cursor.getString(0);
                    }
                } catch (Exception ignored) {
                    // Fall back to the document URI when metadata is unavailable.
                }
                localLibrary.addFile(name == null ? "Imported file" : name,
                        uri.toString(), mimeType == null ? "application/octet-stream" : mimeType);
            }
            showLocalLibrary();
            return;
        }
        if (requestCode != FILE_CHOOSER_REQUEST || fileChooserCallback == null) return;
        Uri[] results = WebChromeClient.FileChooserParams.parseResult(resultCode, data);
        fileChooserCallback.onReceiveValue(results);
        fileChooserCallback = null;
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}