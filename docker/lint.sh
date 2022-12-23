#!/bin/bash

mypy wingtel
black wingtel tests
autoflake --remove-all-unused-imports --recursive --in-place wingtel tests
flake8 wingtel tests
isort wingtel tests