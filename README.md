# Server Component

Deploy with docker: `docker-compose up`. (Binds to localhost:80).

---

# API

## `/api/user`

User session management

### `/register` [POST]
Create a new user. Accepts parameters:
- username (string)
- password (string)

```
{
  error: bool / string,
}
```

### `/<username>/update` [POST]
Change password. Accepts parameters:
- old_password (string)
- new_password (string)

```
{
  error: bool / string,
}
```

### `/login/<app_name>` [POST]
Create a new session. Accepts parameters:
- username (string)
- password (string)

```
{
  error: bool / string,
  token: string
}
```

Note: To recycle the web-app views, it is important to login.
To automatically log in the user to the web app, there exists a
route that accepts a token and uses it to set the appropriate
cookies (if the token is valid). This route is:
`/login/<token>`, it returns 400 on error and 204 on success.

### `/login/exists` [GET]
Test if a given session is valid. Accepts parameters:
- token (string)

```
{
  error: bool / string,
  exists: bool
}
```

### `/logout/<token>` [POST, DELETE]
Deletes the session. Does not return anything.


---


## `/api/app`

Manage a users recorded apps and the reasons he opened them

### `/<uri>` [POST]
Return the given app. Accepts parameters:
- token (string) - session token

```
{
  error: bool / string
  uri: string
  name: string
  icon: string
}
```

### `/<uri>/create` [POST]
Create a new app. Accepts parameters:
- token (string) - session token
- name (string) - name of app
- icon (string) - uri of app icon

```
{
  error: bool / string
}
```

Note on uri's: For [https://tilman.xyz](https://tilman.xyz) the uri would be
`tilman.xyz`, the icon should be `tilman.xyz/favicon.ico`. For an android app,
the uri would be `com.example.myapp`, the icon should be empty.

### `/<uri>/reasons` [GET]
List reasons this app was opened
- token (string) - session token

```
{
  error: bool / string
  reasons: []
}
```

### `/<uri>/reasons/add` [POST]
Add a reason to an app. Accepts:
- token (string) - session token
- reason (string) - reason

```
{
  error: bool / string
  reply: string
}
```
