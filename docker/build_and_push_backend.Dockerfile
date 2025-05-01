# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

ARG LANGINFRA_IMAGE
FROM $LANGINFRA_IMAGE

RUN rm -rf /app/.venv/langinfra/frontend

CMD ["python", "-m", "langinfra", "run", "--host", "0.0.0.0", "--port", "7860", "--backend-only"]
