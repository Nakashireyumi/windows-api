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
2. Installing and setting up the environment
<br>This requires [vcpkg](https://vcpkg.io/en/), [gcc](https://gcc.gnu.org/), and [python](https://www.python.org/).
```cmd
cd windows-api

vcpkg install yaml-cpp nlohmann-json
pip install venv # If not already installed

# Activating the python venv
python -m venv .venv
cd .venv/Scripts/
activate
cd ../..

pip install -r src/contributions/cassitly/python/requirements.txt
deactivate

# Lanuching the client
g++ -std=c++17 -I"your-vcpkg-path/packages/yaml-cpp_x64-windows/include/yaml-cpp" src/global/niwatori/launch-applications.cpp -L"your-vcpkg-path/packages/yaml-cpp_x64-windows/lib" -lyaml-cpp -o launch-applications
launch-applications
```
If you're on windows, use this command
```cmd
g++ -std=c++17 -I"your-vcpkg-path/packages/yaml-cpp_x64-windows/include/yaml-cpp" src/global/niwatori/launch-applications.cpp -L"your-vcpkg-path/packages/yaml-cpp_x64-windows/lib" -static -lstdc++fs -lyaml-cpp -o launch-applications
```
instead of
```cmd
g++ -std=c++17 -I"your-vcpkg-path/packages/yaml-cpp_x64-windows/include/yaml-cpp" src/global/niwatori/launch-applications.cpp -L"your-vcpkg-path/packages/yaml-cpp_x64-windows/lib" -lyaml-cpp -o launch-applications
```
<br>Now windows-api's websocket should be running. You can test it by running the [example gui client](./src/contributions/cassitly/python/examples/gui-client)
<br>Fair warning tho, it will execute actions using your mouse and keyboard.
