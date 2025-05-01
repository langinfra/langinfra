FROM langinfra/langinfra:1.0-alpha

CMD ["python", "-m", "langinfra", "run", "--host", "0.0.0.0", "--port", "7860"]
