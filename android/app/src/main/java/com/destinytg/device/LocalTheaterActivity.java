package com.destinytg.device;

import android.app.Activity;
import android.graphics.Color;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.MediaController;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

public final class LocalTheaterActivity extends Activity {
    private MediaPlayer audioPlayer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Uri mediaUri = getIntent().getData();
        String mimeType = getIntent().getType();
        String displayName = getIntent().getStringExtra("displayName");
        if (mediaUri == null || mimeType == null) {
            finish();
            return;
        }

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setPadding(dp(16), dp(12), dp(16), dp(16));
        root.setBackgroundColor(Color.BLACK);

        TextView eyebrow = new TextView(this);
        eyebrow.setText("LOCAL THEATER");
        eyebrow.setTextColor(Color.rgb(56, 189, 248));
        eyebrow.setTextSize(10);
        eyebrow.setTypeface(android.graphics.Typeface.DEFAULT, android.graphics.Typeface.BOLD);
        root.addView(eyebrow, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView title = new TextView(this);
        title.setText(displayName == null ? "Now playing" : displayName);
        title.setTextColor(Color.rgb(241, 245, 249));
        title.setTextSize(18);
        title.setMaxLines(1);
        title.setEllipsize(android.text.TextUtils.TruncateAt.END);
        title.setGravity(Gravity.CENTER_VERTICAL);
        root.addView(title, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        if (mimeType.startsWith("video/")) {
            VideoView videoView = new VideoView(this);
            videoView.setVideoURI(mediaUri);
            MediaController controls = new MediaController(this);
            controls.setAnchorView(videoView);
            videoView.setMediaController(controls);
            videoView.setOnPreparedListener(MediaPlayer::start);
            videoView.setOnErrorListener((player, what, extra) -> {
                Toast.makeText(this, "This video format is not supported on this device",
                        Toast.LENGTH_LONG).show();
                finish();
                return true;
            });
            root.addView(videoView, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));
        } else if (mimeType.startsWith("audio/")) {
            TextView audioLabel = new TextView(this);
            audioLabel.setText("AUDIO  /  PLAYING FROM THIS DEVICE");
            audioLabel.setTextColor(Color.rgb(148, 163, 184));
            audioLabel.setTextSize(13);
            audioLabel.setGravity(Gravity.CENTER);
            root.addView(audioLabel, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));

            Button playPause = new Button(this);
            playPause.setText("Preparing audio");
                playPause.setTextColor(Color.rgb(7, 9, 13));
                playPause.setTypeface(android.graphics.Typeface.DEFAULT,
                    android.graphics.Typeface.BOLD);
                playPause.setMinHeight(dp(50));
                playPause.setBackgroundTintList(android.content.res.ColorStateList.valueOf(
                    Color.rgb(56, 189, 248)));
            playPause.setEnabled(false);
            root.addView(playPause, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            try {
                audioPlayer = new MediaPlayer();
                audioPlayer.setDataSource(this, mediaUri);
                audioPlayer.setOnPreparedListener(player -> {
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

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    @Override
    protected void onDestroy() {
        if (audioPlayer != null) {
            audioPlayer.release();
            audioPlayer = null;
        }
        super.onDestroy();
    }
}