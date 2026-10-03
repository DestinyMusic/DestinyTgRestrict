package com.destinytg.device

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Download
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Movie
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONArray
import org.json.JSONObject
import java.io.BufferedReader
import java.io.File
import java.io.FileOutputStream
import java.io.FileReader
import java.net.HttpURLConnection
import java.net.URI
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicBoolean
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext

private data class BatchTaskRequest(
    val sourceType: String,
    val link: String,
    val firstId: String,
    val lastId: String,
    val destination: String,
    val mediaTypes: String,
    val includeKeywords: String,
    val excludeKeywords: String,
    val delaySeconds: String,
    val sourceTopicId: String,
    val destinationTopicId: String,
    val cleanupKeywords: String,
    val transferMode: String
)

private data class WatcherRequest(
    val source: String,
    val destination: String,
    val mediaTypes: String,
    val includeKeywords: String,
    val excludeKeywords: String,
    val cleanupKeywords: String,
    val delaySeconds: String,
    val sourceTopicId: String,
    val destinationTopicId: String,
    val transferMode: String
)

private data class LocalTaskRow(
    val id: Long,
    val kind: String,
    val label: String,
    val state: String,
    val detail: String
)

private data class LocalWatcherRow(
    val id: Long,
    val source: String,
    val destination: String,
    val transferMode: String,
    val sourceTopicId: Long,
    val destinationTopicId: Long
)

private data class WorkspaceSnapshot(
    val tasks: List<LocalTaskRow>,
    val watchers: List<LocalWatcherRow>
)

private const val PREFS_NAME = "destiny-device"
private const val PREF_SERVER_ADDRESS = "serverAddress"
private const val PREF_APP_MODE = "appMode"

private val ink = Color(0xFF0A1114)
private val glass = Color(0xC51C292D)
private val glassLine = Color(0x665A777A)
private val textMain = Color(0xFFF1F6F4)
private val textMuted = Color(0xFF9DAEAB)
private val sea = Color(0xFF6BE0CC)
private val coral = Color(0xFFFF987F)
private val citron = Color(0xFFD6E98A)

private enum class WorkspaceTab(val title: String, val icon: ImageVector) {
    HOME("Home", Icons.Outlined.Home),
    TASKS("Tasks", Icons.Outlined.Download),
    THEATER("Theater", Icons.Outlined.Movie),
    EDITOR("Editor", Icons.Outlined.Edit),
    SETTINGS("Settings", Icons.Outlined.Settings)
}

