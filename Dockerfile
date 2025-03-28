FROM python:3.12.9-slim

WORKDIR /app

# Install hatch
RUN pip install --no-cache-dir hatch

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src/ ./src/

# Build and install the package
RUN pip install .

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["mcp-prefect"]