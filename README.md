# NBA Prediction

The recommendation system of [UDN NBA Fantasy](https://nba.udn.com/fantasy/fantasy) game.

## Auto Formatting

```bash
# Install isort.
pip install isort

# Automatically re-format your imports with isort.
isort --settings-path .github/linters/tox.ini ./src
```

# Quick Start
## Installation
1. Clone this repo.

    `git clone https://github.com/kyu-kuanwei/nba_prediction.git`
2. Create and activate the virtual environment.

    `python3 -m venv .nba_env`

    `source .nba_env/bin/activate`
3. Install required environments.

     `pip3 install -r requirements.txt`
4. Create `.env` file with the credential information.

    The file should contains
    - EXECUTABLE_PATH: Chrome driver path.
    - FACEBOOK_ACCOUNT: Facebook account to login UDN NBA Fantasy.
    - FACEBOOK_PASSWORD: Facebook password.
    - WEB_HOOK_KEY: To enable line notification.
    - PROJECT_PATH: Current project path.

    The format would be like
    ```
    EXECUTABLE_PATH=/usr/xxx
    FACEBOOK_ACCOUNT=kkkkk@gmail.com
    FACEBOOK_PASSWORD=11111
    WEB_HOOK_KEY=abcdefg
    PROJECT_PATH=/Users
    ```
5. Run the `main.py` script.

    `python3 main.py`