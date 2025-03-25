FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml /app/
RUN pip install poetry==1.4.2 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . /app/

# Expose the API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "src/main.py"]