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
file_explorer.deleteFile.restype = c_char_p
file_explorer.deleteDirectory.restype = c_char_p

    def deleteItem(self, path):
        if QMessageBox.question(self, "Delete", f"Are you sure you want to delete {path}?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if os.path.isdir(path):
                result = file_explorer.deleteDirectory(path.encode('utf-8')).decode('utf-8')
            else:
                result = file_explorer.deleteFile(path.encode('utf-8')).decode('utf-8')
            if "Error" in result:
                QMessageBox.critical(self, "Delete", result)
            else:
                QMessageBox.information(self, "Delete", result)
            self.model.setRootPath(self.root_path)  # Refresh the model
