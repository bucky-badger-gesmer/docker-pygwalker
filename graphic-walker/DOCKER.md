# Docker Setup for GraphicWalker

This document explains how to build and run the GraphicWalker application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and run in one command
docker-compose up --build

# Run in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Using Docker CLI

```bash
# Build the image
docker build -t graphic-walker:latest .

# Run the container
docker run -d \
  --name graphic-walker \
  -p 5173:5173 \
  --restart unless-stopped \
  graphic-walker:latest

# View logs
docker logs -f graphic-walker

# Stop and remove container
docker stop graphic-walker
docker rm graphic-walker
```

## Access the Application

Once running, access the application at:
- **Local**: http://localhost:5173
- **Network**: http://YOUR_IP:5173

## Docker Image Details

### Base Image
- **Base**: `node:lts-alpine3.22`
- **Size**: Optimized multi-stage build (~150-200 MB)
- **Architecture**: Supports amd64 and arm64

### Build Process

The Dockerfile uses a **multi-stage build** for optimal image size:

1. **Builder Stage**: Installs all dependencies and builds the app
2. **Production Stage**: Only includes production dependencies and built assets

### Environment Variables

- `NODE_ENV=production` - Sets Node environment to production

### Exposed Ports

- **5173** - Vite preview server (production build)

## Advanced Usage

### Custom Port Mapping

Run on a different host port:

```bash
# Run on port 8080 instead of 5173
docker run -p 8080:5173 graphic-walker:latest

# Or with docker-compose, edit docker-compose.yml:
# ports:
#   - "8080:5173"
```

### Development Mode

For development with hot reload:

```bash
# Create a development docker-compose override
cat > docker-compose.dev.yml << EOF
version: '3.8'
services:
  graphic-walker:
    build:
      context: .
      target: builder
    command: npm run dev -- --host 0.0.0.0
    volumes:
      - ./src:/app/src
      - ./public:/app/public
    ports:
      - "5173:5173"
EOF

# Run development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Build with Custom Tag

```bash
# Build with version tag
docker build -t graphic-walker:1.0.0 .
docker build -t graphic-walker:latest .

# Tag for registry
docker tag graphic-walker:latest your-registry.com/graphic-walker:latest
```

### Push to Registry

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag graphic-walker:latest yourusername/graphic-walker:latest

# Push to Docker Hub
docker push yourusername/graphic-walker:latest
```

## Health Checks

The container includes a health check that:
- Runs every 30 seconds
- Times out after 3 seconds
- Retries 3 times before marking unhealthy
- Waits 5 seconds before starting checks

Check container health:

```bash
# Docker CLI
docker inspect --format='{{.State.Health.Status}}' graphic-walker

# Docker Compose
docker-compose ps
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs graphic-walker

# Common issues:
# 1. Port 5173 already in use
#    Solution: Use different port with -p 8080:5173

# 2. Build failed
#    Solution: Check build logs
docker build --no-cache -t graphic-walker:latest .
```

### Can't access from outside

```bash
# Ensure container is listening on 0.0.0.0
docker exec graphic-walker netstat -tuln | grep 5173

# Check firewall rules
# Make sure port 5173 is open on your host firewall
```

### Performance issues

```bash
# Check container resources
docker stats graphic-walker

# Increase memory limit if needed
docker run -m 512m graphic-walker:latest
```

## File Structure

```
graphic-walker/
├── Dockerfile              # Multi-stage production build
├── .dockerignore          # Files to exclude from build
├── docker-compose.yml     # Compose configuration
└── DOCKER.md             # This file
```

## Production Considerations

### Security

1. **Run as non-root user** (consider adding in Dockerfile):
```dockerfile
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs
```

2. **Scan for vulnerabilities**:
```bash
docker scan graphic-walker:latest
```

### Optimization

1. **Use .dockerignore** - Already configured to exclude unnecessary files
2. **Multi-stage builds** - Already implemented
3. **Layer caching** - Dependencies installed before copying source code

### Monitoring

Set up monitoring with:
- Docker stats: `docker stats graphic-walker`
- Health checks: Built-in health check endpoint
- Logs: `docker logs -f graphic-walker`

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t graphic-walker:latest .

      - name: Test container
        run: |
          docker run -d --name test -p 5173:5173 graphic-walker:latest
          sleep 10
          curl -f http://localhost:5173 || exit 1
          docker stop test
```

## Additional Resources

- [Vite Docker Guide](https://vitejs.dev/guide/static-deploy.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Node.js Docker Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)

## Support

For issues specific to:
- **Docker setup**: Check this file and Docker logs
- **Application issues**: See main README.md
- **GraphicWalker library**: See [@kanaries/graphic-walker docs](https://github.com/Kanaries/graphic-walker)
