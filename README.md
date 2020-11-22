# Serijum Backend Project

## Available routes
- Signup
```http
POST /api/v1/user/signup HTTP/1.1
Content-Type: application/json

{
    "name": "Gigle Catabriga",
    "email": "catabriga.gigle@mail.com",
    "password": "example_pass_123"
}
```

 - Login
 ```http
POST /api/v1/user/login HTTP/1.1
Content-Type: application/json

{
    "email": "janice@mail.com",
    "password": "example_pass_123"
}
 ```

 - List Suites by Categories 
```http
GET /api/v1/suite HTTP/1.1
Authorization: Bearer <jwt-token>
```

 - Find for a specific suite informations
```http
GET /api/v1/suite/<int:suite_id> HTTP/1.1
Authorization: Bearer <jwt-token>
```

 - Create a schedule for an user
```http
POST /api/v1/schedule/<int:suite_id> HTTP/1.1
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "is_overnight_stay": false,
  "date_of_overnight_stay": "2020-11-23 20-0-0",
  "entry_datetime": "2020-11-25 20-0-0",
  "exit_datetime": "2020-11-25 23-0-0"
}
```

 - List the scheduling of an user
```http
GET /api/v1/schedule HTTP/1.1
Authorization: Bearer <jwt-token>
```

<br>
<br>
<br>

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
gunicorn --bind 0.0.0.0:5000 -w 4 wsgi:app
```
