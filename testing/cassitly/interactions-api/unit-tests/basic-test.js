// test/cassitly/interactions-api/unit-tests/basic-test.js
// This file path is for vibe coders lol

const WebSocket = require("ws");
const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");
const { expect } = require("chai");

// ---------------------------
// Load configuration dynamically
// ---------------------------
const CONFIG_PATH = path.resolve("src/resources/gui/config/authentication.yaml");

let cfg = {
  host: "127.0.0.1",
  port: 8765,
  auth_token: "replace-with-a-strong-secret",
};

if (fs.existsSync(CONFIG_PATH)) {
  try {
    const file = fs.readFileSync(CONFIG_PATH, "utf8");
    cfg = { ...cfg, ...yaml.load(file) };
  } catch (err) {
    console.warn("⚠️ Failed to load config.yaml, using defaults:", err);
  }
}

const HOST = cfg.host;
const PORT = cfg.port;
const TOKEN = cfg.auth_token;
const WS_URL = `ws://${HOST}:${PORT}`;

// ---------------------------
// Utility to send & receive messages
// ---------------------------
function send(ws, obj) {
  return new Promise((resolve, reject) => {
    ws.once("message", (data) => {
      try {
        resolve(JSON.parse(data));
      } catch (err) {
        reject(err);
      }
    });
    ws.send(JSON.stringify(obj));
  });
}

// ---------------------------
// Tests
// ---------------------------
describe("Python GUI WebSocket Server", () => {
  let ws;

  before(async () => {
    await new Promise((r) => setTimeout(r, 500));
    ws = new WebSocket(WS_URL);
    await new Promise((resolve, reject) => {
      ws.on("open", resolve);
      ws.on("error", reject);
    });
  });

  after(() => {
    ws.close();
  });

  it("rejects unauthorized messages", async () => {
    const res = await send(ws, { action: "reload", token: "wrong" });
    expect(res.status).to.equal("error");
    expect(res.error.message).to.equal("unauthorized");
  });

  it("rejects invalid JSON", async () => {
    await new Promise((resolve) => {
      ws.once("message", (msg) => {
        const res = JSON.parse(msg);
        expect(res.status).to.equal("error");
        expect(res.error.message).to.equal("invalid_json");
        resolve();
      });
      ws.send("{ invalid_json");
    });
  });

  it("reload action works", async () => {
    const res = await send(ws, { action: "reload", token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.message).to.equal("Handlers reloaded");
    expect(typeof res.result.count).to.equal("number");
  });

  it("unsupported action gives proper error", async () => {
    const res = await send(ws, { action: "nonexistent", token: TOKEN });
    expect(res.status).to.equal("error");
    expect(res.error.message).to.equal("unsupported_action");
  });

  it("invalid action type (non-string) rejected", async () => {
    const res = await send(ws, { action: 1234, token: TOKEN });
    expect(res.status).to.equal("error");
    expect(res.error.message).to.equal("invalid_action");
  });
});
