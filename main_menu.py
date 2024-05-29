import pygame
import client

pygame.init()

screen = pygame.display.set_mode((500, 500)) 

base_font = pygame.font.Font(None, 32) 
user_text = '' 

input_rect = pygame.Rect(200, 100, 140, 32)

color_active = pygame.Color('lightskyblue3') 

color_passive = pygame.Color('chartreuse4') 
color = color_passive 
active = False

nameWriten = False
user_text = "Enter Name"

play_button = pygame.Rect(200, 250, 140, 32)

running = True

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
	screen.blit(play_surface, (250 - play_surface.get_width() / 2, 250 - base_font.get_ascent() / 2)) 

	input_rect.w = max(140, text_surface.get_width()+10)
	input_rect.center = (250, 100)
	play_button.w = play_surface.get_width() + 10
	play_button.center = (250, 250)
	pygame.display.flip() 

pygame.quit()