#!/usr/bin/env python3
"""
PyGWalker Dockerized Application
This script loads data from various file formats and launches PyGWalker web interface using Streamlit.
"""

import os
import sys
import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from pathlib import Path


def validate_file_path(file_path):
    """
    Validate that the file exists and is readable.

    Args:
        file_path: Path to the data file

    Returns:
        Path object if valid

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file is not readable
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    if not os.access(path, os.R_OK):
        raise PermissionError(f"File is not readable: {file_path}")

    return path


def load_data(file_path):
    """
    Load data from CSV, Excel, or Parquet file.

    Args:
        file_path: Path to the data file

    Returns:
        pandas DataFrame

    Raises:
        ValueError: If file format is not supported
    """
    path = Path(file_path)
    file_extension = path.suffix.lower()

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
            raise ValueError(
                f"Unsupported file format: {file_extension}\n"
                f"Supported formats: .csv, .xlsx, .xls, .parquet, .json"
            )
        return df

    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")


def get_file_path():
    """
    Get file path from environment variable or default to sample data.

    Returns:
        File path string
    """
    # Check if file path is provided via environment variable
    env_file_path = os.environ.get('DATA_FILE_PATH')
    if env_file_path:
        return env_file_path

    # Default to sample data
    return '/data/sample_data.csv'


# Configure Streamlit page
st.set_page_config(
    page_title="PyGWalker Data Explorer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 PyGWalker Data Explorer")

# Get file path
file_path = get_file_path()

try:
    # Validate and load data
    validated_path = validate_file_path(file_path)
    df = load_data(validated_path)

    # Display data info
    st.sidebar.success(f"✅ Loaded: {validated_path.name}")
    st.sidebar.info(f"📊 {len(df):,} rows × {len(df.columns)} columns")

    # Display column names
    with st.sidebar.expander("📋 Columns"):
        for col in df.columns:
            st.text(f"• {col}")

    # Create PyGWalker renderer
    pyg_app = StreamlitRenderer(df)
    pyg_app.explorer()

except FileNotFoundError as e:
    st.error(f"❌ File not found: {file_path}")
    st.info("Please check that the file path is correct and the file exists.")
    st.code(f"Current path: {file_path}", language="bash")
    st.info("💡 **Tips:**")
    st.markdown("""
    - Make sure the file exists in the mounted volume
    - Check the DATA_FILE_PATH environment variable
    - Default path is: `/data/sample_data.csv`
    """)

except PermissionError as e:
    st.error(f"❌ Permission denied: {file_path}")
    st.info("Please check that you have permission to read the file.")

except ValueError as e:
    st.error(f"❌ Error: {e}")

except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    import traceback
    with st.expander("Error details"):
        st.code(traceback.format_exc())
