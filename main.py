import pygame
from utils import load_image, terminate, generate_level, load_level
from startscreen import start_screen
from camera import Camera

FPS = 50
SIZE = WIDTH, HEIGHT = 600, 400
TILE_WIDTH = TILE_HEIGHT = 50
BACKGROUND_COLOR = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Перемещение героя. Новый уровень')
player = None
clock = pygame.time.Clock()


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
obstacles = {'wall'}
player_image = load_image('mario.png')


class MySprite(pygame.sprite.Sprite):
    def __init__(self, vars):
        super().__init__(vars['all_sprites'])

    def move_ip(self, dx, dy, width_map=WIDTH, height_map=HEIGHT):
        self.rect.x += int(round(dx))
        self.rect.y += int(round(dy))
        if self.rect.right < 0:
            self.rect.x += width_map
        if self.rect.left > WIDTH:
            self.rect.x -= width_map
        if self.rect.bottom < 0:
            self.rect.y += height_map
        if self.rect.top > HEIGHT:
            self.rect.y -= height_map


class Tile(MySprite):
    def __init__(self, tile_type, pos_x, pos_y, vars):
        super().__init__(vars)
        vars['tiles_group'].add(self)
        if tile_type in obstacles:
            vars['obstacles_group'].add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Player(MySprite):
    def __init__(self, pos_x, pos_y, vars):
        super().__init__(vars)
        vars['player_group'].add(self)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + (TILE_WIDTH - self.image.get_width()) // 2,
            TILE_HEIGHT * pos_y + (TILE_HEIGHT - self.image.get_height()) // 2
        )


def main():
    global player, level_x, level_y, all_sprites, tiles_group, player_group, obstacles_group

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    obstacles_group = pygame.sprite.Group()
    start_screen(screen)
    # filename = input('Введите название уровня: ')
    filename = 'map.txt'
    player, level_x, level_y = generate_level(load_level(filename), globals())
    camera = Camera(WIDTH, HEIGHT, level_x * TILE_WIDTH, level_y * TILE_HEIGHT)
    camera.add(player)
    camera.add_group(tiles_group)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                old_player_rect = player.rect.copy()
                if event.key == pygame.K_LEFT:
                    player.move_ip(-TILE_WIDTH, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move_ip(TILE_WIDTH, 0)
                elif event.key == pygame.K_UP:
                    player.move_ip(0, -TILE_HEIGHT)
                elif event.key == pygame.K_DOWN:
                    player.move_ip(0, TILE_HEIGHT)
                if pygame.sprite.spritecollideany(player, obstacles_group):
                    player.rect = old_player_rect
        screen.fill(BACKGROUND_COLOR)
        # изменяем ракурс камеры
        camera.update(player)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
