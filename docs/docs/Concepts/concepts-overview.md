---
title: Langinfra overview
slug: /concepts-overview
---

import Icon from "@site/src/components/icon";

This page explores the fundamental building blocks of Langinfra, beginning with the question, **"What is a flow?"**

## What is a flow?

A **flow** is an application. It receives input, processes it, and produces output.

Flows are created in the **workspace** with components dragged from the components sidebar.

![Basic prompting flow within in the workspace](/img/workspace-basic-prompting.png)

A flow can be as simple as the [basic prompting flow](/get-started-quickstart), which creates an OpenAI chatbot with four components.

- Each component in a flow is a **node** that performs a specific task, like an AI model or a data source.
- Each component has a **Configuration** menu. Click the **Code** pane to see a component's underlying Python code.
- Components are connected with **edges** to form flows.

If you're familiar with [React Flow](https://reactflow.dev/learn), a **flow** is a node-based application, a **component** is a node, and the connections between components are **edges**.

When a flow is run, Langinfra builds a Directed Acyclic Graph (DAG) graph object from the nodes (components) and edges (connections between components), with the nodes sorted to determine the order of execution. The graph build calls the individual components' `def_build` functions to validate and prepare the nodes. This graph is then processed in dependency order. Each node is built and executed sequentially, with results from each built node being passed to nodes that are dependent on the previous node's results.

Flows are stored on local disk at these default locations:

- **Linux or WSL on Windows**: `home/<username>/.cache/langinfra/`
- **MacOS**: `/Users/<username>/Library/Caches/langinfra/`

The flow storage location can be customized with the [LANGINFRA_CONFIG_DIR](/environment-variables#LANGINFRA_CONFIG_DIR) environment variable.

## Find your way around

If you're new to Langinfra, it's OK to feel a bit lost at first. We’ll take you on a tour, so you can orient yourself and start creating applications quickly.

Langinfra has four distinct regions: the [workspace](#workspace) is the main area where you build your flows. The components sidebar is on the left, and lists the available [components](#components). The [playground](#playground) and [Publish pane](#publish-pane) are available in the upper right corner.

![](/img/workspace.png)

## Workspace

The **workspace** is where you create AI applications by connecting and running components in flows.

The workspace controls allow you to adjust your view and lock your flows in place.

- Add **Notes** to flows with the **Add Note** button, similar to commenting in code.
- To access the [Settings](#settings) menu, click <Icon name="Settings" aria-label="Gear icon" /> **Settings**.

This menu contains configuration for **Global Variables**, **Langinfra API**, **Shortcuts**, and **Messages**.

## Components

A **component** is a single building block within a flow and consists of inputs, outputs, and parameters that define its functionality.

To add a component to your flow, drag it from the sidebar onto the workspace.

To connect components, drag a line from the output handle (⚪) of one component to the input handle of another.

For more information, see [Components overview](/concepts-components).

<img src="/img/prompt-component.png" alt="Prompt component" style={{display: 'block', margin: 'auto', width: 300}} />

## Playground

The **Playground** executes the current flow in the workspace.

Chat with your flow, view inputs and outputs, and modify your AI's memories to tune your responses in real time.

Either the **Chat Input** or **Chat Output** component can be opened in the **Playground** and tested in real time.

For more information, see the [Playground](/concepts-playground).

![](/img/playground.png)

## Publish pane {#publish-pane}

The **Publish** pane provides code templates to integrate your flows into external applications.

For more information, see the [Publish pane](/concepts-publish).

![](/img/api-pane.png)

## View logs

The **Logs** pane provides a detailed record of all component executions within a workspace.

To access the **Logs** pane, click your **Flow Name**, and then select **Logs**.

![](/img/logs.png)

Langinfra stores logs at the location specified in the `LANGINFRA_CONFIG_DIR` environment variable.

This directory's default location depends on your operating system.

- **Linux/WSL**: `~/.cache/langinfra/`
- **macOS**: `/Users/<username>/Library/Caches/langinfra/`
- **Windows**: `%LOCALAPPDATA%\langinfra\langinfra\Cache`

To modify the location of your log file:

1. Add `LANGINFRA_LOG_FILE=path/to/logfile.log` in your `.env.` file.
2. To start Langinfra with the values from your `.env` file, start Langinfra with `uv run langinfra run --env-file .env`.

An example `.env` file is available in the [project repository](https://github.com/langinfra/langinfra/blob/main/.env.example).

## Projects

The **My Projects** page displays all the flows and components you've created in the Langinfra workspace.

![](/img/my-projects.png)

**My Projects** is the default project where all new projects and components are initially stored.

Projects and flows are exchanged as JSON objects.

- To create a new project, click 📁 **New Project**.

- To rename a project, double-click the project name.

- To download a project, click 📥 **Download**.

- To upload a project, click 📤 **Upload**. The default maximum file upload size is 100 MB.

- To move a flow or component, drag and drop it into the desired project.

## File management

Upload, store, and manage files in Langinfra's **File management** system.

For more on managing your files, see [Manage files](/concepts-file-management).

## Options menu

The dropdown menu labeled with the project name offers several management and customization options for the current flow in the Langinfra workspace.

- **New**: Create a new flow from scratch.
- **Settings**: Adjust settings specific to the current flow, such as its name, description, and endpoint name.
- **Logs**: View logs for the current project, including execution history, errors, and other runtime events.
- **Import**: Import a flow or component from a JSON file into the workspace.
- **Export**: Export the current flow as a JSON file.
- **Undo (⌘Z)**: Revert the last action taken in the project.
- **Redo (⌘Y)**: Reapply a previously undone action.
- **Refresh All**: Refresh all components and delete cache.

## Settings

Click <Icon name="Settings" aria-label="Gear icon" /> **Settings** to access **Global variables**, **Langinfra API**, **Shortcuts**, and **Messages**.
