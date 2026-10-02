import AVFoundation
import AVKit
import SwiftUI
import UniformTypeIdentifiers

struct LocalFirstAppView: View {
    @StateObject private var store = LocalMediaStore()
    @State private var showingImporter = false
    @State private var playingItem: LocalMediaRecord?
    @State private var editingItem: LocalMediaRecord?

    var body: some View {
        TabView {
            libraryTab
                .tabItem { Label("Library", systemImage: "square.stack") }
            DirectDownloadView(store: store)
                .tabItem { Label("Downloads", systemImage: "arrow.down.circle") }
        }
        .tint(.teal)
        .fileImporter(isPresented: $showingImporter,
                      allowedContentTypes: [.audio, .movie, .video, .data],
                      allowsMultipleSelection: true,
                      onCompletion: importResult)
        .sheet(item: $playingItem) { TheaterView(item: $0) }
        .sheet(item: $editingItem) { LocalEditorView(item: $0, store: store) }
    }

    private var libraryTab: some View {
        NavigationView {
            Group {
                if store.items.isEmpty {
                    VStack(spacing: 10) {
                        Image(systemName: "square.stack")
                            .font(.largeTitle)
                            .foregroundStyle(.secondary)
                        Text("Your library is empty").font(.headline)
                        Text("Import media stored on this device.")
                            .foregroundStyle(.secondary)
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    List {
                        ForEach(store.items) { item in
                            HStack(spacing: 12) {
                                Image(systemName: item.mimeType.hasPrefix("video/")
                                      ? "film" : "waveform")
                                    .font(.title2)
                                    .foregroundStyle(.teal)
                                    .frame(width: 36)
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(item.name).lineLimit(2)
                                    Text(item.mimeType)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                                Spacer(minLength: 4)
                                Button { playingItem = item } label: {
                                    Image(systemName: "play.fill")
                                }
                                .accessibilityLabel("Play \(item.name)")
                                Button { editingItem = item } label: {
                                    Image(systemName: "slider.horizontal.3")
                                }
                                .accessibilityLabel("Edit \(item.name)")
                            }
                            .padding(.vertical, 5)
                            .swipeActions {
                                Button(role: .destructive) { store.delete(item) } label: {
                                    Label("Delete", systemImage: "trash")
                                }
                            }
                        }
                    }
                }
            }
            .navigationTitle("On-device library")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button { showingImporter = true } label: {
                        Image(systemName: "plus")
                    }
                    .accessibilityLabel("Import media")
                }
            }
            .alert("Local storage", isPresented: Binding(
                get: { store.errorMessage != nil },
                set: { if !$0 { store.errorMessage = nil } }
            )) {
                Button("OK", role: .cancel) { store.errorMessage = nil }
            } message: {
                Text(store.errorMessage ?? "")
            }
        }
        .navigationViewStyle(.stack)
    }

    private func importResult(_ result: Result<[URL], Error>) {
        switch result {
        case .success(let urls):
            for url in urls {
                let hasAccess = url.startAccessingSecurityScopedResource()
                defer { if hasAccess { url.stopAccessingSecurityScopedResource() } }
                do {
                    try store.importFile(from: url)
                } catch {
                    store.errorMessage = "Import failed: \(error.localizedDescription)"
                }
            }
        case .failure(let error):
            store.errorMessage = "Import failed: \(error.localizedDescription)"
        }
    }
}

private struct TheaterView: View {
    let item: LocalMediaRecord
    @State private var player: AVPlayer?
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationView {
            Group {
                if let player {
                    VideoPlayer(player: player)
                        .background(Color.black)
                        .onAppear { player.play() }
                        .onDisappear { player.pause() }
                } else {
                    ProgressView("Preparing playback")
                }
            }
            .navigationTitle(item.name)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        player?.pause()
                        dismiss()
                    }
                }
            }
        }
        .onAppear { player = AVPlayer(url: item.fileURL) }
        .navigationViewStyle(.stack)
    }
}

private struct LocalEditorView: View {
    let item: LocalMediaRecord
    @ObservedObject var store: LocalMediaStore
    @Environment(\.dismiss) private var dismiss
    @State private var duration = 0.0
    @State private var trimStart = 0.0
    @State private var trimEnd = 0.0
    @State private var isExporting = false
    @State private var message: String?

