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
file_explorer.moveItem.restype = c_char_p

 def moveItem(self, source_path):
        destination, ok = QInputDialog.getText(self, "Move To", "Enter destination path:")
        if ok and destination:
            result = file_explorer.moveItem(source_path.encode('utf-8'), destination.encode('utf-8')).decode('utf-8')
            if "Error" in result:
                QMessageBox.critical(self, "Move", result)
            else:
                QMessageBox.information(self, "Move", result)
            self.model.setRootPath(self.root_path)  # Refresh the model
