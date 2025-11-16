#!/usr/bin/env python3
"""
PyGWalker Dockerized Application
This script loads data from various file formats and launches PyGWalker web interface using Flask.
"""

import logging
import os
import sys
import io
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any
from threading import Lock
from werkzeug.utils import secure_filename

import pandas as pd
from flask import Flask, render_template_string, jsonify, request, session
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


def get_file_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Get metadata for a data file.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary containing file metadata
    """
    stat = file_path.stat()
    return {
        'name': file_path.name,
        'path': str(file_path),
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'extension': file_path.suffix.lower(),
        'modified': stat.st_mtime
    }


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


def load_data_from_file_storage(file_storage, filename: str) -> pd.DataFrame:
    """
    Load data from a Flask FileStorage object (uploaded file).

    Args:
        file_storage: Flask FileStorage object from request.files
        filename: Original filename for logging and format detection

    Returns:
        pandas DataFrame

    Raises:
        ValueError: If file format is not supported or loading fails
    """
    # Get file extension
    file_extension = Path(filename).suffix.lower()
    logger.info(f"Loading uploaded data from {filename} (format: {file_extension})")

    try:
        # Read file content into memory
        file_content = file_storage.read()
        file_storage.seek(0)  # Reset file pointer

        # Parse based on file extension
        if file_extension == '.csv':
            df = pd.read_csv(io.BytesIO(file_content))
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(io.BytesIO(file_content))
        elif file_extension == '.parquet':
            df = pd.read_parquet(io.BytesIO(file_content))
        elif file_extension == '.json':
            df = pd.read_json(io.BytesIO(file_content))
        else:
            supported_formats = ['.csv', '.xlsx', '.xls', '.parquet', '.json']
            raise ValueError(
                f"Unsupported file format: {file_extension}. "
                f"Supported formats: {', '.join(supported_formats)}"
            )

        logger.info(f"Uploaded data loaded successfully: {len(df):,} rows × {len(df.columns)} columns")
        logger.info(f"Columns: {', '.join(df.columns.tolist())}")

        return df

    except Exception as e:
        logger.error(f"Error loading uploaded file: {str(e)}")
        raise ValueError(f"Error parsing uploaded file: {str(e)}")


def validate_uploaded_file(filename: str, file_size: int, max_size_mb: int = 100) -> tuple[bool, Optional[str]]:
    """
    Validate uploaded file for security and size constraints.

    Args:
        filename: Original filename
        file_size: File size in bytes
        max_size_mb: Maximum allowed file size in megabytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls', '.json', '.parquet'}

    # Check if filename is empty
    if not filename:
        return False, "No filename provided"

    # Get file extension
    file_extension = Path(filename).suffix.lower()

    # Validate file extension
    if file_extension not in ALLOWED_EXTENSIONS:
        return False, (
            f"Unsupported file type: {file_extension}. "
            f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    # Validate file size
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, (
            f"File size ({format_file_size(file_size)}) exceeds maximum allowed size "
            f"({max_size_mb} MB)"
        )

    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False, "Invalid filename: path traversal detected"

    return True, None


def get_file_path() -> str:
    """
    Get file path from environment variable or default to sample_data.csv.

    Returns:
        File path string
    """
    # Check if file path is provided via environment variable
    env_file_path = os.environ.get('DATA_FILE_PATH')
    if env_file_path:
        logger.info(f"Using file path from DATA_FILE_PATH environment variable: {env_file_path}")
        return env_file_path

    # No environment variable set - default to sample_data.csv in project root
    # Get the directory where app.py is located (project root)
    project_root = Path(__file__).parent
    default_filename = 'sample_data.csv'
    default_path = str(project_root / default_filename)

    logger.info(f"DATA_FILE_PATH not set. Defaulting to: {default_path}")
    return default_path


def create_app(dataframe: pd.DataFrame, file_info: dict) -> Flask:
    """
    Create Flask application with PyGWalker integration and dynamic file selection.

    Args:
        dataframe: pandas DataFrame to visualize
        file_info: Dictionary containing file information

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'pygwalker-secret-key-change-in-production')

    # Global state for current data (thread-safe)
    app_state = {
        'current_df': dataframe,
        'current_file_info': file_info,
        'pyg_html': None,
        'lock': Lock()
    }

    # Generate PyGWalker HTML
    logger.info("Generating PyGWalker visualization HTML...")
    with app_state['lock']:
        app_state['pyg_html'] = pyg.to_html(dataframe)

    # HTML template with improved styling and upload functionality
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
            .upload-file-button {
                background: rgba(255, 255, 255, 0.3);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.6);
                padding: 6px 16px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                font-family: inherit;
            }
            .upload-file-button:hover:not(:disabled) {
                background: rgba(255, 255, 255, 0.4);
                border-color: rgba(255, 255, 255, 0.8);
                transform: translateY(-1px);
            }
            .upload-file-button:active:not(:disabled) {
                transform: translateY(0);
            }
            .upload-file-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .file-input {
                display: none;
            }
            .file-upload-hint {
                font-size: 12px;
                opacity: 0.8;
                font-style: italic;
            }
            .info-panel {
                display: flex;
                gap: 30px;
                flex-wrap: wrap;
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
                position: relative;
            }
            .pygwalker-container {
                width: 100%;
                height: 100%;
                min-height: 600px;
            }
            .loading-overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.95);
                display: none;
                justify-content: center;
                align-items: center;
                z-index: 1000;
                border-radius: 8px;
            }
            .loading-overlay.active {
                display: flex;
            }
            .loading-spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .error-message {
                background: #fee;
                border: 2px solid #f88;
                color: #c00;
                padding: 12px 20px;
                border-radius: 6px;
                margin-bottom: 20px;
                display: none;
            }
            .error-message.active {
                display: block;
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
                    <span class="info-value" id="currentFileName">{{ file_name }}</span>
                </div>
                <div class="info-item">
                    <button id="uploadFileButton" class="upload-file-button">Upload File</button>
                    <input type="file" id="fileInput" class="file-input" accept=".csv,.xlsx,.xls,.json,.parquet">
                    <span class="file-upload-hint">Supported formats: CSV, JSON, Excel (.xlsx, .xls)</span>
                </div>
            </div>
        </div>
        <div class="content">
            <div class="loading-overlay" id="loadingOverlay">
                <div class="loading-spinner"></div>
            </div>
            <div class="error-message" id="errorMessage"></div>
            <div class="pygwalker-container" id="pygwalkerContainer">
                {{ pyg_html | safe }}
            </div>
        </div>
        <script>
            let isLoading = false;

            // Upload a file
            async function uploadFile(file) {
                if (isLoading) return;

                // Validate file size (100MB limit)
                const maxSize = 100 * 1024 * 1024; // 100MB
                if (file.size > maxSize) {
                    showError(`File size (${formatFileSize(file.size)}) exceeds maximum allowed size (100 MB)`);
                    return;
                }

                // Validate file type
                const allowedExtensions = ['.csv', '.xlsx', '.xls', '.json', '.parquet'];
                const fileName = file.name.toLowerCase();
                const hasValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));

                if (!hasValidExtension) {
                    showError(`Unsupported file type. Allowed types: ${allowedExtensions.join(', ')}`);
                    return;
                }

                isLoading = true;
                showLoading(true, 'Uploading...');
                hideError();

                try {
                    // Create FormData for file upload
                    const formData = new FormData();
                    formData.append('file', file);

                    const response = await fetch('/api/upload-file', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'Failed to upload file');
                    }

                    const data = await response.json();

                    // Update the visualization
                    document.getElementById('pygwalkerContainer').innerHTML = data.html;

                    // Update file info
                    document.getElementById('currentFileName').textContent = data.file_info.name;

                    console.log('File uploaded successfully:', data.file_info.name);

                    // Clear the file input
                    document.getElementById('fileInput').value = '';
                } catch (error) {
                    console.error('Error uploading file:', error);
                    showError('Failed to upload file: ' + error.message);
                } finally {
                    isLoading = false;
                    showLoading(false);
                }
            }

            function showLoading(show, message = 'Loading...') {
                const overlay = document.getElementById('loadingOverlay');
                const uploadButton = document.getElementById('uploadFileButton');

                if (show) {
                    overlay.classList.add('active');
                    uploadButton.disabled = true;
                    uploadButton.textContent = message;
                } else {
                    overlay.classList.remove('active');
                    uploadButton.disabled = false;
                    uploadButton.textContent = 'Upload File';
                }
            }

            function showError(message) {
                const errorDiv = document.getElementById('errorMessage');
                errorDiv.textContent = message;
                errorDiv.classList.add('active');
            }

            function hideError() {
                const errorDiv = document.getElementById('errorMessage');
                errorDiv.classList.remove('active');
            }

            function formatFileSize(bytes) {
                const units = ['B', 'KB', 'MB', 'GB'];
                let size = bytes;
                let unitIndex = 0;

                while (size >= 1024 && unitIndex < units.length - 1) {
                    size /= 1024;
                    unitIndex++;
                }

                return `${size.toFixed(1)} ${units[unitIndex]}`;
            }

            // Upload file button - triggers file input click
            document.getElementById('uploadFileButton').addEventListener('click', () => {
                document.getElementById('fileInput').click();
            });

            // File input change handler
            document.getElementById('fileInput').addEventListener('change', (event) => {
                const file = event.target.files[0];
                if (file) {
                    uploadFile(file);
                }
            });
        </script>
    </body>
    </html>
    """

    @app.route('/')
    def index():
        """Main route serving the PyGWalker interface."""
        with app_state['lock']:
            current_file = app_state['current_file_info']
            current_html = app_state['pyg_html']

        return render_template_string(
            template,
            pyg_html=current_html,
            file_name=current_file['name'],
            rows=f"{current_file['rows']:,}",
            columns=current_file['columns']
        )

    @app.route('/health')
    def health():
        """Health check endpoint."""
        with app_state['lock']:
            current_file = app_state['current_file_info']

        return jsonify({
            'status': 'healthy',
            'file': current_file['name'],
            'rows': current_file['rows'],
            'columns': current_file['columns']
        })

    @app.route('/info')
    def info():
        """Endpoint returning detailed data information."""
        with app_state['lock']:
            current_file = app_state['current_file_info']
        return jsonify(current_file)

    @app.route('/api/files')
    def list_files():
        """
        API endpoint to list all available data files in /data directory.

        Returns:
            JSON response with list of files and their metadata
        """
        try:
            data_dir = os.environ.get('DATA_DIR', '/data')
            available_files = scan_data_directory(data_dir)

            if not available_files:
                return jsonify({
                    'files': [],
                    'count': 0,
                    'message': 'No data files found'
                })

            # Get metadata for each file
            files_metadata = [get_file_metadata(f) for f in available_files]

            logger.info(f"API: Listed {len(files_metadata)} files")
            return jsonify({
                'files': files_metadata,
                'count': len(files_metadata)
            })

        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return jsonify({
                'error': str(e),
                'message': 'Failed to list files'
            }), 500

    @app.route('/api/load-file', methods=['POST'])
    def load_file_endpoint():
        """
        API endpoint to load a specific data file and regenerate PyGWalker HTML.

        Expected JSON payload:
            {
                "file_path": "/path/to/file.csv"
            }

        Returns:
            JSON response with new PyGWalker HTML and file information
        """
        try:
            # Parse request data
            data = request.get_json()
            if not data or 'file_path' not in data:
                return jsonify({
                    'error': 'Missing file_path in request body'
                }), 400

            file_path_str = data['file_path']
            logger.info(f"API: Loading file: {file_path_str}")

            # Validate file path
            try:
                validated_path = validate_file_path(file_path_str)
            except FileNotFoundError as e:
                logger.warning(f"File not found: {e}")
                return jsonify({'error': str(e)}), 404
            except (PermissionError, ValueError) as e:
                logger.warning(f"Invalid file: {e}")
                return jsonify({'error': str(e)}), 400

            # Load data
            try:
                df = load_data(validated_path)
            except ValueError as e:
                logger.error(f"Failed to load data: {e}")
                return jsonify({'error': str(e)}), 400

            # Generate new PyGWalker HTML
            logger.info("Generating new PyGWalker visualization...")
            new_pyg_html = pyg.to_html(df)

            # Prepare new file info
            new_file_info = {
                'name': validated_path.name,
                'path': str(validated_path),
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'dtypes': df.dtypes.astype(str).to_dict()
            }

            # Update app state (thread-safe)
            with app_state['lock']:
                app_state['current_df'] = df
                app_state['current_file_info'] = new_file_info
                app_state['pyg_html'] = new_pyg_html

            logger.info(f"Successfully loaded file: {new_file_info['name']} "
                       f"({new_file_info['rows']:,} rows x {new_file_info['columns']} columns)")

            return jsonify({
                'success': True,
                'html': new_pyg_html,
                'file_info': {
                    'name': new_file_info['name'],
                    'rows': new_file_info['rows'],
                    'columns': new_file_info['columns'],
                    'column_names': new_file_info['column_names']
                }
            })

        except Exception as e:
            logger.error(f"Unexpected error loading file: {e}")
            logger.exception("Full traceback:")
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500

    @app.route('/api/upload-file', methods=['POST'])
    def upload_file_endpoint():
        """
        API endpoint to handle file uploads from user's computer.

        Accepts multipart/form-data with a 'file' field containing the uploaded file.
        Validates file type and size, parses into pandas DataFrame, and updates visualization.

        Returns:
            JSON response with new PyGWalker HTML and file information
        """
        try:
            # Check if file is in request
            if 'file' not in request.files:
                logger.warning("API: Upload request missing file")
                return jsonify({
                    'error': 'No file provided'
                }), 400

            uploaded_file = request.files['file']

            # Check if a file was actually selected
            if uploaded_file.filename == '':
                logger.warning("API: Empty filename in upload request")
                return jsonify({
                    'error': 'No file selected'
                }), 400

            # Sanitize filename
            original_filename = uploaded_file.filename
            safe_filename = secure_filename(original_filename)

            logger.info(f"API: File upload initiated - {original_filename} (sanitized: {safe_filename})")

            # Get file size
            uploaded_file.seek(0, os.SEEK_END)
            file_size = uploaded_file.tell()
            uploaded_file.seek(0)

            # Validate uploaded file
            is_valid, error_message = validate_uploaded_file(safe_filename, file_size)
            if not is_valid:
                logger.warning(f"API: File validation failed - {error_message}")
                return jsonify({
                    'error': error_message
                }), 400

            logger.info(f"API: File validated - {safe_filename} ({format_file_size(file_size)})")

            # Parse uploaded file into DataFrame
            try:
                df = load_data_from_file_storage(uploaded_file, safe_filename)
            except ValueError as e:
                logger.error(f"Failed to parse uploaded file: {e}")
                return jsonify({
                    'error': str(e)
                }), 400

            # Validate DataFrame is not empty
            if df.empty:
                logger.warning("Uploaded file resulted in empty DataFrame")
                return jsonify({
                    'error': 'Uploaded file contains no data'
                }), 400

            # Generate new PyGWalker HTML
            logger.info("Generating PyGWalker visualization for uploaded file...")
            new_pyg_html = pyg.to_html(df)

            # Prepare new file info
            new_file_info = {
                'name': safe_filename,
                'path': f'uploaded:{safe_filename}',
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'dtypes': df.dtypes.astype(str).to_dict()
            }

            # Update app state (thread-safe)
            with app_state['lock']:
                app_state['current_df'] = df
                app_state['current_file_info'] = new_file_info
                app_state['pyg_html'] = new_pyg_html

            logger.info(f"Successfully uploaded and loaded file: {new_file_info['name']} "
                       f"({new_file_info['rows']:,} rows x {new_file_info['columns']} columns)")

            return jsonify({
                'success': True,
                'html': new_pyg_html,
                'file_info': {
                    'name': new_file_info['name'],
                    'rows': new_file_info['rows'],
                    'columns': new_file_info['columns'],
                    'column_names': new_file_info['column_names']
                },
                'message': f'File uploaded successfully: {safe_filename}'
            })

        except Exception as e:
            logger.error(f"Unexpected error during file upload: {e}")
            logger.exception("Full traceback:")
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500

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
