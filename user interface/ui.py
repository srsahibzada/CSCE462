'''
CSCE 462 Final Project
Laser Harp and Harp Emulator
Katherine Click (Computer Engineering '16), Sijine Roh (Computer Engineering '16) 
and Sarah Sahibzada (Computer Science, Applied Mathematics '16)

'''


import pygame
import pygame.mouse
from pygame.event import *
from pygame.locals import *
from pygame.mixer import *
import math
import os, sys

import play_wav
import pysynth, pysynth_b, pysynth_s
import wave
import string

class major_tuning:
	c_major = ['c','d','e','f','g','a','b','c5', 'd5', 'e5', 'f5', 'g5','a5', 'b5', 'c6']
	c_sharp_major = ['c#', 'd#', 'f', 'f#', 'g#', 'a#', 'c5', 'c#5', 'd#5', 'f5', 'f#5', 'g#5', 'a#5', 'c6','c#6']
	d_major = ['d','e','gb','g','a','b','c#5','d5','e5', 'gb5', 'g5','a5','b5','c#6','d6' ]
	e_flat_major = ['eb','f','g','ab','bb','c5','d5','eb5','f5','g5','ab5','bb5','c6','d6','eb6']
	f_major = ['f','g','a','bb','c5','d5','e5','f5','g5','a5','bb5','c6','d6','e6','f6']
	g_major = ['g','a','b','c5','d5','e5','f#5','g5', 'a5','b5','c5','d5','f#5', 'g6']

	''' 
		2 small issues that keep this from being done asap:
		i need to test for equivalence in notes because it will only accept one and not the other
		for instance b# == c but this program does not accept b#
		and fixing that owuld entail modifying the library

		also unless someone has a text list of these i've been typing them out >_<
	'''

class minor_tuning:
	a_minor = ['a','b','c5','d5','e5','f5','g5','a5','b6','c6','d6','e6','f6','g6','a6']
	g_minor = ['g','a','a#', ]
class player:
#this borrows heavily from menv.py in the pysynth distribution
#credit to pranav ravichandran (me@onloop.net), author of menv.py 
	synth_params = []
	trash_file = True
	out_file = ''

	def remove_file(self, out_file):
		if self.out_file == '':
			self.out_file = 'temp.wav'
		if self.trash_file:
			#print 'taking out the trash'
			os.remove(self.out_file)
			self.out_file = ''

	def play(self, out_file):
		if self.out_file == '':
			self.out_file = 'temp.wav'
		a = play_wav.Sound()
		a.playFile(out_file)
		self.remove_file(self.out_file)
		del self.synth_params[:]

	def synth_sound(self, render_sound):
		if self.out_file == '':
			self.out_file = 'temp.wav'
		render_sound.make_wav(self.synth_params, fn=self.out_file,silent=True)
	def queue_note(self,note):
		self.synth_params.append((note,3)) #writes wav file-- impossible to get correct note in real time

class harp_constructs:
	tuning = major_tuning.c_major
	major = True



origin = 0,0
class colors():
	#http://cloford.com/resources/colours/500col.htm
	black = 0,0,0
	white = 255,255,255
	green = 0,255,0
	red = 255,0,0
	blue = 0,0,255
	gray = 54,54,54
	chartreuse = 113,198,113
	seagreen = 0,250,154
	gold = 	218,165,32
			

class intro_window():
	def __init__(self):
		pygame.init()
		pygame.font.init()
		screen=pygame.display.set_mode((400,400),HWSURFACE|DOUBLEBUF|RESIZABLE)
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill(colors.white)
		screen.blit(background,origin)
		welcome_font = pygame.font.Font("freesansbold.ttf", 17)
		list_font = pygame.font.Font("freesansbold.ttf", 12)
		welcome_message = welcome_font.render("Welcome to the Laser Harp Demo!", 1, colors.black)
		item_0 = list_font.render("We hope you are excited about your new Laser Harp!",1,colors.black)
		item_1 = list_font.render("Try the harp",1,colors.blue)
		item_2 = list_font.render("Instructions",1,colors.blue)
		screen.blit(welcome_message,(50,10))
		screen.blit(item_0,(50,50))
		screen.blit(item_1,(50,70))
		screen.blit(item_2,(50,90))

		pygame.display.flip()
		#so many magical constants TT_TT i am sorry
		while 1:
			event = pygame.event.wait()
			if event.type == pygame.QUIT :
					return
			elif event.type == VIDEORESIZE: 
				surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
			elif event.type == pygame.MOUSEBUTTONDOWN:
					x,y = event.pos
					if (x >= 50 and x <= 100) and (y > 65 and y <= 85):
						main_window()
					elif (x >= 50 and x <= 100) and (y > 85 and y <= 105):
						return
					'''message = intro_font.render("Some text!", 1, (255,255,0))
					screen.blit(message,(100,100))'''


