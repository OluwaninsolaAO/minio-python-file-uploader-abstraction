#!/usr/bin/env python3
"""MinIO API for Python"""
from minio import Minio as M
from os import getenv
from typing import Dict
from fileUploader import FileUpload
from random import choice
from string import ascii_letters
from fileUploader import media_types, media_extensions
from datauri import parse
from PIL import Image
from os import remove
from uuid import uuid4

bucket_name = getenv('PROJECT_SHORT_NAME', 'test') + '-b'
tmp_file_name = '.tmp_file'


class Minio(FileUpload):
    """MinIO API abstract class for Python"""

    def __init__(self, host, access_key, secret_key) -> None:
        """Initialize MinIO class"""
        self.client = M(host, access_key, secret_key)
        self.make_bucket(bucket_name=bucket_name)

    def make_bucket(self, bucket_name: str) -> None:
        """Create bucket"""
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload_file(
        self, file_path=None, data=None, public_id=None, *args, **kwargs
    ) -> Dict[str, str]:
        """Uploads file to MinIO"""

        if not any([file_path, data]):
            return {
                'url': None,
                'public_id': None
            }

        if data is not None:
            public_id = public_id or ''.join(
                choice(ascii_letters) for _ in range(20))
            public_id = public_id + '-' + str(uuid4())
            file_path = tmp_file_name
            try:
                data = parse(data)
                with open(tmp_file_name, 'wb') as f:
                    f.write(data.data)

                # if file is image, then optimize
                if data.media_type in media_types:
                    image = Image.open(tmp_file_name)
                    image.convert('RGB').save(
                        tmp_file_name, format='JPEG', optimized=True)
            except Exception as e:
                raise ValueError('Error Processing data: ' + str(e))
            public_id = public_id + media_extensions.get(data.media_type)
        else:
            public_id = file_path

        resp = self.client.fput_object(
            bucket_name=bucket_name,
            object_name=public_id,
            file_path=file_path
        )

        try:
            remove(tmp_file_name)
        except FileNotFoundError:
            pass

        return {
            'url': self.get_file_url(public_id=public_id),
            'public_id': public_id,
        }

    def delete_file(self, public_id):
        """Deletes file from MinIO"""
        pass

    def get_file_url(self, public_id, bucket_name=bucket_name):
        """Gets file from MinIO"""
        return self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=public_id
        ).split('?')[0]
