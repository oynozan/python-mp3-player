#Imports
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from os import listdir, getcwd, path
import operate

#Operate Class
o = operate.Operate()

#Helpful Functions
def rgb(c):
	return "#%02x%02x%02x" % c

#Variables
currentSong = ""
selected_song = ""
canvasWidth = 375
canvasHeight = 150
stopCounter = 0
preVolume = 0
currentVolume = 100
darkBlue = rgb((4,6,18))

#Button Functions
def playButton(isNext=False):
	global currentSong, song_text_on_canvas, song_text_coords
	#If next song button is not clicked yet
	if (not isNext):
		#Assign the selected song (in listbox) to current song
		currentSong = selected_song
	#Remove canvas text
	player_background.delete(song_text_on_canvas)
	#Add canvas text
	song_text_on_canvas = player_background.create_text(0,0,text="Current Song: {}".format(currentSong),font=("Helvetica", 11, "bold"),fill="white")
	song_text_coords = player_background.bbox(song_text_on_canvas) #Current Canvas Text Position
	player_background.coords(song_text_on_canvas,song_text_coords[2],song_text_coords[3]) #Set Text Position Top Left Corner of Canvas
	#Call Play func from Operate Class
	o.play(currentSong)

def stopButton():
	global stopCounter
	stopCounter+=1
	o.stop(stopCounter)
	if (stopCounter==2):
		stopCounter=0

def nextSongButton():
	global currentSong
	try:
		#Next Song
		currentSong = songs[songs.index(currentSong)+1]
	except:
		#If the song was last of list, select the song which is start of list
		currentSong = songs[0]
	#Play the next song
	playButton(True)

#Slider
def volumeChange(val):
	global preVolume, currentVolume
	currentVolume = val #Get Volume Value from Slider
	if (currentVolume != preVolume): #If Volume Changed
		o.volume(currentVolume) #Change Volume from Operate Class
	preVolume = currentVolume #Update Previous Volume

def updateSongs():
	global songs, songList
	#List of Songs
	songs = []
	for file in listdir(getcwd()+"/"+"songs"):
		#Add all the songs in "songs" directory
		if (".mp3" in file):
			songs.append(file)

	songList = Listbox(root, highlightthickness=0, bg=darkBlue, fg="white") #List of Songs Widget
	for file in songs:
		#Add name of files to Song List widget
		songList.insert('end',file)

#Root Settings
root = Tk()
root.title("dehdul Player")
root.resizable(False,False)
root.configure(bg=darkBlue)

#Player Image
player_image = ImageTk.PhotoImage(Image.open(getcwd()+"/assets/player-background.png"))

#Button Images
play_button_image = ImageTk.PhotoImage(Image.open(getcwd()+"/assets/play-button.png"))
stop_button_image = ImageTk.PhotoImage(Image.open(getcwd()+"/assets/stop-button.png"))
next_button_image = ImageTk.PhotoImage(Image.open(getcwd()+"/assets/next-button.png"))

#WIDGETS

#Player Background
player_background = Canvas(root, width=canvasWidth,height=canvasHeight,highlightthickness=0) #Canvas
player_background.grid(row=0,column=0,columnspan=4,pady=5) #Canvas Position
player_background.create_image(375/2, 150/2, image=player_image)#Canvas Background
song_text_on_canvas = player_background.create_text(0,0,text="Current Song: {}".format(currentSong),font=("Helvetica", 11, "bold"),fill="white") #Canvas Text
song_text_coords = player_background.bbox(song_text_on_canvas) #Current Canvas Text Position
player_background.coords(song_text_on_canvas,song_text_coords[2],song_text_coords[3]) #Set Text Position Top Left Corner of Canvas

#Play Button
play_button = Button(root,highlightthickness=0,borderwidth=0,image=play_button_image,compound=TOP, command=playButton)
play_button.grid(row=1,column=1)

#Stop Button
stop_button = Button(root,highlightthickness=0,borderwidth=0,image=stop_button_image,compound=TOP, command=stopButton)
stop_button.grid(row=1,column=0)

#Next-Song Button
next_song_button = Button(root,highlightthickness=0,borderwidth=0,image=next_button_image,compound=TOP, command=nextSongButton)
next_song_button.grid(row=1,column=2)

#Volume Slider
volume_slider = Scale(orient="horizontal",
	bg=rgb((4,6,17)),
	activebackground=rgb((0,0,0)),
	fg="white",
	troughcolor=darkBlue,
	command=volumeChange)
volume_slider.grid(row=1,column=3)
volume_slider.set(100)

updateSongs()

#Update Selected Song
def updateSelectedSong(auto_bind_parameter):
	global selected_song
	selected_song = songList.get(ACTIVE)
	selected_song_label["text"] = "Selected Song: {}".format(selected_song)

songList.grid(row=2,column=0, columnspan=4, sticky="W", ipadx=130, pady=3)

#If double clicked on song in listbox, call the updateSelectedSong function
songList.bind('<Double-Button>', updateSelectedSong)

#Selected Song
selected_song_label = Label(root, text="", fg="white", bg=darkBlue)
selected_song_label.grid(row=3,column=0, columnspan=4, sticky="W")

#!WIDGETS!

root.mainloop()
