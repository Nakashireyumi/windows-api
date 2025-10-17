// testing/runner.cpp
#include <iostream>
#include <fstream>
#include <yaml-cpp/yaml.h>
#include <cstdlib>
#include <filesystem>

int main() {
    const std::string configPath = "testing/tests.yaml";
    if (!std::filesystem::exists(configPath)) {
        std::cerr << "❌ Config not found: " << configPath << std::endl;
        return 1;
    }

    YAML::Node config = YAML::LoadFile(configPath);
    if (!config["tests"]) {
        std::cerr << "❌ No 'tests' key in " << configPath << std::endl;
        return 1;
    }

    for (const auto& item : config["tests"]) {
        std::string project = item.first.as<std::string>();
        std::cout << "\n🚀 Running tests for: " << project << std::endl;

        for (const auto& fileNode : item.second) {
            std::string file = fileNode.as<std::string>();
            if (!std::filesystem::exists(file)) {
                std::cerr << "❌ File not found: " << file << std::endl;
                return 1;
            }

            std::string cmd = "node \"" + file + "\"";
            std::cout << "▶️  Executing: " << cmd << std::endl;
            int result = std::system(cmd.c_str());
            if (result != 0) {
                std::cerr << "❌ Test failed in " << file << std::endl;
                return result;
            }
        }
    }

    std::cout << "\n✅ All tests passed successfully.\n";
    return 0;
}
