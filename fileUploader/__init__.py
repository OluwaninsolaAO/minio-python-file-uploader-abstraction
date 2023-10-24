#!/usr/bin/env python3
"""FileUploadService Module"""
from PIL import Image
from datauri import parse
from io import BytesIO
from PIL import Image
from typing import Dict
from string import ascii_letters
from random import choice
from os import remove


media_types = {
    'image/jpeg': 'JPEG',
    'image/png': 'PNG',
    'image/bmp': 'BMP',
}

tmp_file_name = '.tmp_file'

# dictionary of media and files extensions
media_extensions = {
    # image
    'image/jpeg': '.jpg',
    'image/jpg': '.jpg',
    'image/png': '.png',
    'image/bmp': '.bmp',
    'image/gif': '.gif',
    'image/tiff': '.tiff',
    'image/webp': '.webp',
    'image/svg+xml': '.svg',
    'image/x-icon': '.ico',
    # pdf
    'application/pdf': '.pdf',
    # doc
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    # excel
    'application/vnd.ms-excel': '.xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    # powerpoint
    'application/vnd.ms-powerpoint': '.ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    # text
    'text/plain': '.txt',
    # zip
    'application/zip': '.zip',
    # json
    'application/json': '.json',
    # xml
    'application/xml': '.xml',
    # csv
    'text/csv': '.csv',
    # html
    'text/html': '.html',
    # rtf
    'application/rtf': '.rtf',
    # mp3
    'audio/mpeg': '.mp3',
    # mp4
    'video/mp4': '.mp4',
    # avi
    'video/x-msvideo': '.avi',
    # mpeg
    'video/mpeg': '.mpeg',
    # webm
    'video/webm': '.webm',
    # ogg
    'video/ogg': '.ogg',
    # 3gp
    'video/3gpp': '.3gp',
    # 3g2
    'video/3gpp2': '.3g2',
    # wmv
    'video/x-ms-wmv': '.wmv',
    # flv
    'video/x-flv': '.flv',
    # mov
    'video/quicktime': '.mov',
}


class FileUpload:
    """FileUpload Class"""

    def optimize_image(self, file_path: str, data: str = None, public_id: str = None) -> Dict[str, any]:
        """Optimize image"""
        response = {}
        if data is not None:
            public_id = public_id or ''.join(
                choice(ascii_letters) for _ in range(50))
            try:
                data = parse(data)
                if data.media_type in media_types:
                    # if file is image, then optimize
                    with open(tmp_file_name, 'wb') as f:
                        f.write(data.data)
                    image = Image.open(tmp_file_name)
                    image.convert('RGB').save(
                        tmp_file_name, format='JPEG', optimized=True)
                    with open(tmp_file_name, 'rb') as f:
                        data = f.read()
                    buffer = BytesIO(data)
                    remove(tmp_file_name)
                    response = {
                        "data": buffer,
                        "file_name": ''.join(public_id.split('.')[0]) + '.jpg',
                        "content_length": buffer.getbuffer().nbytes,
                        "content_type": "image/jpeg",
                    }
                else:
                    # if file is not image, then return data
                    buffer = BytesIO(data.data)
                    response = {
                        "data": buffer,
                        "file_name": public_id + media_extensions.get(data.media_type),
                        "content_length": buffer.getbuffer().nbytes,
                        "content_type": data.media_type,
                    }
            except Exception as e:
                raise ValueError('Error Processing data: ' + str(e))
        else:
            file = open(file_path, 'rb')
            buffer = BytesIO(file.read())
            file.close()
            response = {
                "data": buffer,
                "file_name": file_path.split('/')[-1],
                "content_length": buffer.getbuffer().nbytes,
                "content_type": None,
            }

        return response
