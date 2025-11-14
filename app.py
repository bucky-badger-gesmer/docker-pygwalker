#!/usr/bin/env python3
"""
PyGWalker Dockerized Application
This script loads data from various file formats and launches PyGWalker web interface using Flask.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional, List

import pandas as pd
from flask import Flask, render_template_string, jsonify, request
import pygwalker as pyg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def disable():
        """Disable colors for non-interactive terminals."""
        Colors.HEADER = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.ENDC = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''

# Disable colors on Windows or if not running in a TTY
if not sys.stdout.isatty() or os.name == 'nt':
    Colors.disable()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted string (e.g., "1.2 MB", "890 KB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def scan_data_directory(data_dir: str) -> List[Path]:
    """
    Scan the data directory for supported data files.

    Args:
        data_dir: Path to the data directory to scan

    Returns:
        Sorted list of Path objects for supported data files

    Supported formats: .csv, .xlsx, .xls, .parquet, .json
    """
    logger.info(f"Scanning directory: {data_dir}")

    data_path = Path(data_dir)

    # Handle case where directory doesn't exist
    if not data_path.exists():
        logger.warning(f"Directory does not exist: {data_dir}")
        return []

    if not data_path.is_dir():
        logger.warning(f"Path is not a directory: {data_dir}")
        return []

    # Supported file extensions
    supported_extensions = {'.csv', '.xlsx', '.xls', '.parquet', '.json'}

    # Find all supported files
    available_files = []
    try:
        for file_path in data_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                available_files.append(file_path)

        # Sort files alphabetically by name
        available_files.sort(key=lambda p: p.name.lower())

        logger.info(f"Found {len(available_files)} data file(s)")
        for file in available_files:
            logger.debug(f"  - {file.name} ({format_file_size(file.stat().st_size)})")

        return available_files

    except PermissionError as e:
        logger.error(f"Permission denied when accessing directory: {e}")
        return []
    except Exception as e:
        logger.error(f"Error scanning directory: {e}")
        return []


def prompt_for_file_selection(
    available_files: List[Path],
    default_file: str,
    timeout: Optional[int] = None,
    max_attempts: int = 5
) -> Path:
    """
    Display available files and prompt user for selection with retry logic.

    Args:
        available_files: List of available data files
        default_file: Default filename to use if no selection made
        timeout: Optional timeout in seconds (None = no timeout)
        max_attempts: Maximum number of invalid input attempts before falling back to default

    Returns:
        Selected file Path

    Raises:
        KeyboardInterrupt: If user presses Ctrl+C
    """
    if not available_files:
        logger.warning("No data files available for selection")
        default_path = Path(f"/data/{default_file}")
        return default_path

    # Find default file in available files
    default_index = None
    for i, file_path in enumerate(available_files):
        if file_path.name == default_file:
            default_index = i + 1
            break

    def display_file_list() -> None:
        """Display the list of available files."""
        # Display header
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}PyGWalker Data Explorer - File Selection{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.ENDC}\n")

        # Display available files
        print(f"{Colors.GREEN}Available data files:{Colors.ENDC}\n")
        for i, file_path in enumerate(available_files, start=1):
            file_size = format_file_size(file_path.stat().st_size)
            file_ext = file_path.suffix.upper()[1:]  # Remove dot and uppercase

            # Highlight default file
            if default_index and i == default_index:
                print(f"  {Colors.YELLOW}{i}. {file_path.name} ({file_size}) [{file_ext}] {Colors.BOLD}[DEFAULT]{Colors.ENDC}")
            else:
                print(f"  {Colors.BLUE}{i}.{Colors.ENDC} {file_path.name} ({file_size}) [{file_ext}]")

        print()  # Empty line

    # Display file list initially
    display_file_list()

    # Create prompt message
    if default_index:
        prompt_msg = f"Enter file number (1-{len(available_files)}) or press Enter for default [{default_file}]: "
    else:
        prompt_msg = f"Enter file number (1-{len(available_files)}): "

    # Handle timeout if specified
    if timeout:
        print(f"{Colors.YELLOW}(Timeout: {timeout} seconds){Colors.ENDC}")

    # Retry loop for invalid inputs
    attempt = 0
    while attempt < max_attempts:
        try:
            # Get user input
            print(f"{Colors.BOLD}{prompt_msg}{Colors.ENDC}", end='', flush=True)
            user_input = input().strip()

            # Handle empty or whitespace-only input (use default)
            if not user_input or user_input.isspace():
                if default_index:
                    print(f"{Colors.GREEN}Using default file: {available_files[default_index - 1].name}{Colors.ENDC}")
                    return available_files[default_index - 1]
                else:
                    print(f"{Colors.YELLOW}No default available. Using first file: {available_files[0].name}{Colors.ENDC}")
                    return available_files[0]

            # Validate input is a number
            try:
                selection = int(user_input)
            except ValueError:
                attempt += 1
                print(f"{Colors.RED}Invalid input: Please enter a number between 1-{len(available_files)} or press Enter for default.{Colors.ENDC}\n")

                if attempt < max_attempts:
                    # Display file list again for user convenience
                    display_file_list()
                continue

            # Validate selection is in range (positive and within bounds)
            if selection < 1 or selection > len(available_files):
                attempt += 1
                print(f"{Colors.RED}Invalid selection: {selection} is out of range. Please choose between 1-{len(available_files)}.{Colors.ENDC}\n")

                if attempt < max_attempts:
                    # Display file list again for user convenience
                    display_file_list()
                continue

            # Valid selection - return the selected file
            selected_file = available_files[selection - 1]
            print(f"{Colors.GREEN}Selected file: {selected_file.name}{Colors.ENDC}")
            return selected_file

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Selection cancelled by user.{Colors.ENDC}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during file selection: {e}")
            attempt += 1
            print(f"{Colors.RED}Unexpected error: {e}{Colors.ENDC}\n")

            if attempt < max_attempts:
                display_file_list()
            continue

    # Max attempts reached - fall back to default
    logger.warning(f"Maximum attempts ({max_attempts}) reached for file selection. Falling back to default.")
    print(f"{Colors.YELLOW}Maximum attempts reached ({max_attempts}). Using default file.{Colors.ENDC}")

    if default_index:
        print(f"{Colors.YELLOW}Using default file: {available_files[default_index - 1].name}{Colors.ENDC}")
        return available_files[default_index - 1]
    else:
        print(f"{Colors.YELLOW}No default available. Using first file: {available_files[0].name}{Colors.ENDC}")
        return available_files[0]


def validate_file_path(file_path: str) -> Path:
    """
    Validate that the file exists and is readable.

    Args:
        file_path: Path to the data file

    Returns:
        Path object if valid

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file is not readable
        ValueError: If path is not a file
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    if not os.access(path, os.R_OK):
        raise PermissionError(f"File is not readable: {file_path}")

    logger.info(f"File validated successfully: {path}")
    return path


