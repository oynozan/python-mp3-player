from os import getcwd, environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #Hide Welcome Message of pygame
from pygame import mixer

class Operate:
	def __init__(self):
		mixer.init()

	def play(self,song):
		mixer.music.load('{}/songs/{}'.format(getcwd(),song))
		mixer.music.play(1)

	def stop(self,count):
		if (count%2):
			mixer.music.pause()
		else:
			mixer.music.unpause()

	def volume(self,value):
		mixer.music.set_volume(int(value)/100)