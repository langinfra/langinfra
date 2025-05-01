---
title: Deploy Langinfra on Kubernetes
slug: /deployment-kubernetes
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This guide demonstrates deploying Langinfra on a Kubernetes cluster.

Two charts are available at the [Langinfra Helm Charts repository](https://github.com/langinfra/langinfra-helm-charts):

- Deploy the [Langinfra IDE](#deploy-the-langinfra-ide) for the complete Langinfra development environment.
- Deploy the [Langinfra runtime](#deploy-the-langinfra-runtime) to deploy a standalone Langinfra application in a more secure and stable environment.

## Deploy the Langinfra IDE

The Langinfra IDE deployment is a complete environment for developers to create, test, and debug their flows. It includes both the API and the UI.

The `langinfra-ide` Helm chart is available in the [Langinfra Helm Charts repository](https://github.com/langinfra/langinfra-helm-charts/tree/main/charts/langinfra-ide).

### Prerequisites

- A [Kubernetes](https://kubernetes.io/docs/setup/) cluster
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
- [Helm](https://helm.sh/docs/intro/install/)

### Prepare a Kubernetes cluster

This example uses [Minikube](https://minikube.sigs.k8s.io/docs/start/), but you can use any Kubernetes cluster.

1. Create a Kubernetes cluster on Minikube.

	```text
	minikube start
	```

2. Set `kubectl` to use Minikube.

	```text
	kubectl config use-context minikube
	```

### Install the Langinfra IDE Helm chart

1. Add the repository to Helm and update it.

	```text
	helm repo add langinfra https://langinfra.github.io/langinfra-helm-charts
	helm repo update
	```

2. Install Langinfra with the default options in the `langinfra` namespace.

	```text
	helm install langinfra-ide langinfra/langinfra-ide -n langinfra --create-namespace
	```

3. Check the status of the pods

	```text
	kubectl get pods -n langinfra
	```


	```text
	NAME                                 READY   STATUS    RESTARTS       AGE
	langinfra-0                           1/1     Running   0              33s
	langinfra-frontend-5d9c558dbb-g7tc9   1/1     Running   0              38s
	```


### Configure port forwarding to access Langinfra

Enable local port forwarding to access Langinfra from your local machine.

1. To make the Langinfra API accessible from your local machine at port 7860:
```text
kubectl port-forward -n langinfra svc/langinfra-service-backend 7860:7860
```

2. To make the Langinfra UI accessible from your local machine at port 8080:
```text
kubectl port-forward -n langinfra svc/langinfra-service 8080:8080
```

Now you can access:
- The Langinfra API at `http://localhost:7860`
- The Langinfra UI at `http://localhost:8080`


### Configure the Langinfra version

Langinfra is deployed with the `latest` version by default.

To specify a different Langinfra version, set the `langinfra.backend.image.tag` and `langinfra.frontend.image.tag` values in the [values.yaml](https://github.com/langinfra/langinfra-helm-charts/blob/main/charts/langinfra-ide/values.yaml) file.


```yaml
langinfra:
  backend:
    image:
      tag: "1.0.0a59"
  frontend:
    image:
      tag: "1.0.0a59"

```


### Configure external storage

By default, the chart deploys a SQLite database stored in a local persistent disk.
If you want to use an external PostgreSQL database, you can configure it in two ways:

* Use the built-in PostgreSQL chart:
```yaml
postgresql:
  enabled: true
  auth:
    username: "langinfra"
    password: "langinfra-postgres"
    database: "langinfra-db"
```

* Use an external database:
```yaml
postgresql:
  enabled: false

langinfra:
  backend:
    externalDatabase:
      enabled: true
      driver:
        value: "postgresql"
      port:
        value: "5432"
      user:
        value: "langinfra"
      password:
        valueFrom:
          secretKeyRef:
            key: "password"
            name: "your-secret-name"
      database:
        value: "langinfra-db"
    sqlite:
      enabled: false
```


### Configure scaling

Scale the number of replicas and resources for both frontend and backend services:

```yaml
langinfra:
  backend:
    replicaCount: 1
    resources:
      requests:
        cpu: 0.5
        memory: 1Gi
      # limits:
      #   cpu: 0.5
      #   memory: 1Gi

  frontend:
    enabled: true
    replicaCount: 1
    resources:
      requests:
        cpu: 0.3
        memory: 512Mi
      # limits:
      #   cpu: 0.3
      #   memory: 512Mi
```

## Deploy the Langinfra runtime

The runtime chart is tailored for deploying applications in a production environment. It is focused on stability, performance, isolation, and security to ensure that applications run reliably and efficiently.

The `langinfra-runtime` Helm chart is available in the [Langinfra Helm Charts repository](https://github.com/langinfra/langinfra-helm-charts/tree/main/charts/langinfra-runtime).

:::important
By default, the [Langinfra runtime Helm chart](https://github.com/langinfra/langinfra-helm-charts/blob/main/charts/langinfra-runtime/values.yaml#L46) enables `readOnlyRootFilesystem: true` as a security best practice. This setting prevents modifications to the container's root filesystem at runtime, which is a recommended security measure in production environments.

Disabling `readOnlyRootFilesystem` reduces the security of your deployment. Only disable this setting if you understand the security implications and have implemented other security measures.

For more information, see the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/).
:::

### Prerequisites

- A [Kubernetes](https://kubernetes.io/docs/setup/) server
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
- [Helm](https://helm.sh/docs/intro/install/)

### Install the Langinfra runtime Helm chart

1. Add the repository to Helm.

```shell
helm repo add langinfra https://langinfra.github.io/langinfra-helm-charts
helm repo update
```

2. Install the Langinfra app with the default options in the `langinfra` namespace.

If you have a created a [custom image with packaged flows](/deployment-docker#package-your-flow-as-a-docker-image), you can deploy Langinfra by overriding the default [values.yaml](https://github.com/langinfra/langinfra-helm-charts/blob/main/charts/langinfra-runtime/values.yaml) file with the `--set` flag.

* Use a custom image with bundled flows:
```shell
helm install my-langinfra-app langinfra/langinfra-runtime -n langinfra --create-namespace --set image.repository=myuser/langinfra-hello-world --set image.tag=1.0.0
```

* Alternatively, install the chart and download the flows from a URL with the `--set` flag:
```shell
helm install my-langinfra-app-with-flow langinfra/langinfra-runtime \
  -n langinfra \
  --create-namespace \
  --set 'downloadFlows.flows[0].url=https://raw.githubusercontent.com/langinfra/langinfra/dev/tests/data/basic_example.json'
```

:::important
You may need to escape the square brackets in this command if you are using a shell that requires it:
```shell
helm install my-langinfra-app-with-flow langinfra/langinfra-runtime \
  -n langinfra \
  --create-namespace \
  --set 'downloadFlows.flows\[0\].url=https://raw.githubusercontent.com/langinfra/langinfra/dev/tests/data/basic_example.json'
```
:::

3. Check the status of the pods.
```shell
kubectl get pods -n langinfra
```

### Access the Langinfra app API

1. Get your service name.
```shell
kubectl get svc -n langinfra
```

The service name is your release name followed by `-langinfra-runtime`. For example, if you used `helm install my-langinfra-app-with-flow` the service name is `my-langinfra-app-with-flow-langinfra-runtime`.

2. Enable port forwarding to access Langinfra from your local machine:

```shell
kubectl port-forward -n langinfra svc/my-langinfra-app-with-flow-langinfra-runtime 7860:7860
```

3. Confirm you can access the API at `http://localhost:7860/api/v1/flows/` and view a list of flows.
```shell
curl -v http://localhost:7860/api/v1/flows/
```

4. Execute the packaged flow.

The following command gets the first flow ID from the flows list and runs the flow.

```shell
# Get flow ID
id=$(curl -s "http://localhost:7860/api/v1/flows/" | jq -r '.[0].id')

# Run flow
curl -X POST \
    "http://localhost:7860/api/v1/run/$id?stream=false" \
    -H 'Content-Type: application/json' \
    -d '{
      "input_value": "Hello!",
      "output_type": "chat",
      "input_type": "chat"
    }'
```

### Configure secrets

To inject secrets and Langinfra global variables, use the `secrets` and `env` sections in the [values.yaml](https://github.com/langinfra/langinfra-helm-charts/blob/main/charts/langinfra-runtime/values.yaml) file.

For example, the [example flow JSON](https://raw.githubusercontent.com/langinfra/langinfra-helm-charts/refs/heads/main/examples/flows/basic-prompting-hello-world.json) uses a global variable that is a secret. When you export the flow as JSON, it's recommended to not include the secret.

Instead, when importing the flow in the Langinfra runtime, you can set the global variable in one of the following ways:

<Tabs>
<TabItem value="values" label="Using values.yaml">

```yaml
env:
  - name: openai_key_var
    valueFrom:
      secretKeyRef:
        name: openai-key
        key: openai-key
```

Or directly in the values file (not recommended for secret values):

```yaml
env:
  - name: openai_key_var
    value: "sk-...."
```

</TabItem>
<TabItem value="helm" label="Using Helm Commands">

1. Create the secret:
```shell
kubectl create secret generic openai-credentials \
  --namespace langinfra \
  --from-literal=OPENAI_API_KEY=sk...
```

2. Verify the secret exists. The result is encrypted.
```shell
kubectl get secrets -n langinfra openai-credentials
```

3. Upgrade the Helm release to use the secret.
```shell
helm upgrade my-langinfra-app-image langinfra/langinfra-runtime -n langinfra \
  --reuse-values \
  --set "extraEnv[0].name=OPENAI_API_KEY" \
  --set "extraEnv[0].valueFrom.secretKeyRef.name=openai-credentials" \
  --set "extraEnv[0].valueFrom.secretKeyRef.key=OPENAI_API_KEY"
```

</TabItem>
</Tabs>

### Configure the log level

Set the log level and other Langinfra configurations in the [values.yaml](https://github.com/langinfra/langinfra-helm-charts/blob/main/charts/langinfra-runtime/values.yaml) file.

```yaml
env:
  - name: LANGINFRA_LOG_LEVEL
    value: "INFO"
```

### Configure scaling

To scale the number of replicas for the Langinfra appplication, change the `replicaCount` value in the [values.yaml](https://github.com/langinfra/langinfra-helm-charts/blob/main/charts/langinfra-runtime/values.yaml) file.

```yaml
replicaCount: 3
```

To scale the application vertically by increasing the resources for the pods, change the `resources` values in the [values.yaml](https://github.com/langinfra/langinfra-helm-charts/blob/main/charts/langinfra-runtime/values.yaml) file.


```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
```

## Deploy Langinfra on AWS EKS, Google GKE, or Azure AKS and other examples

For more information, see the [Langinfra Helm Charts repository](https://github.com/langinfra/langinfra-helm-charts).


