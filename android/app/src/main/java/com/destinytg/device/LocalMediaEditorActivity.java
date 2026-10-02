package com.destinytg.device;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.media.MediaCodec;
import android.media.MediaExtractor;
import android.media.MediaMetadataRetriever;
import android.media.MediaMuxer;
import android.net.Uri;
import android.os.Bundle;
import android.os.ParcelFileDescriptor;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Map;

public final class LocalMediaEditorActivity extends Activity {
    private Uri mediaUri;
    private String displayName;
    private String mimeType;
    private LocalLibraryStore libraryStore;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        libraryStore = new LocalLibraryStore(this);
        mediaUri = getIntent().getData();
        displayName = getIntent().getStringExtra("displayName");
        mimeType = getIntent().getType();

        if (mediaUri == null) {
            Toast.makeText(this, "No media selected for editing", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(20, 20, 20, 20);
        root.setGravity(Gravity.TOP);

        TextView title = new TextView(this);
        title.setText("Media editor");
        title.setTextSize(22);
        title.setTextColor(0xFFF1F5F9);
        title.setGravity(Gravity.CENTER);
        root.addView(title, matchWrap());

        TextView info = new TextView(this);
        info.setText(buildInfoText());
        info.setTextColor(0xFFCBD5E1);
        info.setTextSize(14);
        LinearLayout.LayoutParams infoParams = matchWrap();
        infoParams.topMargin = 12;
        root.addView(info, infoParams);

        EditText trimStart = new EditText(this);
        trimStart.setSingleLine(true);
        trimStart.setHint("Trim start (seconds)");
        trimStart.setInputType(android.text.InputType.TYPE_CLASS_NUMBER
                | android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);
        root.addView(trimStart, matchWrap());

        EditText trimEnd = new EditText(this);
        trimEnd.setSingleLine(true);
        trimEnd.setHint("Trim end (seconds)");
        trimEnd.setInputType(android.text.InputType.TYPE_CLASS_NUMBER
                | android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);
        root.addView(trimEnd, matchWrap());

        TextView editStatus = new TextView(this);
        editStatus.setTextColor(0xFFCBD5E1);
        root.addView(editStatus, matchWrap());

        Button trim = new Button(this);
        trim.setText("Trim and export MP4");
        trim.setOnClickListener(view -> {
            try {
                double startSeconds = Double.parseDouble(trimStart.getText().toString().trim());
                double endSeconds = Double.parseDouble(trimEnd.getText().toString().trim());
                if (startSeconds < 0 || endSeconds <= startSeconds) {
                    throw new IllegalArgumentException();
                }
                trimMedia(startSeconds, endSeconds, editStatus, trim);
            } catch (Exception exception) {
                editStatus.setText("Enter valid start/end times in seconds.");
            }
        });
        root.addView(trim, matchWrap());

        Button theater = new Button(this);
        theater.setText("Open in theater");
        theater.setOnClickListener(view -> openInTheater());
        root.addView(theater, matchWrap());

        Button export = new Button(this);
        export.setText("Duplicate to local editor export");
        export.setOnClickListener(view -> duplicateCurrentFile());
        root.addView(export, matchWrap());

        Button rename = new Button(this);
        rename.setText("Rename export");
        rename.setOnClickListener(view -> renameCurrentFile());
        root.addView(rename, matchWrap());

        Button back = new Button(this);
        back.setText("Back to library");
        back.setOnClickListener(view -> finish());
        root.addView(back, matchWrap());

        setContentView(root);
    }

    private String buildInfoText() {
        String fileName = displayName == null ? "Selected media" : displayName;
        String mediaType = mimeType == null || mimeType.trim().isEmpty() ? "unknown" : mimeType;
        String duration = "unknown";

        MediaMetadataRetriever retriever = new MediaMetadataRetriever();
        try {
            retriever.setDataSource(this, mediaUri);
            String rawDuration = retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION);
            if (rawDuration != null && !rawDuration.isEmpty()) {
                long ms = Long.parseLong(rawDuration);
                duration = formatDuration(ms);
            }
        } catch (Exception ignored) {
            duration = "unknown";
        } finally {
            try {
                retriever.release();
            } catch (Exception ignored) {
                // no-op
            }
        }

        return "Name: " + fileName + "\nType: " + mediaType + "\nDuration: " + duration + "\nMode: local export and quick media cleanup";
    }

