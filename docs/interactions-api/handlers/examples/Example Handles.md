# Handle Examples
This page contains the examples for the interaction-api's expected websocket input. Linked with their respective filenames.
Also to note, all handles expect the following:
```json
{ "token": "your set auth token", "action": "the desired action to run (define its action name)", (The parameters for the specific handle goes here) }
```

## Available handles
These are the available handles<br><br>
[``handlers/click.py``](../../../../src/contributions/cassitly/interactions-api/handlers/click.py)
```json
{ "x": 0, "y": 1, "button": "left|right|middle" }
```

[``move.py``](../../../../src/contributions/cassitly/interactions-api/handlers/move.py)
```json
{ "x": 0, "y": 1 }
```