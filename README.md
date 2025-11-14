# Docker PyGWalker

A Dockerized PyGWalker application that provides an interactive web interface for data visualization and exploration. Load your CSV, Excel, or Parquet files and explore them with an intuitive drag-and-drop interface.

This application uses Flask with PyGWalker's native rendering capabilities for a lightweight, production-ready deployment.

## Features

- 🐳 Fully containerized with Docker
- 📊 Supports multiple data formats (CSV, Excel, Parquet, JSON)
- 🎨 Interactive web-based visualization interface powered by PyGWalker
- 🎯 **Interactive file selection** - Choose from available data files at startup
- 🔒 File validation and error handling
- 📦 Easy deployment with Docker
- 🗂️ Volume mounting for local data access
- 🚀 Lightweight Flask-based server (no Streamlit dependency)
- 📝 Comprehensive logging for debugging
- 💉 Health check endpoints for monitoring
- 🌈 Colored terminal output for better user experience

## Prerequisites

- Docker (version 20.10 or higher)

## Quick Start

1. **Clone or download this repository**

2. **Place your data files in the `data` directory**
   ```bash
   # The data directory is already created
   # Copy your CSV, Excel, or Parquet files here
   cp /path/to/your/data.csv ./data/
   ```

3. **Build the Docker image**
   ```bash
   docker build -t pygwalker-app .
   ```

4. **Run the container with interactive file selection**
   ```bash
   docker run -it --rm \
     -p 8888:8888 \
     -v "$(pwd)/data:/data:ro" \
     pygwalker-app
   ```

   This will present you with an interactive menu to choose from available data files:
   ```
   ============================================================
   PyGWalker Data Explorer - File Selection
   ============================================================

   Available data files:

     1. sample_data.csv (1.2 MB) [CSV] [DEFAULT]
     2. sales_data.xlsx (3.4 MB) [XLSX]
     3. customer_data.parquet (890 KB) [PARQUET]

   Enter file number (1-3) or press Enter for default [sample_data.csv]:
   ```

5. **Access the application**
   - Open your browser and navigate to: `http://localhost:8888`

6. **Stop the container**
   - Press Ctrl+C in the terminal

### Skip File Selection

To skip interactive selection, pass the file path directly:
   ```bash
   docker run -it --rm \
     -p 8888:8888 \
     -v "$(pwd)/data:/data:ro" \
     -e DATA_FILE_PATH=/data/sample_data.csv \
     pygwalker-app
   ```

## Usage Examples

### Example 1: Interactive File Selection (New!)

Place multiple data files in the `data` directory and let the application prompt you to choose:

```bash
# Add multiple files to the data directory
cp ~/Downloads/sales_data.xlsx ./data/
cp ~/Downloads/customer_data.parquet ./data/

# Run with interactive mode
docker run -it --rm \
  -p 8888:8888 \
  -v "$(pwd)/data:/data:ro" \
  pygwalker-app
```

You'll be prompted to select which file to load. Press Enter to use the default, or type a number to select a specific file.

### Example 2: Skip Selection with Environment Variable

Set the file path directly to skip the interactive selection:

```bash
docker run -it --rm \
  -p 8888:8888 \
  -v "$(pwd)/data:/data:ro" \
  -e DATA_FILE_PATH=/data/sales_data.xlsx \
  pygwalker-app
```

### Example 3: Mount Different Data Directory

If your data is in a different location:

```bash
docker run -it --rm \
  -p 8888:8888 \
  -v "/path/to/your/data:/data:ro" \
  pygwalker-app
```

## Supported File Formats

- **CSV** (`.csv`) - Comma-separated values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel files
- **Parquet** (`.parquet`) - Apache Parquet format
- **JSON** (`.json`) - JSON files

## Interactive File Selection

When you run the application without setting the `DATA_FILE_PATH` environment variable, it will automatically scan the `/data` directory for supported files and present an interactive menu:

### Features:
- Lists all available data files with sizes and formats
- Shows which file is the default (if `sample_data.csv` exists)
- Allows selection by number or pressing Enter for default
- Displays file sizes in human-readable format (KB, MB, GB)
- Handles invalid input gracefully
- Supports Ctrl+C to cancel and use default

