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
file_explorer.createDirectory.restype = c_char_p
file_explorer.createFile.restype = c_char_p

    def createFile(self, path):
        name, ok = QInputDialog.getText(self, "Create File", "Enter file name:")
        if ok and name:
            full_path = os.path.join(path, name)
            result = file_explorer.createFile(full_path.encode('utf-8')).decode('utf-8')
            if "Error" in result:
                QMessageBox.critical(self, "Create File", result)
            else:
                QMessageBox.information(self, "Create File", result)
            self.model.setRootPath(self.root_path)  # Refresh the model

    def createDirectory(self, path):
        name, ok = QInputDialog.getText(self, "Create Directory", "Enter directory name:")
        if ok and name:
            full_path = os.path.join(path, name)
            result = file_explorer.createDirectory(full_path.encode('utf-8')).decode('utf-8')
            if "Error" in result:
                QMessageBox.critical(self, "Create Directory", result)
            else:
                QMessageBox.information(self, "Create Directory", result)
            self.model.setRootPath(self.root_path)  # Refresh the model
