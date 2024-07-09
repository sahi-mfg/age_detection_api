#!/bin/sh
poetry run uvicorn "app.main:app" --reload