### Example Flow:
```
============================================================
PyGWalker Data Explorer - File Selection
============================================================

Available data files:

  1. sample_data.csv (1.2 MB) [CSV] [DEFAULT]
  2. sales_data.xlsx (3.4 MB) [XLSX]
  3. customer_data.parquet (890.5 KB) [PARQUET]
  4. users.json (245.8 KB) [JSON]

Enter file number (1-4) or press Enter for default [sample_data.csv]: 2

Selected file: sales_data.xlsx

Loading data file: sales_data.xlsx
Full path: /data/sales_data.xlsx

============================================================
Application Ready
============================================================
...
```

### Edge Cases Handled:
- **Empty directory**: Falls back to default file path
- **Invalid selection**: Uses default file
- **Ctrl+C during selection**: Gracefully exits or uses default
- **Directory doesn't exist**: Falls back to default
- **No default file exists**: Uses first available file

## Configuration

### Environment Variables

You can customize the application using these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PYGWALKER_HOST` | `0.0.0.0` | Host address for the web server |
| `PYGWALKER_PORT` | `8888` | Port for the web interface |
| `DATA_FILE_PATH` | *Interactive selection* | Path to the data file (if not set, prompts for selection) |

**Note:** If `DATA_FILE_PATH` is not set, the application will scan the `/data` directory and present an interactive menu to choose from available files.

### Changing the Port

To use a different port (e.g., 8080):

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

This usually means there was an error. Run with interactive mode to see errors:
```bash
docker run -it --rm \
  -p 8888:8888 \
  -v "$(pwd)/data:/data:ro" \
  pygwalker-app
```

## Development

### Modifying the Application

1. Edit `app.py` to change the application logic
2. Edit `requirements.txt` to add/remove dependencies
3. Rebuild the image:
   ```bash
   docker build -t pygwalker-app .
   ```

### Testing Changes

```bash
# Rebuild and run
docker build -t pygwalker-app . && \
docker run -it --rm \
  -p 8888:8888 \
  -v "$(pwd)/data:/data:ro" \
  pygwalker-app
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
2. Run in interactive mode to see detailed logs
3. Ensure your data file is in a supported format
4. Verify Docker is properly installed

## API Endpoints

The application exposes the following endpoints:

- `GET /` - Main PyGWalker visualization interface
- `GET /health` - Health check endpoint returning application status
- `GET /info` - Detailed data information (rows, columns, dtypes)

Example health check:
```bash
curl http://localhost:8888/health
```

Response:
```json
{
  "status": "healthy",
  "file": "sample_data.csv",
  "rows": 1000,
  "columns": 5
}
```

## Architecture

The application is built with:
- **Flask**: Lightweight web framework serving the PyGWalker interface
- **PyGWalker**: Interactive data visualization library
- **Pandas**: Data manipulation and loading
- **Python 3.11**: Modern Python runtime

Key benefits over Streamlit-based approach:
- Smaller container size (no Streamlit/Jupyter dependencies)
- Faster startup time
- Lower memory footprint
- Production-ready Flask server
- RESTful API endpoints for monitoring
- Better control over routing and middleware

## Version History

- **v2.1.0** - Interactive file selection
  - Added interactive file selection functionality
  - Automatic scanning of `/data` directory for supported files
  - User-friendly file selection prompt with file sizes and formats
  - Enhanced error handling for Ctrl+C and invalid selections
  - Colored terminal output for better UX
  - Smart fallback to default file when needed
  - Improved startup messages and logging

- **v2.0.0** - Flask refactor
  - Replaced Streamlit with Flask for lightweight deployment
  - Added health check and info API endpoints
  - Comprehensive structured logging
  - Improved error handling and user feedback
  - Type hints throughout codebase
  - Modern Python best practices

- **v1.0.0** - Initial release
  - Docker support with Python 3.11
  - Support for CSV, Excel, Parquet, and JSON files
  - Interactive web interface
  - Volume mounting for local data access
  - Comprehensive error handling

---

Made with using PyGWalker, Flask, and Docker
