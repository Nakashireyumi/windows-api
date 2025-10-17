#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <filesystem>
#include <cstdlib>
#include <yaml-cpp/yaml.h>
#include <process.h>     // for _spawnl or similar (Windows)
#include <windows.h>

namespace fs = std::filesystem;

// Helper: run a command detached
void launchDetached(const std::string& command, const std::string& args) {
    STARTUPINFOA si{};
    PROCESS_INFORMATION pi{};
    si.cb = sizeof(si);

    std::string fullCmd = command + " " + args;
    if (!CreateProcessA(
            nullptr,
            fullCmd.data(),
            nullptr,
            nullptr,
            FALSE,
            CREATE_NEW_CONSOLE,
            nullptr,
            nullptr,
            &si,
            &pi))
    {
        std::cerr << "[LAUNCH ERROR] Failed to start: " << command
                  << " " << args << " (Error " << GetLastError() << ")\n";
        return;
    }

    std::cout << "[OK] Launched: " << fullCmd << "\n";
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
}

// Reads the YAML packages file
std::map<std::string, std::map<std::string, std::string>> loadPackages(const std::string& path) {
    std::map<std::string, std::map<std::string, std::string>> result;

    try {
        YAML::Node root = YAML::LoadFile(path);
        if (!root["packages"]) {
            std::cerr << "No 'packages' key found in YAML.\n";
            return result;
        }

        for (auto langNode : root["packages"]) {
            std::string lang = langNode.first.as<std::string>();
            auto pkgs = langNode.second;
            for (auto pkg : pkgs) {
                std::string name = pkg.first.as<std::string>();
                std::string module = pkg.second.as<std::string>();
                result[lang][name] = module;
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "[YAML ERROR] " << e.what() << "\n";
    }
    return result;
}

int main() {
    std::string yamlPath = "A:/windows-api/src/resources/packages.yaml";
    if (!fs::exists(yamlPath)) {
        std::cerr << "File not found: " << yamlPath << "\n";
        return 1;
    }

    auto packages = loadPackages(yamlPath);
    if (packages.empty()) {
        std::cerr << "No packages found.\n";
        return 1;
    }

    for (auto& [lang, pkgs] : packages) {
        std::cout << "[LANG] " << lang << "\n";
        for (auto& [name, module] : pkgs) {
            std::cout << "Launching " << name << " -> " << module << "\n";

            if (lang == "python") {
                std::string pythonExe = "python";  // assumes Python in PATH
                std::string args = "-m " + module;
                launchDetached(pythonExe, args);
            } else {
                std::cerr << "[WARN] Unsupported language: " << lang << "\n";
            }
        }
    }

    std::cout << "All packages launched.\n";
    return 0;
}
