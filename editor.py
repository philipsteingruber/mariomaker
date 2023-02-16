import pygame
import sys
from pygame.math import Vector2
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, LINE_COLOR


class Editor:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.origin = Vector2()
		self.pan_active = False
		self.pan_offset = Vector2()

		self.gridlines_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.gridlines_surface.set_colorkey('green')
		self.gridlines_surface.set_alpha(20)

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			self.pan_screen(event)

	def pan_screen(self, event):

		if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
			self.pan_active = True
			self.pan_offset = Vector2(pygame.mouse.get_pos()) - self.origin

		if not pygame.mouse.get_pressed()[1]:
			self.pan_active = False

		if event.type == pygame.MOUSEWHEEL:
			if pygame.key.get_pressed()[pygame.K_LCTRL]:
				self.origin.y -= event.y * 50
			else:
				self.origin.x -= event.y * 50

		if self.pan_active:
			self.origin = Vector2(pygame.mouse.get_pos()) - self.pan_offset

	def draw_gridlines(self):
		cols = WINDOW_WIDTH // TILE_SIZE
		rows = WINDOW_HEIGHT // TILE_SIZE

		origin_offset = Vector2(
			x=self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
			y=self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE)

		self.gridlines_surface.fill('green')

		for col in range(cols + 1):
			x = origin_offset.x + col * TILE_SIZE
			pygame.draw.line(self.gridlines_surface, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

		for row in range(rows + 1):
			y = origin_offset.y + row * TILE_SIZE
			pygame.draw.line(self.gridlines_surface, LINE_COLOR, (0, y), (WINDOW_WIDTH, y))

		self.display_surface.blit(self.gridlines_surface, (0, 0))

	def run(self, dt):
		self.event_loop()

		# drawing
		self.display_surface.fill('white')
		self.draw_gridlines()
		pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
