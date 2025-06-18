# Lightspeed-stack service installation on macOS

## Prerequisities

- brew
- git
- Python 3.11 or 3.12
- pip

## Installation steps

1. `brew install pdm`
1. `pdm --version` -- should return no error
1. Clone the repo to the current dir:
`git clone https://github.com/lightspeed-core/lightspeed-stack`
1. `cd service`
1. `pdm info` -- should return no error
1. `pdm install` -- if it fails (for example because you ran `pdm install` before changing `pyproject.toml`) run:
```sh
pdm update
pdm install
```

