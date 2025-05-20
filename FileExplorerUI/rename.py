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
file_explorer.renameFile.restype = c_char_p
file_explorer.renameDirectory.restype = c_char_p
file_explorer.getCurrentName.restype = c_char_p

    def renameItem(self, path):
        currentName = file_explorer.getCurrentName(path.encode('utf-8')).decode('utf-8')
        newName, ok = QInputDialog.getText(self, "Rename To", "Enter new name:", text=currentName)
        if ok and newName:
            if os.path.isdir(path):
                result = file_explorer.renameDirectory(path.encode('utf-8'), newName.encode('utf-8')).decode('utf-8')
            else:
                result = file_explorer.renameFile(path.encode('utf-8'), newName.encode('utf-8')).decode('utf-8')
            if "Error" in result:
                QMessageBox.critical(self, "Rename", result)
            else:
                QMessageBox.information(self, "Rename", result)
            self.model.setRootPath(self.root_path)  # Refresh the model
