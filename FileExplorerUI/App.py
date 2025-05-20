import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QMenu, QAction, QMessageBox, QInputDialog, QAbstractItemView, QFileSystemModel
from PyQt5.QtCore import Qt, QMimeData
import ctypes
from ctypes import c_char_p, c_bool

# Specify the full path to the DLL file
dll_path = r"./FileExplorerLogicDLL.dll"
file_explorer = ctypes.CDLL(dll_path)

# Define the functions with the correct return types
file_explorer.displayDirectoryContents.restype = c_char_p
file_explorer.deleteFile.restype = c_char_p
file_explorer.deleteDirectory.restype = c_char_p
file_explorer.createDirectory.restype = c_char_p
file_explorer.createFile.restype = c_char_p
file_explorer.displayFileProperties.restype = c_char_p
file_explorer.openFileWithDefaultApplication.restype = c_char_p
file_explorer.renameFile.restype = c_char_p
file_explorer.renameDirectory.restype = c_char_p
file_explorer.copyItem.restype = c_char_p
file_explorer.pasteItem.restype = c_char_p
file_explorer.hasCopiedItem.restype = c_bool
file_explorer.moveItem.restype = c_char_p
file_explorer.getCurrentName.restype = c_char_p

class FileExplorerApp(QMainWindow):
    def __init__(self, root_path):
        super().__init__()
        self.root_path = root_path
        self.initUI()
        self.copied_path = None

    def initUI(self):
        self.setWindowTitle('File Explorer')
        self.setGeometry(100, 100, 800, 600)

        self.model = QFileSystemModel()
        self.model.setRootPath(self.root_path)
        self.tree = QTreeView(self)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.root_path))
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openContextMenu)
        self.tree.setAcceptDrops(True)
        self.tree.setDragEnabled(True)
        self.tree.setDragDropMode(QAbstractItemView.InternalMove)
        self.tree.setDropIndicatorShown(True)
        self.tree.dragEnterEvent = self.onDragEnterEvent
        self.tree.dragMoveEvent = self.onDragMoveEvent
        self.tree.dropEvent = self.onDropEvent
        self.tree.doubleClicked.connect(self.onDoubleClick)
        self.setCentralWidget(self.tree)

    def openContextMenu(self, position):
        indexes = self.tree.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            path = self.model.filePath(index)
        else:
            path = self.root_path

        menu = QMenu()

        createMenu = QMenu("Create", self)
        createFileAction = QAction("File", self)
        createDirAction = QAction("Directory", self)
        createMenu.addAction(createFileAction)
        createMenu.addAction(createDirAction)
        createFileAction.triggered.connect(lambda: self.createFile(path))
        createDirAction.triggered.connect(lambda: self.createDirectory(path))

        openAction = QAction("Open", self)
        deleteAction = QAction("Delete", self)
        renameAction = QAction("Rename", self)
        copyAction = QAction("Copy", self)
        pasteAction = QAction("Paste", self)
        pasteAction.setEnabled(file_explorer.hasCopiedItem())
        moveAction = QAction("Move", self)
        copyPathAction = QAction("Copy Path", self)
        propertiesAction = QAction("Properties", self)

        openAction.triggered.connect(lambda: self.openItem(path))
        deleteAction.triggered.connect(lambda: self.deleteItem(path))
        renameAction.triggered.connect(lambda: self.renameItem(path))
        copyAction.triggered.connect(lambda: self.copyItem(path))
        pasteAction.triggered.connect(lambda: self.pasteItem(path))
        moveAction.triggered.connect(lambda: self.moveItem(path))
        copyPathAction.triggered.connect(lambda: self.copyPath(path))
        propertiesAction.triggered.connect(lambda: self.displayProperties(path))

        menu.addMenu(createMenu)
        menu.addAction(openAction)
        menu.addAction(deleteAction)
        menu.addAction(renameAction)
        menu.addAction(copyAction)
        menu.addAction(pasteAction)
        menu.addAction(moveAction)
        menu.addAction(copyPathAction)
        menu.addAction(propertiesAction)

        menu.exec_(self.tree.viewport().mapToGlobal(position))

    def copyPath(self, path):
        QApplication.clipboard().setText(path)
        QMessageBox.information(self, "Copy Path", f"Path copied to clipboard: {path}")

    def onDragEnterEvent(self, event):
        event.accept()

    def onDragMoveEvent(self, event):
        event.accept()

    def onDropEvent(self, event):
        source_index = self.tree.indexAt(event.pos())
        if not source_index.isValid():
            event.ignore()
            return
        destination_path = self.model.filePath(self.tree.indexAt(event.pos()))
        source_path = self.model.filePath(self.tree.currentIndex())
        result = file_explorer.moveItem(source_path.encode('utf-8'), destination_path.encode('utf-8')).decode('utf-8')
        if "Error" in result:
            QMessageBox.critical(self, "Move", result)
        else:
            QMessageBox.information(self, "Move", result)
        self.model.setRootPath(self.root_path)  # Refresh the model
        event.accept()

    def onDoubleClick(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.openItem(path)

if __name__ == '__main__':
    root_directory = r"C:\Test"
    app = QApplication(sys.argv)
    ex = FileExplorerApp(root_directory)
    ex.show()
    sys.exit(app.exec_())
