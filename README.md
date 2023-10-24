# MinIO File Uploader (Abstraction)

The MinIO File Uploader (Abstraction) is a Python-based project designed to simplify the process of uploading various file types (e.g., PDFs, DOCs, images) to a MinIO server and obtaining public URL links for easy sharing and access. This project abstracts the interaction with MinIO, making it easier for developers to integrate file uploading functionality into their applications.

MinIO is a high-performance, distributed object storage server, and this project leverages the MinIO client library to facilitate file uploads. With this tool, you can quickly and easily upload files to a MinIO server and generate public URL links to share with others.

> This docs did not include a detailed instruction on how to setup MinIO on your machine.

### Environment setup

`.env` is required at the project root with the following params

```
PROJECT_SHORT_NAME=test # optional

MINIO_HOST=someminiourl.com
MINIO_ACCESS_KEY=someaccesskey
MINIO_SECRET_KEY=somesecretkey
```

Furthermore, the code within `main.py` is flexible and can be placed in any part of your project. You can instantiate the MinIO class to upload your documents wherever it's suitable. For optimal performance, it is advisable to create a new instance for each thread when working in a multithreading environment.

### Usecase

```python
from main import cloud
cloud.upload_file(file_path='img.png')
# {'url': 'https://someminiourl.com/test-b/img.png', 'public_id': 'img.png'}

from datauri import parse
with open('img.png', 'rb') as f:
    data = f.read()

from base64 import b64encode
data[:10] # b'\x89PNG\r\n\x1a\n\x00\x00'
data = b64encode(data)
data[:10] # b'iVBORw0KGg'
img = b'data:image/png;base64,' + data
img[:30] # b'data:image/png;base64,iVBORw0K'

cloud.upload_file(data=img.decode('utf-8'))
# {'url': 'https://someminiourl.com/test-b/BADDetnPKBUkUxDllTUc-e216010e-44d3-4509-b765-74774d4e4542.png', 'public_id': 'BADDetnPKBUkUxDllTUc-e216010e-44d3-4509-b765-74774d4e4542.png'}
```

> Please note that the token was intentionally removed, to effectively use this class, you'd need to configure anonymous access to read contents of your bucket from MinIO bucket configuration. Further updates to this repository will include the configuration while creating the bucket.
