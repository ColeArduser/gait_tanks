from level.audio import *
from level.bullet import Bullet


class Tank(pygame.sprite.Sprite):
    def __init__(self, game, image_path, start_pos, start_angle, bullets_group, visual_effects_group, walls):
        super(Tank, self).__init__()
        self.game = game
        self.walls = walls
        self.bullets_group = bullets_group
        self.visual_effects_group = visual_effects_group
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.angle = start_angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=start_pos)
        self.wall_hitbox = self.rect.inflate(-24, -24)
        self.pathfinding_hitbox = self.rect.inflate(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2(0, -1).rotate(-self.angle)
        self.FORWARD_VELOCITY = 4
        self.BACKWARD_VELOCITY = 4
        self.ROTATION_SPEED = 4
        self.shoot_cooldown = 1000
        self.last_shot_time = 0
        load_sounds()

    def rotate(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pathfinding_hitbox.center = self.rect.center
        self.wall_hitbox.center = self.rect.center
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2(0, -1).rotate(-self.angle)

    def move(self, direction, walls):
        if check_tank_moving_sound():
            pass
        else:
            tank_moving_sound()
        new_position = self.rect.copy()
        new_position.move_ip(direction * self.FORWARD_VELOCITY)
        if not self.check_collisions(new_position, walls):
            self.rect = new_position
            self.pathfinding_hitbox.center = self.rect.center
            self.wall_hitbox.center = self.rect.center

    def check_collisions(self, new_rect, walls):
        for wall in walls:
            if new_rect.colliderect(wall):
                return True
        return False

    def render(self, display):
        display.blit(self.image, self.rect.topleft)

    def shoot(self):
        tank_shoot_sound()
        bullet_start_pos = self.rect.center + self.direction * 15
        new_bullet = Bullet(
            self.game,
            self.walls,
            bullet_start_pos,
            self.angle,
            self.visual_effects_group
        )
        self.bullets_group.add(new_bullet)
