// test/cassitly/interactions-api/unit-tests/handlers-test.js
// This file path is for vibe coders lol

import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import WebSocket from "ws";

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

  beforeAll(async () => {
    // Give the Python server time to start
    await new Promise((r) => setTimeout(r, 500));
    ws = new WebSocket(WS_URL);
    await new Promise((resolve, reject) => {
      ws.on("open", resolve);
      ws.on("error", reject);
    });
  });

  afterAll(() => {
    ws.close();
  });

  // ----------- Core handler tests -----------

  test("move handler works", async () => {
    const res = await send(ws, { action: "move", x: 100, y: 150, token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.moved_to).toEqual([100, 150]);
  });

  test("click handler works", async () => {
    const res = await send(ws, { action: "click", x: 200, y: 250, button: "right", token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.clicked).toEqual([200, 250]);
    expect(res.result.button).toBe("right");
  });

  test("dragrel handler works", async () => {
    const res = await send(ws, { action: "dragrel", x: 10, y: 15, duration: 0.1, token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.dragged_rel).toEqual([10, 15]);
  });

  test("dragto handler works", async () => {
    const res = await send(ws, { action: "dragto", x: 300, y: 400, token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.dragged_to).toEqual([300, 400]);
  });

  test("scroll handler works", async () => {
    const res = await send(ws, { action: "scroll", clicks: -200, token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.scrolled).toBe(-200);
  });

  test("keydown handler works", async () => {
    const res = await send(ws, { action: "keydown", key: "a", token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.keydown).toBe("a");
  });

  test("keyup handler works", async () => {
    const res = await send(ws, { action: "keyup", key: "a", token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.keyup).toBe("a");
  });

  test("press handler works", async () => {
    const res = await send(ws, { action: "press", key: "enter", token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.pressed).toBe("enter");
  });

  test("type handler works", async () => {
    const res = await send(ws, { action: "type", text: "Hello", token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.typed).toBe("Hello");
  });

  test("screenshot handler saves file", async () => {
    const res = await send(ws, { action: "screenshot", name: "test_snap.png", token: TOKEN });
    expect(res.status).toBe("ok");
    expect(res.result.saved).toMatch(/test_snap\.png$/);
  });

  // ----------- Error case tests -----------

  test("move handler rejects missing params", async () => {
    const res = await send(ws, { action: "move", token: TOKEN });
    expect(res.status).toBe("error");
    expect(res.error.message).toBe("invalid_params");
  });

  test("dragto handler rejects missing coords", async () => {
    const res = await send(ws, { action: "dragto", token: TOKEN });
    expect(res.status).toBe("error");
    expect(res.error.message).toBe("invalid_params");
  });

  test("type handler rejects empty text", async () => {
    const res = await send(ws, { action: "type", text: "", token: TOKEN });
    expect(res.status).toBe("error");
    expect(res.error.message).toBe("No text to type");
  });
});
