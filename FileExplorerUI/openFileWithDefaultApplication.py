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
file_explorer.openFileWithDefaultApplication.restype = c_char_p

    def openItem(self, path):
        result = file_explorer.openFileWithDefaultApplication(path.encode('utf-8')).decode('utf-8')
        if result:  # Виводимо повідомлення тільки якщо є помилка
            QMessageBox.information(self, "Open", result)
