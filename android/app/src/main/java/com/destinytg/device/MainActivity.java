package com.destinytg.device;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.RippleDrawable;
import android.net.Uri;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebResourceError;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.ScrollView;
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
import org.json.JSONArray;

public class MainActivity extends Activity {
    private static final int FILE_CHOOSER_REQUEST = 41;
    private static final int LOCAL_FILE_REQUEST = 42;
    private static final int NOTIFICATION_PERMISSION_REQUEST = 43;
    private final int backgroundColor = Color.rgb(7, 9, 13);
    private final int surfaceColor = Color.rgb(17, 24, 39);
    private final int accentColor = Color.rgb(56, 189, 248);
    private final int foregroundColor = Color.rgb(241, 245, 249);
    private final int mutedColor = Color.rgb(148, 163, 184);
    private static final String PREF_APP_MODE = "appMode";
    private static final String MODE_LOCAL = "LOCAL";
    private static final String MODE_WEB = "WEB";

    private SharedPreferences preferences;
    private LocalLibraryStore localLibrary;
    private LocalSecretsStore secretsStore;
    private boolean embeddedRuntimeReady;
    private boolean dashboardShowing;
    private LinearLayout root;
    private LinearLayout content;
    private ScrollView localScrollView;
    private WebView webView;
    private ProgressBar pageProgress;
    private TextView pageError;
    private ValueCallback<Uri[]> fileChooserCallback;
    private String serverAddress = "";
    private String appMode = MODE_LOCAL;
    private String activeLocalTab = "Home";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        preferences = getSharedPreferences("destiny-device", MODE_PRIVATE);
        serverAddress = preferences.getString("serverAddress", "");
        appMode = preferences.getString(PREF_APP_MODE, MODE_LOCAL);
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
        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(backgroundColor);
        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setPadding(20, 24, 20, 28);
        localScrollView = new ScrollView(this);
        localScrollView.setFillViewport(true);
        localScrollView.setClipToPadding(false);
        localScrollView.addView(content, new ScrollView.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        setContentView(root);

        webView = new WebView(this);
        configureWebView();
        if (isLocalMode()) {
            showLocalHome();
        } else if (serverAddress.isEmpty()) {
            showSetup();
        } else {
            showDashboard();
        }
        if (isLocalMode()) resumeInterruptedDownloads();
    }

    private void showLocalHome() {
        activeLocalTab = "Home";
        dashboardShowing = false;
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(18), dp(18), dp(18), dp(24));

        int fileCount = countRows(localLibrary.getFiles());
        int watcherCount = countRows(localLibrary.getWatchers());
        int taskCount = countRows(localLibrary.getTasks());

