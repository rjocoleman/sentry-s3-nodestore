default:
  just --list

install:
  poetry install --with test

package:
  poetry build

test:
  pytest tests/test_backend.py