class ModernHomeActivity : ComponentActivity() {
    private var refreshConnectionStatus: (() -> Unit)? = null
    private val directDownloadCancellations = ConcurrentHashMap<Long, AtomicBoolean>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = android.graphics.Color.TRANSPARENT
        window.navigationBarColor = android.graphics.Color.TRANSPARENT
        val preferences = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val savedAddress = preferences.getString(PREF_SERVER_ADDRESS, "") ?: ""
        initializeRuntime()
        setContent {
            var connected by remember { mutableStateOf(hasTelegramSession()) }
            DisposableEffect(Unit) {
                refreshConnectionStatus = { connected = hasTelegramSession() }
                onDispose { refreshConnectionStatus = null }
            }
            DestinyGlassTheme {
                DestinyWorkspace(
                    telegramConnected = connected,
                    savedAddress = savedAddress,
                    onOpenLocal = ::openLocal,
                    onPlayLink = ::openMediaLink,
                    onEditLink = ::editMediaLink,
                    onOpenDashboard = ::openDashboard,
                    onRunBatchTask = ::runBatchTask,
                    onCancelBatchTask = ::cancelBatchTask,
                    onStartWatcher = ::startWatcher,
                    onLoadWorkspaceSnapshot = ::loadWorkspaceSnapshot,
                    onStopWatcher = ::stopWatcher,
                    onSaveAddress = { address ->
                        preferences.edit().putString(PREF_SERVER_ADDRESS, address).apply()
                    }
                )
            }
        }
    }

    override fun onResume() {
        super.onResume()
        refreshConnectionStatus?.invoke()
    }

    private fun hasTelegramSession(): Boolean =
        runCatching { LocalSecretsStore(this).get("telegram_session") != null }
            .getOrDefault(false)

    private fun loadWorkspaceSnapshot(): WorkspaceSnapshot {
        val tasks = mutableListOf<LocalTaskRow>()
        val watchers = mutableListOf<LocalWatcherRow>()
        LocalLibraryStore(this).use { library ->
            library.getTasks().use { cursor ->
                while (cursor.moveToNext()) {
                    tasks += LocalTaskRow(cursor.getLong(0), cursor.getString(1),
                        cursor.getString(2), cursor.getString(3), cursor.getString(4))
                }
            }
            library.getWatchers().use { cursor ->
                while (cursor.moveToNext()) {
                    watchers += LocalWatcherRow(cursor.getLong(0), cursor.getString(1),
                        cursor.getString(2), cursor.getString(12), cursor.getLong(8),
                        cursor.getLong(9))
                }
            }
        }
        return WorkspaceSnapshot(tasks, watchers)
    }

    private fun initializeRuntime() {
        try {
            if (!Python.isStarted()) Python.start(AndroidPlatform(this))
            val runtime = Python.getInstance().getModule("destiny_runtime")
            runtime.callAttr("set_storage_directory", filesDir.absolutePath)
            runtime.callAttr("runtime_status")
            val secrets = LocalSecretsStore(this)
            val apiId = secrets.get("telegram_api_id")
            val apiHash = secrets.get("telegram_api_hash")
            val streamTokens = secrets.get("stream_worker_tokens") ?: ""
            val taskTokens = secrets.get("task_worker_tokens") ?: ""
            if (apiId != null && apiHash != null
                && (streamTokens.isNotBlank() || taskTokens.isNotBlank())) {
                Thread({
                    runCatching {
                        runtime.callAttr("configure_worker_pools", apiId, apiHash,
                            streamTokens, taskTokens)
                    }
                }, "destiny-compose-worker-pools").start()
            }
        } catch (_: Exception) {
            Toast.makeText(this, "Local runtime could not start", Toast.LENGTH_LONG).show()
        }
    }

    private fun runBatchTask(request: BatchTaskRequest, report: (String) -> Unit) {
        Thread({
            var taskId = -1L
            try {
                if (request.sourceType == "DIRECT") {
                    runDirectDownload(request.link, report)
                    return@Thread
                }
                val secrets = LocalSecretsStore(this)
                val apiId = secrets.get("telegram_api_id")
                    ?: throw IllegalStateException("Connect Telegram in Settings first")
                val apiHash = secrets.get("telegram_api_hash")
                    ?: throw IllegalStateException("Connect Telegram in Settings first")
                val session = secrets.get("telegram_session")
                    ?: throw IllegalStateException("Connect Telegram in Settings first")
                val savedRequest = JSONArray()
                    .put(request.link).put(request.firstId).put(request.lastId)
                    .put(request.destination).put(request.mediaTypes)
                    .put(request.includeKeywords).put(request.excludeKeywords)
                    .put(request.delaySeconds).put(request.sourceTopicId)
                    .put(request.destinationTopicId).put(request.cleanupKeywords)
                    .put(request.transferMode)
                val library = LocalLibraryStore(this)
                val label = request.link + if (request.firstId.isBlank()) ""
                    else "  IDs ${request.firstId}-${request.lastId.ifBlank { request.firstId }}"
                taskId = library.addTask(request.transferMode, label, savedRequest.toString())
                library.close()
                postStatus(report, "TASK_STARTED:$taskId")
                val args = arrayOf(
                    apiId, apiHash, session, request.link, request.firstId, request.lastId,
                    request.destination.ifBlank { "me" }, request.mediaTypes,
                    request.includeKeywords, request.excludeKeywords, request.delaySeconds,
                    request.sourceTopicId, request.destinationTopicId,
                    request.cleanupKeywords, taskId.toString(), "", request.transferMode
                )
                val response = Python.getInstance().getModule("destiny_runtime")
                    .callAttr("download_messages", *args).toString()
                val summary = response.substringAfter("TASK_SUMMARY|", response)
                val state = when {
                    summary.contains("cancelled=1") -> "CANCELLED"
                    summary.contains("failed=0") -> "COMPLETE"
                    summary.contains("downloaded=0") -> "FAILED"
                    else -> "PARTIAL"
                }
                consumeTaskEvents(taskId)
                LocalLibraryStore(this).use { it.updateTask(taskId, state, summary) }
                deleteTaskProgress(taskId)
                postStatus(report, summary)
            } catch (error: Exception) {
                if (taskId > 0) {
                    LocalLibraryStore(this).use {
                        it.updateTask(taskId, "FAILED", error.message ?: "Task failed")
                    }
                }
                postStatus(report, error.message ?: "Unable to start task")
            }
        }, "destiny-compose-batch-task").start()
    }

    private fun runDirectDownload(link: String, report: (String) -> Unit) {
        val address = URI(link)
        if (address.host.isNullOrBlank()
            || !(address.scheme.equals("http", true) || address.scheme.equals("https", true))) {
            throw IllegalArgumentException("Enter a valid direct HTTP(S) URL")
        }
        val task = LocalLibraryStore(this)
        val taskId = task.addTask("DIRECT_DOWNLOAD", link,
            JSONArray().put(link).put("DOWNLOAD").toString())
        task.close()
        val cancellation = AtomicBoolean(false)
        directDownloadCancellations[taskId] = cancellation
        postStatus(report, "TASK_STARTED:$taskId")

        var connection: HttpURLConnection? = null
        var outputFile: File? = null
        try {
            connection = address.toURL().openConnection() as HttpURLConnection
            connection.connectTimeout = 15000
            connection.readTimeout = 30000
            connection.instanceFollowRedirects = true
            val responseCode = connection.responseCode
            if (responseCode !in 200..299) {
                throw IllegalStateException("Server returned HTTP $responseCode")
            }
            val directory = File(filesDir, "downloads")
            if (!directory.exists() && !directory.mkdirs()) {
                throw IllegalStateException("Cannot create the local download folder")
            }
            val pathName = address.path.substringAfterLast('/').ifBlank { "download.bin" }
            val safeName = pathName.replace(Regex("[^A-Za-z0-9._-]"), "_")
            val downloadedFile = File(directory, "${System.currentTimeMillis()}-$safeName")
            outputFile = downloadedFile
            val expectedBytes = connection.contentLengthLong
            var copiedBytes = 0L
            connection.inputStream.use { input ->
                FileOutputStream(downloadedFile).use { output ->
                    val buffer = ByteArray(65536)
                    var lastProgressBytes = 0L
                    while (true) {
                        if (cancellation.get()) throw InterruptedException("Download cancelled")
                        val count = input.read(buffer)
                        if (count < 0) break
                        output.write(buffer, 0, count)
                        copiedBytes += count
                        if (copiedBytes - lastProgressBytes >= 262144L) {
                            writeDirectProgress(taskId, "RUNNING", copiedBytes,
                                expectedBytes, copiedBytes)
                            lastProgressBytes = copiedBytes
                        }
                    }
                }
            }
            if (cancellation.get()) throw InterruptedException("Download cancelled")
            val mimeType = connection.contentType?.substringBefore(';')
                ?.trim()?.takeIf { it.isNotEmpty() } ?: "application/octet-stream"
            LocalLibraryStore(this).use {
                it.addFile(safeName, Uri.fromFile(downloadedFile).toString(), mimeType)
            }
            LocalLibraryStore(this).use {
                it.updateTask(taskId, "COMPLETE", "Saved $safeName to this device")
            }
            writeDirectProgress(taskId, "COMPLETE", copiedBytes, expectedBytes, copiedBytes)
            postStatus(report, "Saved $safeName to this device")
        } catch (error: Exception) {
            outputFile?.delete()
            val state = if (error is InterruptedException) "CANCELLED" else "FAILED"
            LocalLibraryStore(this).use {
                it.updateTask(taskId, state, error.message ?: "Direct download failed")
            }
            writeDirectProgress(taskId, state, 0L, 0L, 0L)
            postStatus(report, error.message ?: "Direct download failed")
        } finally {
            connection?.disconnect()
            directDownloadCancellations.remove(taskId)
            File(File(filesDir, "tasks"), "$taskId.txt").delete()
        }
    }

    private fun writeDirectProgress(taskId: Long, state: String, current: Long,
                                    total: Long, downloaded: Long) {
        val directory = File(filesDir, "tasks")
        if (!directory.exists()) directory.mkdirs()
        val progressFile = File(directory, "$taskId.txt")
        val temporaryFile = File(directory, "$taskId.txt.tmp")
        temporaryFile.writeText("$state|$current|$total|$downloaded|0|0")
        if (!temporaryFile.renameTo(progressFile)) {
            progressFile.writeText(temporaryFile.readText())
            temporaryFile.delete()
        }
    }

    private fun startWatcher(request: WatcherRequest, report: (String) -> Unit) {
        Thread({
            try {
                val secrets = LocalSecretsStore(this)
                if (secrets.get("telegram_api_id") == null
                    || secrets.get("telegram_api_hash") == null
                    || secrets.get("telegram_session") == null) {
                    throw IllegalStateException("Connect Telegram in Settings first")
                }
                LocalLibraryStore(this).use { library ->
                    library.addWatcher(
                        request.source, request.destination.ifBlank { "me" },
                        request.mediaTypes, request.includeKeywords, request.excludeKeywords,
                        request.cleanupKeywords, request.delaySeconds.toIntOrNull() ?: 3,
                        request.sourceTopicId.toLongOrNull() ?: 0L,
                        request.destinationTopicId.toLongOrNull() ?: 0L,
                        request.transferMode
                    )
                }
                val service = Intent(this, LocalWatcherService::class.java)
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) startForegroundService(service)
                else startService(service)
                postStatus(report, "Watcher started in ${request.transferMode.lowercase()} mode")
            } catch (error: Exception) {
                postStatus(report, error.message ?: "Unable to start watcher")
            }
        }, "destiny-compose-watcher").start()
    }

    private fun cancelBatchTask(taskId: String, report: (String) -> Unit) {
        Thread({
            val directId = taskId.toLongOrNull()
            val directCancellation = directId?.let { directDownloadCancellations[it] }
            val result = if (directCancellation != null) {
                directCancellation.set(true)
                "CANCEL_REQUESTED"
            } else runCatching {
                Python.getInstance().getModule("destiny_runtime")
                    .callAttr("cancel_download_task", taskId).toString()
            }.getOrElse { "Unable to request cancellation" }
            postStatus(report, if (result == "CANCEL_REQUESTED")
                "Cancellation requested" else result)
        }, "destiny-compose-cancel-task").start()
    }

    private fun stopWatcher(watcher: LocalWatcherRow, report: (String) -> Unit) {
        Thread({
            try {
                LocalLibraryStore(this).use { library -> library.removeWatcher(watcher.id) }
                if (Python.isStarted()) {
                    runCatching {
                        Python.getInstance().getModule("destiny_runtime").callAttr(
                            "remove_watcher", watcher.source, watcher.destination,
                            watcher.sourceTopicId.toString(), watcher.destinationTopicId.toString())
                    }
                }
                val hasWatchers = LocalLibraryStore(this).use { library ->
                    library.getWatchers().use { it.count > 0 }
                }
                if (!hasWatchers) stopService(Intent(this, LocalWatcherService::class.java))
                postStatus(report, "Watcher stopped")
            } catch (error: Exception) {
                postStatus(report, error.message ?: "Unable to stop watcher")
            }
        }, "destiny-compose-stop-watcher").start()
    }

    private fun consumeTaskEvents(taskId: Long) {
        val events = File(File(filesDir, "tasks"), "$taskId.jsonl")
        if (!events.isFile) return
        try {
            LocalLibraryStore(this).use { library ->
                BufferedReader(FileReader(events)).useLines { lines ->
                    lines.forEach { line ->
                        runCatching {
                            val event = JSONObject(line)
                            if (event.optString("type") == "file") {
                                library.addFile(
                                    event.getString("name"),
                                    Uri.fromFile(File(event.getString("path"))).toString(),
                                    event.optString("mime_type", "application/octet-stream")
                                )
                            }
                        }
                    }
                }
            }
        } catch (_: Exception) {
            // Progress events can be replaced while the runtime is writing them.
        }
    }

    private fun deleteTaskProgress(taskId: Long) {
        val directory = File(filesDir, "tasks")
        listOf(".txt", ".checkpoint", ".jsonl").forEach { suffix ->
            File(directory, "$taskId$suffix").delete()
        }
    }

    private fun postStatus(report: (String) -> Unit, message: String) {
        Handler(Looper.getMainLooper()).post { report(message) }
    }

    private fun openLocal(destination: String, transferMode: String? = null) {
        startActivity(Intent(this, MainActivity::class.java).apply {
            putExtra("destiny_local_destination", destination)
            transferMode?.let { putExtra("destiny_transfer_mode", it) }
        })
    }

    private fun openMediaLink(link: String) {
        startActivity(Intent(this, MainActivity::class.java).putExtra(
            "destiny_play_media_link", link.trim()))
    }

    private fun editMediaLink(link: String) {
        startActivity(Intent(this, MainActivity::class.java).putExtra(
            "destiny_edit_media_link", link.trim()))
    }

    private fun openDashboard(address: String) {
        val uri = Uri.parse(address.trim())
        if (uri.host.isNullOrBlank()
            || !(uri.scheme.equals("http", true) || uri.scheme.equals("https", true))) {
            Toast.makeText(this, "Enter a valid HTTP(S) server address", Toast.LENGTH_SHORT).show()
            return
        }
        getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE).edit()
            .putString(PREF_SERVER_ADDRESS, address.trim().trimEnd('/'))
            .putString(PREF_APP_MODE, "WEB")
            .apply()
        startActivity(Intent(this, MainActivity::class.java))
    }
}

