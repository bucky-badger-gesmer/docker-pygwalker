# Docker PyGWalker

Interactive data visualization powered by PyGWalker in a Docker container.

## Prerequisites

- Docker

## Quick Start

1. **Build the image**
   ```bash
   docker build -t pygwalker .
   ```

2. **Run the container**
   ```bash
   docker run -it --rm -p 8888:8888 pygwalker
   ```

3. **Open your browser**
   - Navigate to `http://localhost:8888`

That's it! The app will prompt you to select a data file from the `/data` directory.

## Supported Formats

- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- Parquet (`.parquet`)
- JSON (`.json`)

## Ports

Default port is `8888`. To use a different port:

```bash
docker run -it --rm -p 9000:8888 pygwalker
```

Then access at `http://localhost:9000`