    var body: some View {
        NavigationView {
            Form {
                Section("Media") {
                    metadataRow("Name", value: item.name)
                    metadataRow("Format", value: item.mimeType)
                    metadataRow("Duration", value: duration > 0 ? timeString(duration) : "Unknown")
                }
                if duration > 0 {
                    Section("Trim") {
                        VStack(alignment: .leading) {
                            Text("Start: \(timeString(trimStart))")
                            Slider(value: $trimStart, in: 0...max(duration, 0.1))
                                .onChange(of: trimStart) { value in
                                    if value >= trimEnd { trimEnd = min(duration, value + 0.1) }
                                }
                        }
                        VStack(alignment: .leading) {
                            Text("End: \(timeString(trimEnd))")
                            Slider(value: $trimEnd, in: 0...max(duration, 0.1))
                                .onChange(of: trimEnd) { value in
                                    if value <= trimStart { trimStart = max(0, value - 0.1) }
                                }
                        }
                        Button {
                            Task { await exportTrim() }
                        } label: {
                            HStack {
                                if isExporting { ProgressView() }
                                Text(isExporting ? "Exporting" : "Export trimmed copy")
                            }
                        }
                        .disabled(isExporting || trimEnd - trimStart < 0.1)
                    }
                }
                Section {
                    Text("The source file stays unchanged. Exports are saved to this device's library.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Media editor")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
            .task { await loadDuration() }
            .alert("Media editor", isPresented: Binding(
                get: { message != nil },
                set: { if !$0 { message = nil } }
            )) {
                Button("OK", role: .cancel) { message = nil }
            } message: {
                Text(message ?? "")
            }
        }
        .navigationViewStyle(.stack)
    }

    private func loadDuration() async {
        do {
            let asset = AVURLAsset(url: item.fileURL)
            let time = try await asset.load(.duration)
            let seconds = time.seconds
            guard seconds.isFinite, seconds > 0 else { return }
            duration = seconds
            trimEnd = seconds
        } catch {
            message = "Could not read media duration: \(error.localizedDescription)"
        }
    }

    private func exportTrim() async {
        isExporting = true
        defer { isExporting = false }

        let isVideo = item.mimeType.hasPrefix("video/")
        let asset = AVURLAsset(url: item.fileURL)
        let preset = isVideo ? AVAssetExportPresetHighestQuality : AVAssetExportPresetAppleM4A
        guard let session = AVAssetExportSession(asset: asset, presetName: preset) else {
            message = "This media format cannot be exported on this device."
            return
        }

        do {
            let directory = try store.mediaDirectory()
            let suffix = isVideo ? "mp4" : "m4a"
            let baseName = item.fileURL.deletingPathExtension().lastPathComponent
            let output = directory.appendingPathComponent("\(baseName)-trimmed-\(UUID().uuidString).\(suffix)")
            session.outputURL = output
            session.outputFileType = isVideo ? .mp4 : .m4a
            session.timeRange = CMTimeRange(
                start: CMTime(seconds: trimStart, preferredTimescale: 600),
                duration: CMTime(seconds: trimEnd - trimStart, preferredTimescale: 600)
            )

            let status: AVAssetExportSession.Status = await withCheckedContinuation { continuation in
                session.exportAsynchronously { continuation.resume(returning: session.status) }
            }
            guard status == .completed else {
                try? FileManager.default.removeItem(at: output)
                throw session.error ?? NSError(domain: "DestinyMediaExport", code: Int(status.rawValue))
            }
            try store.addExport(at: output, named: output.lastPathComponent)
            message = "Trimmed copy added to the local library."
        } catch {
            message = "Export failed: \(error.localizedDescription)"
        }
    }

    private func timeString(_ seconds: Double) -> String {
        let total = max(0, Int(seconds))
        return String(format: "%02d:%02d", total / 60, total % 60)
    }

    private func metadataRow(_ title: String, value: String) -> some View {
        HStack {
            Text(title)
            Spacer()
            Text(value).foregroundStyle(.secondary).multilineTextAlignment(.trailing)
        }
    }
}

private struct DirectDownloadView: View {
    @ObservedObject var store: LocalMediaStore
    @State private var address = ""
    @State private var status = ""
    @State private var isDownloading = false

    var body: some View {
        NavigationView {
            Form {
                Section("Direct download") {
                    TextField("https://example.com/media.mp4", text: $address)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                        .keyboardType(.URL)
                    Button {
                        Task { await download() }
                    } label: {
                        HStack {
                            if isDownloading { ProgressView() }
                            Text(isDownloading ? "Downloading" : "Download to this device")
                        }
                    }
                    .disabled(isDownloading)
                    if !status.isEmpty { Text(status).font(.footnote) }
                }
                Section {
                    Text("Downloads use this device's network and are stored only in its local library. Enter a direct HTTP(S) media URL you are authorized to access.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Downloads")
        }
        .navigationViewStyle(.stack)
    }

    private func download() async {
        guard let components = URLComponents(string: address.trimmingCharacters(in: .whitespacesAndNewlines)),
              ["http", "https"].contains(components.scheme?.lowercased() ?? ""),
              let url = components.url else {
            status = "Enter a valid direct HTTP(S) URL."
            return
        }

        isDownloading = true
        status = "Connecting…"
        defer { isDownloading = false }
        do {
            let (temporaryURL, response) = try await URLSession.shared.download(from: url)
            if let response = response as? HTTPURLResponse,
               !(200...299).contains(response.statusCode) {
                throw NSError(domain: "DestinyDownload", code: response.statusCode,
                              userInfo: [NSLocalizedDescriptionKey: "Server returned HTTP \(response.statusCode)"])
            }
            let name: String
            if let suggestedName = response.suggestedFilename, !suggestedName.isEmpty {
                name = suggestedName
            } else {
                name = url.lastPathComponent.isEmpty ? "download" : url.lastPathComponent
            }
            try store.importFile(from: temporaryURL, named: name)
            status = "Saved \(name) to the local library."
        } catch {
            status = "Download failed: \(error.localizedDescription)"
        }
    }
}
