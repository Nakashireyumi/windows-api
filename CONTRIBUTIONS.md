## Codebase Execution
The entire codebase is meant to be ran from the main root. Not through individual directories under your folder name.
The execution chain goes as follows:
```
┌─────────────────────────────────────────────┐
│ Top-level Application's Launcher Hook       │
└─────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│ packages.yaml — list of available packages  │
└─────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│ Language group (e.g. Python, JS, Rust, ...) │
└─────────────────────────────────────────────┘
                       │
        ┌──────────────┴───────────────┐
        ▼                              ▼
┌────────────────┐             ┌────────────────┐
│ Package A      │             │ Package B      │
│ (launcher file)│             │ (launcher file)│
└────────────────┘             └────────────────┘
        │                              │
        ▼                              ▼
┌─────────────────────────────────────────────────┐
│         Main Contributions Launcher             │
└─────────────────────────────────────────────────┘
```
This graph above, shows the execution pipeline for the windows-api, for your contribution.<br><br>
The Main Contributions Launcher, should contain and launch all of the packages in each language group.
<br><br>Right now, [resources/packages.yaml](./src/resources/packages.yaml) contains the individual package list that will be launched by the main application launcher.
But that is scheduled to be changed when more packages have been added.

## Contributions
You can either add a new package under your contributor name. Or you can contribute to the already existing packages.
<br><br>To contribute a package, your package must follow a few defined rules below:
1. They must have dynamically swappable modules
<br>Take the [interactions-api](./src/contributions/cassitly/python/interactions-api) for example, they have hotswappable handlers.
2. They must be able to be hotswapped during use (i.e. a safe reload).
3. If the package is in python, use the __main__.py file in an package folder.
4. Create a pyproject.toml file for the package, so we can install it to the source easily.
<br>You could also open an PR (Pull Request).
5. There should be a sanitized requirements.txt for your package (under your package contribution name).
<br>If your package is in python, otherwise. It's not necessary
<br>Though for nodejs, both the ``package-lock.json`` and ``package.json`` is required also.
6. Your package should contain new documentation for its usage, syntax, and any other aspect of your contribution as well.

### Adding an handle to the interactions-api
The interactions-api websocket server expects a few things from a handle.
<br>They one, expects a ``handle()`` function, with two arguments ``msg and context``.
<br>And two, an response for ``ok()`` and ``err()``, in these JSON format.
```json
{"status": "ok", "result": {"dragged_rel": [int(dx), int(dy)], "button": button}}
{"status": "error", "error": {"message": "invalid_params", "details": "Requires 'x' and 'y'"}}
```
These are examples from [dragrel.py](./src/contributions/cassitly/python/interactions-api/handlers/dragrel.py)
<br>Below, is an full working example of an handle for interactions-api (taken from [dragrel.py](./src/contributions/cassitly/python/interactions-api/handlers/dragrel.py))
```py
import pyautogui

async def handle(msg, context):
    dx = msg.get("x")
    dy = msg.get("y")
    if dx is None or dy is None:
        return {"status": "error", "error": {"message": "invalid_params", "details": "Requires 'x' and 'y'"}}
    duration = float(msg.get("duration", 0.0))
    button = msg.get("button", "left")
    pyautogui.dragRel(int(dx), int(dy), duration=duration, button=button)
    return {"status": "ok", "result": {"dragged_rel": [int(dx), int(dy)], "button": button}}
```
Your arguments will be passed in msg (by the gui-client handler), and context is an argument passed by the interactions-api itself.
<br><br>The msg argument can contain your defined arguments, they do not have to be defined by the interactions-api. They are defined by the client.
<br><br>Though, the context is defined by the websocket server (the interactions-api)