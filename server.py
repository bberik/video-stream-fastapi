import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn

CHUNK_SIZE = 1024 * 1024  
file_path = r"C:\Users\berik\Desktop\getvideofile.mp4"
file_name = os.path.basename(file_path)
file_size = os.stat(file_path).st_size
app = FastAPI()

@app.get('/getvideofile')
def download_video_file():
    def iterfile():
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(file_path, 'rb') as f:
            i = 0
            while chunk := f.read(CHUNK_SIZE):
                yield chunk

    headers = {'Content-Disposition': f'attachment; filename={file_name}; filesize={file_size}'}
    response = StreamingResponse(iterfile(), headers=headers, media_type='video/mp4')
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)