import os
from pytube import YouTube
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #root
        self.title("VocalRemover")
        self.geometry("600x100")
        self.resizable(False, False)
        #label
        self.label = tk.Label(self, text="Type in url", font=35, fg="black")
        self.label.pack()
        #textBox
        self.textBox = tk.Text(self, font = 50, width=48, height=1)
        self.textBox.pack()
        #button
        self.button = tk.Button(self, text="Download", width=8, command=self.initiate_downloading)
        self.button.pack()
        self.mainloop()

    def initiate_downloading(self):
        url = self.textBox.get("1.0",'end-1c')
        audo_file_name = self.download_mp3(url)
        if(audo_file_name != None):
            self.separete(audo_file_name)
            #deleting original mp3 file
            os.remove(audo_file_name)

    def download_mp3(self, url):
        try:
            yt = YouTube(url)
            self.label.config(text = "Downloading...")
            self.update()
            self.after(200)
            stream = yt.streams.get_audio_only()
            stream.download()
        except Exception as e:
            self.label.config(text = type(e).__name__)
        else:
            self.label.config(text = "Downloaded!")
            self.update()
            self.after(200)
            return stream.default_filename

    def separete(self, audo_file_name):
        self.label.config(text = "Separating...")
        self.update()
        self.after(200)
        separator = Separator('spleeter:2stems')
        separator.separate_to_file(audo_file_name, './audio')
        self.label.config(text = "Audio separated")


if __name__ == '__main__':
    app = App()
    app.mainloop()

