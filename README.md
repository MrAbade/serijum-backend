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
 - run:
```zsh
gunicorn --bind 0.0.0.0:5000 app
```

### Have a nice experience with Serijum Server 😁😉