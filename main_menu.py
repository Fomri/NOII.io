import pygame
import client
from settings import *

icon= pygame.image.load("pictures/icon.png")

pygame.init()

screen = pygame.display.set_mode(VIEW_SIZE) 
pygame.display.set_caption('NOII.io')
pygame.display.set_icon(icon)

base_font = pygame.font.Font(None, 32) 
user_text = '' 

input_rect = pygame.Rect(640, 450, 200, 65)
color_active = pygame.Color('lightskyblue3') 
color_passive = pygame.Color('chartreuse4') 
color = color_passive 
active = False

nameWriten = False
user_text = "Enter Name"

bg = pygame.image.load("pictures/bg.png")

play_button = pygame.Rect(450, 250, 200, 65)

running = True
clock = pygame.time.Clock()
while running:
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT:
			running = False
			break

		if event.type == pygame.MOUSEBUTTONDOWN: 
			if input_rect.collidepoint(event.pos): 
				active = not active
			else: 
				active = False
			if(play_button.collidepoint(event.pos)):
				if(nameWriten):
					client.main(user_text)
				else:
					client.main('')

		if event.type == pygame.KEYDOWN and active: 
			if(not nameWriten):
				user_text = ""
			nameWriten = True
			if event.key == pygame.K_BACKSPACE: 
				user_text = user_text[:-1] 
			else: 
				user_text += event.unicode
			if(user_text == ""):
				nameWriten = False
				user_text = "Enter Name"

	screen.fill((255, 255, 255)) 

	if active: 
		color = color_active 
	else: 
		color = color_passive 

	pygame.draw.rect(screen, color, input_rect) 
	text_surface = base_font.render(user_text, True, (255, 255, 255)) 
	screen.blit(text_surface, (input_rect.centerx - text_surface.get_width() / 2, input_rect.centery - base_font.get_ascent() / 2)) 
	play_surface = base_font.render("Play Game", True, (255, 255, 255))
	pygame.draw.rect(screen, color_passive, play_button) 
	screen.blit(play_surface, (640 - play_surface.get_width() / 2, 450 - base_font.get_ascent() / 2)) 

	input_rect.w = max(140, text_surface.get_width()+10)
	input_rect.center = (VIEW_SIZE[0] / 2, VIEW_SIZE[1] / 2.88)
	play_button.w = play_surface.get_width() + 10
	play_button.center = (VIEW_SIZE[0] / 2, VIEW_SIZE[1] / 1.6)
	screen.blit(bg, (0, 0))
	pygame.display.flip() 
	clock.tick(30)

pygame.quit()
