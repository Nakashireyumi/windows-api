## How to post tests / unit tests
Create a folder under your github username, and then a .mjs file (or any other file), that is used to launch all your tests.
This file will have to be added to [tests.yaml](./tests.yaml).

## Requirements for unit-tests
The individual unit tests for a separate function that is supposed to be ran by github workflows, have to be added to [unit-tests.yaml](../src/resources/unit-tests.yaml).
Your main file that will be added to [tests.yaml](./tests.yaml), have to read from the [unit-tests.yaml](../src/resources/unit-tests.yaml) file, to run the tests.