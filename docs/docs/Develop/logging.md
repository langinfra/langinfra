---
title: Logging options in Langinfra
slug: /logging
---

Langinfra uses the `loguru` library for logging.

The default `log_level` is `ERROR`. Other options are `DEBUG`, `INFO`, `WARNING`, and `CRITICAL`.

The default logfile is called `langinfra.log`, and its location depends on your operating system.

* Linux/WSL: `\~/.cache/langinfra/`
* macOS: `/Users/\<username\>/Library/Caches/langinfra/`
* Windows: `%LOCALAPPDATA%\langinfra\langinfra\Cache`

The `LANGINFRA_LOG_ENV` controls log output and formatting. The `container` option outputs serialized JSON to stdout. The `container_csv` option outputs CSV-formatted plain text to stdout. The `default` (or not set) logging option outputs prettified output with [RichHandler](https://rich.readthedocs.io/en/stable/reference/logging.html).

To modify Langinfra's logging configuration, add them to your `.env` file and start Langinfra.

```text
LANGINFRA_LOG_LEVEL=ERROR
LANGINFRA_LOG_FILE=path/to/logfile.log
LANGINFRA_LOG_ENV=container
```

To start Langinfra with the values from your .env file, start Langinfra with `uv run langinfra run --env-file .env`