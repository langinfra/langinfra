---
title: Install Langinfra
slug: /get-started-installation
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Langinfra can be installed in three ways:

* As a [Python package](#install-and-run-langinfra-oss) with Langinfra OSS
* As a [standalone desktop application](#install-and-run-langinfra-desktop) with Langinfra Desktop
* As a [cloud-hosted service](#datastax-langinfra) with DataStax Langinfra

## Install and run Langinfra OSS

Before you install and run Langinfra OSS, be sure you have the following items.

- [Python 3.10 to 3.13](https://www.python.org/downloads/release/python-3100/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) or [pip](https://pypi.org/project/pip/)
- A virtual environment created with [uv](https://docs.astral.sh/uv/pip/environments) or [venv](https://docs.python.org/3/library/venv.html)

Install and run Langinfra OSS with [uv (recommended)](https://docs.astral.sh/uv/getting-started/installation/) or [pip](https://pypi.org/project/pip/).

1. To install Langinfra, use one of the following commands:

<Tabs groupId="package-manager">
<TabItem value="uv" label="uv" default>

```bash
uv pip install langinfra
```

</TabItem>
<TabItem value="pip" label="pip">

```bash
pip install langinfra
```

</TabItem>
</Tabs>

2. To run Langinfra, use one of the following commands:

<Tabs groupId="package-manager">
    <TabItem value="uv" label="uv">

```bash
uv run langinfra run
```

</TabItem>
<TabItem value="pip" label="pip">

```bash
python -m langinfra run
```

</TabItem>
</Tabs>

3. To confirm that a local Langinfra instance starts, go to the default Langinfra URL at `http://127.0.0.1:7860`.

After confirming that Langinfra is running, create your first flow with the [Quickstart](/get-started-quickstart).

### Manage Langinfra OSS versions

To upgrade Langinfra to the latest version, use one of the following commands:

<Tabs groupId="package-manager">
<TabItem value="uv" label="uv" default>

```bash
uv pip install langinfra -U
```

</TabItem>
<TabItem value="pip" label="pip">

```bash
pip install langinfra -U
```

</TabItem>
</Tabs>

To install a specific version of the Langinfra package, add the required version to the command.
<Tabs groupId="package-manager">
<TabItem value="uv" label="uv" default>

```bash
uv pip install langinfra==1.3.2
```

</TabItem>
<TabItem value="pip" label="pip">

```bash
pip install langinfra==1.3.2
```

</TabItem>
</Tabs>

To reinstall Langinfra and all of its dependencies, add the `--force-reinstall` flag to the command.
<Tabs groupId="package-manager">
<TabItem value="uv" label="uv" default>

```bash
uv pip install langinfra --force-reinstall
```

</TabItem>
<TabItem value="pip" label="pip">

```bash
pip install langinfra --force-reinstall
```

</TabItem>
</Tabs>

### Install optional dependencies for Langinfra OSS

Langinfra OSS provides optional dependency groups that extend its functionality.

These dependencies are listed in the [pyproject.toml](https://github.com/langinfra/langinfra/blob/main/pyproject.toml#L191) file under `[project.optional-dependencies]`.

Install dependency groups using pip's `[extras]` syntax. For example, to install Langinfra with the `postgresql` dependency group, enter one of the following commands:

<Tabs groupId="package-manager">
<TabItem value="uv" label="uv" default>

```bash
uv pip install "langinfra[postgresql]"
```

</TabItem>
<TabItem value="pip" label="pip">

```bash
pip install "langinfra[postgresql]"
```

</TabItem>
</Tabs>

To install multiple extras, enter one of the following commands:

<Tabs groupId="package-manager">
<TabItem value="uv" label="uv" default>

```bash
uv pip install "langinfra[deploy,local,postgresql]"
```

</TabItem>
<TabItem value="pip" label="pip">

```bash
pip install "langinfra[deploy,local,postgresql]"
```

</TabItem>
</Tabs>

To add your own custom dependencies, see [Install custom dependencies](/install-custom-dependencies).

### Stop Langinfra OSS

To stop Langinfra, in the terminal where it's running, enter `Ctrl+C`.

To deactivate your virtual environment, enter `deactivate`.

### Common OSS installation issues

This is a list of possible issues that you may encounter when installing and running Langinfra.

#### No `langinfra.__main__` module

When you try to run Langinfra with the command `langinfra run`, you encounter the following error:

```bash
> No module named 'langinfra.__main__'
```

1. Run `uv run langinfra run` instead of `langinfra run`.
2. If that doesn't work, reinstall the latest Langinfra version with `uv pip install langinfra -U`.
3. If that doesn't work, reinstall Langinfra and its dependencies with `uv pip install langinfra --pre -U --force-reinstall`.

#### Langinfra runTraceback

When you try to run Langinfra using the command `langinfra run`, you encounter the following error:

```bash
> langinfra runTraceback (most recent call last): File ".../langinfra", line 5, in <module>  from langinfra.__main__ import mainModuleNotFoundError: No module named 'langinfra.__main__'
```

There are two possible reasons for this error:

1. You've installed Langinfra using `pip install langinfra` but you already had a previous version of Langinfra installed in your system. In this case, you might be running the wrong executable. To solve this issue, run the correct executable by running `python -m langinfra run` instead of `langinfra run`. If that doesn't work, try uninstalling and reinstalling Langinfra with `uv pip install langinfra --pre -U`.
2. Some version conflicts might have occurred during the installation process. Run `python -m pip install langinfra --pre -U --force-reinstall` to reinstall Langinfra and its dependencies.

#### Something went wrong running migrations

```bash
> Something went wrong running migrations. Please, run 'langinfra migration --fix'
```

Clear the cache by deleting the contents of the cache folder.

This folder can be found at:

- **Linux or WSL2 on Windows**: `home/<username>/.cache/langinfra/`
- **MacOS**: `/Users/<username>/Library/Caches/langinfra/`

This error can occur during Langinfra upgrades when the new version can't override `langinfra-pre.db` in `.cache/langinfra/`. Clearing the cache removes this file but also erases your settings.

If you wish to retain your files, back them up before clearing the folder.

#### Langinfra installation freezes at pip dependency resolution

Installing Langinfra with `pip install langinfra` slowly fails with this error message:

```text
pip is looking at multiple versions of <<library>> to determine which version is compatible with other requirements. This could take a while.
```

To work around this issue, install Langinfra with [`uv`](https://docs.astral.sh/uv/getting-started/installation/) instead of `pip`.

```text
uv pip install langinfra
```

To run Langinfra with uv:

```text
uv run langinfra run
```

## Install and run Langinfra Desktop

:::important
Langinfra Desktop is in **Alpha**.
Development is ongoing, and the features and functionality are subject to change.
:::

**Langinfra Desktop** is a desktop version of Langinfra that includes all the features of open source Langinfra, with an additional [version management](#manage-your-langinfra-version-in-langinfra-desktop) feature for managing your Langinfra version.

:::important
Langinfra Desktop is available only for macOS.
:::

To install Langinfra Desktop, follow these steps:

1. Navigate to [Langinfra Desktop](https://www.langinfra.org/desktop).
2. Enter your **Name**, **Email address**, and **Company**, and then click **Download**.
3. Open the **Finder**, and then navigate to **Downloads**.
4. Double-click the downloaded `*.dmg` file.
5. To install Langinfra Desktop, drag and drop the application icon to the **Applications** folder.
6. When the installation completes, open the Langinfra application.

The application checks [uv](https://docs.astral.sh/uv/concepts/tools/), your local environment, and the Langinfra version, and then starts.

### Manage your Langinfra version in Langinfra Desktop

When a new version of Langinfra is available, Langinfra Desktop displays an upgrade message.

To manage your Langinfra version in Langinfra Desktop, follow these steps:

1. To access Langinfra Desktop's **Version Management** pane, click your **Profile Image**, and then select **Version Management**.
Langinfra Desktop's current version is displayed, with other version options listed after it.
The **latest** version is always highlighted.
2. To change your Langinfra version, select another version.
A confirmation pane containing the selected version's changelog appears.
3. To change to the selected version, click **Confirm**.
The application restarts with the new version installed.

## DataStax Langinfra {#datastax-langinfra}

**DataStax Langinfra** is a hosted version of Langinfra integrated with [Astra DB](https://www.datastax.com/products/datastax-astra). Be up and running in minutes with no installation or setup required. [Sign up for free](https://astra.datastax.com/signup?type=langinfra).
