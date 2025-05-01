---
title: Configure an external PostgreSQL database
slug: /configuration-custom-database
---
Langinfra's default database is [SQLite](https://www.sqlite.org/docs.html), but you can configure Langinfra to use PostgreSQL instead.

This guide walks you through setting up an external database for Langinfra by replacing the default SQLite connection string `sqlite:///./langinfra.db` with PostgreSQL.

## Prerequisite

* A [PostgreSQL](https://www.pgadmin.org/download/) database

## Connect Langinfra to PostgreSQL

To connect Langinfra to PostgreSQL, follow these steps.

1. Find your PostgreSQL database's connection string.
It looks like `postgresql://user:password@host:port/dbname`.

The hostname in your connection string depends on how you're running PostgreSQL.
- If you're running PostgreSQL directly on your machine, use `localhost`.
- If you're running PostgreSQL in Docker Compose, use the service name, such as `postgres`.
- If you're running PostgreSQL in a separate Docker container with `docker run`, use the container's IP address or network alias.

2. Create a `.env` file for configuring Langinfra.
```
touch .env
```

3. To set the database URL environment variable, add it to your `.env` file:
```text
LANGINFRA_DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

:::tip
The Langinfra project includes a [`.env.example`](https://github.com/langinfra/langinfra/blob/main/.env.example) file to help you get started.
You can copy the contents of this file into your own `.env` file and replace the example values with your own preferred settings.
Replace the value for `LANGINFRA_DATABASE_URL` with your PostgreSQL connection string.
:::

4. Run Langinfra with the `.env` file:
```bash
uv run langinfra run --env-file .env
```

5. In Langinfra, create traffic by running a flow.
6. Inspect your PostgreSQL deployment's tables and activity.
New tables and traffic are created.

## Example Langinfra and PostgreSQL docker-compose.yml

The Langinfra project includes a [docker-compose.yml](https://github.com/langinfra/langinfra/blob/main/docker_example/docker-compose.yml) file for quick deployment with PostgreSQL.

This configuration launches Langinfra and PostgreSQL containers in the same Docker network, ensuring proper connectivity between services. It also sets up persistent volumes for both Langinfra and PostgreSQL data.

To start the services, navigate to the `/docker_example` directory, and then run `docker-compose up`.

```yaml
services:
  langinfra:
    image: langinfra/langinfra:latest    # or another version tag on https://hub.docker.com/r/langinfra/langinfra
    pull_policy: always                   # set to 'always' when using 'latest' image
    ports:
      - "7860:7860"
    depends_on:
      - postgres
    environment:
      - LANGINFRA_DATABASE_URL=postgresql://langinfra:langinfra@postgres:5432/langinfra
      # This variable defines where the logs, file storage, monitor data, and secret keys are stored.
      - LANGINFRA_CONFIG_DIR=app/langinfra
    volumes:
      - langinfra-data:/app/langinfra

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: langinfra
      POSTGRES_PASSWORD: langinfra
      POSTGRES_DB: langinfra
    ports:
      - "5432:5432"
    volumes:
      - langinfra-postgres:/var/lib/postgresql/data

volumes:
  langinfra-postgres:    # Persistent volume for PostgreSQL data
  langinfra-data:        # Persistent volume for Langinfra data
```

:::note
Docker Compose creates an isolated network for all services defined in the docker-compose.yml file. This ensures that the services can communicate with each other using their service names as hostnames, for example, `postgres` in the database URL. If you were to run PostgreSQL separately using `docker run`, it would be in a different network and Langinfra wouldn't be able to connect to it using the service name.
:::

## Deploy multiple Langinfra instances with a shared database

To configure multiple Langinfra instances that share the same PostgreSQL database, modify your `docker-compose.yml` file to include multiple Langinfra services.

Use environment variables for more centralized configuration management:

1. Update your `.env` file with values for your PostgreSQL database:
```text
POSTGRES_USER=langinfra
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=langinfra
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
LANGINFRA_CONFIG_DIR=app/langinfra
LANGINFRA_PORT_1=7860
LANGINFRA_PORT_2=7861
LANGINFRA_HOST=0.0.0.0
```
2. Reference these variables in your `docker-compose.yml`:
```yaml
services:
  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - langinfra-postgres:/var/lib/postgresql/data

  langinfra-1:
    image: langinfra/langinfra:latest
    pull_policy: always
    ports:
      - "${LANGINFRA_PORT_1}:7860"
    depends_on:
      - postgres
    environment:
      - LANGINFRA_DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
      - LANGINFRA_CONFIG_DIR=${LANGINFRA_CONFIG_DIR}
      - LANGINFRA_HOST=${LANGINFRA_HOST}
      - PORT=7860
    volumes:
      - langinfra-data-1:/app/langinfra

  langinfra-2:
    image: langinfra/langinfra:latest
    pull_policy: always
    ports:
      - "${LANGINFRA_PORT_2}:7860"
    depends_on:
      - postgres
    environment:
      - LANGINFRA_DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
      - LANGINFRA_CONFIG_DIR=${LANGINFRA_CONFIG_DIR}
      - LANGINFRA_HOST=${LANGINFRA_HOST}
      - PORT=7860
    volumes:
      - langinfra-data-2:/app/langinfra

volumes:
  langinfra-postgres:
  langinfra-data-1:
  langinfra-data-2:
```

3. Deploy the file with `docker-compose up`.
You can access the first Langinfra instance at `http://localhost:7860`, and the second Langinfra instance at `http://localhost:7861`.

4. To confirm both instances are using the same database, run the `docker exec` command to start `psql` in your PostgreSQL container.
Your container name may vary.
```bash
docker exec -it docker-test-postgres-1 psql -U langinfra -d langinfra
```

5. Query the database for active connections:
```sql
langinfra=# SELECT * FROM pg_stat_activity WHERE datname = 'langinfra';
```

6. Examine the query results for multiple connections with different `client_addr` values, for example `172.21.0.3` and `172.21.0.4`.

Since each Langinfra instance runs in its own container on the Docker network, using different incoming IP addresses confirms that both instances are actively connected to the PostgreSQL database.

7. To quit psql, type `quit`.