@Composable
private fun DestinyGlassTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = sea,
            secondary = coral,
            tertiary = citron,
            background = ink,
            surface = Color(0xFF152125),
            onPrimary = ink,
            onSecondary = ink,
            onBackground = textMain,
            onSurface = textMain
        ),
        content = content
    )
}

@Composable
private fun DestinyWorkspace(
    telegramConnected: Boolean,
    savedAddress: String,
    onOpenLocal: (String, String?) -> Unit,
    onPlayLink: (String) -> Unit,
    onEditLink: (String) -> Unit,
    onOpenDashboard: (String) -> Unit,
    onRunBatchTask: (BatchTaskRequest, (String) -> Unit) -> Unit,
    onCancelBatchTask: (String, (String) -> Unit) -> Unit,
    onStartWatcher: (WatcherRequest, (String) -> Unit) -> Unit,
    onLoadWorkspaceSnapshot: () -> WorkspaceSnapshot,
    onStopWatcher: (LocalWatcherRow, (String) -> Unit) -> Unit,
    onSaveAddress: (String) -> Unit
) {
    var selectedTab by remember { mutableStateOf(WorkspaceTab.HOME) }
    var selectedMode by remember { mutableStateOf("FORWARD") }
    var sourceLink by remember { mutableStateOf("") }
    var serverAddress by remember { mutableStateOf(savedAddress) }
    val tabs = WorkspaceTab.entries

    Scaffold(
        containerColor = Color.Transparent,
        bottomBar = {
            NavigationBar(containerColor = Color(0xE610191C)) {
                tabs.forEach { tab ->
                    NavigationBarItem(
                        selected = selectedTab == tab,
                        onClick = { selectedTab = tab },
                        icon = { Icon(tab.icon, contentDescription = tab.title) },
                        label = { Text(tab.title) }
                    )
                }
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.linearGradient(
                        listOf(Color(0xFF17292B), ink, Color(0xFF201B1A))
                    )
                )
                .padding(innerPadding)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 22.dp, vertical = 18.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("DESTINY TG", color = sea, fontSize = 11.sp,
                        fontWeight = FontWeight.Bold, letterSpacing = 1.5.sp)
                    Text(selectedTab.title, color = textMain, fontSize = 26.sp,
                        fontWeight = FontWeight.SemiBold)
                }
                Surface(
                    color = if (telegramConnected) Color(0x333BD2A6) else Color(0x33FF987F),
                    shape = RoundedCornerShape(50),
                    border = BorderStroke(1.dp, if (telegramConnected) sea.copy(alpha = .45f)
                        else coral.copy(alpha = .45f))
                ) {
                    Text(
                        if (telegramConnected) "Telegram ready" else "Account setup",
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                        color = if (telegramConnected) sea else coral,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
            AnimatedContent(
                targetState = selectedTab,
                transitionSpec = {
                    (fadeIn() + slideInVertically { it / 18 }) togetherWith fadeOut()
                },
                label = "workspace-tab"
            ) { tab ->
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(rememberScrollState())
                        .padding(horizontal = 18.dp, vertical = 4.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    when (tab) {
                        WorkspaceTab.HOME -> HomeScreen(
                            telegramConnected,
                            onOpenTasks = { selectedTab = WorkspaceTab.TASKS },
                            onOpenEditor = { selectedTab = WorkspaceTab.EDITOR },
                            onPlayLink = { selectedTab = WorkspaceTab.THEATER }
                        )
                        WorkspaceTab.TASKS -> TaskScreen(
                            selectedMode = selectedMode,
                            onModeChange = { selectedMode = it },
                            onRunBatchTask = onRunBatchTask,
                            onCancelBatchTask = onCancelBatchTask,
                            onStartWatcher = onStartWatcher,
                            onLoadWorkspaceSnapshot = onLoadWorkspaceSnapshot,
                            onStopWatcher = onStopWatcher
                        )
                        WorkspaceTab.THEATER -> TheaterScreen(
                            sourceLink = sourceLink,
                            onSourceChange = { sourceLink = it },
                            onPlay = { if (sourceLink.isNotBlank()) onPlayLink(sourceLink) }
                        )
                        WorkspaceTab.EDITOR -> EditorScreen(
                            sourceLink = sourceLink,
                            onSourceChange = { sourceLink = it },
                            onEdit = { if (sourceLink.isNotBlank()) onEditLink(sourceLink) },
                            onOpenLocal = onOpenLocal
                        )
                        WorkspaceTab.SETTINGS -> SettingsScreen(
                            connected = telegramConnected,
                            serverAddress = serverAddress,
                            onServerAddressChange = {
                                serverAddress = it
                                onSaveAddress(it)
                            },
                            onOpenLocal = onOpenLocal,
                            onOpenDashboard = {
                                if (serverAddress.isNotBlank()) onOpenDashboard(serverAddress)
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun HomeScreen(
    connected: Boolean,
    onOpenTasks: () -> Unit,
    onOpenEditor: () -> Unit,
    onPlayLink: () -> Unit
) {
    GlassPanel {
        Text("Your device workspace", color = textMain, fontSize = 23.sp,
            fontWeight = FontWeight.SemiBold)
        Spacer(Modifier.height(8.dp))
        Text(
            if (connected) "Telegram session connected. Local media stays on this device."
            else "Direct URL downloads work now. Connect Telegram for chat tasks and watchers.",
            color = textMuted, fontSize = 14.sp, lineHeight = 21.sp
        )
        Spacer(Modifier.height(18.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            MetricPill("TASKS", "Forward / download", sea)
            MetricPill("MEDIA", "Local + links", citron)
        }
    }
    SectionTitle("Pick up where you left off")
    ActionPanel("Tasks and watchers", "Create, resume, and inspect transfers", Icons.Outlined.Download) {
        onOpenTasks()
    }
    ActionPanel("Media theater", "Play local files, Telegram posts, or direct URLs", Icons.Outlined.Movie) {
        onPlayLink()
    }
    ActionPanel("Media editor", "Trim and rename a local or staged media copy", Icons.Outlined.Edit) {
        onOpenEditor()
    }
}

@Composable
private fun TaskScreen(
    selectedMode: String,
    onModeChange: (String) -> Unit,
    onRunBatchTask: (BatchTaskRequest, (String) -> Unit) -> Unit,
    onCancelBatchTask: (String, (String) -> Unit) -> Unit,
    onStartWatcher: (WatcherRequest, (String) -> Unit) -> Unit,
    onLoadWorkspaceSnapshot: () -> WorkspaceSnapshot,
    onStopWatcher: (LocalWatcherRow, (String) -> Unit) -> Unit
) {
    var sourceType by remember { mutableStateOf("TELEGRAM") }
    var source by remember { mutableStateOf("") }
    var destination by remember { mutableStateOf("me") }
    var firstId by remember { mutableStateOf("") }
    var lastId by remember { mutableStateOf("") }
    var sourceTopic by remember { mutableStateOf("0") }
    var destinationTopic by remember { mutableStateOf("0") }
    var mediaTypes by remember { mutableStateOf("video,document,audio,photo,voice,animation,sticker,text") }
    var includeKeywords by remember { mutableStateOf("") }
    var excludeKeywords by remember { mutableStateOf("") }
    var cleanupKeywords by remember { mutableStateOf("") }
    var delay by remember { mutableStateOf("3") }
    var status by remember { mutableStateOf("") }
    var activeTaskId by remember { mutableStateOf("") }
    var refreshKey by remember { mutableStateOf(0) }
    var snapshot by remember { mutableStateOf(WorkspaceSnapshot(emptyList(), emptyList())) }
    val context = androidx.compose.ui.platform.LocalContext.current
    LaunchedEffect(refreshKey) {
        snapshot = withContext(Dispatchers.IO) { onLoadWorkspaceSnapshot() }
    }
    LaunchedEffect(activeTaskId) {
        while (activeTaskId.isNotEmpty()) {
            val progress = withContext(Dispatchers.IO) {
                runCatching {
                    val progressFile = File(File(context.filesDir, "tasks"),
                        "$activeTaskId.txt")
                    if (!progressFile.isFile) null else {
                        val parts = progressFile.readText().trim().split('|')
                        if (parts.size != 6) null else {
                            val total = parts[2].toLongOrNull()?.takeIf { it > 0 }
                                ?.toString() ?: "?"
                            "${parts[0]} ${parts[1]}/$total | sent ${parts[3]}, " +
                                "skipped ${parts[4]}, failed ${parts[5]}"
                        }
                    }
                }.getOrNull()
            }
            if (progress != null) status = progress
            delay(750)
        }
    }
    GlassPanel {
        Text(if (sourceType == "DIRECT") "Direct URL download" else "Telegram transfers",
            color = textMain, fontSize = 19.sp, fontWeight = FontWeight.SemiBold)
        Text("Direct URLs save to the device. Telegram sources can be forwarded or downloaded.",
            color = textMuted, fontSize = 13.sp, lineHeight = 19.sp)
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            ModeChoice("TELEGRAM", sourceType == "TELEGRAM", sea) {
                sourceType = "TELEGRAM"
            }
            ModeChoice("DIRECT URL", sourceType == "DIRECT", coral) {
                sourceType = "DIRECT"
                onModeChange("DOWNLOAD")
            }
        }
        GlassField(source, { source = it }, if (sourceType == "DIRECT")
            "Direct HTTP(S) media URL" else "Telegram message or channel link")
        if (sourceType == "TELEGRAM") {
            Text("Forward preserves attribution. Download saves a device copy and re-uploads.",
                color = textMuted, fontSize = 13.sp, lineHeight = 19.sp)
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                ModeChoice("FORWARD", selectedMode == "FORWARD", sea) {
                    onModeChange("FORWARD")
                }
                ModeChoice("DOWNLOAD", selectedMode == "DOWNLOAD", coral) {
                    onModeChange("DOWNLOAD")
                }
            }
            GlassField(destination, { destination = it },
                "Destination chat (me = Saved Messages)")
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                GlassField(firstId, { firstId = it }, "First message ID", Modifier.weight(1f))
                GlassField(lastId, { lastId = it }, "Last message ID", Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                GlassField(sourceTopic, { sourceTopic = it }, "Source topic", Modifier.weight(1f))
                GlassField(destinationTopic, { destinationTopic = it }, "Destination topic",
                    Modifier.weight(1f))
            }
            GlassField(mediaTypes, { mediaTypes = it }, "Media types, comma-separated")
            GlassField(includeKeywords, { includeKeywords = it }, "Include keywords")
            GlassField(excludeKeywords, { excludeKeywords = it }, "Exclude keywords")
            GlassField(cleanupKeywords, { cleanupKeywords = it }, "Cleanup tags (download mode)")
            GlassField(delay, { delay = it }, "Delay per message in seconds")
        } else {
            Text("The URL downloads directly to this device. Live watchers require a Telegram chat.",
                color = textMuted, fontSize = 13.sp, lineHeight = 19.sp)
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Button(
                onClick = {
                    if (source.isBlank()) status = if (sourceType == "DIRECT")
                        "Enter a direct HTTP(S) URL first" else "Enter a Telegram link first"
                    else if (sourceType == "TELEGRAM" && selectedMode == "FORWARD"
                        && cleanupKeywords.isNotBlank()) {
                        status = "Cleanup tags require Download mode"
                    } else if (activeTaskId.isNotEmpty()) {
                        status = "A batch task is already running"
                    } else onRunBatchTask(BatchTaskRequest(
                        sourceType, source.trim(), firstId.trim(), lastId.trim(), destination.trim(),
                        mediaTypes.trim(), includeKeywords.trim(), excludeKeywords.trim(),
                        delay.trim(), sourceTopic.trim(), destinationTopic.trim(),
                        cleanupKeywords.trim(), selectedMode
                    )) {
                        if (it.startsWith("TASK_STARTED:")) {
                            activeTaskId = it.substringAfter(':')
                            status = "Task $activeTaskId running"
                            refreshKey++
                        } else {
                            activeTaskId = ""
                            status = it
                            refreshKey++
                        }
                    }
                },
                modifier = Modifier.weight(1f),
                colors = ButtonDefaults.buttonColors(containerColor = sea, contentColor = ink)
            ) { Text(if (sourceType == "DIRECT") "Download to device" else "Start batch") }
            FilledTonalButton(
                onClick = {
                    if (sourceType != "TELEGRAM") status = "Watchers require a Telegram chat"
                    else if (source.isBlank()) status = "Enter a Telegram source first"
                    else if (selectedMode == "FORWARD" && cleanupKeywords.isNotBlank()) {
                        status = "Cleanup tags require Download mode"
                    } else onStartWatcher(WatcherRequest(
                        source.trim(), destination.trim(), mediaTypes.trim(),
                        includeKeywords.trim(), excludeKeywords.trim(), cleanupKeywords.trim(),
                        delay.trim(), sourceTopic.trim(), destinationTopic.trim(), selectedMode
                    )) {
                        status = it
                        refreshKey++
                    }
                },
                modifier = Modifier.weight(1f),
                enabled = sourceType == "TELEGRAM"
            ) { Text("Start watcher") }
        }
        if (activeTaskId.isNotEmpty()) {
            FilledTonalButton(
                onClick = {
                    onCancelBatchTask(activeTaskId) { status = it }
                },
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.filledTonalButtonColors(
                    containerColor = Color(0x443B2522), contentColor = coral
                )
            ) { Text("Cancel task $activeTaskId") }
        }
        if (status.isNotBlank()) Text(status, color = citron, fontSize = 12.sp)
    }
    SectionTitle("Active watchers")
    if (snapshot.watchers.isEmpty()) {
        Text("No active watchers", color = textMuted, fontSize = 13.sp,
            modifier = Modifier.padding(horizontal = 4.dp))
    } else {
        snapshot.watchers.forEach { watcher ->
            GlassPanel {
                Text(watcher.source, color = textMain, fontWeight = FontWeight.SemiBold)
                Text("To ${watcher.destination}  |  ${watcher.transferMode}  |  topics " +
                    "${watcher.sourceTopicId}/${watcher.destinationTopicId}",
                    color = textMuted, fontSize = 12.sp)
                FilledTonalButton(
                    onClick = {
                        onStopWatcher(watcher) {
                            status = it
                            refreshKey++
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.filledTonalButtonColors(
                        containerColor = Color(0x443B2522), contentColor = coral
                    )
                ) { Text("Stop watcher") }
            }
        }
    }
    SectionTitle("Recent tasks")
    if (snapshot.tasks.isEmpty()) {
        Text("No recent tasks", color = textMuted, fontSize = 13.sp,
            modifier = Modifier.padding(horizontal = 4.dp))
    } else {
        snapshot.tasks.forEach { task ->
            GlassPanel {
                Text(task.label, color = textMain, fontWeight = FontWeight.SemiBold,
                    maxLines = 2)
                Text("${task.kind}  |  ${task.state}", color = sea, fontSize = 11.sp,
                    fontWeight = FontWeight.Bold)
                Text(task.detail, color = textMuted, fontSize = 12.sp, lineHeight = 17.sp)
            }
        }
    }
}

@Composable
private fun TheaterScreen(
    sourceLink: String,
    onSourceChange: (String) -> Unit,
    onPlay: () -> Unit
) {
    GlassPanel {
        Text("Universal theater", color = textMain, fontSize = 20.sp,
            fontWeight = FontWeight.SemiBold)
        Text("Open local media, a Telegram message, or a direct HTTP(S) media URL.",
            color = textMuted, fontSize = 13.sp, lineHeight = 19.sp)
        GlassField(sourceLink, onSourceChange, "Telegram or direct media link")
        Button(
            onClick = onPlay,
            modifier = Modifier.fillMaxWidth(),
            enabled = sourceLink.isNotBlank(),
            colors = ButtonDefaults.buttonColors(containerColor = sea, contentColor = ink)
        ) { Text("Play in theater", fontWeight = FontWeight.SemiBold) }
    }
}

@Composable
private fun EditorScreen(
    sourceLink: String,
    onSourceChange: (String) -> Unit,
    onEdit: () -> Unit,
    onOpenLocal: (String, String?) -> Unit
) {
    GlassPanel {
        Text("Media editor", color = textMain, fontSize = 20.sp,
            fontWeight = FontWeight.SemiBold)
        Text("Remote sources are staged locally before editing. Original links are not modified.",
            color = textMuted, fontSize = 13.sp, lineHeight = 19.sp)
        GlassField(sourceLink, onSourceChange, "Telegram or direct media link")
        Button(
            onClick = onEdit,
            modifier = Modifier.fillMaxWidth(),
            enabled = sourceLink.isNotBlank(),
            colors = ButtonDefaults.buttonColors(containerColor = coral, contentColor = ink)
        ) { Text("Stage and edit", fontWeight = FontWeight.SemiBold) }
    }
    ActionPanel("Open device library", "Import, play, and edit files already saved here", Icons.Outlined.Edit) {
        onOpenLocal("library", null)
    }
}

@Composable
private fun SettingsScreen(
    connected: Boolean,
    serverAddress: String,
    onServerAddressChange: (String) -> Unit,
    onOpenLocal: (String, String?) -> Unit,
    onOpenDashboard: () -> Unit
) {
    GlassPanel {
        Text("Connections", color = textMain, fontSize = 20.sp,
            fontWeight = FontWeight.SemiBold)
        Text(if (connected) "Telegram is connected on this device." else "Telegram is not connected.",
            color = textMuted, fontSize = 13.sp)
        Button(
            onClick = { onOpenLocal("account", null) },
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.filledTonalButtonColors()
        ) { Text(if (connected) "Telegram and worker bots" else "Connect Telegram") }
        GlassField(serverAddress, onServerAddressChange, "https://your-destiny-server")
        Button(
            onClick = onOpenDashboard,
            modifier = Modifier.fillMaxWidth(),
            enabled = serverAddress.isNotBlank(),
            colors = ButtonDefaults.buttonColors(containerColor = citron, contentColor = ink)
        ) { Text("Open optional server workspace", fontWeight = FontWeight.SemiBold) }
    }
    GlassPanel {
        Text("Worker pools", color = textMain, fontSize = 16.sp,
            fontWeight = FontWeight.SemiBold)
        Text("Stream/editor bots and task/watcher bots reconnect independently.",
            color = textMuted, fontSize = 13.sp, lineHeight = 19.sp)
    }
}

@Composable
private fun GlassPanel(content: @Composable androidx.compose.foundation.layout.ColumnScope.() -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(
                Brush.verticalGradient(listOf(Color(0xD925373A), glass)),
                RoundedCornerShape(18.dp)
            )
            .border(1.dp, glassLine, RoundedCornerShape(18.dp))
            .padding(17.dp),
        verticalArrangement = Arrangement.spacedBy(11.dp),
        content = content
    )
}

@Composable
private fun ActionPanel(title: String, description: String, icon: ImageVector, onClick: () -> Unit) {
    Surface(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        color = glass,
        border = BorderStroke(1.dp, glassLine)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = sea, modifier = Modifier.size(25.dp))
            Spacer(Modifier.width(13.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(title, color = textMain, fontWeight = FontWeight.SemiBold, fontSize = 15.sp)
                Spacer(Modifier.height(3.dp))
                Text(description, color = textMuted, fontSize = 12.sp, lineHeight = 17.sp)
            }
            Text("›", color = sea, fontSize = 25.sp)
        }
    }
}

@Composable
private fun GlassField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        modifier = modifier.fillMaxWidth(),
        label = { Text(label) },
        singleLine = true,
        colors = OutlinedTextFieldDefaults.colors(
            focusedTextColor = textMain,
            unfocusedTextColor = textMain,
            focusedBorderColor = sea,
            unfocusedBorderColor = glassLine,
            focusedLabelColor = sea,
            unfocusedLabelColor = textMuted,
            cursorColor = sea
        )
    )
}

@Composable
private fun RowScope.ModeChoice(label: String, selected: Boolean, accent: Color, onClick: () -> Unit) {
    FilledTonalButton(
        onClick = onClick,
        modifier = Modifier.weight(1f),
        colors = ButtonDefaults.filledTonalButtonColors(
            containerColor = if (selected) accent.copy(alpha = .22f) else Color(0x332B3C3E),
            contentColor = if (selected) accent else textMuted
        ),
        border = BorderStroke(1.dp, if (selected) accent.copy(alpha = .65f) else glassLine)
    ) { Text(label, fontWeight = FontWeight.SemiBold) }
}

@Composable
private fun RowScope.MetricPill(label: String, value: String, tint: Color) {
    Column(
        modifier = Modifier
            .weight(1f)
            .background(Color(0x332E4546), RoundedCornerShape(13.dp))
            .padding(horizontal = 12.dp, vertical = 11.dp)
    ) {
        Text(label, color = tint, fontSize = 10.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(4.dp))
        Text(value, color = textMain, fontSize = 12.sp, fontWeight = FontWeight.Medium)
    }
}

@Composable
private fun SectionTitle(text: String) {
    Text(text, color = textMuted, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
        modifier = Modifier.padding(start = 3.dp, top = 4.dp))
}