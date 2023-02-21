import pygame
from pygame.math import Vector2
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, LINE_COLOR, EDITOR_DATA
from menu import Menu
from timer import Timer


class Editor:
	def __init__(self) -> None:
		self.display_surface = pygame.display.get_surface()

		self.origin = Vector2()
		self.pan_active = False
		self.pan_offset = Vector2()

		self.gridlines_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.gridlines_surface.set_colorkey('green')
		self.gridlines_surface.set_alpha(20)

		self.selected_index = 2
		self.menu = Menu()

		self.canvas_data = {}
		self.changed_cell = Timer(200)

	def pan_screen(self, events: list[pygame.event.Event]) -> None:
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
				self.pan_active = True
				self.pan_offset = Vector2(pygame.mouse.get_pos()) - self.origin

			if not pygame.mouse.get_pressed()[1]:
				self.pan_active = False

			if event.type == pygame.MOUSEWHEEL:
				if pygame.key.get_pressed()[pygame.K_LCTRL]:
					self.origin.y += event.y * 50
				else:
					self.origin.x -= event.y * 50

			if self.pan_active:
				self.origin = Vector2(pygame.mouse.get_pos()) - self.pan_offset

	def draw_gridlines(self) -> None:
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

	def change_selected_index(self, events: list[pygame.event.Event]) -> None:
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					self.selected_index += 1
				elif event.key == pygame.K_LEFT:
					self.selected_index -= 1
				if self.selected_index < 2:
					self.selected_index = 18
				elif self.selected_index > 18:
					self.selected_index = 2

	def menu_click(self, events: list[pygame.event.Event]):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(pygame.mouse.get_pos()):
				self.selected_index = self.menu.click(mouse_pos=pygame.mouse.get_pos(), mouse_button=pygame.mouse.get_pressed())

	def get_current_cell(self) -> tuple[int, int]:
		vector_to_origin = Vector2(pygame.mouse.get_pos()) - self.origin

		x = int(vector_to_origin.x / TILE_SIZE)
		if vector_to_origin.x < 0:
			x -= 1

		y = int(vector_to_origin.y / TILE_SIZE)
		if vector_to_origin.y < 0:
			y -= 1

		return x, y

	def handle_canvas_click(self, events: list[pygame.event.Event]) -> None:
		if pygame.MOUSEBUTTONDOWN in [event.type for event in events]:
			if pygame.mouse.get_pressed()[0] and not self.menu.rect.collidepoint(pygame.mouse.get_pos()):  # and not self.changed_cell.active:
				cell = self.get_current_cell()
				if cell in self.canvas_data:
					self.canvas_data[cell].add_tile_id(self.selected_index)
				else:
					self.canvas_data[cell] = CanvasTile(self.selected_index)
				self.changed_cell.activate()
				for key, value in self.canvas_data.items():
					print(f'{key}: {value.has_terrain}, {value.has_water}')

	def run(self, dt: float, events: list[pygame.event.Event]) -> None:
		self.display_surface.fill('white')
		self.draw_gridlines()

		self.pan_screen(events)

		self.change_selected_index(events)
		self.menu_click(events)
		self.menu.display(self.selected_index)

		pygame.draw.circle(self.display_surface, 'red', self.origin, 10)

		self.handle_canvas_click(events)

		self.changed_cell.update()


class CanvasTile:
	def __init__(self, tile_id: int) -> None:
		self.has_terrain = False
		self.terrain_neighbours = []

		self.has_water = False
		self.water_on_top = False

		self.coin = None

		self.enemy = None

		self.objects = []

		self.add_tile_id(tile_id)

	def add_tile_id(self, tile_id: int) -> None:
		options = {key: value['style'] for key, value in EDITOR_DATA.items()}
		style = options[tile_id]
		match style:
			case 'terrain':
				self.has_terrain = True
			case 'water':
				self.has_water = True
			case 'coin':
				self.coin = tile_id
			case 'enemy':
				self.enemy = tile_id

