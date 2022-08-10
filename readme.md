# Portty
[![Actions Status](https://github.com/sahilkhanna/sp-ui-tool/workflows/Build%20and%20Test/badge.svg)](https://github.com/sahilkhanna/sp-ui-tool/actions)
[![GitHub release](https://img.shields.io/github/release/sahilkhanna/sp-ui-tool.svg)](https://github.com/sahilkhanna/sp-ui-tool/releases/)
[![GitHub license](https://img.shields.io/github/license/sahilkhanna/sp-ui-tool.svg)](https://github.com/sahilkhanna/sp-ui-tool/blob/master/LICENSE)
[![GitHub branches](https://badgen.net/github/branches/sahilkhanna/sp-ui-tool)](https://github.com/sahilkhanna/sp-ui-tool/)

__Serial Port Gui Tool__

![Porty](docs/porty.png?raw=true "Porty")

## Setup

Create Virtual environment

```
python -m venv .venv
```

Activate virtual environment

```
.\.venv\Scripts\Activate.ps1
```

```
pip install -r requirements.txt
```

## Running the software

```
python entry.py
```

## Create Windows distribution

Make sure to run this in the virtual environment.

```
pyinstaller --name="Portty" --noconsole --windowed --add-data "assets/logo.ico;assets" --icon assets/logo.ico --onefile entry.py  
```
