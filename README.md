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
Create a new user. Accepts parameters:
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

### `/logout/<token>` [POST, DELETE]
Deletes the session. Does not return anything.


---


## `/api/app`

Manage a users recorded apps and the reasons he opened them

### `/<uri>/create` [POST]
Create a new app. Accepts parameters:
- token (string) - session token
- name (string) - name of app
- icon (string) - uri of app icon

Note on uri's: For [https://tilman.xyz](https://tilman.xyz) the uri would be
`tilman.xyz`, the icon should be `tilman.xyz/favicon.ico`. For an android app,
the uri would be `com.example.myapp`, the icon should be empty.

## `/<uri>/reason` [POST]
Add a reason to an app. Accepts:
- token (string) - session token
- reason (string) - reason
