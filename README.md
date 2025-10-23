#  Age Detection API

An API that predicts age ranges from images using a pre-trained Vision Transformer (ViT) model from Hugging Face.

![Age Detection App](age-detection-app.png)

🌐 **Live Demo**: [age-detection-app](https://age-detection.streamlit.app)

## ✨ Features

- **Model**: Uses Vision Transformer (ViT) for accurate age prediction
- **FastAPI**: High-performance REST API with automatic documentation
- **Docker Ready**: Containerized for easy deployment
- **Web Interface**: Interactive Streamlit UI for testing
- **Modern Tooling**: Built with `uv`, `ruff`, and `pre-commit`

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Model**: Vision Transformer (ViT) from Hugging Face
- **Package Manager**: uv
- **Image Processing**: Pillow
- **ML Libraries**: PyTorch, Transformers
- **Linting/Formatting**: Ruff
- **Testing**: Pytest
- **Containerization**: Docker

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (optional, for containerized deployment)

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/sahi-mfg/age_detection_api.git
   cd age_detection_api
   ```

2. **Install dependencies**
   ```bash
   make install
   ```

3. **Run the API**
   ```bash
   make run
   ```
   The API will be available at `http://localhost:8000`

4. **Run the Streamlit UI** (in another terminal)
   ```bash
   uv run streamlit run ui/streamlit_app.py
   ```
   The UI will be available at `http://localhost:8501`

### Using Docker

1. **Build the Docker image**
   ```bash
   docker build -t age-detection-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 age-detection-api
   ```

## 📚 API Documentation

Once the API is running, visit:
- **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

### Endpoints

#### `POST /predict`
Upload an image and get the predicted age range.

**Request**: Multipart form data with an image file
**Response**: JSON with filename, content type, and age prediction

Example:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

## 🛠️ Development

### Available Make Commands

```bash
make install    # Install dependencies
make run        # Run development server with reload
make run-prod   # Run production server
make test       # Run tests
make lint       # Check code with ruff
make format     # Format code with ruff
```

### Code Quality

This project uses:
- **Ruff** for linting and formatting
- **Pre-commit hooks** for automated code quality checks
- **Pytest** for testing

Run quality checks:
```bash
make lint       # Check for issues
make format     # Auto-fix formatting
make test       # Run test suite
```

## 🚢 Deployment

### Render Deployment

This project is optimized for deployment on Render:

1. Connect your GitHub repository to Render
2. Select "Web Service"
3. Use the following settings:
   - **Build Command**: `docker build -t age-detection-api .`
   - **Start Command**: `docker run -p $PORT:8000 age-detection-api`
   - **Environment**: Docker

### Environment Variables

For production deployment, you may want to set:
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## 🧪 Testing

Run the test suite:
```bash
make test
```

Run with coverage:
```bash
uv run pytest --cov=app tests/
```

## 📁 Project Structure

```
age_detection_api/
├── app/                    # Main application code
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   └── model.py           # ML model logic
├── ui/                    # Streamlit interface
│   └── streamlit_app.py
├── tests/                 # Test files
│   ├── test_predict.py
│   └── files/
├── Dockerfile             # Docker configuration
├── Makefile              # Development commands
├── pyproject.toml        # Project dependencies
├── uv.lock              # Locked dependencies
└── README.md            # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run quality checks (`make lint format test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for the Vision Transformer model
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Streamlit](https://streamlit.io/) for the interactive UI framework
