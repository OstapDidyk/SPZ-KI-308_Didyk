#include "pch.h"
#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>
#include <vector>
#include <windows.h>
#include <shellapi.h>

#define DLLEXPORT __declspec(dllexport)

using namespace std;
namespace fs = std::filesystem;

// Глобальна змінна для зберігання шляху скопійованого файлу або директорії
static std::string copiedPath;

extern "C" {
    DLLEXPORT const char* copyItem(const char* sourcePath);
    DLLEXPORT const char* pasteItem(const char* destinationPath);
    DLLEXPORT bool hasCopiedItem();
}

const char* copyItem(const char* sourcePath)
{
    static std::string result;
    try {
        if (fs::exists(sourcePath)) {
            copiedPath = sourcePath;
            result = "Item copied.";
        }
        else {
            result = "Source path does not exist.";
        }
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}

const char* pasteItem(const char* destinationPath)
{
    static std::string result;
    try {
        if (!copiedPath.empty() && fs::exists(copiedPath)) {
            fs::path dest = fs::path(destinationPath) / fs::path(copiedPath).filename();
            int copy_index = 1;

            // Перевіряємо, чи файл або директорія з таким ім'ям вже існує, і додаємо суфікс для унікальності
            while (fs::exists(dest)) {
                dest = fs::path(destinationPath) / (fs::path(copiedPath).stem().string() + " - Copy " + to_string(copy_index) + fs::path(copiedPath).extension().string());
                copy_index++;
            }

            if (fs::is_directory(copiedPath)) {
                fs::copy(copiedPath, dest, fs::copy_options::recursive);
                result = "Directory pasted successfully.";
            }
            else {
                fs::copy(copiedPath, dest);
                result = "File pasted successfully.";
            }
        }
        else {
            result = "No item to paste or source path does not exist.";
        }
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}

bool hasCopiedItem()
{
    return !copiedPath.empty();
}

const char* copyFile(const char* sourceFilePath, const char* destinationFilePath)
{
    static std::string result;
    try {
        fs::copy(sourceFilePath, destinationFilePath);
        result = "File copied successfully.";
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}

const char* copyDirectory(const char* sourceDirPath, const char* destinationDirPath)
{
    static std::string result;
    try {
        fs::copy(sourceDirPath, destinationDirPath, fs::copy_options::recursive);
        result = "Directory copied successfully.";
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}
