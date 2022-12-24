#!/bin/bash

mypy wingtel
black wingtel tests --check
flake8 wingtel tests tests
isort wingtel tests --check-only
autoflake --remove-all-unused-imports --recursive --check  wingtel tests | grep 'Unused imports/variables detected'