class main_window():
	def __init__(self):

		pygame.init()
		pygame.font.init()
        #pic = pygame.image.load('stock_photo_of_a_picture_frame.jpg')
        #the (resizable) window
		pygame.display.set_caption('Laser Harp Computer Demo')
		screen = pygame.display.set_mode((1200,800),HWSURFACE|DOUBLEBUF|RESIZABLE)
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill(colors.white)
		screen.blit(background,origin)
        #the harp
		harp = pygame.Surface((600,600))
		harp.fill(colors.gold)
		innerharp = pygame.Surface((500,500))
		innerharp.fill(colors.white)	
		screen.blit(harp,(300,100))
		screen.blit(innerharp,(350,150))
		#set defaults for harp -- scales and stuff
		'''scale_title_font = pygame.font.Font("freesansbold.ttf", 13)
		scale_label_font = pygame.font.Font("freesansbold.ttf", 7)
		scale_title_font.render("Major Scales",1,colors.black)
		screen.blit(scale_title_font,())'''
		for i in range(15):
					if i % 2 == 0:
						pygame.draw.lines(screen,colors.seagreen,False,[(380+30*i, 150),(380+30*i,650)],10)
					else:
						pygame.draw.lines(screen,colors.chartreuse,False,[(380+30*i, 150),(380+30*i,650)],10)

		'''volume_control = pygame.Surface((250,200))
		volume_control.fill(colors.blue)
		screen.blit(volume_control,(950,600))'''
		pygame.display.flip()
		while 1:
			event = pygame.event.wait()
			if event.type == pygame.QUIT :
					return
			elif event.type == VIDEORESIZE: #still kind of buggy but oh well
				surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
				background = pygame.Surface(screen.get_size())
				background = background.convert()
				background.fill(colors.white)
				screen.blit(background,origin)
				harp = pygame.Surface((600,600))
				harp.fill(colors.black)
				innerharp = pygame.Surface((500,500))
				innerharp.fill(colors.white)	
				screen.blit(harp,(300,100))
				screen.blit(innerharp,(350,150))
				for i in range(15):
					if i % 2 == 0:
						pygame.draw.lines(screen,colors.seagreen,False,[(380+30*i, 150),(380+30*i,650)],10)
					else:
						pygame.draw.lines(screen,colors.chartreuse,False,[(380+30*i, 150),(380+30*i,650)],10)


				pygame.display.flip()
			elif event.type == MOUSEBUTTONDOWN:
				x,y = event.pos
				print x, y
				if (x >= 380 and x <= 800) and (y >= 150 and y <= 650):
					if x >= 380 and x <= 390:
						a = player()
						pygame.draw.lines(screen,colors.red,False,[(380+30*x, 150),(380+30*x,650)],10)
						pygame.display.flip()
						a.queue_note(harp_constructs.tuning[0])
						print harp_constructs.tuning[0]
						a.synth_sound(pysynth)
						#print a.out_file + "!"
						a.play(a.out_file)
						
					else:
						note = (x - 370) / 30        
						a = player()
						pygame.draw.lines(screen,colors.red,False,[(380+30*x, 150),(380+30*x,650)],10)
						pygame.display.flip()
						a.queue_note(harp_constructs.tuning[note])
						print harp_constructs.tuning[note]
						a.synth_sound(pysynth)
						#print a.out_file + "!"
						a.play(a.out_file)
					pygame.display.flip()
						




def main():
	intro_window()


main()

