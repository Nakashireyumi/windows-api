// testing/cassitly/launch.js
// This file path is for vibe coders lol

import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import { spawn } from "child_process";

// ---------------------------
// Load YAML config
// ---------------------------
const CONFIG_PATH = path.resolve("src/resources/unit-tests.yaml");
const config = yaml.load(fs.readFileSync(CONFIG_PATH, "utf8"));

// ---------------------------
// Utility: spawn a process and return handle
// ---------------------------
function startProcess(command, args, options = {}) {
  const [cmd, ...cmdArgs] = command.split(" ");
  const child = spawn(cmd, cmdArgs.concat(args || []), {
    stdio: "inherit",
    shell: true,
    ...options,
  });
  return child;
}

// ---------------------------
// Run all test files per package
// ---------------------------
async function runTests() {
  for (const [pkg, files] of Object.entries(config.packages || {})) {
    console.log(`\n=== Running tests for package: ${pkg} ===`);

    // Launch backend requirements if defined
    const reqConfig = config.requirements?.[pkg];
    const backends = [];

    if (reqConfig && reqConfig.files?.length) {
      const { files: reqFiles, metadata = {} } = reqConfig;

      for (const reqFile of reqFiles) {
        const isPython = metadata.python === true;
        const reqPath = isPython ? reqFile.replace(".py", "").replace("/", ".") : path.resolve(reqFile);
        const command = isPython ? "python -m" : "node";

        console.log(`🚀 Starting backend (${isPython ? "Python" : "Node"}): ${reqPath}`);
        const backend = startProcess(command, [reqPath]);
        backends.push(backend);

        // Give backend a moment to start
        await new Promise((r) => setTimeout(r, 3000));
      }
    }

    // Run all test files for this package
    for (const file of files) {
      const testPath = path.resolve(file);
      console.log(`\n▶️  Executing: ${testPath}`);

      await new Promise((resolve, reject) => {
        const child = startProcess("npx mocha", [testPath]);
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

    // Kill backends after tests finish
    for (const backend of backends) {
      console.log("🧹 Stopping backend...");
      backend.kill("SIGTERM");
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
