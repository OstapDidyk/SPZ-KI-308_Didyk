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
    DLLEXPORT const char* moveItem(const char* sourcePath, const char* destinationPath);
}

const char* moveItem(const char* sourcePath, const char* destinationPath)
{
    static std::string result;
    try {
        if (fs::exists(sourcePath)) {
            fs::path dest = fs::path(destinationPath) / fs::path(sourcePath).filename();
            if (fs::is_directory(sourcePath)) {
                fs::rename(sourcePath, dest);
                result = "Directory moved successfully.";
            }
            else {
                fs::rename(sourcePath, dest);
                result = "File moved successfully.";
            }
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
