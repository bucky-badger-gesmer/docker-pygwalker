# Docker PyGWalker

A Dockerized PyGWalker application that provides an interactive web interface for data visualization and exploration. Load your CSV, Excel, or Parquet files and explore them with an intuitive drag-and-drop interface.

## Features

- 🐳 Fully containerized with Docker
- 📊 Supports multiple data formats (CSV, Excel, Parquet, JSON)
- 🎨 Interactive web-based visualization interface powered by PyGWalker
- 🔒 File validation and error handling
- 📦 Easy deployment with Docker Compose
- 🗂️ Volume mounting for local data access

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Clone or download this repository**

2. **Place your data files in the `data` directory**
   ```bash
   # The data directory is already created
   # Copy your CSV, Excel, or Parquet files here
   cp /path/to/your/data.csv ./data/
   ```

3. **Build and run the container**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - The container will start and automatically load the data file
   - Open your browser and navigate to: `http://localhost:8888`

5. **Stop the container**
   ```bash
   # Press Ctrl+C in the terminal, or in another terminal:
   docker-compose down
   ```

### Option 2: Using Docker Commands

1. **Build the Docker image**
   ```bash
   docker build -t pygwalker-app .
   ```

2. **Run the container**
   ```bash
   docker run -it --rm \
     -p 8888:8888 \
     -v "$(pwd)/data:/data:ro" \
     pygwalker-app
   ```

3. **Or pass the file path directly**
   ```bash
   docker run -it --rm \
     -p 8888:8888 \
     -v "$(pwd)/data:/data:ro" \
     -e DATA_FILE_PATH=/data/sample_data.csv \
     pygwalker-app
   ```

   Or as a command-line argument:
   ```bash
   docker run -it --rm \
     -p 8888:8888 \
     -v "$(pwd)/data:/data:ro" \
     pygwalker-app /data/sample_data.csv
   ```

## Usage Examples

### Example 1: Using Sample Data

Try the included sample dataset:

```bash
docker-compose up
# Open browser to http://localhost:8888
```

### Example 2: Using Your Own Data

1. Copy your data file to the data directory:
   ```bash
   cp ~/Downloads/sales_data.xlsx ./data/
   ```

2. Set the file path in docker-compose.yml or run:
   ```bash
   DATA_FILE_PATH=/data/sales_data.xlsx docker-compose up
   ```

### Example 3: Using Environment Variables

Edit `docker-compose.yml` to set the file path:

```yaml
environment:
  - DATA_FILE_PATH=/data/my_data.csv
```

Then run:
```bash
docker-compose up
```

### Example 4: Mount Different Data Directory

If your data is in a different location:

```bash
docker run -it --rm \
  -p 8888:8888 \
  -v "/path/to/your/data:/data:ro" \
  pygwalker-app /data/your-file.csv
```

## Supported File Formats

- **CSV** (`.csv`) - Comma-separated values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel files
- **Parquet** (`.parquet`) - Apache Parquet format
- **JSON** (`.json`) - JSON files

## Configuration

### Environment Variables

You can customize the application using these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PYGWALKER_HOST` | `0.0.0.0` | Host address for the web server |
| `PYGWALKER_PORT` | `8888` | Port for the web interface |
| `DATA_FILE_PATH` | `/data/sample_data.csv` | Path to the data file |

### Changing the Port

To use a different port (e.g., 8080):

**Docker Compose:**
Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:8888"
environment:
  - PYGWALKER_PORT=8888
```

**Docker Command:**
```bash
docker run -it --rm \
  -p 8080:8888 \
  -e PYGWALKER_PORT=8888 \
  -v "$(pwd)/data:/data:ro" \
  pygwalker-app
```

Then access at `http://localhost:8080`

## Project Structure

```
docker-pygwalker/
├── app.py                  # Main Python application
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── data/                  # Directory for data files
    └── sample_data.csv    # Sample dataset
```

## Features of PyGWalker Interface

Once the application is running, you can:

- **Drag and drop** fields to create visualizations
- **Switch between chart types** (bar, line, scatter, etc.)
- **Filter and transform data** on the fly
- **Create multiple views** and dashboards
- **Export visualizations** as images
- **Save and load analysis** configurations

## Troubleshooting

### Port Already in Use

If port 8888 is already in use, change the port mapping:
```bash
docker run -it --rm \
  -p 9000:8888 \
  -e PYGWALKER_PORT=8888 \
  -v "$(pwd)/data:/data:ro" \
  pygwalker-app
```

### File Not Found Error

Make sure:
1. Your file is in the `data` directory
2. You're using the correct path format: `/data/filename.csv`
3. The file has the correct permissions (readable)

### Permission Denied

On Linux/Mac, ensure the data files are readable:
```bash
chmod 644 data/your-file.csv
```

### Container Exits Immediately

This usually means there was an error. Check logs:
```bash
docker-compose logs
```

Or run with interactive mode to see errors:
```bash
docker-compose run --rm pygwalker
```

## Development

### Modifying the Application

1. Edit `app.py` to change the application logic
2. Edit `requirements.txt` to add/remove dependencies
3. Rebuild the image:
   ```bash
   docker-compose build
   ```

### Testing Changes

```bash
# Rebuild and run
docker-compose up --build

# Or run tests (if you add them)
docker-compose run --rm pygwalker python -m pytest
```

## Security Considerations

- The container runs with read-only access to mounted volumes (`:ro` flag)
- No data is persisted in the container (use volumes for data)
- The application validates file paths and formats before loading
- Consider running on a private network or behind a reverse proxy for production use

## Performance Tips

- **Large Files**: For files > 1GB, consider using Parquet format for faster loading
- **Memory**: Increase Docker memory limits for large datasets
- **Network**: Use localhost (127.0.0.1) instead of 0.0.0.0 if not accessing from other machines

## Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License

This project is open source and available under the MIT License.

## Resources

- [PyGWalker Documentation](https://docs.kanaries.net/pygwalker)
- [Docker Documentation](https://docs.docker.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Docker logs: `docker-compose logs`
3. Ensure your data file is in a supported format
4. Verify Docker and Docker Compose are properly installed

## Version History

- **v1.0.0** - Initial release
  - Docker support with Python 3.11
  - Support for CSV, Excel, Parquet, and JSON files
  - Interactive web interface
  - Volume mounting for local data access
  - Comprehensive error handling

---

Made with ❤️ using PyGWalker and Docker
