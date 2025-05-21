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
file_explorer.copyItem.restype = c_char_p
file_explorer.pasteItem.restype = c_char_p
file_explorer.hasCopiedItem.restype = c_bool

    def copyItem(self, path):
        result = file_explorer.copyItem(path.encode('utf-8')).decode('utf-8')
        if result:
            self.copied_path = path
            QMessageBox.information(self, "Copy", result)

    def pasteItem(self, path):
        result = file_explorer.pasteItem(path.encode('utf-8')).decode('utf-8')
        if "Error" in result:
            QMessageBox.critical(self, "Paste", result)
        else:
            QMessageBox.information(self, "Paste", result)
        self.model.setRootPath(self.root_path)  # Refresh the model
