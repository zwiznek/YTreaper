# -*- coding: utf-8 -*-
"""
Created on  Jul 13 07:37:55 2021

@author: z.czaplinski
"""
#importing packages:
import tkinter as tk
from tkinter import filedialog
import os
from pytube import YouTube
from moviepy.editor import *

#variables for start:
url = ""
direc = os.getcwd()

#class for program window: 
class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("YTreaper")
        self.grid()
        self.widgets()
        
    def widgets(self):
        
        self.label_URL= tk.Label(root,text="URL adress of video:")
        self.label_URL.grid()
               
        self.entry_URL = tk.Entry(root)
        self.entry_URL.grid()
        
        self.label_format = tk.Label(root, text="Choose format of file: ")
        self.label_format.grid()
        
        self.option = tk.StringVar()
        self.option.set(value=".mp4")
        
        self.r_button_mp4 = tk.Radiobutton(root, text ="MP4", var=self.option, value=".mp4", command=None)
        self.r_button_mp4.grid()
        
        self.r_button_mp3 = tk.Radiobutton(root, text ="MP3", var=self.option, value=".mp3", command=None)
        self.r_button_mp3.grid()
       
        self.r_button_wav = tk.Radiobutton(root, text ="WAV", var=self.option, value=".wav", command=None)
        self.r_button_wav.grid()
        
        self.label_direction=tk.Label(root, text="Where to save it?")
        self.label_direction.grid()
        
        self.entry_dir = tk.Entry(root)
        self.entry_dir.insert(0, direc)
        self.entry_dir.grid()
        
    
        self.button_dir = tk.Button(root, text ="Direction", command=self.get_dir)
        self.button_dir.grid()
        
        self.button_download = tk.Button(root, text ="DOWNLOAD", command=self.downloading)
        self.button_download.grid()
        
    #changing dir where save output:
    def get_dir (self):
        
        self.entry_dir.delete(0,'end')
        direc=tk.filedialog.askdirectory()
        self.entry_dir.insert(0, direc)
        
        
    def downloading (self):
       
        #getting input from user
        url = self.entry_URL.get()
        opt = self.option.get()
        direc = self.entry_dir.get()
        
        if os.path.exists(direc)==False:
            os.mkdir(direc)
       
        #uploading URl of YT file and preparing name:
        yt =YouTube(url)
        name=yt.title
        name = name.replace(r'/' , " ")
        name+= opt
      
            
        if opt == ".mp3" or opt == ".wav": 
            
            #dowload temporary file and convert it:
            videoa=yt.streams.filter(only_audio=True, file_extension='mp4').first().download(filename="tem_file")
            ad = AudioFileClip(r"tem_file.mp4")
            ad.write_audiofile(os.path.join(direc, name))
           
            ad.close()
            os.remove(r"tem_file.mp4")
            
            
        elif opt == ".mp4":
            
            #dowload  video and audio file separately for better resolution
            video_v=yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first().download(filename="v")
            audio_a=yt.streams.filter(only_audio=True,file_extension='mp4').first().download(filename="a")
            
            #adding audio to video
            a=AudioFileClip(r"a.mp4")
            v=VideoFileClip(r"v.mp4")
            v.set_audio(a).write_videofile(os.path.join(direc, name))
            
            a.close()
            v.close()
            
            os.remove(r"a.mp4")
            os.remove(r"v.mp4")
            
            
    
root = tk.Tk()

app = Application(master=root)
app.mainloop()