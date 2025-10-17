// test/cassitly/interactions-api/unit-tests/handlers-test.js
// This file path is for vibe coders lol

const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");
const WebSocket = require("ws");
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
// Utility to send and receive JSON
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
// Handlers test suite
// ---------------------------
describe("Python GUI Handlers (via WebSocket)", () => {
  let ws;

  before(async () => {
    // Give the Python server time to start
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

  // ----------- Core handler tests -----------

  it("move handler works", async () => {
    const res = await send(ws, { action: "move", x: 100, y: 150, token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.moved_to).to.deep.equal([100, 150]);
  });

  it("click handler works", async () => {
    const res = await send(ws, { action: "click", x: 200, y: 250, button: "right", token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.clicked).to.deep.equal([200, 250]);
    expect(res.result.button).to.equal("right");
  });

  it("dragrel handler works", async () => {
    const res = await send(ws, { action: "dragrel", x: 10, y: 15, duration: 0.1, token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.dragged_rel).to.deep.equal([10, 15]);
  });

  it("dragto handler works", async () => {
    const res = await send(ws, { action: "dragto", x: 300, y: 400, token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.dragged_to).to.deep.equal([300, 400]);
  });

  it("scroll handler works", async () => {
    const res = await send(ws, { action: "scroll", clicks: -200, token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.scrolled).to.equal(-200);
  });

  it("keydown handler works", async () => {
    const res = await send(ws, { action: "keydown", key: "a", token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.keydown).to.equal("a");
  });

  it("keyup handler works", async () => {
    const res = await send(ws, { action: "keyup", key: "a", token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.keyup).to.equal("a");
  });

  it("press handler works", async () => {
    const res = await send(ws, { action: "press", key: "enter", token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.pressed).to.equal("enter");
  });

  it("type handler works", async () => {
    const res = await send(ws, { action: "type", text: "Hello", token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.typed).to.equal("Hello");
  });

  it("screenshot handler saves file", async () => {
    const res = await send(ws, { action: "screenshot", name: "test_snap.png", token: TOKEN });
    expect(res.status).to.equal("ok");
    expect(res.result.saved).to.match(/test_snap\.png$/);
  });

  // ----------- Error case tests -----------

  it("move handler rejects missing params", async () => {
    const res = await send(ws, { action: "move", token: TOKEN });
    expect(res.status).to.equal("error");
    expect(res.error.message).to.equal("invalid_params");
  });

  it("dragto handler rejects missing coords", async () => {
    const res = await send(ws, { action: "dragto", token: TOKEN });
    expect(res.status).to.equal("error");
    expect(res.error.message).to.equal("invalid_params");
  });

  it("type handler rejects empty text", async () => {
    const res = await send(ws, { action: "type", text: "", token: TOKEN });
    expect(res.status).to.equal("error");
    expect(res.error.message).to.equal("No text to type");
  });
});
