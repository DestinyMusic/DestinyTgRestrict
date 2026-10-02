import CoreData
import Combine
import Foundation
import UniformTypeIdentifiers

@objc(LocalMediaRecord)
final class LocalMediaRecord: NSManagedObject, Identifiable {
    @NSManaged var id: UUID
    @NSManaged var name: String
    @NSManaged var path: String
    @NSManaged var mimeType: String
    @NSManaged var createdAt: Date

    var fileURL: URL { URL(fileURLWithPath: path) }
}

@MainActor
final class LocalMediaStore: ObservableObject {
    @Published private(set) var items: [LocalMediaRecord] = []
    @Published var errorMessage: String?

    private let container: NSPersistentContainer

    init() {
        let model = NSManagedObjectModel()
        let entity = NSEntityDescription()
        entity.name = "LocalMediaRecord"
        entity.managedObjectClassName = NSStringFromClass(LocalMediaRecord.self)
        entity.properties = [
            Self.attribute("id", type: .UUIDAttributeType),
            Self.attribute("name", type: .stringAttributeType),
            Self.attribute("path", type: .stringAttributeType),
            Self.attribute("mimeType", type: .stringAttributeType),
            Self.attribute("createdAt", type: .dateAttributeType)
        ]
        model.entities = [entity]

        container = NSPersistentContainer(name: "DestinyLocal", managedObjectModel: model)
        let supportDirectory = FileManager.default.urls(for: .applicationSupportDirectory,
                                                        in: .userDomainMask)[0]
        try? FileManager.default.createDirectory(at: supportDirectory,
                                                 withIntermediateDirectories: true,
                                                 attributes: nil)
        let storeURL = supportDirectory.appendingPathComponent("destiny-local.sqlite")
        container.persistentStoreDescriptions = [NSPersistentStoreDescription(url: storeURL)]
        container.loadPersistentStores { [weak self] _, error in
            Task { @MainActor in
                if let error {
                    self?.errorMessage = "Local database could not open: \(error.localizedDescription)"
                } else {
                    self?.refresh()
                }
            }
        }
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
    }

    func refresh() {
        let request = NSFetchRequest<LocalMediaRecord>(entityName: "LocalMediaRecord")
        request.sortDescriptors = [NSSortDescriptor(key: "createdAt", ascending: false)]
        do {
            items = try container.viewContext.fetch(request)
        } catch {
            errorMessage = "Could not load the local library: \(error.localizedDescription)"
        }
    }

    func importFile(from source: URL, named requestedName: String? = nil) throws {
        let directory = try mediaDirectory()
        let name = safeFileName(requestedName ?? source.lastPathComponent)
        let destination = directory.appendingPathComponent(UUID().uuidString + "-" + name)
        try FileManager.default.copyItem(at: source, to: destination)

        let record = LocalMediaRecord(context: container.viewContext)
        record.id = UUID()
        record.name = name
        record.path = destination.path
        record.mimeType = UTType(filenameExtension: destination.pathExtension)?.preferredMIMEType
            ?? "application/octet-stream"
        record.createdAt = Date()
        try save()
    }

    func addExport(at fileURL: URL, named name: String) throws {
        let record = LocalMediaRecord(context: container.viewContext)
        record.id = UUID()
        record.name = safeFileName(name)
        record.path = fileURL.path
        record.mimeType = UTType(filenameExtension: fileURL.pathExtension)?.preferredMIMEType
            ?? "application/octet-stream"
        record.createdAt = Date()
        try save()
    }

    func delete(_ item: LocalMediaRecord) {
        try? FileManager.default.removeItem(at: item.fileURL)
        container.viewContext.delete(item)
        try? save()
    }

    func mediaDirectory() throws -> URL {
        let directory = FileManager.default.urls(for: .documentDirectory,
                                                 in: .userDomainMask)[0]
            .appendingPathComponent("Media", isDirectory: true)
        try FileManager.default.createDirectory(at: directory,
                                                withIntermediateDirectories: true,
                                                attributes: nil)
        return directory
    }

    private func save() throws {
        try container.viewContext.save()
        refresh()
    }

    private func safeFileName(_ value: String) -> String {
        let cleaned = value.replacingOccurrences(of: "/", with: "_")
            .replacingOccurrences(of: "\\\\", with: "_")
            .trimmingCharacters(in: .whitespacesAndNewlines)
        return cleaned.isEmpty ? "media" : cleaned
    }

    private static func attribute(_ name: String,
                                  type: NSAttributeType) -> NSAttributeDescription {
        let attribute = NSAttributeDescription()
        attribute.name = name
        attribute.attributeType = type
        attribute.isOptional = false
        return attribute
    }
}
