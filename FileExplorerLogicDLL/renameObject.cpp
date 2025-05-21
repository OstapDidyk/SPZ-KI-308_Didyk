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
    DLLEXPORT const char* renameFile(const char* filePath, const char* newFileName);
    DLLEXPORT const char* renameDirectory(const char* dirPath, const char* newDirName);
}

const char* renameFile(const char* filePath, const char* newFileName)
{
    static std::string result;
    try {
        if (fs::exists(filePath) && fs::is_regular_file(filePath)) {
            fs::path parentPath = fs::path(filePath).parent_path();
            fs::path newFilePath = parentPath / newFileName;
            if (fs::exists(newFilePath)) {
                result = "A file with the new name already exists.";
            }
            else {
                fs::rename(filePath, newFilePath);
                result = "File renamed successfully.";
            }
        }
        else {
            result = "Invalid file path.";
        }
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}

const char* renameDirectory(const char* dirPath, const char* newDirName)
{
    static std::string result;
    try {
        if (fs::exists(dirPath) && fs::is_directory(dirPath)) {
            fs::path parentPath = fs::path(dirPath).parent_path();
            fs::path newDirPath = parentPath / newDirName;
            fs::rename(dirPath, newDirPath);
            result = "Directory renamed successfully.";
        }
        else {
            result = "Invalid directory path.";
        }
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}
