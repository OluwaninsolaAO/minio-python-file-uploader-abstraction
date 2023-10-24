#!/usr/bin/env python3
"""Main module for testing MinIO"""

from fileUploader.minio import Minio
from dotenv import load_dotenv
from os import getenv

load_dotenv()
MINIO_HOST = getenv('MINIO_HOST')
MINIO_ACCESS_KEY = getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = getenv('MINIO_SECRET_KEY')

cloud = Minio(MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)
