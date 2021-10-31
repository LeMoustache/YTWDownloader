from youtube_dl import YoutubeDL
from fastapi.staticfiles import StaticFiles
import os

URLs = []
global video_title 

def DownloadVideo(UrlDowload):
    
    if os.path.exists("DownloadableFile.mp4"):
        os.remove("DownloadableFile.mp4")
        
    global video_title
    #ChosenDirectory = FileLocationInput.get()
    
    #if ChosenDirectory != "" and ChosenDirectory != ChosenLang[1]:
    #    location = ChosenDirectory
    
    ydl_opts = {
    'no-playlist': True,
    'updatetime': False,
    'format': 'bestvideo[ext!=webm][vcodec!*=av01]+bestaudio[ext!=webm]‌​/best[ext!=webm]',
  	#'outtmpl': '%(title)s.%(ext)s',
    'outtmpl': "DownloadableFile"+'.%(ext)s'
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(UrlDowload)
        video_title = info_dict.get('title', None)+".mp4"
    
    URLs.pop(0)
    #print(URLs)
    #print("FASDKJSDALKJSDALKDASJNLASDK")
    
def SoundDownload(UrlDowload):
    
    if os.path.exists("DownloadableFile.mp3"):
        os.remove("DownloadableFile.mp3")
    
    global video_title
    
    ydl_opts = {
    'updatetime': False,
    'format': 'bestaudio/best',
    #'outtmpl': '%(title)s.%(ext)s', 
    'outtmpl': "DownloadableFile"+'.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }]
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(UrlDowload)
        video_title = info_dict.get('title', None)+".mp3"
        
    URLs.pop(0)
    #print(URLs)
    #print("FASDKJSDALKJSDALKDASJNLASDK")


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Video(BaseModel):
    ##VideoID: str
    action: str
    url: str
    ##name: str

@app.get("/lol")
async def main():
    return {"VideoName":""}

@app.get("/video")
def get_Video():
    #print(URLs)
    return URLs

@app.get("/video/{video_id}")
def read_root(URL: str, request: Request):
    client_host = request.client.host
    print(client_host, URL)

@app.get("/video/{video_id}")
def get_VideoId(video_id: int):
    return URLs[video_id-1]

@app.post("/video")
def add_Video(VideoList: Video): #, action: Action
    #print(VideoList)
    #print(Video)      
    URLs.append(VideoList.dict())
    #print(URLs)
    #print(URLs[0])
    
    if URLs[0].get("action") == "Video":
        #print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        DownloadVideo(URLs[0].get("url"))
    else:
        #print("no")
        SoundDownload(URLs[0].get("url"))
        
    #return URLs[-1]
    return []
    
@app.delete("/video/{video_id}")
def delete_video(video_id: int):
    URLs.pop(video_id-1)
    return {}



app.mount("/", StaticFiles(directory="html", html=True), name="html")
