The file **server.py** is a RESTful API server implemented with FastAPI. It has single route **GET /getvideofile** that streams a video file to the client.

To run the server:
1. clone this repository to your machine
2. change your directory to video-stream-fastapi/
3. ```pip3 install fastapi uvicorn```
4. ```python server.py```

The file **client.py** is a Python client implemented with **Requests** package and **tqdm** package (for progress bar). It downloads the video file being streamed from the server. 

To run the client:
1. clone this repository to your machine
2. change your directory to video-stream-fastapi/
3. ```pip3 install tqdm request urllib3```
4. ```python client.py```

