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
    DLLEXPORT const char* deleteFile(const char* path);
    DLLEXPORT const char* deleteDirectory(const char* path);
}


const char* deleteFile(const char* path)
{
    static std::string result;
    try {
        if (fs::exists(path)) {
            fs::remove(path);
            result = "File deleted successfully.";
        }
        else {
            result = "File not found.";
        }
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}

const char* deleteDirectory(const char* path)
{
    static std::string result;
    try {
        if (fs::exists(path) && fs::is_directory(path)) {
            fs::remove_all(path);
            result = "Directory deleted successfully.";
        }
        else {
            result = "Directory not found.";
        }
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}
