FROM denoland/deno:1.40.2

WORKDIR /app

# Create a directory for node_modules
RUN mkdir -p /app/node_modules

# Set permissions for node_modules
RUN chmod 777 /app/node_modules

# Expose port 8000 for the SSE server
EXPOSE 8000

# Pre-warm the server to download Python standard library
RUN deno run \
    --allow-net \
    --allow-read=node_modules \
    --allow-write=node_modules \
    --node-modules-dir=true \
    jsr:@pydantic/mcp-run-python warmup

# Run the server with SSE transport
CMD ["deno", "run", "--allow-net", "--allow-read=.,node_modules", "--allow-write=node_modules", "--node-modules-dir=true", "jsr:@pydantic/mcp-run-python", "sse", "--host", "0.0.0.0", "--port", "8000"]
# Use the following command to build the Docker image
# docker build -t mcp-run-python .
# Use the following command to run the Docker container
# docker run -p 8000:8000 mcp-run-python
