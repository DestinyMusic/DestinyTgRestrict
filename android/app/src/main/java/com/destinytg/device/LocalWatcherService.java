package com.destinytg.device;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.os.Build;
import android.os.IBinder;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import android.database.Cursor;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public final class LocalWatcherService extends Service {
    private static final String CHANNEL_ID = "destiny-watchers";
    private static final int NOTIFICATION_ID = 7314;
    private ScheduledExecutorService statusExecutor;

    @Override
    public void onCreate() {
        super.onCreate();
        createNotificationChannel();
        startForeground(NOTIFICATION_ID, buildNotification());
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent != null && "STOP".equals(intent.getAction())) {
            stopSelf();
            return START_NOT_STICKY;
        }
        new Thread(this::restoreWatchers, "destiny-restore-watchers").start();
        return START_STICKY;
    }

    private void restoreWatchers() {
        LocalSecretsStore secrets = new LocalSecretsStore(this);
        String apiId = secrets.get("telegram_api_id");
        String apiHash = secrets.get("telegram_api_hash");
        String session = secrets.get("telegram_session");
        if (apiId == null || apiHash == null || session == null) {
            stopSelf();
            return;
        }

        try {
            if (!Python.isStarted()) Python.start(new AndroidPlatform(this));
            Python runtime = Python.getInstance();
            runtime.getModule("destiny_runtime").callAttr("set_storage_directory",
                    getFilesDir().getAbsolutePath());
            LocalLibraryStore store = new LocalLibraryStore(this);
            Cursor watchers = store.getWatchers();
            int restored = 0;
            while (watchers.moveToNext()) {
                try {
                    String result = runtime.getModule("destiny_runtime").callAttr("start_watcher", apiId, apiHash,
                            session, watchers.getString(1), watchers.getString(2), watchers.getString(3),
                            watchers.getString(4), watchers.getString(5),
                            String.valueOf(watchers.getInt(6)), String.valueOf(watchers.getLong(8)),
                            String.valueOf(watchers.getLong(9)), watchers.getString(7),
                            String.valueOf(watchers.getLong(10))).toString();
                    if (result.startsWith("WATCHING|")) {
                        long checkpoint = Long.parseLong(result.substring("WATCHING|".length()));
                        store.updateWatcherCheckpoint(watchers.getLong(0), checkpoint);
                        restored++;
                    }
                } catch (Exception watcherError) {
                    NotificationManager manager = getSystemService(NotificationManager.class);
                    if (manager != null) {
                        notifyIfAllowed(manager, buildNotification("Watch restore failed: "
                            + watcherError.getMessage()));
                    }
                }
            }
            watchers.close();
            store.close();
            if (restored == 0) stopSelf();
            else startStatusSync();
        } catch (Exception exception) {
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) {
                notifyIfAllowed(manager, buildNotification("Watcher error: "
                    + exception.getMessage()));
            }
            stopSelf();
        }
    }

    private void startStatusSync() {
        statusExecutor = Executors.newSingleThreadScheduledExecutor();
        statusExecutor.scheduleWithFixedDelay(this::syncWatcherStatus, 2, 3, TimeUnit.SECONDS);
    }

    private void syncWatcherStatus() {
        if (!Python.isStarted()) return;
        try (LocalLibraryStore store = new LocalLibraryStore(this)) {
            String response = Python.getInstance().getModule("destiny_runtime")
                    .callAttr("get_watcher_status").toString();
            JSONArray active = new JSONArray(response);
            long forwarded = 0;
            long skipped = 0;
            long failed = 0;
            for (int i = 0; i < active.length(); i++) {
                JSONObject watcher = active.getJSONObject(i);
                String source = watcher.getString("source");
                String destination = watcher.getString("destination");
                long sourceThread = watcher.getLong("source_thread_id");
                long destinationThread = watcher.getLong("destination_thread_id");
                long checkpoint = watcher.getLong("last_message_id");
                JSONObject stats = watcher.getJSONObject("stats");
                forwarded += stats.optLong("success", 0);
                skipped += stats.optLong("skipped", 0);
                failed += stats.optLong("failed", 0);

                Cursor rows = store.getWatchers();
                long localId = -1;
                while (rows.moveToNext()) {
                    if (source.equals(rows.getString(1)) && destination.equals(rows.getString(2))
                            && sourceThread == rows.getLong(8)
                            && destinationThread == rows.getLong(9)) {
                        localId = rows.getLong(0);
                        break;
                    }
                }
                rows.close();
                if (localId > 0) store.updateWatcherStatus(localId, checkpoint, stats.toString());
            }
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null && active.length() > 0) {
                notifyIfAllowed(manager, buildNotification(active.length() + " active · "
                    + forwarded + " forwarded · " + skipped + " filtered · " + failed + " failed"));
            }
        } catch (Exception ignored) {
            // A status refresh should not stop active Watch tasks.
        }
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return;
        NotificationChannel channel = new NotificationChannel(CHANNEL_ID,
                "Telegram watchers", NotificationManager.IMPORTANCE_LOW);
        NotificationManager manager = getSystemService(NotificationManager.class);
        if (manager != null) manager.createNotificationChannel(channel);
    }

    private void notifyIfAllowed(NotificationManager manager, Notification notification) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU
                && checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS)
                != android.content.pm.PackageManager.PERMISSION_GRANTED) {
            return;
        }
        manager.notify(NOTIFICATION_ID, notification);
    }

    private Notification buildNotification() {
        return buildNotification("Watching Telegram sources on this device");
    }

    private Notification buildNotification(String text) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            return new Notification.Builder(this, CHANNEL_ID)
                    .setSmallIcon(android.R.drawable.stat_notify_sync)
                    .setContentTitle("Destiny TG watchers")
                    .setContentText(text)
                    .setOngoing(true)
                    .build();
        }
        return new Notification.Builder(this)
                .setSmallIcon(android.R.drawable.stat_notify_sync)
                .setContentTitle("Destiny TG watchers")
                .setContentText(text)
                .setOngoing(true)
                .build();
    }

    @Override
    public void onDestroy() {
        if (statusExecutor != null) statusExecutor.shutdownNow();
        if (Python.isStarted()) {
            new Thread(() -> {
                try {
                    Python.getInstance().getModule("destiny_runtime").callAttr("stop_watchers");
                } catch (Exception ignored) {
                    // The runtime may not have started if there were no valid watchers.
                }
            }, "destiny-stop-watchers").start();
        }
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}