# Server Component

Deploy with docker: `docker-compose up`. (Binds to localhost:80).

# API

## `/api/user`

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
