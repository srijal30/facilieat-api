# How to Setup
- First clone the repo
```
$ git clone https://github.com/srijal30/facilieat-api.git
```
- Setup the virtual enviorment
```
$ python -m venv .venv
$ source .venv/bin/activate  # change bin to Scripts for Windows
$ python -m pip install -r requirements.txt
```
- Setup the database
```
$ prisma db push
```
- Set up .env file
    - create a file names `.env` in root directory
    - include these variables:
```
SALT=#secure string to be used as password salt
JWT=#secure string to be used as jwt key
```
# How to Run
- Activate the virtual enviorment 
```
$ source .venv/bin/activate  # change bin to Scripts for Windows
```
- Start the server
```
$ python main.py
```

# Endpoints
All the endpoints with their expected request/response format.

**Notes:**
- All requests will have the following base format:
```json
{
    "success": boolean,
    "message": String, 
    "data": Map
}
```
- If an error occurs while processing the response, `success` will be `false`. The error message will be in `message`.
- If a particular request has response data, you can access it through the `data` key.
- Typing is very important. If the types are off, then the server will return an error.
- Some keys are listed as optional because the server assumes a default value. If the default value is not the what you want, then make sure to override it in your request.
- If an endpoint requires authentication, include `token` in the request.

## User Account Endpoints
`user/create` <br>
To create a new user

**Request**
```json
{
    "email": String,
    "phone": String,
    "password": String,
    "firstName": String,
    "lastName": String,
    //Optional Keys
    "sendNotifications": boolean // default: true
}
```
**Response**
```
```

---

`user/login` <br>
Logs a user in

**Request:**
```json
{
    "email": String,
    "password": String
}
```
**Response:**
```json
{
    "token": String
}
```

---

`user/update` <br>
Authentication required.
Update user data.

**Request:**
```json
{
    "token": String,
    //Include the keys you want to change
}
```
**Response:**
```json
```

`user/user` <br>
Authentication required.
Gives the user data for currently logged in user.

**Request:**
```json
{
    "token": String,
}
```
**Response:**
```json
{
    "email":  String,
    "phone": String,
    "firstName": String,
    "lastName": String,
    "sendNotifications": boolean
}
```