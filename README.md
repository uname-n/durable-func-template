# durable-func-template

### prerequisites
- **pyenv**: manage python versions
    - `brew update && brew install azure-cli`
- **black**: python code formatter
    - `pip install black`
- **azureite**: local azure storage emulator
    - `npm install -g azurite`
- **azure-cli**: azure command line tool
    - `brew update && brew install azure-cli`
- **mk**: project level command orchestrator
    - `https://github.com/uname-n/mk`

### getting started
- install **prerequisites**
- install python version with **pyenv**
    - `pyenv install 3.11.6`
- create virtual environment and activate it. 
    - `python -m venv .venv`
    - `source .venv/bin/activate`
- install **requirements.txt**
    - `pip install -r requirements.txt`
- start azureite & func locally
    - `mk local` *(command can be found in mk.toml)*
