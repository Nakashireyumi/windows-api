# Windows API
Is a tool used to control windows autonomously. Built for Large Language Models (LLMs), to easily use, by converting windows user inputs into a JSON websocket message.
<br><br>The Windows API has a bunch of avaliable handlers via the interaction api (which is an package built under the windows-api to interact with windows, like a user).
View the [handlers documentation](./docs/interactions-api/handlers/Getting%20Started.md) to get started.
<br><br>If you would like a general guide on getting started with the windows API, visit [this guide here](./docs/Getting%20Started%20with%20the%20windows-api.md)

## Installation
Right now, the windows-api isn't currently ready for a full release. As it's in the alpha stage of development.
So, the only currently avaliable installation method is installing from source.
<br><br>Since the windows-api is built on multiple languages, multiple libraries and dependencies are required for building it from source.
Right now, we currently don't have a way to auto-install, setup, and bootstrap the software. All installation is required to be done manually.

### Steps to install windows-api
1. Downloading the repository
<br>For this, you will need [git](https://git-scm.com/)
```cmd
git clone https://github.com/Nakashireyumi/windows-api.git
```
2. Installing dependencies and setting up the environment
<br>This requires [vcpkg](https://vcpkg.io/en/), and [python](https://www.python.org/).
```cmd
cd windows-api

vcpkg install
pip install venv # If not already installed

# Activating the python venv
python -m venv .venv
cd .venv/Scripts/
activate
cd ../..

pip install -r src/contributions/cassitly/python/requirements.txt

# Lanuching the client
python -m src.contributions.cassitly.python.launcher
```
<br>Now windows-api's websocket should be running. You can test it by running the [example interactions client](./src/contributions/cassitly/python/examples/interactions-client)
<br>Fair warning tho, it will execute actions using your mouse and keyboard.
