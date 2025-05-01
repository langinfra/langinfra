# Running LangInfra with Docker

This guide will help you get LangInfra up and running using Docker and Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Steps

1. Clone the LangInfra repository:

   ```sh
   git clone https://github.com/langinfra/langinfra.git
   ```

2. Navigate to the `docker_example` directory:

   ```sh
   cd langinfra/docker_example
   ```

3. Run the Docker Compose file:

   ```sh
   docker compose up
   ```

LangInfra will now be accessible at [http://localhost:7860/](http://localhost:7860/).

## Docker Compose Configuration

The Docker Compose configuration spins up two services: `langinfra` and `postgres`.

### LangInfra Service

The `langinfra` service uses the `langinfra/langinfra:latest` Docker image and exposes port 7860. It depends on the `postgres` service.

Environment variables:

- `LANGINFRA_DATABASE_URL`: The connection string for the PostgreSQL database.
- `LANGINFRA_CONFIG_DIR`: The directory where LangInfra stores logs, file storage, monitor data, and secret keys.

Volumes:

- `langinfra-data`: This volume is mapped to `/app/langinfra` in the container.

### PostgreSQL Service

The `postgres` service uses the `postgres:16` Docker image and exposes port 5432.

Environment variables:

- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
- `POSTGRES_DB`: The name of the PostgreSQL database.

Volumes:

- `langinfra-postgres`: This volume is mapped to `/var/lib/postgresql/data` in the container.

## Switching to a Specific LangInfra Version

If you want to use a specific version of LangInfra, you can modify the `image` field under the `langinfra` service in the Docker Compose file. For example, to use version 1.0-alpha, change `langinfra/langinfra:latest` to `langinfra/langinfra:1.0-alpha`.
