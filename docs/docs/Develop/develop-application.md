---
title: Develop an application in Langinfra
slug: /develop-application
---

Follow this guide to learn how to build an application using Langinfra.
You'll learn how to set up a project directory, manage dependencies, configure environment variables, and package your Langinfra application in a Docker image.

To deploy your application to Docker or Kubernetes, see [Deployment](/deployment-docker).

## Create a project directory

Create a project directory similar to this one.

```text
LANGINFRA-APPLICATION/
├── flows/
│   ├── flow1.json
│   └── flow2.json
├── langinfra-config-dir/
├── docker.env
├── Dockerfile
├── README.md
```

The `/flows` folder holds the flows you want to host.

The `langinfra-config-dir` is referenced in the Dockerfile as the location for Langinfra's configuration files, database, and logs. For more information, see [Environment variables](/environment-variables).

The `docker.env` file is copied to the Docker image as a `.env` file in the container root. This file controls Langinfra's behavior, holds secrets, and configures runtime settings like authentication, database storage, API keys, and server configurations.

The `Dockerfile` controls how your image is built. This file copies your flows and `docker.env` files to your image.

### Package management

The base Docker image includes the Langinfra core dependencies by using `langinfra/langinfra:latest` as the parent image.

If your application requires additional dependencies, create a `pyproject.toml` file and add the dependencies to the file. For more information, see [Install custom dependencies](/install-custom-dependencies).

To deploy the application with the additional dependencies to Docker, copy the `pyproject.toml` and `uv.lock` files to the Docker image by adding the following to the Dockerfile.

```text
COPY pyproject.toml uv.lock /app/
```

## Environment variables

The `docker.env` file is a `.env` file loaded into your Docker image.

The following example `docker.env` file defines auto-login behavior and which port to expose. Your environment may vary. For more information, see [Environment variables](/environment-variables).

```text
LANGINFRA_AUTO_LOGIN=true
LANGINFRA_SAVE_DB_IN_CONFIG_DIR=true
LANGINFRA_BASE_URL=http://0.0.0.0:7860
OPENAI_API_KEY=sk-...
```

This example uses Langinfra's default [SQLite](https://www.sqlite.org/) database for storage, and configures no authentication.

To modify Langinfra's default memory behavior, see [Memory](/memory).

To add authentication to your server, see [Authentication](/configuration-authentication).

## Add flows and components

Add your flow's `.JSON` files to the `/flows` folder.

To export your flows from Langinfra, see [Flows](/concepts-flows).

Optionally, add any custom components to a `/components` folder, and specify the path in your `docker.env`.

## Package your Langinfra project in a Docker image

1. Add the following commands to your Dockerfile.

```dockerfile
# Use the latest version of langinfra
FROM langinfra/langinfra:latest

# Create accessible folders and set the working directory in the container
RUN mkdir /app/flows
RUN mkdir /app/langinfra-config-dir
WORKDIR /app

# Copy the flows, optional components, and langinfra-config-dir folders to the container
COPY flows /app/flows
COPY components /app/components
COPY langinfra-config-dir /app/langinfra-config-dir

# copy docker.env file
COPY docker.env /app/.env

# Set environment variables
ENV PYTHONPATH=/app
ENV LANGINFRA_LOAD_FLOWS_PATH=/app/flows
ENV LANGINFRA_CONFIG_DIR=/app/langinfra-config-dir
ENV LANGINFRA_COMPONENTS_PATH=/app/components
ENV LANGINFRA_LOG_ENV=container

# Command to run the server
EXPOSE 7860
CMD ["langinfra", "run", "--backend-only", "--env-file","/app/.env","--host", "0.0.0.0", "--port", "7860"]
```

The environment variables set in the Dockerfile specify resource paths and allow Langinfra to access them. Values from `docker.env` override the values set in the Dockerfile. Additionally, logging behavior is set here with `ENV LANGINFRA_LOG_ENV=container` for serialized JSON to `stdout`, for tracking your application's behavior in a containerized environment. For more information on configuring logs, see [Logging](/logging).

:::note
Optionally, remove the `--backend-only` flag from the startup command to start Langinfra with the frontend enabled.
For more on `--backend-only` mode and the Langinfra Docker image, see [Docker](/deployment-docker).
:::

2. Save your Dockerfile.
3. Build the Docker image:
```bash
docker build -t langinfra-pokedex:1.2.0 .
```
4. Run the Docker container:
```bash
docker run -p 7860:7860 langinfra-pokedex:1.2.0
```

:::note
For instructions on building and pushing your image to Docker Hub, see [Docker](/deployment-docker).
:::

5. Confirm the server is serving your flows.
Open a `.JSON` file in your `/flows` folder and find the file's `id` value. It's the first value in the flow document.

```json
"id": "e4167236-938f-4aca-845b-21de3f399858",
```

6. Add the file's `id` value as the `flow-id` to a POST request to the `/run` endpoint.

This command also uses a custom `session_id` value of `charizard_test_request`.
By default, session IDs use the `flow-id` value.
A custom session ID maintains a unique conversation thread, which keeps LLM contexts clean and can make debugging easier.
For more information, see [Session ID](/session-id).

```bash
curl --request POST \
  --url 'http://127.0.0.1:7860/api/v1/run/e4167236-938f-4aca-845b-21de3f399858?stream=false' \
  --header 'Content-Type: application/json' \
  --data '{
    "input_value": "Tell me about Charizard please",
    "output_type": "chat",
    "input_type": "chat",
    "session_id": "charizard_test_request"
}'
```

If the flow streams the result back to you, your flow is being served, and can be consumed from a front-end application by submitting POST requests to this endpoint.

To trigger your application from an external event, see [Webhook](/webhook).

:::note
The test application returns a large amount of text, so the example command used `?stream=true`. If you prefer, set `?stream=false` to use batching. For more information, see the [API examples](/api-reference-api-examples#run-flow).
:::

## Deploy to Docker Hub and Kubernetes

For instructions on building and pushing your image to Docker Hub, see [Docker](/deployment-docker).

To deploy your application to Kubernetes, see [Kubernetes](/deployment-kubernetes).