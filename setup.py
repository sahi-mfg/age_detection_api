from setuptools import setup, find_packages  # type: ignore

setup(
    name="age-detection-api",
    version="0.1.0",
    description="API to detect age from photos",
    author="Sahi Mohamed Francis Gonsangbeu",
    author_email="mohamedfrancissahi@gmail.com",
    packages=find_packages(),
    install_requires=[
        "python-multipart",
        "fastapi",
        "pydantic",
        "torch",
        "transformers",
        "streamlit",
        "requests",
        "httpx",
        "uvicorn",
        "pillow",
        "pytest",
    ],
)
