package com.destinytg.device;

import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.media.MediaPlayer;
import android.media.PlaybackParams;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.JavascriptInterface;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.MediaController;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;
import org.json.JSONObject;

public final class LocalTheaterActivity extends Activity {
    private MediaPlayer audioPlayer;
    private MediaPlayer videoPlayer;
    private LocalTelegramStreamServer telegramStream;
    private LocalMediaProxyServer mediaProxy;
    private WebView advancedWebView;
    private VideoView videoView;
    private Uri currentMediaUri;
    private String currentMimeType;
    private String currentDisplayName;
    private float playbackSpeed = 1.0f;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Uri mediaUri = getIntent().getData();
        String mimeType = getIntent().getType();
        String displayName = getIntent().getStringExtra("displayName");
        String telegramLink = getIntent().getStringExtra("telegramLink");
        if (telegramLink == null && isTelegramLink(mediaUri)) {
            telegramLink = mediaUri.toString();
        }
        if (telegramLink != null) {
            openTelegramMedia(telegramLink, displayName);
            return;
        }
        if (mediaUri == null) {
            finish();
            return;
        }
        currentMediaUri = mediaUri;
        currentDisplayName = displayName;
        String resolvedMimeType = mimeType;
        if (resolvedMimeType == null || resolvedMimeType.isEmpty()) {
            resolvedMimeType = guessMimeType(mediaUri);
        }
        currentMimeType = resolvedMimeType;
        showPlayer(mediaUri, resolvedMimeType, displayName);
    }

    private void showPlayer(Uri mediaUri, String mimeType, String displayName) {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setPadding(dp(16), dp(12), dp(16), dp(16));
        root.setBackground(new GradientDrawable(GradientDrawable.Orientation.TL_BR,
            new int[]{Color.rgb(20, 43, 43), Color.rgb(8, 15, 18), Color.rgb(30, 24, 22)}));

        TextView eyebrow = new TextView(this);
        eyebrow.setText("DESTINY  /  THEATER");
        eyebrow.setTextColor(Color.rgb(107, 224, 204));
        eyebrow.setTextSize(10);
        eyebrow.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        root.addView(eyebrow, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView sourceLabel = new TextView(this);
        sourceLabel.setText(isRemoteUri(mediaUri) ? "STREAMING SOURCE" : "DEVICE LIBRARY");
        sourceLabel.setTextColor(Color.rgb(157, 174, 171));
        sourceLabel.setTextSize(10);
        root.addView(sourceLabel, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView title = new TextView(this);
        title.setText(displayName == null ? "Now playing" : displayName);
        title.setTextColor(Color.rgb(241, 245, 249));
        title.setTextSize(21);
        title.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        title.setMaxLines(1);
        title.setEllipsize(android.text.TextUtils.TruncateAt.END);
        title.setGravity(Gravity.CENTER_VERTICAL);
        root.addView(title, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        Button settings = new Button(this);
        settings.setText("Playback speed");
        styleTheaterButton(settings, Color.rgb(26, 43, 44), Color.rgb(107, 224, 204));
        settings.setOnClickListener(view -> showPlaybackSettings());
        root.addView(settings, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        Button threeDimensional = new Button(this);
        threeDimensional.setText("On-device 3D and subtitles");
        styleTheaterButton(threeDimensional, Color.rgb(31, 47, 49), Color.rgb(255, 152, 127));
        threeDimensional.setOnClickListener(view -> openAdvancedTheater());
        root.addView(threeDimensional, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        if ((mimeType != null && mimeType.startsWith("video/"))
            || (isRemoteUri(mediaUri)
            && (mimeType == null || !mimeType.startsWith("audio/")))) {
            videoView = new VideoView(this);
            videoView.setVideoURI(mediaUri);
            MediaController controls = new MediaController(this);
            controls.setAnchorView(videoView);
            videoView.setMediaController(controls);
            videoView.setOnPreparedListener(player -> {
                videoPlayer = player;
                applyPlaybackSpeed(player);
                player.start();
            });
            videoView.setOnErrorListener((player, what, extra) -> {
                Toast.makeText(this, "This video format is not supported on this device",
                        Toast.LENGTH_LONG).show();
                finish();
                return true;
            });
            root.addView(videoView, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));
        } else if (mimeType != null && mimeType.startsWith("audio/")) {
            TextView audioLabel = new TextView(this);
            audioLabel.setText("AUDIO  /  PLAYING FROM THIS DEVICE");
            audioLabel.setTextColor(Color.rgb(148, 163, 184));
            audioLabel.setTextSize(13);
            audioLabel.setGravity(Gravity.CENTER);
            root.addView(audioLabel, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));

            Button playPause = new Button(this);
            playPause.setText("Preparing audio");
            styleTheaterButton(playPause, Color.rgb(107, 224, 204), Color.rgb(7, 16, 17));
            playPause.setEnabled(false);
            root.addView(playPause, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            try {
                audioPlayer = new MediaPlayer();
                audioPlayer.setDataSource(this, mediaUri);
                audioPlayer.setOnPreparedListener(player -> {
                    applyPlaybackSpeed(player);
                    playPause.setText("Pause");
                    playPause.setEnabled(true);
                    player.start();
                });
                audioPlayer.setOnCompletionListener(player -> playPause.setText("Replay"));
                audioPlayer.setOnErrorListener((player, what, extra) -> {
                    Toast.makeText(this, "This audio format is not supported on this device",
                            Toast.LENGTH_LONG).show();
                    finish();
                    return true;
                });
                playPause.setOnClickListener(view -> {
                    if (audioPlayer == null) return;
                    if (audioPlayer.isPlaying()) {
                        audioPlayer.pause();
                        playPause.setText("Play");
                    } else {
                        if (audioPlayer.getCurrentPosition() >= audioPlayer.getDuration()) {
                            audioPlayer.seekTo(0);
                        }
                        audioPlayer.start();
                        playPause.setText("Pause");
                    }
                });
                audioPlayer.prepareAsync();
            } catch (Exception exception) {
                Toast.makeText(this, "Unable to open this audio file", Toast.LENGTH_LONG).show();
                finish();
            }
        }

        setContentView(root);
    }

    private void openTelegramMedia(String link, String displayName) {
        TextView loading = new TextView(this);
        loading.setText("Connecting to Telegram media…");
        loading.setTextColor(Color.rgb(241, 246, 244));
        loading.setGravity(Gravity.CENTER);
        loading.setBackgroundColor(Color.rgb(10, 17, 20));
        setContentView(loading);
        new Thread(() -> {
            try {
                LocalSecretsStore secrets = new LocalSecretsStore(this);
                String apiId = secrets.get("telegram_api_id");
                String apiHash = secrets.get("telegram_api_hash");
                String session = secrets.get("telegram_session");
                if (apiId == null || apiHash == null || session == null) {
                    throw new IllegalStateException("Connect Telegram before opening this link");
                }
                LocalTelegramStreamServer server = new LocalTelegramStreamServer();
                server.start(apiId, apiHash, session, link);
                telegramStream = server;
                currentMediaUri = Uri.parse(server.getUrl());
                currentMimeType = server.getMimeType();
                currentDisplayName = displayName == null ? server.getFileName() : displayName;
                new Handler(Looper.getMainLooper()).post(() -> showPlayer(currentMediaUri,
                    currentMimeType, currentDisplayName));
            } catch (Exception exception) {
                new Handler(Looper.getMainLooper()).post(() -> {
                    Toast.makeText(this, "Unable to open Telegram media: "
                            + exception.getMessage(), Toast.LENGTH_LONG).show();
                    finish();
                });
            }
        }, "destiny-theater-telegram").start();
    }

    private void openAdvancedTheater() {
        if (videoView != null) videoView.pause();
        TextView loading = new TextView(this);
        loading.setText("Preparing on-device 3D theater…");
        loading.setTextColor(Color.rgb(241, 246, 244));
        loading.setGravity(Gravity.CENTER);
        loading.setBackgroundColor(Color.rgb(10, 17, 20));
        setContentView(loading);
        new Thread(() -> {
            try {
                String mediaUrl;
                String sourceKind;
                if (telegramStream != null) {
                    mediaUrl = telegramStream.getUrl();
                    sourceKind = "TELEGRAM / DEVICE NETWORK";
                } else if (isRemoteUri(currentMediaUri)) {
                    mediaProxy = LocalMediaProxyServer.forRemoteUrl(this,
                            currentMediaUri.toString(), currentMimeType);
                    mediaProxy.start();
                    mediaUrl = mediaProxy.getUrl();
                    sourceKind = "DIRECT URL / DEVICE NETWORK";
                } else {
                    mediaProxy = LocalMediaProxyServer.forLocalUri(this,
                            currentMediaUri, currentMimeType);
                    mediaProxy.start();
                    mediaUrl = mediaProxy.getUrl();
                    sourceKind = "LOCAL FILE";
                }
                String finalUrl = mediaUrl;
                String finalSourceKind = sourceKind;
                String finalName = currentDisplayName == null ? "Now playing" : currentDisplayName;
                new Handler(Looper.getMainLooper()).post(() -> showWebGlTheater(
                        finalUrl, finalName, finalSourceKind));
            } catch (Exception exception) {
                new Handler(Looper.getMainLooper()).post(() -> {
                    Toast.makeText(this, "Unable to prepare local 3D theater: "
                            + exception.getMessage(), Toast.LENGTH_LONG).show();
                    showPlayer(currentMediaUri, currentMimeType, currentDisplayName);
                });
            }
        }, "destiny-local-webgl-theater").start();
    }

    private void showWebGlTheater(String url, String name, String sourceKind) {
        WebView theater = new WebView(this);
        advancedWebView = theater;
        WebSettings settings = theater.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        theater.setBackgroundColor(Color.rgb(9, 17, 20));
        theater.addJavascriptInterface(new Object() {
            @JavascriptInterface
            public void backToPlayer() {
                runOnUiThread(() -> {
                    if (advancedWebView != null) {
                        advancedWebView.destroy();
                        advancedWebView = null;
                    }
                    if (mediaProxy != null) {
                        mediaProxy.close();
                        mediaProxy = null;
                    }
                    showPlayer(currentMediaUri, currentMimeType, currentDisplayName);
                });
            }
        }, "Android");
        theater.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String pageUrl) {
                String script = "window.loadMedia(" + JSONObject.quote(url) + ","
                        + JSONObject.quote(name) + "," + JSONObject.quote(sourceKind) + ")";
                view.evaluateJavascript(script, null);
            }
        });
        setContentView(theater);
        theater.loadUrl("file:///android_asset/local_theater.html");
    }

    private void showPlaybackSettings() {
        String[] speeds = {"0.5×", "0.75×", "1.0×", "1.25×", "1.5×", "2.0×"};
        float[] values = {0.5f, 0.75f, 1.0f, 1.25f, 1.5f, 2.0f};
        new AlertDialog.Builder(this)
                .setTitle("Playback speed")
                .setSingleChoiceItems(speeds, speedIndex(values), (dialog, index) -> {
                    playbackSpeed = values[index];
                    if (videoPlayer != null) applyPlaybackSpeed(videoPlayer);
                    if (audioPlayer != null) applyPlaybackSpeed(audioPlayer);
                    dialog.dismiss();
                })
                .setNegativeButton("Close", null)
                .show();
    }

    private int speedIndex(float[] values) {
        for (int index = 0; index < values.length; index++) {
            if (values[index] == playbackSpeed) return index;
        }
        return 2;
    }

    private void applyPlaybackSpeed(MediaPlayer player) {
        try {
            PlaybackParams params = player.getPlaybackParams();
            player.setPlaybackParams(params.setSpeed(playbackSpeed));
        } catch (IllegalStateException ignored) {
            // The player may not be prepared yet.
        }
    }

    private boolean isTelegramLink(Uri uri) {
        if (uri == null || uri.getHost() == null) return false;
        String host = uri.getHost().toLowerCase(java.util.Locale.ROOT);
        return host.equals("t.me") || host.equals("www.t.me")
                || host.equals("telegram.me") || host.equals("www.telegram.me");
    }

    private boolean isRemoteUri(Uri uri) {
        String scheme = uri.getScheme();
        return "http".equalsIgnoreCase(scheme) || "https".equalsIgnoreCase(scheme);
    }

    private String guessMimeType(Uri uri) {
        String path = uri.getLastPathSegment();
        if (path != null) {
            int dot = path.lastIndexOf('.');
            if (dot >= 0 && dot < path.length() - 1) {
                String type = android.webkit.MimeTypeMap.getSingleton()
                        .getMimeTypeFromExtension(path.substring(dot + 1).toLowerCase(
                                java.util.Locale.ROOT));
                if (type != null) return type;
            }
        }
        return "application/octet-stream";
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private void styleTheaterButton(Button button, int background, int foreground) {
        button.setTextColor(foreground);
        button.setTextSize(14);
        button.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        button.setMinHeight(dp(48));
        GradientDrawable surface = new GradientDrawable();
        surface.setColor(background);
        surface.setCornerRadius(dp(12));
        surface.setStroke(dp(1), Color.rgb(74, 107, 105));
        button.setBackground(surface);
    }

    @Override
    protected void onDestroy() {
        if (mediaProxy != null) {
            mediaProxy.close();
            mediaProxy = null;
        }
        if (telegramStream != null) {
            telegramStream.close();
            telegramStream = null;
        }
        if (audioPlayer != null) {
            audioPlayer.release();
            audioPlayer = null;
        }
        super.onDestroy();
    }
}