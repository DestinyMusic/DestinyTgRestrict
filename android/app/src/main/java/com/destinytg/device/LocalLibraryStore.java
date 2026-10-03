package com.destinytg.device;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

final class LocalLibraryStore extends SQLiteOpenHelper {
    private static final String DATABASE_NAME = "destiny-local.db";
    private static final int DATABASE_VERSION = 8;
    private static final String TABLE_FILES = "local_files";
    private static final String TABLE_WATCHERS = "local_watchers";
    private static final String TABLE_TASKS = "local_tasks";

    LocalLibraryStore(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase database) {
        createFilesTable(database);
        createWatchersTable(database);
        createTasksTable(database);
    }

    private void createFilesTable(SQLiteDatabase database) {
        database.execSQL("CREATE TABLE " + TABLE_FILES + " ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                + "name TEXT NOT NULL, "
                + "uri TEXT NOT NULL UNIQUE, "
                + "mime_type TEXT NOT NULL)");
    }

    private void createWatchersTable(SQLiteDatabase database) {
        database.execSQL("CREATE TABLE " + TABLE_WATCHERS + " ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                + "source TEXT NOT NULL, "
                + "destination TEXT NOT NULL, "
                + "media_types TEXT NOT NULL DEFAULT 'video,audio,photo,document,animation', "
                + "include_keywords TEXT NOT NULL DEFAULT '', "
                + "exclude_keywords TEXT NOT NULL DEFAULT '', "
                + "cleanup_keywords TEXT NOT NULL DEFAULT '', "
                + "delay_seconds INTEGER NOT NULL DEFAULT 0, "
                + "source_thread_id INTEGER NOT NULL DEFAULT 0, "
                + "destination_thread_id INTEGER NOT NULL DEFAULT 0, "
                + "last_message_id INTEGER NOT NULL DEFAULT 0, "
                + "stats_json TEXT NOT NULL DEFAULT '{}', "
                + "transfer_mode TEXT NOT NULL DEFAULT 'AUTO', "
                + "UNIQUE(source, destination, source_thread_id, destination_thread_id))");
    }

    private void createTasksTable(SQLiteDatabase database) {
        database.execSQL("CREATE TABLE " + TABLE_TASKS + " ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                + "kind TEXT NOT NULL, "
                + "label TEXT NOT NULL, "
                + "state TEXT NOT NULL, "
                + "detail TEXT NOT NULL, "
                + "request_json TEXT NOT NULL DEFAULT '', "
                + "last_message_id INTEGER NOT NULL DEFAULT 0, "
                + "created_at INTEGER NOT NULL)");
    }

