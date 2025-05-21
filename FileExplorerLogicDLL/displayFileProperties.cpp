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
    DLLEXPORT const char* displayFileProperties(const char* path);
}

const char* displayFileProperties(const char* path)
{
    static std::string result;
    try {
        if (fs::exists(path)) {
            result = "File Properties: \n";
            result += "Path: " + fs::absolute(path).string() + "\n";
            result += "Size: " + to_string(fs::file_size(path)) + " bytes\n";
            result += "Permissions: ";
            if ((fs::status(path).permissions() & fs::perms::owner_read) != fs::perms::none) {
                result += "Read ";
            }
            if ((fs::status(path).permissions() & fs::perms::owner_write) != fs::perms::none) {
                result += "Write ";
            }
            if ((fs::status(path).permissions() & fs::perms::owner_exec) != fs::perms::none) {
                result += "Execute ";
            }
            result += "\n";
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
