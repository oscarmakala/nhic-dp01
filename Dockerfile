FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml /app/

RUN pip install --no-cache-dir pip-tools && \
    python -c "import tomli; import json; f=open('pyproject.toml', 'rb'); p=tomli.load(f); deps = p['project']['dependencies']; print('\n'.join(deps))" > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Expose the API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "src/main.py"]