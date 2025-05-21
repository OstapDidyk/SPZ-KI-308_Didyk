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
    DLLEXPORT const char* createDirectory(const char* path);
    DLLEXPORT const char* createFile(const char* path);
}


const char* createDirectory(const char* path)
{
    static std::string result;
    try {
        if (fs::create_directory(path)) {
            result = "Directory created successfully.";
        }
        else {
            result = "Failed to create directory.";
        }
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}

const char* createFile(const char* path)
{
    static std::string result;
    try {
        ofstream file(path);
        if (file) {
            result = "File created successfully.";
        }
        else {
            result = "Failed to create file.";
        }
        file.close();
        return result.c_str();
    }
    catch (const fs::filesystem_error& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}
