import os
import uuid
from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi.responses import FileResponse

router = APIRouter(
prefix= '/file',
tags= ['file']
)

@router.post('/file')
def get_file(file: bytes = File(...)): # type: ignore
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {'lines': lines}

#@router.post('/uploadfile')
#def get_uploadfile(upload_file: UploadFile = File(...)): # type: ignore
#    path = f"files/{upload_file.filename}"
#    with open(path, 'w+b') as buffer:
#        shutil.copyfileobj(upload_file.file, buffer)

#    return{
#        'filename': path,
#         'type': upload_file.filename
#    }

@router.post('/uploadfile')
def get_uploadfile(upload_file: UploadFile = File(...)):
    # Generate a unique identifier
    unique_id = str(uuid.uuid4())
    
    # Extract the file extension
    filename, file_extension = os.path.splitext(upload_file.filename) # type: ignore
    
    # Create a new filename with the unique identifier
    new_filename = f"{filename}_{unique_id}{file_extension}"
    
    path = os.path.join("files", new_filename)
    
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return {
        "filename": new_filename
            
            }

@router.get('/download{name}', response_class=FileResponse)
def get_file(name: str):
    path = f'files/{name}'
    return path