# Serijum Backend Project

## How can i run this project?

 - Create a virtual envirornment
```zsh
python -m venv venv
```

 - Enter into the virtual envirornment

```zsh
source venv/bin/activate
```

 - Install all dependencies
```zsh
pip install -r requirements.txt
```

 - Initialize migrations folder | 
__OBS: make sure you have postgres running into your system__

```zsh
flask db init
```

 - Get all migrations from models
```zsh
flask db migrate
```

 - Run all migrations
```zsh
flask db upgrade

```
 - Run server
```zsh
gunicorn --bind 0.0.0.0:5000 app
```

## Available routes

### Have a nice experience with Serijum Server 😁😉

