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
    DLLEXPORT const char* openFileWithDefaultApplication(const char* filePath);
}

const char* openFileWithDefaultApplication(const char* filePath)
{
    static std::string result;
    try {
        if (fs::exists(filePath) && fs::is_regular_file(filePath)) {
            // Convert filePath to wide string
            wchar_t wFilePath[MAX_PATH];
            MultiByteToWideChar(CP_ACP, 0, filePath, -1, wFilePath, MAX_PATH);

            HINSTANCE ret = ShellExecute(NULL, L"open", wFilePath, NULL, NULL, SW_SHOW);
            if ((int)ret <= 32) {
                result = "Failed to open file.";
            }
            else {
                result = "";
            }
        }
        else {
            result = "Invalid file path.";
        }
        return result.c_str();
    }
    catch (const exception& e) {
        result = "Error: " + std::string(e.what());
        return result.c_str();
    }
}
