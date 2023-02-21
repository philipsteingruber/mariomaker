import pygame
import sys

from editor import Editor
from settings import WINDOW_HEIGHT, WINDOW_WIDTH


class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()

		self.editor = Editor()

		cursor_surface = pygame.image.load('./graphics/cursors/mouse.png').convert_alpha()
		cursor = pygame.cursors.Cursor((0, 0), cursor_surface)
		pygame.mouse.set_cursor(cursor)

	def run(self):
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			dt = self.clock.tick() / 1000
			
			self.editor.run(dt, events)
			pygame.display.update()




if __name__ == '__main__':
	main = Main()
	main.run()
