from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root=Tk() 
root.title("MP3 Player")
root.geometry("700x500")

pygame.mixer.init()

def playTime():

    if stopped:
        return

    currentTime=pygame.mixer.music.get_pos()/1000

    convertTime=time.strftime("%M:%S",time.gmtime(currentTime))


    

    song=song_box.get(ACTIVE)
    song=f'/home/ashish/Downloads/{song}.mp3'
    audio=MP3(song)
    global totalTime
    totalTime=audio.info.length
    convertTotalTime=time.strftime("%M:%S",time.gmtime(totalTime))
    currentTime+=1
    
    if int(slider.get())==int(totalTime):
        statusBar.config(text=f'{convertTotalTime}') 
    elif paused:
        statusBar.config(text=f'Paused')

    elif (int(slider.get())==int(currentTime)):
        sliderPosition=int(totalTime)
        slider.config(to=sliderPosition, value=int(currentTime))
        
    else:
        sliderPosition=int(totalTime)
        slider.config(to=sliderPosition, value=int(slider.get()))
        convertTime=time.strftime("%M:%S",time.gmtime(int(slider.get())))
        statusBar.config(text=f'{convertTime}/{convertTotalTime}') 
        nextTime=int(slider.get())+1
        slider.config(value=nextTime)       


    statusBar.after(1000,playTime)



def addSong():
    song=filedialog.askopenfilename(initialdir="/home/ashish",title="Select a file",filetypes=(("mp3 files","*.mp3"),("all files","*.*")))
    song=song.replace("/home/ashish/Downloads/","")
    song=song.replace(".mp3","")
    song_box.insert(END,song)


def deleteSong():
    stopSong()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()        

def deleteAllSong():
    song_box.delete(0,END)
    pygame.mixer.music.stop()

def playSong():
    global stopped 
    stopped=False
    song=song_box.get(ACTIVE)
    song=f'/home/ashish/Downloads/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playTime()

    statusBar.config(text=f'Playing {song}')
    #sliderPosition=int(totalTime)
    #slider.config(to=sliderPosition, value=0)


global stopped
stopped=False

def stopSong():
    statusBar.config(text=f'Stopped')
    slider.config(value=0)

    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    statusBar.config(text=f'Stopped')
    global stopped 
    stopped=True



global paused
paused=False    

def pauseSong(is_paused):
    global paused
    paused=is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused=False
    else:
        pygame.mixer.music.pause()
        paused=True


def nextSong():
    statusBar.config(text=f'Stopped')
    slider.config(value=0)
    nextOne=song_box.curselection()
    nextOne=nextOne[0]+1
    song=song_box.get(nextOne)
    song=f'/home/ashish/Downloads/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0,END)
    song_box.activate(nextOne)
    song_box.selection_set(nextOne,last=None)

def previousSong():
    statusBar.config(text=f'Stopped')
    slider.config(value=0)
    previousOne=song_box.curselection()
    previousOne=previousOne[0]-1
    song_name=song_box.get(previousOne)
    song_name=f'/home/ashish/Downloads/{song_name}.mp3'
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0,END)
    song_box.activate(previousOne)
    song_box.selection_set(previousOne,last=None)


def slide(event):  
    song=song_box.get(ACTIVE)
    song=f'/home/ashish/Downloads/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(slider.get()))
    

def setVolume(event):
    pygame.mixer.music.set_volume(volumeSlider.get())
    currentVolume=pygame.mixer.music.get_volume()
    volumeLabel.config(text=f'{currentVolume*100}%')

masterFrame=Frame(root)
masterFrame.pack(pady=20)




song_box=Listbox(masterFrame,bg="black",fg="white",width=60,selectbackground="gray",selectforeground="white")
song_box.grid(row=0,column=0)

backButtonImg=PhotoImage(file="images/back.png")
playButtonImg=PhotoImage(file="images/play.png")
pauseButtonImg=PhotoImage(file="images/pause.png")
stopButtonImg=PhotoImage(file="images/stop.png")
forwardButtonImg=PhotoImage(file="images/forward.png")

controls_frame=Frame(masterFrame)
controls_frame.grid(row=1,column=0,pady=20)

volumeFrame=LabelFrame(masterFrame,text="Volume")
volumeFrame.grid(row=2,column=0)


backButton=Button(controls_frame,image=backButtonImg,borderwidth=0 ,command=previousSong)
playButton=Button(controls_frame,image=playButtonImg ,borderwidth=0,command=playSong)
pauseButton=Button(controls_frame,image=pauseButtonImg,borderwidth=0,command=lambda:pauseSong(paused))
stopButton=Button(controls_frame,image=stopButtonImg,borderwidth=0,command=stopSong)
forwordButton=Button(controls_frame,image=forwardButtonImg,borderwidth=0,command=nextSong)

backButton.grid(row=0,column=0)
playButton.grid(row=0,column=1)
pauseButton.grid(row=0,column=2)
stopButton.grid(row=0,column=3)
forwordButton.grid(row=0,column=4)

menu=Menu(root)
root.config(menu=menu)

addSongMenu=Menu(menu)
menu.add_cascade(label="Menu",menu=addSongMenu)
addSongMenu.add_command(label="Add Song",command=addSong)

addSongMenu.add_command(label="Remove Song",command=lambda:song_box.delete(ACTIVE))
addSongMenu.add_command(label="Remove All Song",command=lambda:song_box.delete(0,END))


statusBar=Label(root,text="Welcome to MP3 Player",bd=1,relief=GROOVE,anchor=W)
statusBar.pack(fill=X ,side="bottom")


slider=ttk.Scale(masterFrame,from_=0,to=100,orient=HORIZONTAL,value=0,length=360,command=slide)
slider.grid(row=3,column=0,pady=10)

volumeSlider=ttk.Scale(volumeFrame,from_=0,to=1,orient=HORIZONTAL,value=1,length=125,command=setVolume)
volumeSlider.pack(pady=10)
volumeLabel=Label(volumeFrame,text="100.0%",bg="black",fg="white")
volumeLabel.pack(pady=10)

root.mainloop()