    private String formatDuration(long ms) {
        long totalSeconds = ms / 1000L;
        long hours = totalSeconds / 3600L;
        long minutes = (totalSeconds % 3600L) / 60L;
        long seconds = totalSeconds % 60L;
        if (hours > 0) {
            return String.format("%02d:%02d:%02d", hours, minutes, seconds);
        }
        return String.format("%02d:%02d", minutes, seconds);
    }

    private void openInTheater() {
        try {
            if (mimeType == null || mimeType.isEmpty()) {
                mimeType = "application/octet-stream";
            }
            Intent theaterIntent = new Intent(this, LocalTheaterActivity.class);
            theaterIntent.setDataAndType(mediaUri, mimeType);
            theaterIntent.putExtra("displayName", displayName == null ? "Local media" : displayName);
            startActivity(theaterIntent);
        } catch (Exception exception) {
            Toast.makeText(this, "Unable to open this file in the theater", Toast.LENGTH_SHORT).show();
        }
    }

    private void duplicateCurrentFile() {
        try {
            File exportDir = new File(getFilesDir(), "editor_exports");
            if (!exportDir.exists()) {
                exportDir.mkdirs();
            }

            String fileName = displayName == null ? "exported_media" : displayName;
            File target = new File(exportDir, sanitizeName(fileName));
            if (target.exists()) {
                String withoutExt = removeExtension(fileName);
                String extension = extensionOf(fileName);
                target = new File(exportDir, withoutExt + "-copy" + (extension.isEmpty() ? "" : "." + extension));
            }

            try (InputStream in = getContentResolver().openInputStream(mediaUri);
                 OutputStream out = new FileOutputStream(target)) {
                if (in == null) {
                    throw new IllegalStateException("Unable to read source file");
                }
                byte[] buffer = new byte[8192];
                int count;
                while ((count = in.read(buffer)) != -1) {
                    out.write(buffer, 0, count);
                }
                out.flush();
            }

            libraryStore.addFile(target.getName(), Uri.fromFile(target).toString(), mimeType == null ? "application/octet-stream" : mimeType);
            Toast.makeText(this, "Duplicated to " + target.getName(), Toast.LENGTH_SHORT).show();
        } catch (Exception exception) {
            Toast.makeText(this, "Copy failed: " + exception.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    private void trimMedia(double startSeconds, double endSeconds,
                           TextView status, Button trimButton) {
        trimButton.setEnabled(false);
        status.setText("Preparing local trim…");
        new Thread(() -> {
            MediaExtractor extractor = new MediaExtractor();
            MediaMuxer muxer = null;
            ParcelFileDescriptor descriptor = null;
            File output = null;
            boolean muxerStarted = false;
            String result;
            try {
                descriptor = getContentResolver().openFileDescriptor(mediaUri, "r");
                if (descriptor == null) throw new IllegalStateException("Cannot read source media");
                extractor.setDataSource(descriptor.getFileDescriptor());

                File exportDirectory = new File(getFilesDir(), "editor_exports");
                if (!exportDirectory.exists() && !exportDirectory.mkdirs()) {
                    throw new IllegalStateException("Cannot create editor export folder");
                }
                String baseName = removeExtension(displayName == null ? "media" : displayName);
                output = new File(exportDirectory, baseName + "-trimmed-"
                        + System.currentTimeMillis() + ".mp4");
                muxer = new MediaMuxer(output.getAbsolutePath(),
                        MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);

                Map<Integer, Integer> outputTracks = new HashMap<>();
                boolean hasVideo = false;
                for (int sourceTrack = 0; sourceTrack < extractor.getTrackCount(); sourceTrack++) {
                    android.media.MediaFormat format = extractor.getTrackFormat(sourceTrack);
                    String trackMime = format.getString(android.media.MediaFormat.KEY_MIME);
                    if (trackMime != null && (trackMime.startsWith("video/")
                            || trackMime.startsWith("audio/"))) {
                        extractor.selectTrack(sourceTrack);
                        outputTracks.put(sourceTrack, muxer.addTrack(format));
                        hasVideo |= trackMime.startsWith("video/");
                    }
                }
                if (outputTracks.isEmpty()) {
                    throw new IllegalArgumentException("No audio or video tracks can be exported");
                }

                muxer.start();
                muxerStarted = true;
                long startUs = (long) (startSeconds * 1_000_000L);
                long endUs = (long) (endSeconds * 1_000_000L);
                ByteBuffer buffer = ByteBuffer.allocate(4 * 1024 * 1024);
                MediaCodec.BufferInfo bufferInfo = new MediaCodec.BufferInfo();
                int writtenSamples = 0;
                while (true) {
                    int sourceTrack = extractor.getSampleTrackIndex();
                    if (sourceTrack < 0) break;
                    long sampleTimeUs = extractor.getSampleTime();
                    if (sampleTimeUs > endUs) break;
                    if (sampleTimeUs < startUs) {
                        extractor.advance();
                        continue;
                    }

                    buffer.clear();
                    int sampleSize = extractor.readSampleData(buffer, 0);
                    if (sampleSize < 0) break;
                    if (sampleSize > buffer.capacity()) {
                        throw new IllegalArgumentException("A sample exceeds the local trim buffer");
                    }
                    bufferInfo.set(0, sampleSize, sampleTimeUs - startUs,
                            extractor.getSampleFlags());
                    Integer outputTrack = outputTracks.get(sourceTrack);
                    if (outputTrack != null) {
                        muxer.writeSampleData(outputTrack, buffer, bufferInfo);
                        writtenSamples++;
                    }
                    extractor.advance();
                }
                if (writtenSamples == 0) {
                    throw new IllegalArgumentException("No media samples found in that time range");
                }
                muxer.stop();
                muxerStarted = false;
                libraryStore.addFile(output.getName(), Uri.fromFile(output).toString(),
                        hasVideo ? "video/mp4" : "audio/mp4");
                result = "Trimmed export saved as " + output.getName();
            } catch (Exception exception) {
                if (output != null) output.delete();
                result = "Trim failed: " + exception.getMessage();
            } finally {
                if (muxer != null) {
                    try {
                        if (muxerStarted) muxer.stop();
                    } catch (RuntimeException ignored) {
                        // The output may be incomplete after a codec or container error.
                    }
                    muxer.release();
                }
                extractor.release();
                if (descriptor != null) {
                    try {
                        descriptor.close();
                    } catch (Exception ignored) {
                        // no-op
                    }
                }
            }
            String finalResult = result;
            runOnUiThread(() -> {
                trimButton.setEnabled(true);
                status.setText(finalResult);
            });
        }, "destiny-media-trim").start();
    }

    private void renameCurrentFile() {
        final EditText input = new EditText(this);
        input.setText(displayName == null ? "renamed_media" : displayName);
        input.setHint("New name");

        new AlertDialog.Builder(this)
                .setTitle("Rename export")
                .setView(input)
                .setPositiveButton("Save", (dialog, which) -> {
                    String newName = input.getText().toString().trim();
                    if (newName.isEmpty()) {
                        Toast.makeText(this, "Name cannot be empty", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    duplicateCurrentFileAs(newName);
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void duplicateCurrentFileAs(String newName) {
        try {
            File exportDir = new File(getFilesDir(), "editor_exports");
            if (!exportDir.exists()) {
                exportDir.mkdirs();
            }

            File target = new File(exportDir, sanitizeName(newName));
            try (InputStream in = getContentResolver().openInputStream(mediaUri);
                 OutputStream out = new FileOutputStream(target)) {
                if (in == null) {
                    throw new IllegalStateException("Unable to read source file");
                }
                byte[] buffer = new byte[8192];
                int count;
                while ((count = in.read(buffer)) != -1) {
                    out.write(buffer, 0, count);
                }
                out.flush();
            }

            libraryStore.addFile(target.getName(), Uri.fromFile(target).toString(), mimeType == null ? "application/octet-stream" : mimeType);
            Toast.makeText(this, "Saved renamed export as " + target.getName(), Toast.LENGTH_SHORT).show();
        } catch (Exception exception) {
            Toast.makeText(this, "Rename export failed: " + exception.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    private String sanitizeName(String name) {
        String safe = name == null ? "media_export" : name.trim();
        safe = safe.replace("/", "_").replace("\\", "_");
        if (safe.isEmpty()) {
            safe = "media_export";
        }
        return safe;
    }

    private String removeExtension(String value) {
        String name = sanitizeName(value);
        int index = name.lastIndexOf('.');
        if (index > 0 && index < name.length() - 1) {
            return name.substring(0, index);
        }
        return name;
    }

    private String extensionOf(String value) {
        String name = sanitizeName(value);
        int index = name.lastIndexOf('.');
        if (index > 0 && index < name.length() - 1) {
            return name.substring(index + 1);
        }
        return "";
    }

    private LinearLayout.LayoutParams matchWrap() {
        return new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        );
    }
}
