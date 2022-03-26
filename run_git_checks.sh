#!/bin/sh

pflake8 turbo
black -S --target-version=py38 --line-length=100 . --exclude "doc|migrations"
pytest turbo