        LinearLayout overview = new LinearLayout(this);
        overview.setOrientation(LinearLayout.VERTICAL);
        overview.setPadding(dp(18), dp(18), dp(18), dp(18));
        GradientDrawable overviewBackground = new GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            new int[]{Color.rgb(18, 39, 57), surfaceColor});
        overviewBackground.setCornerRadius(dp(8));
        overviewBackground.setStroke(dp(1), Color.rgb(37, 66, 89));
        overview.setBackground(overviewBackground);
        TextView eyebrow = localLabel("DESTINY TG  /  DEVICE DASHBOARD", accentColor);
        eyebrow.setTextSize(10);
        eyebrow.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        overview.addView(eyebrow, matchWrap());

        TextView heading = new TextView(this);
        heading.setText("System overview");
        heading.setTextColor(foregroundColor);
        heading.setTextSize(25);
        heading.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        LinearLayout.LayoutParams headingParams = matchWrap();
        headingParams.topMargin = dp(7);
        overview.addView(heading, headingParams);

        TextView subtitle = localLabel("Telegram tasks and media, managed on this device.",
            mutedColor);
        subtitle.setTextSize(13);
        LinearLayout.LayoutParams subtitleParams = matchWrap();
        subtitleParams.topMargin = dp(4);
        overview.addView(subtitle, subtitleParams);

        Button createTask = new Button(this);
        createTask.setText("Create task or watcher");
        createTask.setTextColor(backgroundColor);
        createTask.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        createTask.setMinHeight(dp(48));
        createTask.setBackground(createRoundedBackground(accentColor, dp(6)));
        createTask.setOnClickListener(view -> showLocalTools());
        LinearLayout.LayoutParams createTaskParams = matchWrap();
        createTaskParams.topMargin = dp(16);
        overview.addView(createTask, createTaskParams);
        content.addView(overview, matchWrap());

        addSectionTitle("System overview", content);
        addDashboardMetricRow("Active tasks", String.valueOf(taskCount),
            "Live watchers", String.valueOf(watcherCount));
        addDashboardMetricRow("Media library", String.valueOf(fileCount) + " files",
            "Local runtime", embeddedRuntimeReady ? "READY" : "OFFLINE");

        LinearLayout sessionPanel = new LinearLayout(this);
        sessionPanel.setOrientation(LinearLayout.HORIZONTAL);
        sessionPanel.setGravity(Gravity.CENTER_VERTICAL);
        sessionPanel.setPadding(dp(14), dp(12), dp(14), dp(12));
        sessionPanel.setBackground(createRoundedBackground(surfaceColor, dp(6)));
        LinearLayout.LayoutParams sessionParams = matchWrap();
        sessionParams.topMargin = dp(12);
        content.addView(sessionPanel, sessionParams);
        TextView sessionLabel = localLabel("TELEGRAM SESSION", mutedColor);
        sessionLabel.setTextSize(10);
        sessionLabel.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        sessionPanel.addView(sessionLabel, new LinearLayout.LayoutParams(0,
            ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        TextView sessionState = localLabel(secretsStore.get("telegram_session") == null
            ? "NOT CONNECTED" : "ONLINE",
            secretsStore.get("telegram_session") == null ? mutedColor : Color.rgb(52, 211, 153));
        sessionState.setTextSize(11);
        sessionState.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        sessionPanel.addView(sessionState, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        addSectionTitle("Quick actions", content);
        addDashboardActionRow("Downloads", "Telegram and direct links", view -> {
            if (secretsStore.get("telegram_session") == null) showTelegramSetup();
            else showTelegramDownload();
        }, "Watchers", "Automate source forwarding", view -> {
            if (secretsStore.get("telegram_session") == null) showTelegramSetup();
            else showTelegramWatcherSetup();
        });
        addDashboardActionRow("Media library", "Play, edit, and import", view -> showLocalLibrary(),
            "All dashboard tools", "Network, system, and account", view -> showLocalTools());
        }

        private void addDashboardMetricRow(String firstLabel, String firstValue,
                           String secondLabel, String secondValue) {
        LinearLayout row = new LinearLayout(this);
        LinearLayout.LayoutParams firstParams = new LinearLayout.LayoutParams(0,
            ViewGroup.LayoutParams.WRAP_CONTENT, 1);
        firstParams.rightMargin = dp(6);
        row.addView(createDashboardMetric(firstLabel, firstValue), firstParams);
        LinearLayout.LayoutParams secondParams = new LinearLayout.LayoutParams(0,
            ViewGroup.LayoutParams.WRAP_CONTENT, 1);
        secondParams.leftMargin = dp(6);
        row.addView(createDashboardMetric(secondLabel, secondValue), secondParams);
        LinearLayout.LayoutParams rowParams = matchWrap();
        rowParams.bottomMargin = dp(8);
        content.addView(row, rowParams);
        }

        private LinearLayout createDashboardMetric(String labelText, String valueText) {
        LinearLayout metric = new LinearLayout(this);
        metric.setOrientation(LinearLayout.VERTICAL);
        metric.setPadding(dp(13), dp(12), dp(13), dp(12));
        metric.setMinimumHeight(dp(80));
        GradientDrawable card = createRoundedBackground(surfaceColor, dp(6));
        card.setStroke(dp(1), Color.rgb(39, 51, 68));
        metric.setBackground(card);
        TextView label = localLabel(labelText.toUpperCase(java.util.Locale.ROOT), mutedColor);
        label.setTextSize(10);
        label.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        metric.addView(label, matchWrap());
        TextView value = localLabel(valueText, foregroundColor);
        value.setTextSize(21);
        value.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        LinearLayout.LayoutParams valueParams = matchWrap();
        valueParams.topMargin = dp(5);
        metric.addView(value, valueParams);
        return metric;
        }

        private void addDashboardActionRow(String firstTitle, String firstDetail,
                           View.OnClickListener firstListener,
                           String secondTitle, String secondDetail,
                           View.OnClickListener secondListener) {
        LinearLayout row = new LinearLayout(this);
        LinearLayout.LayoutParams firstParams = new LinearLayout.LayoutParams(0,
            ViewGroup.LayoutParams.WRAP_CONTENT, 1);
        firstParams.rightMargin = dp(5);
        row.addView(createLocalAction(firstTitle, firstDetail, firstListener), firstParams);
        LinearLayout.LayoutParams secondParams = new LinearLayout.LayoutParams(0,
            ViewGroup.LayoutParams.WRAP_CONTENT, 1);
        secondParams.leftMargin = dp(5);
        row.addView(createLocalAction(secondTitle, secondDetail, secondListener), secondParams);
        LinearLayout.LayoutParams rowParams = matchWrap();
        rowParams.bottomMargin = dp(8);
        content.addView(row, rowParams);
    }

    private void showLocalTasks() {
        activeLocalTab = "Tasks";
        dashboardShowing = false;
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(20), dp(20), dp(20), dp(24));
        addPageHeading("Tasks", "Downloads and Telegram watches running on this device.");

        Button download = new Button(this);
        download.setText("New Telegram download");
        stylePrimaryButton(download);
        download.setOnClickListener(view -> {
            if (secretsStore.get("telegram_session") == null) showTelegramSetup();
            else showTelegramDownload();
        });
        content.addView(download, matchWrap());

        Button watch = new Button(this);
        watch.setText("Add Telegram watch");
        watch.setOnClickListener(view -> {
            if (secretsStore.get("telegram_session") == null) showTelegramSetup();
            else showTelegramWatcherSetup();
        });
        LinearLayout.LayoutParams watchParams = matchWrap();
        watchParams.topMargin = dp(8);
        content.addView(watch, watchParams);

        addSectionTitle("Active watches", content);
        Cursor watchers = localLibrary.getWatchers();
        if (watchers.getCount() == 0) {
            content.addView(localLabel("No active Telegram watches", Color.rgb(172, 174, 161)),
                    matchWrap());
        } else {
            while (watchers.moveToNext()) {
                long watcherId = watchers.getLong(0);
                String source = watchers.getString(1);
                String destination = watchers.getString(2);
                long sourceThread = watchers.getLong(8);
                long destinationThread = watchers.getLong(9);
                LinearLayout row = new LinearLayout(this);
                row.setGravity(Gravity.CENTER_VERTICAL);
                row.setPadding(dp(12), dp(10), dp(8), dp(10));
                row.setBackground(createRoundedBackground(surfaceColor, dp(6)));
                TextView label = new TextView(this);
                label.setText(source + "\n→ " + destination + " · " + watchers.getString(3));
                label.setTextColor(foregroundColor);
                label.setTextSize(13);
                label.setMaxLines(3);
                row.addView(label, new LinearLayout.LayoutParams(0,
                        ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                Button stop = new Button(this);
                stop.setText("Stop");
                stop.setOnClickListener(view -> {
                    localLibrary.removeWatcher(watcherId);
                    if (Python.isStarted()) {
                        new Thread(() -> {
                            try {
                                Python.getInstance().getModule("destiny_runtime")
                                        .callAttr("remove_watcher", source, destination,
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
                    showLocalTasks();
                });
                row.addView(stop, new LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
                LinearLayout.LayoutParams rowParams = matchWrap();
                rowParams.topMargin = dp(8);
                content.addView(row, rowParams);
            }
        }
        watchers.close();

        addSectionTitle("Recent downloads", content);
        Cursor tasks = localLibrary.getTasks();
        if (tasks.getCount() == 0) {
            content.addView(localLabel("Your recent task history will appear here.",
                    Color.rgb(172, 174, 161)), matchWrap());
        } else {
            while (tasks.moveToNext()) {
                LinearLayout row = new LinearLayout(this);
                row.setOrientation(LinearLayout.VERTICAL);
                row.setPadding(dp(12), dp(10), dp(12), dp(10));
                row.setBackground(createRoundedBackground(surfaceColor, dp(6)));
                TextView label = localLabel(tasks.getString(2), foregroundColor);
                label.setMaxLines(2);
                row.addView(label, matchWrap());
                TextView detail = localLabel(tasks.getString(1) + "  ·  " + tasks.getString(3)
                        + "\n" + tasks.getString(4), Color.rgb(172, 174, 161));
                detail.setTextSize(12);
                LinearLayout.LayoutParams detailParams = matchWrap();
                detailParams.topMargin = dp(4);
                row.addView(detail, detailParams);
                LinearLayout.LayoutParams rowParams = matchWrap();
                rowParams.topMargin = dp(8);
                content.addView(row, rowParams);
            }
        }
        tasks.close();
    }

    private void showLocalAccount() {
        activeLocalTab = "Account";
        dashboardShowing = false;
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(20), dp(20), dp(20), dp(24));
        addPageHeading("Account & connection", "Your Telegram session and files stay in app storage.");

        TextView account = localLabel(secretsStore.get("telegram_session") == null
                ? "Telegram account not connected" : "Telegram account connected on this device",
                foregroundColor);
        content.addView(account, matchWrap());

        Button telegram = new Button(this);
        telegram.setText(secretsStore.get("telegram_session") == null
                ? "Connect Telegram" : "Manage Telegram connection");
        stylePrimaryButton(telegram);
        telegram.setOnClickListener(view -> showTelegramSetup());
        LinearLayout.LayoutParams telegramParams = matchWrap();
        telegramParams.topMargin = dp(14);
        content.addView(telegram, telegramParams);

        addSectionTitle("Device network", content);
        TextView network = localLabel("Telegram traffic uses this device's active network. "
                + "Downloads and the media library are stored in this app's local storage.",
                Color.rgb(172, 174, 161));
        content.addView(network, matchWrap());

        Button server = new Button(this);
        server.setText("Local server dashboard settings");
        server.setOnClickListener(view -> showSetup());
        LinearLayout.LayoutParams serverParams = matchWrap();
        serverParams.topMargin = dp(14);
        content.addView(server, serverParams);

        addSectionTitle("Worker bot pools", content);
        content.addView(localLabel("Use separate Telegram bots for media streams and task uploads. "
                + "Tokens are encrypted in this app and are never sent to a Destiny server.",
                mutedColor), matchWrap());
        EditText streamTokens = new EditText(this);
        streamTokens.setHint("Stream/editor bot tokens, one per line");
        streamTokens.setMinLines(2);
        streamTokens.setGravity(Gravity.TOP | Gravity.START);
        streamTokens.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_FLAG_MULTI_LINE
                | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD);
        streamTokens.setText(secretsStore.get("stream_worker_tokens"));
        styleInput(streamTokens);
        LinearLayout.LayoutParams streamTokenParams = matchWrap();
        streamTokenParams.topMargin = dp(10);
        content.addView(streamTokens, streamTokenParams);

        EditText taskTokens = new EditText(this);
        taskTokens.setHint("Task/watcher bot tokens, one per line");
        taskTokens.setMinLines(2);
        taskTokens.setGravity(Gravity.TOP | Gravity.START);
        taskTokens.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_FLAG_MULTI_LINE
                | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD);
        taskTokens.setText(secretsStore.get("task_worker_tokens"));
        styleInput(taskTokens);
        LinearLayout.LayoutParams taskTokenParams = matchWrap();
        taskTokenParams.topMargin = dp(8);
        content.addView(taskTokens, taskTokenParams);

        TextView workerStatus = localLabel("Worker pools are managed by this device.", mutedColor);
        LinearLayout.LayoutParams workerStatusParams = matchWrap();
        workerStatusParams.topMargin = dp(8);
        content.addView(workerStatus, workerStatusParams);
        Button saveWorkers = new Button(this);
        saveWorkers.setText("Save and connect worker bots");
        stylePrimaryButton(saveWorkers);
        saveWorkers.setOnClickListener(view -> {
            String apiId = secretsStore.get("telegram_api_id");
            String apiHash = secretsStore.get("telegram_api_hash");
            if (apiId == null || apiHash == null) {
                workerStatus.setText("Connect Telegram before configuring worker bots.");
                return;
            }
            String streamValues = streamTokens.getText().toString().trim();
            String taskValues = taskTokens.getText().toString().trim();
            secretsStore.put("stream_worker_tokens", streamValues);
            secretsStore.put("task_worker_tokens", taskValues);
            workerStatus.setText("Connecting worker bots…");
            new Thread(() -> {
                String result;
                try {
                    result = Python.getInstance().getModule("destiny_runtime")
                            .callAttr("configure_worker_pools", apiId, apiHash,
                                    streamValues, taskValues).toString();
                } catch (Exception exception) {
                    result = "Worker setup failed: " + exception.getMessage();
                }
                String workerResult = result;
                new Handler(Looper.getMainLooper()).post(() -> workerStatus.setText(workerResult));
            }, "destiny-configure-workers").start();
        });
        LinearLayout.LayoutParams saveWorkersParams = matchWrap();
        saveWorkersParams.topMargin = dp(8);
        content.addView(saveWorkers, saveWorkersParams);
    }

        private void showLocalTools() {
        activeLocalTab = "Tools";
        dashboardShowing = false;
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(20), dp(20), dp(20), dp(24));
        addPageHeading("Dashboard tools", "Choose a workspace. Device tools run in this app.");

        addSectionTitle("On this device", content);
        content.addView(createLocalAction("Downloads",
            "Download Telegram messages or fetch direct URLs", view -> {
                if (secretsStore.get("telegram_session") == null) showTelegramSetup();
                else showTelegramDownload();
            }), actionParams());
        content.addView(createLocalAction("Watchers",
            "Create, inspect, and stop Telegram source watches", view -> showLocalTasks()),
            actionParams());
        content.addView(createLocalAction("Telegram account",
            "Connect Telegram directly from this device", view -> showLocalAccount()),
            actionParams());
        content.addView(createLocalAction("Media library, theater & editor",
            "Play, trim, import, and manage locally saved media", view -> showLocalLibrary()),
            actionParams());

        addSectionTitle("Server dashboard", content);
        TextView serverNote = localLabel("These panels require a Destiny server connection. "
            + "The Telegram and media tools above work directly from this device.",
            Color.rgb(172, 174, 161));
        content.addView(serverNote, matchWrap());
        content.addView(createLocalAction("Chats & IDs",
            "Browse Telegram dialogs and chat identifiers", view -> openServerDashboard()),
            actionParams());
        content.addView(createLocalAction("World Explorer",
            "Open the dashboard's interactive globe", view -> openServerDashboard()),
            actionParams());
        content.addView(createLocalAction("Live Network",
            "View connected clients and network activity", view -> openServerDashboard()),
            actionParams());
        content.addView(createLocalAction("Speedtest",
            "Measure the server's network throughput", view -> openServerDashboard()),
            actionParams());
        content.addView(createLocalAction("System SOS & System Logs",
            "Inspect server health and diagnostic logs", view -> openServerDashboard()),
            actionParams());
        content.addView(createLocalAction("Media Inspector & Audio Spectrogram",
            "Analyze media through the connected server", view -> openServerDashboard()),
            actionParams());
        content.addView(createLocalAction("Admin Panel",
            "Manage server users and access roles", view -> openServerDashboard()),
            actionParams());

        Button settings = new Button(this);
        settings.setText("Account and connection settings");
        settings.setOnClickListener(view -> showLocalAccount());
        LinearLayout.LayoutParams settingsParams = matchWrap();
        settingsParams.topMargin = dp(18);
        content.addView(settings, settingsParams);
        }

        private void openServerDashboard() {
        if (serverAddress == null || serverAddress.isEmpty()) showSetup();
        else showDashboard();
        }

    private int countRows(Cursor cursor) {
        try {
            return cursor.getCount();
        } finally {
            cursor.close();
        }
    }

    private void addPageHeading(String titleText, String descriptionText) {
        TextView title = new TextView(this);
        title.setText(titleText);
        title.setTextColor(foregroundColor);
        title.setTextSize(28);
        title.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        content.addView(title, matchWrap());
        TextView description = localLabel(descriptionText, Color.rgb(172, 174, 161));
        LinearLayout.LayoutParams descriptionParams = matchWrap();
        descriptionParams.topMargin = dp(6);
        content.addView(description, descriptionParams);
    }

    private void addSectionTitle(String titleText, LinearLayout parent) {
        TextView title = new TextView(this);
        title.setText(titleText);
        title.setTextColor(foregroundColor);
        title.setTextSize(18);
        title.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        LinearLayout.LayoutParams params = matchWrap();
        params.topMargin = dp(22);
        params.bottomMargin = dp(8);
        parent.addView(title, params);
    }

    private TextView localLabel(String text, int color) {
        TextView label = new TextView(this);
        label.setText(text);
        label.setTextColor(color);
        label.setTextSize(14);
        return label;
    }

    private LinearLayout createLocalAction(String titleText, String detailText,
                                           View.OnClickListener listener) {
        LinearLayout action = new LinearLayout(this);
        action.setOrientation(LinearLayout.VERTICAL);
        action.setPadding(dp(14), dp(12), dp(14), dp(12));
        action.setMinimumHeight(dp(82));
        GradientDrawable actionSurface = createRoundedBackground(surfaceColor, dp(6));
        actionSurface.setStroke(dp(1), Color.rgb(39, 51, 68));
        action.setBackground(new RippleDrawable(
            android.content.res.ColorStateList.valueOf(Color.rgb(56, 189, 248)),
            actionSurface, null));
        TextView title = localLabel(titleText, foregroundColor);
        title.setTextSize(16);
        title.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        action.addView(title, matchWrap());
        TextView detail = localLabel(detailText, Color.rgb(172, 174, 161));
        detail.setTextSize(13);
        LinearLayout.LayoutParams detailParams = matchWrap();
        detailParams.topMargin = dp(4);
        action.addView(detail, detailParams);
        action.setClickable(true);
        action.setFocusable(true);
        action.setOnClickListener(listener);
        return action;
    }

    private LinearLayout.LayoutParams actionParams() {
        LinearLayout.LayoutParams params = matchWrap();
        params.bottomMargin = dp(8);
        return params;
    }

    private void showLocalLibrary() {
        activeLocalTab = "Media";
        dashboardShowing = false;
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(18), dp(18), dp(18), dp(24));
        addPageHeading("Media library", "Saved and imported files stay on this device.");

        addSectionTitle("Your files", content);

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
        importParams.topMargin = dp(8);
        content.addView(importButton, importParams);

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
                row.setOrientation(LinearLayout.VERTICAL);
                row.setPadding(dp(12), dp(10), dp(12), dp(10));
                row.setBackground(createRoundedBackground(surfaceColor, dp(6)));
                TextView fileName = new TextView(this);
                fileName.setText(name);
                fileName.setTextColor(foregroundColor);
                fileName.setMaxLines(2);
                fileName.setTextSize(15);
                row.addView(fileName, matchWrap());
                LinearLayout actions = new LinearLayout(this);
                actions.setGravity(Gravity.CENTER_VERTICAL);
                Button openButton = new Button(this);
                openButton.setText("Open");
                openButton.setOnClickListener(view -> openLocalFile(name, uri, mimeType));
                actions.addView(openButton, new LinearLayout.LayoutParams(0,
                    ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                Button editButton = new Button(this);
                editButton.setText("Edit");
                editButton.setOnClickListener(view -> openLocalEditor(name, uri, mimeType));
                actions.addView(editButton, new LinearLayout.LayoutParams(0,
                    ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                Button removeButton = new Button(this);
                removeButton.setText("Remove");
                removeButton.setOnClickListener(view -> {
                    localLibrary.removeFile(id);
                    showLocalLibrary();
                });
                actions.addView(removeButton, new LinearLayout.LayoutParams(0,
                    ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                row.addView(actions, matchWrap());
                LinearLayout.LayoutParams rowParams = matchWrap();
                rowParams.topMargin = dp(8);
                content.addView(row, rowParams);
            }
        }
        files.close();
    }

    private void showTelegramSetup() {
        activeLocalTab = "Account";
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(18), dp(18), dp(18), dp(24));
        addPageHeading("Connect Telegram", "Sign in directly from this device using Telegram's login code.");

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
        styleStatusMessage(status);
        LinearLayout.LayoutParams statusParams = matchWrap();
        statusParams.topMargin = dp(12);
        content.addView(status, statusParams);

        Button sendCode = new Button(this);
        sendCode.setText("Send login code");
        stylePrimaryButton(sendCode);
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
        stylePrimaryButton(verifyCode);
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
        stylePrimaryButton(verifyPassword);
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
        back.setText("Return to dashboard");
        back.setOnClickListener(view -> showLocalHome());
        content.addView(back, matchWrap());
    }

    private void showTelegramDownload() {
        activeLocalTab = "Tasks";
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(18), dp(18), dp(18), dp(24));
        addPageHeading("Telegram download", "Choose a message range, destination, and filters.");

        EditText link = addAccountInput("https://t.me/channel/123", null);
        link.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        addPickerButton("Browse source chats", view -> showChatPicker(link, true));
        EditText startId = addAccountInput("First message ID (blank = linked message)", null);
        startId.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText endId = addAccountInput("Last message ID (blank = first only)", null);
        endId.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        EditText destination = addAccountInput("Destination chat (default: Saved Messages)", "me");
        addPickerButton("Browse destination chats", view -> showChatPicker(destination, false));
        EditText sourceTopic = addAccountInput("Source topic ID (0 for all topics)", "0");
        sourceTopic.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        addPickerButton("Choose source topic", view -> showTopicPicker(link, sourceTopic));
        EditText destinationTopic = addAccountInput("Destination topic ID (0 for default)", "0");
        destinationTopic.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        addPickerButton("Choose destination topic", view -> showTopicPicker(destination, destinationTopic));
        EditText mediaTypes = addAccountInput("Media types: video,document,text,audio,photo,voice,animation,sticker",
            "video,document,text,audio,photo,voice,animation,sticker");
        EditText includeKeywords = addAccountInput("Include keywords (comma-separated, optional)", null);
        EditText excludeKeywords = addAccountInput("Exclude keywords (comma-separated, optional)", null);
        EditText cleanupKeywords = addAccountInput("Cleanup tags (comma-separated, optional)", null);
        EditText delay = addAccountInput("Delay per message in seconds (3-3600)", "3");
        delay.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);

        TextView status = new TextView(this);
        styleStatusMessage(status);
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
        styleDangerButton(cancelTask);
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
                File checkpointFile = new File(new File(getFilesDir(), "tasks"),
                        activeTaskId[0] + ".checkpoint");
                if (checkpointFile.isFile()) {
                    try (BufferedReader reader = new BufferedReader(new FileReader(checkpointFile))) {
                        localLibrary.updateTaskCheckpoint(activeTaskId[0],
                                Long.parseLong(reader.readLine()));
                    } catch (Exception ignored) {
                        // The checkpoint is replaced atomically after each completed message.
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
        stylePrimaryButton(start);
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
            String[] downloadArgs = new String[]{apiId, apiHash, session, messageLink,
                first, last, target.isEmpty() ? "me" : target,
                mediaTypes.getText().toString().trim(),
                includeKeywords.getText().toString().trim(),
                excludeKeywords.getText().toString().trim(), String.valueOf(delaySeconds),
                String.valueOf(sourceThreadId), String.valueOf(destinationThreadId),
                cleanupKeywords.getText().toString().trim(), "", ""};
            JSONArray savedRequest = new JSONArray();
            for (int index = 3; index <= 13; index++) savedRequest.put(downloadArgs[index]);
            long taskId = localLibrary.addTask("DOWNLOAD", label, savedRequest.toString());
            downloadArgs[14] = String.valueOf(taskId);
            activeTaskId[0] = taskId;
            taskEventOffset[0] = 0L;
            taskFinished[0] = false;
            cancellationRequested[0] = false;
            start.setEnabled(false);
            cancelTask.setEnabled(true);
            progressHandler.post(progressPoll);
                runPython("download_messages", downloadArgs,
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
        activeLocalTab = "Tasks";
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(18), dp(18), dp(18), dp(24));
        addPageHeading("Direct download", "Fetch a file over HTTP or HTTPS to app storage.");

        EditText address = addAccountInput("https://example.com/media.mp4", null);
        address.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        TextView status = new TextView(this);
        styleStatusMessage(status);
        LinearLayout.LayoutParams statusParams = matchWrap();
        statusParams.topMargin = 12;
        content.addView(status, statusParams);

        Button start = new Button(this);
        start.setText("Download to this device");
        stylePrimaryButton(start);
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
        activeLocalTab = "Tasks";
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(18), dp(18), dp(18), dp(24));
        addPageHeading("Create watcher", "Forward new matching posts from a Telegram source.");

        EditText source = addAccountInput("Source channel/chat link", null);
        source.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        addPickerButton("Browse source chats", view -> showChatPicker(source, true));
        EditText destination = addAccountInput("Destination chat (default: Saved Messages)", "me");
        addPickerButton("Browse destination chats", view -> showChatPicker(destination, false));
        EditText sourceTopic = addAccountInput("Source topic ID (0 for all topics)", "0");
        sourceTopic.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        addPickerButton("Choose source topic", view -> showTopicPicker(source, sourceTopic));
        EditText destinationTopic = addAccountInput("Destination topic ID (0 for default)", "0");
        destinationTopic.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        addPickerButton("Choose destination topic", view -> showTopicPicker(destination, destinationTopic));
        EditText mediaTypes = addAccountInput("Media types: video,document,text,audio,photo,voice,animation,sticker",
            "video,document,text,audio,photo,voice,animation,sticker");
        EditText includeKeywords = addAccountInput("Include keywords (comma-separated, optional)", null);
        EditText excludeKeywords = addAccountInput("Exclude keywords (comma-separated, optional)", null);
        EditText cleanupKeywords = addAccountInput("Cleanup caption tags (comma-separated, optional)", null);
        EditText delay = addAccountInput("Delay before forwarding (seconds, 3-3600)", "3");
        delay.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);

        TextView status = new TextView(this);
        styleStatusMessage(status);
        LinearLayout.LayoutParams statusParams = matchWrap();
        statusParams.topMargin = 8;
        content.addView(status, statusParams);

        Button start = new Button(this);
        start.setText("Start Watch task");
        stylePrimaryButton(start);
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
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU
                    && checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS)
                    != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{android.Manifest.permission.POST_NOTIFICATIONS},
                        NOTIFICATION_PERMISSION_REQUEST);
                status.setText("Allow notifications, then tap Start Watch task again.");
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
        styleInput(input);
        LinearLayout.LayoutParams params = matchWrap();
        params.topMargin = dp(8);
        content.addView(input, params);
        return input;
    }

    private Button addPickerButton(String label, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setMinHeight(dp(42));
        button.setOnClickListener(listener);
        LinearLayout.LayoutParams params = matchWrap();
        params.topMargin = dp(2);
        params.bottomMargin = dp(4);
        content.addView(button, params);
        return button;
    }

    private void showChatPicker(EditText target, boolean sourceLink) {
        String apiId = secretsStore.get("telegram_api_id");
        String apiHash = secretsStore.get("telegram_api_hash");
        String session = secretsStore.get("telegram_session");
        if (apiId == null || apiHash == null || session == null) {
            showTelegramSetup();
            return;
        }
        new Thread(() -> {
            try {
                String response = Python.getInstance().getModule("destiny_runtime")
                        .callAttr("get_chats", apiId, apiHash, session).toString();
                JSONArray chats = new JSONArray(response);
                String[] labels = new String[chats.length()];
                String[] ids = new String[chats.length()];
                String[] usernames = new String[chats.length()];
                for (int index = 0; index < chats.length(); index++) {
                    JSONObject chat = chats.getJSONObject(index);
                    ids[index] = chat.optString("id");
                    usernames[index] = chat.optString("username");
                    labels[index] = chat.optString("title", ids[index]) + "  ·  "
                            + chat.optString("type", "chat") + "  ·  " + ids[index];
                }
                new Handler(Looper.getMainLooper()).post(() ->
                        new android.app.AlertDialog.Builder(this)
                                .setTitle(sourceLink ? "Choose Telegram source" : "Choose destination")
                                .setItems(labels, (dialog, which) -> {
                                    String value = sourceLink && !usernames[which].isEmpty()
                                            ? "https://t.me/" + usernames[which] : ids[which];
                                    target.setText(value);
                                })
                                .setNegativeButton("Cancel", null)
                                .show());
            } catch (Exception exception) {
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(this, "Unable to load Telegram chats: "
                                + exception.getMessage(), Toast.LENGTH_LONG).show());
            }
        }, "destiny-chat-picker").start();
    }

    private void showTopicPicker(EditText chatInput, EditText topicInput) {
        String chatReference = chatInput.getText().toString().trim();
        if (chatReference.isEmpty() || "me".equalsIgnoreCase(chatReference)) {
            Toast.makeText(this, "Choose a forum chat first", Toast.LENGTH_SHORT).show();
            return;
        }
        String apiId = secretsStore.get("telegram_api_id");
        String apiHash = secretsStore.get("telegram_api_hash");
        String session = secretsStore.get("telegram_session");
        if (apiId == null || apiHash == null || session == null) {
            showTelegramSetup();
            return;
        }
        new Thread(() -> {
            try {
                String response = Python.getInstance().getModule("destiny_runtime")
                        .callAttr("get_forum_topics", apiId, apiHash, session,
                                chatReference).toString();
                JSONArray topics = new JSONArray(response);
                String[] labels = new String[topics.length()];
                String[] ids = new String[topics.length()];
                for (int index = 0; index < topics.length(); index++) {
                    JSONObject topic = topics.getJSONObject(index);
                    ids[index] = topic.optString("id");
                    labels[index] = topic.optString("title", "Topic") + "  ·  " + ids[index];
                }
                new Handler(Looper.getMainLooper()).post(() -> {
                    if (labels.length == 0) {
                        Toast.makeText(this, "No forum topics found for this chat",
                                Toast.LENGTH_SHORT).show();
                        return;
                    }
                    new android.app.AlertDialog.Builder(this)
                            .setTitle("Choose forum topic")
                            .setItems(labels, (dialog, which) -> topicInput.setText(ids[which]))
                            .setNegativeButton("Cancel", null)
                            .show();
                });
            } catch (Exception exception) {
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(this, "Unable to load forum topics: "
                                + exception.getMessage(), Toast.LENGTH_LONG).show());
            }
        }, "destiny-topic-picker").start();
    }

    private void styleInput(EditText input) {
        input.setTextColor(foregroundColor);
        input.setHintTextColor(mutedColor);
        input.setTextSize(14);
        input.setPadding(dp(14), dp(12), dp(14), dp(12));
        input.setMinHeight(dp(50));
        GradientDrawable field = createRoundedBackground(surfaceColor, dp(6));
        field.setStroke(dp(1), Color.rgb(39, 51, 68));
        input.setBackground(field);
    }

    private void styleStatusMessage(TextView status) {
        status.setTextColor(mutedColor);
        status.setTextSize(13);
        status.setPadding(dp(12), dp(10), dp(12), dp(10));
        status.setBackground(createRoundedBackground(surfaceColor, dp(6)));
    }

    private void stylePrimaryButton(Button button) {
        button.setTextColor(backgroundColor);
        button.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        button.setMinHeight(dp(48));
        button.setBackground(new RippleDrawable(
                android.content.res.ColorStateList.valueOf(Color.rgb(125, 211, 252)),
                createRoundedBackground(accentColor, dp(6)), null));
    }

    private void styleDangerButton(Button button) {
        button.setTextColor(Color.rgb(248, 113, 113));
        button.setMinHeight(dp(46));
        GradientDrawable dangerSurface = createRoundedBackground(surfaceColor, dp(6));
        dangerSurface.setStroke(dp(1), Color.rgb(127, 29, 29));
        button.setBackground(new RippleDrawable(
                android.content.res.ColorStateList.valueOf(Color.rgb(127, 29, 29)),
                dangerSurface, null));
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

    private void resumeInterruptedDownloads() {
        String apiId = secretsStore.get("telegram_api_id");
        String apiHash = secretsStore.get("telegram_api_hash");
        String session = secretsStore.get("telegram_session");
        if (apiId == null || apiHash == null || session == null || !embeddedRuntimeReady) return;

        ArrayList<String[]> pending = new ArrayList<>();
        Cursor tasks = localLibrary.getInterruptedDownloads();
        try {
            while (tasks.moveToNext()) {
                try {
                    JSONArray request = new JSONArray(tasks.getString(1));
                    if (request.length() != 11) continue;
                    long taskId = tasks.getLong(0);
                    String[] args = new String[16];
                    args[0] = apiId;
                    args[1] = apiHash;
                    args[2] = session;
                    for (int index = 0; index < request.length(); index++) {
                        args[index + 3] = request.getString(index);
                    }
                    args[14] = String.valueOf(taskId);
                    long checkpoint = tasks.getLong(2);
                    File checkpointFile = new File(new File(getFilesDir(), "tasks"),
                            taskId + ".checkpoint");
                    if (checkpointFile.isFile()) {
                        try (BufferedReader reader = new BufferedReader(
                                new FileReader(checkpointFile))) {
                            checkpoint = Math.max(checkpoint, Long.parseLong(reader.readLine()));
                        } catch (Exception ignored) {
                            // Keep the last checkpoint committed to SQLite.
                        }
                    }
                    args[15] = String.valueOf(checkpoint);
                    pending.add(args);
                    localLibrary.updateTask(taskId, "RUNNING", "Resuming after interruption");
                } catch (Exception invalidTask) {
                    localLibrary.updateTask(tasks.getLong(0), "FAILED",
                            "Saved task settings could not be restored");
                }
            }
        } finally {
            tasks.close();
        }
        if (pending.isEmpty()) return;

        new Thread(() -> {
            for (String[] args : pending) {
                long taskId = Long.parseLong(args[14]);
                try {
                    String response = Python.getInstance().getModule("destiny_runtime")
                            .callAttr("download_messages", (Object[]) args).toString();
                    if (!response.contains("TASK_SUMMARY|")) {
                        localLibrary.updateTask(taskId, "INTERRUPTED", response);
                        continue;
                    }
                    consumeTaskEvents(taskId, new long[]{Long.MAX_VALUE});
                    localLibrary.updateTask(taskId, taskSummaryState(response),
                            response.substring(response.indexOf("TASK_SUMMARY|")
                                    + "TASK_SUMMARY|".length()));
                    deleteTaskProgressFiles(taskId);
                } catch (Exception exception) {
                    localLibrary.updateTask(taskId, "INTERRUPTED",
                            "Will retry when the app is opened: " + exception.getMessage());
                }
            }
        }, "destiny-resume-downloads").start();
    }

    private String taskSummaryState(String response) {
        String summary = response.substring(response.indexOf("TASK_SUMMARY|")
                + "TASK_SUMMARY|".length());
        long downloaded = 0;
        long failed = 0;
        boolean cancelled = false;
        for (String value : summary.split(",")) {
            String[] pair = value.split("=", 2);
            if (pair.length != 2) continue;
            try {
                if ("downloaded".equals(pair[0])) downloaded = Long.parseLong(pair[1]);
                if ("failed".equals(pair[0])) failed = Long.parseLong(pair[1]);
                if ("cancelled".equals(pair[0])) cancelled = "1".equals(pair[1]);
            } catch (NumberFormatException ignored) {
                // Keep the summary state conservative if its counters are malformed.
            }
        }
        if (cancelled) return "CANCELLED";
        if (failed > 0) return downloaded > 0 ? "PARTIAL" : "FAILED";
        return "COMPLETE";
    }

    private void deleteTaskProgressFiles(long taskId) {
        File taskDirectory = new File(getFilesDir(), "tasks");
        new File(taskDirectory, taskId + ".txt").delete();
        new File(taskDirectory, taskId + ".checkpoint").delete();
        new File(taskDirectory, taskId + ".checkpoint.tmp").delete();
        new File(taskDirectory, taskId + ".jsonl").delete();
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
                        new File(new File(getFilesDir(), "tasks"), taskId + ".checkpoint").delete();
                        new File(new File(getFilesDir(), "tasks"), taskId + ".jsonl").delete();
                    }
                    status.setText(summary);
                    if (completion != null) completion.run();
                    return;
                }
                if (response.startsWith("AUTH_OK:")) {
                    secretsStore.put("telegram_session", response.substring("AUTH_OK:".length()));
                    showLocalHome();
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
                    localLibrary.updateTask(taskId, "INTERRUPTED", response);
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
        settings.setAllowContentAccess(true);
        settings.setSupportZoom(false);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            settings.setSafeBrowsingEnabled(true);
        }
        webView.setBackgroundColor(backgroundColor);
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                if (pageError != null) pageError.setVisibility(View.GONE);
                if (pageProgress != null) {
                    pageProgress.setProgress(0);
                    pageProgress.setVisibility(View.VISIBLE);
                }
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                if (pageProgress != null) pageProgress.setVisibility(View.GONE);
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request,
                                        WebResourceError error) {
                if (request.isForMainFrame() && pageError != null) {
                    pageError.setText("Dashboard unavailable\nCheck your server connection and tap to retry.");
                    pageError.setVisibility(View.VISIBLE);
                }
            }

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
            public void onProgressChanged(WebView view, int progress) {
                if (pageProgress == null) return;
                pageProgress.setProgress(progress);
                pageProgress.setVisibility(progress >= 100 ? View.GONE : View.VISIBLE);
            }

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
        activeLocalTab = "Account";
        dashboardShowing = false;
        showLocalSurface();
        content.removeAllViews();
        content.setPadding(dp(18), dp(18), dp(18), dp(24));
        addPageHeading("Connect to Destiny", "Link a local-network or public dashboard server.");

        LinearLayout modeRow = new LinearLayout(this);
        modeRow.setOrientation(LinearLayout.HORIZONTAL);
        Button localButton = new Button(this);
        localButton.setText("Local network");
        localButton.setEnabled(!isLocalMode());
        localButton.setOnClickListener(view -> {
            appMode = MODE_LOCAL;
            preferences.edit().putString(PREF_APP_MODE, appMode).apply();
            showSetup();
        });
        Button webButton = new Button(this);
        webButton.setText("Public server");
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
        styleInput(addressInput);
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
        stylePrimaryButton(connect);
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

        Button localLibrary = new Button(this);
        localLibrary.setText("Continue to device library");
        localLibrary.setOnClickListener(view -> showLocalHome());
        LinearLayout.LayoutParams localLibraryParams = matchWrap();
        localLibraryParams.topMargin = 8;
        content.addView(localLibrary, localLibraryParams);
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
        dashboardShowing = true;
        root.removeAllViews();

        LinearLayout toolbar = new LinearLayout(this);
        toolbar.setGravity(Gravity.CENTER_VERTICAL);
        toolbar.setPadding(18, 6, 14, 6);
        toolbar.setBackgroundColor(backgroundColor);

        LinearLayout identity = new LinearLayout(this);
        identity.setOrientation(LinearLayout.VERTICAL);
        TextView brand = new TextView(this);
        brand.setText("DESTINY");
        brand.setTextColor(foregroundColor);
        brand.setTextSize(16);
        brand.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        TextView connection = new TextView(this);
        connection.setText(Uri.parse(serverAddress).getHost());
        connection.setTextColor(Color.rgb(154, 174, 170));
        connection.setTextSize(11);
        connection.setMaxLines(1);
        connection.setEllipsize(android.text.TextUtils.TruncateAt.END);
        identity.addView(brand, matchWrap());
        identity.addView(connection, matchWrap());
        toolbar.addView(identity, new LinearLayout.LayoutParams(0,
            ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        toolbar.addView(createToolbarAction("Library", view -> showLocalLibrary()),
            toolbarActionParams());
        toolbar.addView(createToolbarAction("Server", view -> showSetup()),
            toolbarActionParams());
        root.addView(toolbar, matchWrap());

        pageProgress = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        pageProgress.setMax(100);
        pageProgress.setProgressTintList(android.content.res.ColorStateList.valueOf(accentColor));
        pageProgress.setProgressBackgroundTintList(android.content.res.ColorStateList.valueOf(surfaceColor));
        pageProgress.setVisibility(View.VISIBLE);
        root.addView(pageProgress, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, dp(2)));

        FrameLayout dashboardFrame = new FrameLayout(this);
        dashboardFrame.setBackgroundColor(Color.BLACK);
        if (webView.getParent() != null) {
            ((ViewGroup) webView.getParent()).removeView(webView);
        }
        dashboardFrame.addView(webView, new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        pageError = new TextView(this);
        pageError.setTextColor(foregroundColor);
        pageError.setTextSize(16);
        pageError.setGravity(Gravity.CENTER);
        pageError.setPadding(dp(32), dp(24), dp(32), dp(24));
        pageError.setBackgroundColor(backgroundColor);
        pageError.setVisibility(View.GONE);
        pageError.setFocusable(true);
        pageError.setClickable(true);
        pageError.setOnClickListener(view -> webView.reload());
        dashboardFrame.addView(pageError, new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        root.addView(dashboardFrame, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));
        webView.loadUrl(serverAddress);
    }

    private void showLocalSurface() {
        dashboardShowing = false;
        root.removeAllViews();
        LinearLayout shell = new LinearLayout(this);
        shell.setOrientation(LinearLayout.VERTICAL);
        shell.setBackgroundColor(backgroundColor);

        LinearLayout header = new LinearLayout(this);
        header.setGravity(Gravity.CENTER_VERTICAL);
        header.setPadding(dp(12), dp(8), dp(12), dp(8));
        header.setBackgroundColor(surfaceColor);
        header.addView(createToolbarAction("Tools", view -> showLocalTools()),
            new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, dp(42)));
        TextView brand = new TextView(this);
        brand.setText("DESTINY TG\n" + activeLocalTab.toUpperCase(java.util.Locale.ROOT));
        brand.setTextColor(foregroundColor);
        brand.setTextSize(13);
        brand.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        brand.setGravity(Gravity.CENTER_VERTICAL);
        brand.setMaxLines(2);
        header.addView(brand, new LinearLayout.LayoutParams(0,
            ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        header.addView(createToolbarAction("Account", view -> showLocalAccount()),
            new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, dp(42)));
        shell.addView(header, matchWrap());

        if (localScrollView.getParent() != null) {
            ((ViewGroup) localScrollView.getParent()).removeView(localScrollView);
        }
        shell.addView(localScrollView, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));

        LinearLayout navigation = new LinearLayout(this);
        navigation.setGravity(Gravity.CENTER);
        navigation.setPadding(dp(6), dp(5), dp(6), dp(5));
        navigation.setBackgroundColor(surfaceColor);
        addNavItem(navigation, "Home", view -> showLocalHome());
        addNavItem(navigation, "Tasks", view -> showLocalTasks());
        addNavItem(navigation, "Media", view -> showLocalLibrary());
        addNavItem(navigation, "Tools", view -> showLocalTools());
        addNavItem(navigation, "Account", view -> showLocalAccount());
        shell.addView(navigation, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, dp(56)));
        root.addView(shell, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));
        }

        private void addNavItem(LinearLayout navigation, String label,
                    View.OnClickListener listener) {
        TextView item = new TextView(this);
        item.setText(label);
        item.setTextColor(label.equals(activeLocalTab)
            ? accentColor : Color.rgb(172, 174, 161));
        item.setTextSize(12);
        item.setTypeface(Typeface.DEFAULT, label.equals(activeLocalTab)
            ? Typeface.BOLD : Typeface.NORMAL);
        item.setMinHeight(dp(44));
        item.setGravity(Gravity.CENTER);
        GradientDrawable itemSurface = createRoundedBackground(
                label.equals(activeLocalTab) ? Color.rgb(17, 45, 64) : Color.TRANSPARENT, dp(6));
        item.setBackground(new RippleDrawable(
            android.content.res.ColorStateList.valueOf(Color.rgb(56, 189, 248)), itemSurface, null));
        item.setClickable(true);
        item.setFocusable(true);
        item.setOnClickListener(listener);
        navigation.addView(item, new LinearLayout.LayoutParams(0,
            ViewGroup.LayoutParams.MATCH_PARENT, 1));
    }

    private Button createToolbarAction(String label, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setTextSize(12);
        button.setTextColor(accentColor);
        button.setAllCaps(false);
        button.setMinHeight(dp(40));
        button.setMinimumHeight(dp(40));
        button.setPadding(dp(12), 0, dp(12), 0);
        button.setBackground(new RippleDrawable(
                android.content.res.ColorStateList.valueOf(Color.rgb(43, 68, 72)),
                createRoundedBackground(surfaceColor, dp(10)), null));
        button.setOnClickListener(listener);
        return button;
    }

    private LinearLayout.LayoutParams toolbarActionParams() {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, dp(42));
        params.leftMargin = dp(8);
        return params;
    }

    private GradientDrawable createRoundedBackground(int color, int radius) {
        GradientDrawable drawable = new GradientDrawable();
        drawable.setColor(color);
        drawable.setCornerRadius(radius);
        return drawable;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
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
        if (dashboardShowing && webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}