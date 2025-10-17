// testing/cassitly/launch.js
// This file path is for vibe coders lol

// src/resources/launch.js
// This file path is for vibe coders lol

import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import { spawn } from "child_process";

// ---------------------------
// Load YAML config
// ---------------------------
const CONFIG_PATH = path.resolve("src/resources/unit-test.yaml");
const config = yaml.load(fs.readFileSync(CONFIG_PATH, "utf8"));

// ---------------------------
// Run all test files per package
// ---------------------------
async function runTests() {
  for (const [pkg, files] of Object.entries(config.packages || {})) {
    console.log(`\n=== Running tests for package: ${pkg} ===`);

    for (const file of files) {
      const testPath = path.resolve(file);
      console.log(`\n▶ Launching: ${testPath}`);

      // Use Node to execute test file
      await new Promise((resolve, reject) => {
        const child = spawn("node", [testPath], { stdio: "inherit" });

        child.on("close", (code) => {
          if (code === 0) {
            console.log(`✅ Completed: ${file}`);
            resolve();
          } else {
            console.error(`❌ Failed: ${file} (exit code ${code})`);
            reject(new Error(`Test failed: ${file}`));
          }
        });
      });
    }
  }
  console.log("\n🎉 All tests finished!");
}

// ---------------------------
// Entry point
// ---------------------------
runTests().catch((err) => {
  console.error("\n💥 Test suite failed:", err.message);
  process.exit(1);
});
