# To Build and run the server for the first time

# for a better experince install poetry with this command

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

# then create a virtual envirnment for your host to resolve the depenedencies

```bash
poetry config virtualenvs.in-project true
poetry install --no-root

```

```bash
docker compose up
```

and check http://localhost:8000/docs

# To access the pgadmin visit localhost:9001 & enter

    email:raidrockstar040@gmil.com
    password:lol
