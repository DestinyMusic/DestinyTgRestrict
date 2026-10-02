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
        root.setPadding(16, 16, 16, 16);
        root.setBackgroundColor(Color.BLACK);

        TextView title = new TextView(this);
        title.setText(displayName == null ? "Now playing" : displayName);
        title.setTextColor(Color.WHITE);
        title.setTextSize(18);
        title.setGravity(Gravity.CENTER);
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
            audioLabel.setText("Audio playback");
            audioLabel.setTextColor(Color.LTGRAY);
            audioLabel.setGravity(Gravity.CENTER);
            root.addView(audioLabel, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));

            Button playPause = new Button(this);
            playPause.setText("Preparing audio");
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

    @Override
    protected void onDestroy() {
        if (audioPlayer != null) {
            audioPlayer.release();
            audioPlayer = null;
        }
        super.onDestroy();
    }
}