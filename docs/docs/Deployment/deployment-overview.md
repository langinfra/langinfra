---
title: Langinfra deployment overview
slug: /deployment-overview
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

You have a flow, and want to share it with the world in a production environment.

This page outlines the journey from locally-run flow to a cloud-hosted production server.

More specific instructions are available in the [Docker](/deployment-docker) and [Kubernetes](/deployment-kubernetes) pages.

## Langinfra deployment architecture

Langinfra can be deployed as an [IDE](https://github.com/langinfra/langinfra-helm-charts/tree/main/charts/langinfra-ide) or as a [runtime](https://github.com/langinfra/langinfra-helm-charts/tree/main/charts/langinfra-runtime).

The **IDE** includes the frontend for visual development of your flow. The default [docker-compose.yml](https://github.com/langinfra/langinfra/blob/main/docker_example/docker-compose.yml) file hosted in the Langinfra repository builds the Langinfra IDE image. To deploy the Langinfra IDE, see [Docker](/deployment-docker).

The **runtime** is a headless or backend-only mode. The server exposes your flow as an endpoint, and runs only the processes necessary to serve your flow, with PostgreSQL as the database for improved scalability. Use the Langinfra **runtime** to deploy your flows, because you don't require the frontend for visual development.

:::tip
You can start Langinfra in headless mode with the [LANGINFRA_BACKEND_ONLY](/environment-variables#LANGINFRA_BACKEND_ONLY) environment variable.
:::

## Package your flow with the Langinfra runtime image

To package your flow as a Docker image, copy your flow's `.JSON` file with a command in the Dockerfile.

An example [Dockerfile](https://github.com/langinfra/langinfra-helm-charts/blob/main/examples/langinfra-runtime/docker/Dockerfile) for bundling flows is hosted in the Langinfra Helm Charts repository.

For more on building the Langinfra docker image and pushing it to Docker Hub, see [Package your flow as a docker image](/deployment-docker#package-your-flow-as-a-docker-image).

## Deploy to Kubernetes

After your flow is packaged as a Docker image and available on Docker Hub, deploy your application by overriding the values in the [langinfra-runtime](https://github.com/langinfra/langinfra-helm-charts/blob/main/charts/langinfra-runtime/Chart.yaml) Helm chart.

For more information, see [Deploy Langinfra on Kubernetes](/deployment-kubernetes).





