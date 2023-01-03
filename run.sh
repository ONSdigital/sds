#!/bin/bash
export PYTHONPATH=src
export FIREBASE_KEYFILE_LOCATION=firebase_key.json
uvicorn src.app:app --reload