// testing/runner.js
import fs from "fs";
import { execSync } from "child_process";
import YAML from "yaml";
import chalk from "chalk";

// Config path
const configPath = "testing/tests.yaml";

// Color helpers
const log = {
  info: (...msg) => console.log(chalk.cyan(...msg)),
  warn: (...msg) => console.warn(chalk.yellow(...msg)),
  error: (...msg) => console.error(chalk.red(...msg)),
  success: (...msg) => console.log(chalk.green(...msg)),
};

// Check config file
if (!fs.existsSync(configPath)) {
  log.error(`❌ Config not found: ${configPath}`);
  process.exit(1);
}

// Load YAML
let config;
try {
  const file = fs.readFileSync(configPath, "utf8");
  config = YAML.parse(file);
} catch (err) {
  log.error(`❌ Failed to load YAML: ${err.message}`);
  process.exit(1);
}

// Validate tests key
if (!config.tests || typeof config.tests !== "object") {
  log.error(`❌ No valid 'tests' key in ${configPath}`);
  process.exit(1);
}

let allPassed = true;

for (const [projectName, files] of Object.entries(config.tests)) {
  console.log(`\n🚀 Running tests for: ${chalk.cyan(projectName)}`);

  if (!Array.isArray(files)) {
    log.error(`❌ Expected a list of files for project: ${projectName}`);
    allPassed = false;
    continue;
  }

  for (const filePath of files) {
    if (!fs.existsSync(filePath)) {
      log.error(`❌ File not found: ${filePath}`);
      allPassed = false;
      continue;
    }

    const cmd = `npx mocha "${filePath}"`;
    console.log(`▶️  Executing: ${chalk.yellow(cmd)}`);

    try {
      execSync(cmd, { stdio: "inherit" });
    } catch {
      log.error(`❌ Test failed in ${filePath}`);
      allPassed = false;
    }
  }
}

if (allPassed) {
  log.success("\n✅ All tests passed successfully.");
  process.exit(0);
} else {
  log.error("\n❌ Some tests failed.");
  process.exit(1);
}
