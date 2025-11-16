# Data Visualization Explorers

Two interactive data visualization applications for exploring and analyzing data:

- **Graphic Walker** - React/Vite frontend using @kanaries/graphic-walker
- **PyGWalker** - Flask backend using pygwalker

Both applications support file uploads and multiple data formats.

## Graphic Walker (React)

Modern React application built with Vite and TypeScript, featuring the Graphic Walker visualization library.

### Prerequisites

- Docker

### Quick Start

1. **Navigate to the graphic-walker directory**
   ```bash
   cd graphic-walker
   ```

2. **Build the Docker image**
   ```bash
   docker build -t graphic-walker .
   ```

3. **Run the container**
   ```bash
   docker run -it --rm -p 5173:5173 graphic-walker
   ```

4. **Open your browser**
   - Navigate to `http://localhost:5173`

---

## PyGWalker (Flask)

Python Flask application with PyGWalker for powerful data visualization capabilities.

### Prerequisites

- Docker

### Quick Start

1. **Navigate to the pygwalker directory**
   ```bash
   cd pygwalker
   ```

2. **Build the Docker image**
   ```bash
   docker build -t pygwalker .
   ```

3. **Run the container**
   ```bash
   docker run -it --rm -p 8888:8888 pygwalker
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8888`
---

## Features Comparison

| Feature | Graphic Walker | PyGWalker |
|---------|---------------|-----------|
| File Upload | ✅ | ✅ |
| CSV Support | ✅ | ✅ |
| Excel Support | ✅ | ✅ |
| JSON Support | ✅ | ✅ |
| Parquet Support | ❌ | ✅ |
| Auto Field Detection | ✅ | ✅ |
| Docker Support | ✅ | ✅ |
| Default Port | 5173 | 8888 |
| Technology | React/Vite | Flask/Python |

---

## Supported Formats

Both applications support the following data formats:

- **CSV** (`.csv`) - Comma-separated values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel files
- **JSON** (`.json`) - JSON array of objects

**PyGWalker only:**
- **Parquet** (`.parquet`) - Apache Parquet columnar format

---

## Custom Ports

### Graphic Walker

```bash
docker run -it --rm -p 3000:5173 graphic-walker
```
Access at `http://localhost:3000`

### PyGWalker

```bash
docker run -it --rm -p 9000:8888 pygwalker
```
Access at `http://localhost:9000`

---

## Project Structure

```
docker-pygwalker/
├── graphic-walker/          # React/Vite application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── data/            # Sample data
│   │   └── utils/           # Utility functions
│   ├── Dockerfile
│   └── package.json
│
├── pygwalker/               # Flask application
│   ├── app.py               # Main Flask application
│   ├── sample_data.csv      # Default sample data
│   ├── Dockerfile
│   └── requirements.txt
│
└── README.md                # This file
```

---

## Contributing

Both applications are designed to be extensible and easy to modify. Feel free to customize the styling, add new features, or adapt them to your specific use cases.