def load_data(file_path: Path) -> pd.DataFrame:
    """
    Load data from CSV, Excel, Parquet, or JSON file.

    Args:
        file_path: Path to the data file

    Returns:
        pandas DataFrame

    Raises:
        ValueError: If file format is not supported or loading fails
    """
    file_extension = file_path.suffix.lower()
    logger.info(f"Loading data from {file_path} (format: {file_extension})")

    try:
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.parquet':
            df = pd.read_parquet(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        else:
            supported_formats = ['.csv', '.xlsx', '.xls', '.parquet', '.json']
            raise ValueError(
                f"Unsupported file format: {file_extension}. "
                f"Supported formats: {', '.join(supported_formats)}"
            )

        logger.info(f"Data loaded successfully: {len(df):,} rows × {len(df.columns)} columns")
        logger.info(f"Columns: {', '.join(df.columns.tolist())}")

        return df

    except Exception as e:
        logger.error(f"Error loading file: {str(e)}")
        raise ValueError(f"Error loading file: {str(e)}")


def get_file_path() -> str:
    """
    Get file path from environment variable, interactive selection, or default to sample data.

    Returns:
        File path string

    Raises:
        KeyboardInterrupt: If user cancels selection with Ctrl+C
    """
    # Check if file path is provided via environment variable
    env_file_path = os.environ.get('DATA_FILE_PATH')
    if env_file_path:
        logger.info(f"Using file path from DATA_FILE_PATH environment variable: {env_file_path}")
        return env_file_path

    # No environment variable set - scan directory and prompt for selection
    logger.info("DATA_FILE_PATH not set. Scanning /data directory for available files...")

    data_dir = '/data'
    default_filename = 'sample_data.csv'

    # Scan for available files
    available_files = scan_data_directory(data_dir)

    if not available_files:
        # No files found - fall back to default
        logger.warning(f"No data files found in {data_dir}. Falling back to default: {default_filename}")
        print(f"\n{Colors.YELLOW}Warning: No data files found in {data_dir}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Falling back to default: {default_filename}{Colors.ENDC}\n")
        return f"{data_dir}/{default_filename}"

    # Prompt user for file selection
    try:
        selected_file = prompt_for_file_selection(
            available_files=available_files,
            default_file=default_filename,
            timeout=None  # No timeout by default
        )
        logger.info(f"User selected file: {selected_file}")
        return str(selected_file)

    except KeyboardInterrupt:
        # User cancelled - fall back to default
        logger.info("File selection cancelled by user. Using default.")
        print(f"\n{Colors.YELLOW}Using default file: {default_filename}{Colors.ENDC}\n")
        return f"{data_dir}/{default_filename}"


def create_app(dataframe: pd.DataFrame, file_info: dict) -> Flask:
    """
    Create Flask application with PyGWalker integration.

    Args:
        dataframe: pandas DataFrame to visualize
        file_info: Dictionary containing file information

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Generate PyGWalker HTML
    logger.info("Generating PyGWalker visualization HTML...")
    pyg_html = pyg.to_html(dataframe)

    # HTML template with improved styling and information panel
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PyGWalker Data Explorer</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background-color: #f5f5f5;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .header h1 {
                font-size: 28px;
                font-weight: 600;
                margin-bottom: 10px;
            }
            .info-panel {
                display: flex;
                gap: 30px;
                flex-wrap: wrap;
                margin-top: 10px;
            }
            .info-item {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .info-label {
                font-weight: 500;
                opacity: 0.9;
            }
            .info-value {
                background: rgba(255, 255, 255, 0.2);
                padding: 4px 12px;
                border-radius: 4px;
                font-weight: 600;
            }
            .content {
                flex: 1;
                padding: 20px;
                overflow: auto;
                background-color: white;
                margin: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            .pygwalker-container {
                width: 100%;
                height: 100%;
                min-height: 600px;
            }
            .columns-info {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .columns-list {
                max-width: 500px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 22px;
                }
                .info-panel {
                    gap: 15px;
                }
                .content {
                    margin: 10px;
                    padding: 10px;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>PyGWalker Data Explorer</h1>
            <div class="info-panel">
                <div class="info-item">
                    <span class="info-label">File:</span>
                    <span class="info-value">{{ file_name }}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Rows:</span>
                    <span class="info-value">{{ rows }}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Columns:</span>
                    <span class="info-value">{{ columns }}</span>
                </div>
                <div class="columns-info">
                    <span class="info-label">Fields:</span>
                    <span class="columns-list" title="{{ column_names }}">{{ column_names }}</span>
                </div>
            </div>
        </div>
        <div class="content">
            <div class="pygwalker-container">
                {{ pyg_html | safe }}
            </div>
        </div>
    </body>
    </html>
    """

    @app.route('/')
    def index():
        """Main route serving the PyGWalker interface."""
        return render_template_string(
            template,
            pyg_html=pyg_html,
            file_name=file_info['name'],
            rows=f"{file_info['rows']:,}",
            columns=file_info['columns'],
            column_names=', '.join(file_info['column_names'])
        )

    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'file': file_info['name'],
            'rows': file_info['rows'],
            'columns': file_info['columns']
        })

    @app.route('/info')
    def info():
        """Endpoint returning detailed data information."""
        return jsonify(file_info)

    return app


