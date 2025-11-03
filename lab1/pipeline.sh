#!/bin/bash

# pipeline.sh - bash-скрипт, последовательно запускающий все python-скрипты.

set -e  # Остановить выполнение при любой ошибке

python data_creation.py

python data_preprocessing.py

python model_preparation.py

python model_testing.py

echo "готово"