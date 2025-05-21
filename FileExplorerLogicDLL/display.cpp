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
    DLLEXPORT const char* displayDirectoryContents(const char* path);
}

const char* displayDirectoryContents(const char* path)
{
    static std::string result;
    try {
        result = "";
        for (const auto& entry : fs::directory_iterator(path))
        {
            result += (fs::is_directory(entry.status()) ? "[DIR] " : "[FILE] ") + entry.path().filename().string() + "\n";
        }
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}