def main():
    """Main application entry point."""
    # Print startup banner
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}PyGWalker Data Explorer - Starting Application{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.ENDC}\n")

    # Get configuration from environment variables
    host = os.environ.get('PYGWALKER_HOST', '0.0.0.0')
    port = int(os.environ.get('PYGWALKER_PORT', '8888'))

    try:
        # Get and validate file path
        file_path_str = get_file_path()
        validated_path = validate_file_path(file_path_str)

        # Log file selection
        print(f"\n{Colors.GREEN}Loading data file: {validated_path.name}{Colors.ENDC}")
        print(f"{Colors.BLUE}Full path: {validated_path}{Colors.ENDC}\n")

        # Load data
        df = load_data(validated_path)

        # Prepare file information
        file_info = {
            'name': validated_path.name,
            'path': str(validated_path),
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict()
        }

        # Create Flask app
        app = create_app(df, file_info)

        # Log startup information
        print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}Application Ready{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}Configuration:{Colors.ENDC}")
        print(f"  Host:    {Colors.CYAN}{host}{Colors.ENDC}")
        print(f"  Port:    {Colors.CYAN}{port}{Colors.ENDC}")
        print(f"  File:    {Colors.CYAN}{file_info['name']}{Colors.ENDC}")
        print(f"  Data:    {Colors.CYAN}{file_info['rows']:,} rows × {file_info['columns']} columns{Colors.ENDC}")
        print(f"  Columns: {Colors.CYAN}{', '.join(file_info['column_names'][:5])}{Colors.ENDC}{'...' if len(file_info['column_names']) > 5 else ''}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}Server starting at {Colors.CYAN}http://{host}:{port}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Press CTRL+C to quit{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 60}{Colors.ENDC}\n")

        # Run Flask application
        app.run(
            host=host,
            port=port,
            debug=False,
            threaded=True
        )

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Application stopped by user (Ctrl+C){Colors.ENDC}")
        print(f"{Colors.YELLOW}{'=' * 60}{Colors.ENDC}\n")
        logger.info("Application stopped by user")
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"\n{Colors.RED}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.RED}{Colors.BOLD}Error: File Not Found{Colors.ENDC}")
        print(f"{Colors.RED}{'=' * 60}{Colors.ENDC}")
        logger.error(f"File not found: {e}")
        print(f"{Colors.RED}{e}{Colors.ENDC}\n")
        print(f"{Colors.YELLOW}Tips:{Colors.ENDC}")
        print(f"  - Make sure the file exists in the mounted volume")
        print(f"  - Check the DATA_FILE_PATH environment variable")
        print(f"  - Default path is: /data/sample_data.csv")
        print(f"  - Available files in /data:")

        # Show available files
        available_files = scan_data_directory('/data')
        if available_files:
            for file in available_files:
                print(f"    * {file.name}")
        else:
            print(f"    {Colors.RED}(No data files found){Colors.ENDC}")
        print()
        sys.exit(1)

    except PermissionError as e:
        print(f"\n{Colors.RED}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.RED}{Colors.BOLD}Error: Permission Denied{Colors.ENDC}")
        print(f"{Colors.RED}{'=' * 60}{Colors.ENDC}")
        logger.error(f"Permission denied: {e}")
        print(f"{Colors.RED}{e}{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}Please check that you have permission to read the file.{Colors.ENDC}\n")
        sys.exit(1)

    except ValueError as e:
        print(f"\n{Colors.RED}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.RED}{Colors.BOLD}Error: Invalid Data{Colors.ENDC}")
        print(f"{Colors.RED}{'=' * 60}{Colors.ENDC}")
        logger.error(f"ValueError: {e}")
        print(f"{Colors.RED}{e}{Colors.ENDC}\n")
        sys.exit(1)

    except Exception as e:
        print(f"\n{Colors.RED}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.RED}{Colors.BOLD}Error: Unexpected Error{Colors.ENDC}")
        print(f"{Colors.RED}{'=' * 60}{Colors.ENDC}")
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full traceback:")
        print(f"{Colors.RED}{e}{Colors.ENDC}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
