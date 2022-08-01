# Serial Port GUI Tool

Serial Port Gui Tool

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
pyinstaller --name="Porty" --noconsole --onefile entry.py
```
