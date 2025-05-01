---
title: Deploy Langinfra on Docker
slug: /deployment-docker
---

This guide demonstrates deploying Langinfra with Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Clone the repo and build the Langinfra Docker container

1. Clone the Langinfra repository:

   `git clone https://github.com/langinfra/langinfra.git`

2. Navigate to the `docker_example` directory:

   `cd langinfra/docker_example`

3. Run the Docker Compose file:

   `docker compose up`

Langinfra is now accessible at `http://localhost:7860/`.

## Configure Docker services

The Docker Compose configuration spins up two services: `langinfra` and `postgres`.

To configure values for these services at container startup, include them in your `.env` file.

An example `.env` file is available in the [project repository](https://github.com/langinfra/langinfra/blob/main/.env.example).

To pass the `.env` values at container startup, include the flag in your `docker run` command:

```
docker run -it --rm \
    -p 7860:7860 \
    --env-file .env \
    langinfra/langinfra:latest
```

### Langinfra service

The `langinfra`service serves both the backend API and frontend UI of the Langinfra web application.

The `langinfra` service uses the `langinfra/langinfra:latest` Docker image and exposes port `7860`. It depends on the `postgres` service.

Environment variables:

- `LANGINFRA_DATABASE_URL`: The connection string for the PostgreSQL database.
- `LANGINFRA_CONFIG_DIR`: The directory where Langinfra stores logs, file storage, monitor data, and secret keys.

Volumes:

- `langinfra-data`: This volume is mapped to `/app/langinfra` in the container.

### PostgreSQL service

The `postgres` service is a database that stores Langinfra's persistent data including flows, users, and settings.

The service runs on port 5432 and includes a dedicated volume for data storage.

The `postgres` service uses the `postgres:16` Docker image.

Environment variables:

- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
- `POSTGRES_DB`: The name of the PostgreSQL database.

Volumes:

- `langinfra-postgres`: This volume is mapped to `/var/lib/postgresql/data` in the container.

### Deploy a specific Langinfra version with Docker Compose

If you want to deploy a specific version of Langinfra, you can modify the `image` field under the `langinfra` service in the Docker Compose file. For example, to use version `1.0-alpha`, change `langinfra/langinfra:latest` to `langinfra/langinfra:1.0-alpha`.

## Package your flow as a Docker image

You can include your Langinfra flow with the application image.
When you build the image, your saved flow `.JSON` flow is included.
This enables you to serve a flow from a container, push the image to Docker Hub, and deploy on Kubernetes.

An example flow is available in the [Langinfra Helm Charts](https://github.com/langinfra/langinfra-helm-charts/tree/main/examples/flows) repository, or you can provide your own `JSON` file.

1. Create a project directory:

```bash
mkdir langinfra-custom && cd langinfra-custom
```

2. Download the example flow or include your flow's `.JSON` file in the `langinfra-custom` directory.

```bash
wget https://raw.githubusercontent.com/langinfra/langinfra-helm-charts/refs/heads/main/examples/flows/basic-prompting-hello-world.json
```

3. Create a Dockerfile:

```dockerfile
FROM langinfra/langinfra-backend:latest
RUN mkdir /app/flows
COPY ./*json /app/flows/.
ENV LANGINFRA_LOAD_FLOWS_PATH=/app/flows
```

The `COPY ./*json` command copies all JSON files in your current directory to the `/flows` folder.

The `ENV LANGINFRA_LOAD_FLOWS_PATH=/app/flows` command sets the environment variable within the Docker container. By pointing it to `/app/flows`, you ensure that the application can find and utilize the JSON flow files that have been copied into that directory during the image build process.

4. Build and run the image locally.

```bash
docker build -t myuser/langinfra-hello-world:1.0.0 .
docker run -p 7860:7860 myuser/langinfra-hello-world:1.0.0
```

5. Build and push the image to Docker Hub.
   Replace `myuser` with your Docker Hub username.

```bash
docker build -t myuser/langinfra-hello-world:1.0.0 .
docker push myuser/langinfra-hello-world:1.0.0
```

To deploy the image with Helm, see [Langinfra runtime deployment](/deployment-kubernetes#deploy-the-langinfra-runtime).

## Customize the Langinfra Docker image with your own code

You can customize the Langinfra Docker image by adding your own code or modifying existing components.

This example Dockerfile demonstrates how to customize Langinfra by replacing the `astradb_graph.py` component, but the pattern can be adapted for any other components or custom code.

```dockerfile
FROM langinfra/langinfra:latest
# Set working directory
WORKDIR /app
# Copy your modified astradb_graph.py file
COPY src/backend/base/langinfra/components/vectorstores/astradb_graph.py /tmp/astradb_graph.py
# Find the site-packages directory where langinfra is installed
RUN python -c "import site; print(site.getsitepackages()[0])" > /tmp/site_packages.txt
# Replace the file in the site-packages location
RUN SITE_PACKAGES=$(cat /tmp/site_packages.txt) && \
    echo "Site packages at: $SITE_PACKAGES" && \
    mkdir -p "$SITE_PACKAGES/langinfra/components/vectorstores" && \
    cp /tmp/astradb_graph.py "$SITE_PACKAGES/langinfra/components/vectorstores/"
# Clear Python cache in the site-packages directory only
RUN SITE_PACKAGES=$(cat /tmp/site_packages.txt) && \
    find "$SITE_PACKAGES" -name "*.pyc" -delete && \
    find "$SITE_PACKAGES" -name "__pycache__" -type d -exec rm -rf {} +
# Expose the default Langinfra port
EXPOSE 7860
# Command to run Langinfra
CMD ["python", "-m", "langinfra", "run", "--host", "0.0.0.0", "--port", "7860"]
```

To use this custom Dockerfile, do the following:

1. Create a directory for your custom Langinfra setup:
```bash
mkdir langinfra-custom && cd langinfra-custom
```

2. Create the necessary directory structure for your custom code.
In this example, Langinfra expects `astradb_graph.py` to exist in the `/vectorstores` directory, so you create a directory in that location.
```bash
mkdir -p src/backend/base/langinfra/components/vectorstores
```

3. Place your modified `astradb_graph.py` file in the `/vectorstores` directory.

4. Create a new file named `Dockerfile` in your `langinfra-custom` directory, and then copy the Dockerfile contents shown above into it.

5. Build and run the image:
```bash
docker build -t myuser/langinfra-custom:1.0.0 .
docker run -p 7860:7860 myuser/langinfra-custom:1.0.0
```

This approach can be adapted for any other components or custom code you want to add to Langinfra by modifying the file paths and component names.
