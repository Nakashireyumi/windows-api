// This is unncessary AF
// Yeah, it could've been some other language. Why C++?

// testing/run-tests.cpp
#include <iostream>
#include <fstream>
#include <yaml-cpp/yaml.h>
#include <cstdlib>
#include <filesystem>
#include <string>

// Simple ANSI color helpers
#define GREEN "\033[32m"
#define RED "\033[31m"
#define YELLOW "\033[33m"
#define CYAN "\033[36m"
#define RESET "\033[0m"

int main() {
    const std::string configPath = "testing/tests.yaml";

    if (!std::filesystem::exists(configPath)) {
        std::cerr << RED << "❌ Config not found: " << configPath << RESET << std::endl;
        return 1;
    }

    YAML::Node config;
    try {
        config = YAML::LoadFile(configPath);
    } catch (const YAML::Exception& e) {
        std::cerr << RED << "❌ Failed to load YAML: " << e.what() << RESET << std::endl;
        return 1;
    }

    if (!config["tests"]) {
        std::cerr << RED << "❌ No 'tests' key in " << configPath << RESET << std::endl;
        return 1;
    }

    const YAML::Node tests = config["tests"];

    // Validate YAML structure
    if (!tests.IsMap()) {
        std::cerr << RED << "❌ 'tests' must be a map (project -> [files])" << RESET << std::endl;
        return 1;
    }

    bool allPassed = true;

    for (auto it = tests.begin(); it != tests.end(); ++it) {
        std::string projectName = it->first.as<std::string>();
        const YAML::Node files = it->second;

        std::cout << "\n🚀 Running tests for: " << CYAN << projectName << RESET << std::endl;

        if (!files.IsSequence()) {
            std::cerr << RED << "❌ Expected a list of files for project: " << projectName << RESET << std::endl;
            allPassed = false;
            continue;
        }

        for (const auto& fileNode : files) {
            std::string filePath = fileNode.as<std::string>();

            if (!std::filesystem::exists(filePath)) {
                std::cerr << RED << "❌ File not found: " << filePath << RESET << std::endl;
                allPassed = false;
                continue;
            }

            std::string cmd = "npx mocha \"" + filePath + "\"";
            std::cout << "▶️  Executing: " << YELLOW << cmd << RESET << std::endl;

            int result = std::system(cmd.c_str());
            if (result != 0) {
                std::cerr << RED << "❌ Test failed in " << filePath << RESET << std::endl;
                allPassed = false;
            }
        }
    }

    if (allPassed) {
        std::cout << "\n" << GREEN << "✅ All tests passed successfully." << RESET << std::endl;
        return 0;
    } else {
        std::cerr << "\n" << RED << "❌ Some tests failed." << RESET << std::endl;
        return 1;
    }
}
