import pygame

from bullet import Bullet


class Tank(pygame.sprite.Sprite):
    def __init__(self, screen, image_path, start_pos, start_angle, bullets_group, walls):
        super(Tank, self).__init__()
        self.screen = screen
        self.walls = walls
        self.bullets_group = bullets_group
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.angle = start_angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=start_pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2(0, -1).rotate(-self.angle)
        self.FORWARD_VELOCITY = 5
        self.BACKWARD_VELOCITY = 2
        self.ROTATION_SPEED = 3
        self.shoot_cooldown = 1000
        self.last_shot_time = 0

    def rotate(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2(0, -1).rotate(-self.angle)

    def move(self, direction, walls):
        new_position = self.rect.copy()
        new_position.move_ip(direction * self.FORWARD_VELOCITY)
        if not self.check_collisions(new_position, walls):
            self.rect = new_position

    def check_collisions(self, new_rect, walls):
        for wall in walls:
            if new_rect.colliderect(wall):
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def shoot(self):
        bullet_start_pos = self.rect.center + self.direction * 40
        new_bullet = Bullet(self.screen, self.walls, bullet_start_pos, self.angle)
        self.bullets_group.add(new_bullet)