    @Override
    public void onUpgrade(SQLiteDatabase database, int oldVersion, int newVersion) {
        if (oldVersion < 1) createFilesTable(database);
        if (oldVersion < 2) {
            createWatchersTable(database);
        } else if (oldVersion == 2) {
            database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                + " ADD COLUMN media_types TEXT NOT NULL DEFAULT 'video,audio,photo,document,animation'");
            database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                + " ADD COLUMN include_keywords TEXT NOT NULL DEFAULT ''");
            database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                + " ADD COLUMN exclude_keywords TEXT NOT NULL DEFAULT ''");
            database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                + " ADD COLUMN delay_seconds INTEGER NOT NULL DEFAULT 0");
        }
            if (oldVersion >= 2 && oldVersion < 4) {
                database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                    + " ADD COLUMN cleanup_keywords TEXT NOT NULL DEFAULT ''");
                database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                    + " ADD COLUMN source_thread_id INTEGER NOT NULL DEFAULT 0");
                database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                    + " ADD COLUMN destination_thread_id INTEGER NOT NULL DEFAULT 0");
                database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                    + " ADD COLUMN last_message_id INTEGER NOT NULL DEFAULT 0");
            }
        if (oldVersion < 3) createTasksTable(database);
        if (oldVersion >= 2 && oldVersion < 5) rebuildWatchersTable(database);
        if (oldVersion == 5) {
            database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                + " ADD COLUMN stats_json TEXT NOT NULL DEFAULT '{}'");
        }
        if (oldVersion >= 3 && oldVersion < 7) {
            database.execSQL("ALTER TABLE " + TABLE_TASKS
                + " ADD COLUMN request_json TEXT NOT NULL DEFAULT ''");
            database.execSQL("ALTER TABLE " + TABLE_TASKS
                + " ADD COLUMN last_message_id INTEGER NOT NULL DEFAULT 0");
        }
            if (oldVersion >= 2 && oldVersion < 8) {
                database.execSQL("ALTER TABLE " + TABLE_WATCHERS
                + " ADD COLUMN transfer_mode TEXT NOT NULL DEFAULT 'AUTO'");
            }
    }

                private void rebuildWatchersTable(SQLiteDatabase database) {
                String temporaryTable = TABLE_WATCHERS + "_new";
                database.execSQL("CREATE TABLE " + temporaryTable + " ("
                    + "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    + "source TEXT NOT NULL, "
                    + "destination TEXT NOT NULL, "
                    + "media_types TEXT NOT NULL DEFAULT 'video,audio,photo,document,animation', "
                    + "include_keywords TEXT NOT NULL DEFAULT '', "
                    + "exclude_keywords TEXT NOT NULL DEFAULT '', "
                    + "cleanup_keywords TEXT NOT NULL DEFAULT '', "
                    + "delay_seconds INTEGER NOT NULL DEFAULT 0, "
                    + "source_thread_id INTEGER NOT NULL DEFAULT 0, "
                    + "destination_thread_id INTEGER NOT NULL DEFAULT 0, "
                    + "last_message_id INTEGER NOT NULL DEFAULT 0, "
                    + "stats_json TEXT NOT NULL DEFAULT '{}', "
                    + "UNIQUE(source, destination, source_thread_id, destination_thread_id))");
                database.execSQL("INSERT INTO " + temporaryTable + " (id, source, destination, media_types, "
                    + "include_keywords, exclude_keywords, cleanup_keywords, delay_seconds, "
                    + "source_thread_id, destination_thread_id, last_message_id) SELECT id, source, "
                    + "destination, media_types, include_keywords, exclude_keywords, cleanup_keywords, "
                    + "delay_seconds, source_thread_id, destination_thread_id, last_message_id FROM "
                    + TABLE_WATCHERS);
                database.execSQL("DROP TABLE " + TABLE_WATCHERS);
                database.execSQL("ALTER TABLE " + temporaryTable + " RENAME TO " + TABLE_WATCHERS);
                }

    void addFile(String name, String uri, String mimeType) {
        ContentValues values = new ContentValues();
        values.put("name", name);
        values.put("uri", uri);
        values.put("mime_type", mimeType);
        getWritableDatabase().insertWithOnConflict(TABLE_FILES, null, values,
                SQLiteDatabase.CONFLICT_REPLACE);
    }

    Cursor getFiles() {
        return getReadableDatabase().query(TABLE_FILES,
                new String[]{"id", "name", "uri", "mime_type"},
                null, null, null, null, "name COLLATE NOCASE ASC");
    }

    void removeFile(long id) {
        getWritableDatabase().delete(TABLE_FILES, "id = ?", new String[]{String.valueOf(id)});
    }

        void addWatcher(String source, String destination, String mediaTypes,
                        String includeKeywords, String excludeKeywords, String cleanupKeywords,
                        int delaySeconds, long sourceThreadId, long destinationThreadId,
                        String transferMode) {
        ContentValues values = new ContentValues();
        values.put("source", source);
        values.put("destination", destination);
        values.put("media_types", mediaTypes);
        values.put("include_keywords", includeKeywords);
        values.put("exclude_keywords", excludeKeywords);
        values.put("cleanup_keywords", cleanupKeywords);
        values.put("delay_seconds", delaySeconds);
        values.put("source_thread_id", sourceThreadId);
        values.put("destination_thread_id", destinationThreadId);
        values.put("transfer_mode", transferMode);
        getWritableDatabase().insertWithOnConflict(TABLE_WATCHERS, null, values,
                SQLiteDatabase.CONFLICT_REPLACE);
    }

    Cursor getWatchers() {
        return getReadableDatabase().query(TABLE_WATCHERS,
            new String[]{"id", "source", "destination", "media_types", "include_keywords",
                "exclude_keywords", "delay_seconds", "cleanup_keywords", "source_thread_id",
                    "destination_thread_id", "last_message_id", "stats_json", "transfer_mode"},
            null, null, null, null, "id ASC");
    }

    void removeWatcher(long id) {
        getWritableDatabase().delete(TABLE_WATCHERS, "id = ?", new String[]{String.valueOf(id)});
    }

    void updateWatcherCheckpoint(long id, long messageId) {
        ContentValues values = new ContentValues();
        values.put("last_message_id", messageId);
        getWritableDatabase().update(TABLE_WATCHERS, values, "id = ?",
                new String[]{String.valueOf(id)});
    }

    void updateWatcherStatus(long id, long messageId, String statsJson) {
        ContentValues values = new ContentValues();
        values.put("last_message_id", messageId);
        values.put("stats_json", statsJson);
        getWritableDatabase().update(TABLE_WATCHERS, values, "id = ?",
                new String[]{String.valueOf(id)});
    }

    void removeAllWatchers() {
        getWritableDatabase().delete(TABLE_WATCHERS, null, null);
    }

    long addTask(String kind, String label) {
        return addTask(kind, label, "");
    }

    long addTask(String kind, String label, String requestJson) {
        ContentValues values = new ContentValues();
        values.put("kind", kind);
        values.put("label", label);
        values.put("state", "RUNNING");
        values.put("detail", "Task started on this device");
        values.put("request_json", requestJson);
        values.put("created_at", System.currentTimeMillis());
        return getWritableDatabase().insert(TABLE_TASKS, null, values);
    }

    void updateTask(long id, String state, String detail) {
        ContentValues values = new ContentValues();
        values.put("state", state);
        values.put("detail", detail);
        getWritableDatabase().update(TABLE_TASKS, values, "id = ?",
                new String[]{String.valueOf(id)});
    }

    void updateTaskCheckpoint(long id, long messageId) {
        ContentValues values = new ContentValues();
        values.put("last_message_id", messageId);
        getWritableDatabase().update(TABLE_TASKS, values, "id = ?",
                new String[]{String.valueOf(id)});
    }

    void markInterruptedTasks() {
        ContentValues values = new ContentValues();
        values.put("state", "INTERRUPTED");
        values.put("detail", "App stopped before this task completed");
        getWritableDatabase().update(TABLE_TASKS, values, "state IN (?, ?)",
            new String[]{"RUNNING", "INTERRUPTED"});
        values.put("state", "CANCELLED");
        values.put("detail", "Task was cancelled before the app stopped");
        getWritableDatabase().update(TABLE_TASKS, values, "state = ?",
            new String[]{"CANCEL_REQUESTED"});
    }

    Cursor getTasks() {
        return getReadableDatabase().query(TABLE_TASKS,
                new String[]{"id", "kind", "label", "state", "detail", "created_at"},
                null, null, null, null, "created_at DESC", "20");
    }

    Cursor getInterruptedDownloads() {
        return getReadableDatabase().query(TABLE_TASKS,
                new String[]{"id", "request_json", "last_message_id"},
                "kind IN (?, ?) AND state = ? AND request_json != ''",
                new String[]{"DOWNLOAD", "FORWARD", "INTERRUPTED"},
                null, null, "created_at ASC");
    }
}