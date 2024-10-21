import random
import pygame
import math

# Pygame窗口大小
WIDTH = 800
HEIGHT = 600

# Boid类，表示个体
class Boid:
    def __init__(self):
        # 初始化随机位置和速度
        self.position = [random.uniform(0, WIDTH), random.uniform(0, HEIGHT)]
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.acceleration = [0, 0]
        self.max_speed = 4
        self.max_force = 0.1
        self.perception_radius = 50

    # 更新位置
    def update(self):
        # 更新速度、加速度
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        # 限制最大速度
        speed = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        if speed > self.max_speed:
            self.velocity[0] = (self.velocity[0] / speed) * self.max_speed
            self.velocity[1] = (self.velocity[1] / speed) * self.max_speed

        # 更新位置
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # 清除加速度
        self.acceleration = [0, 0]

    # 边界检测
    def edges(self):
        if self.position[0] > WIDTH:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = WIDTH
        if self.position[1] > HEIGHT:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = HEIGHT

    # 加速度的累加
    def apply_force(self, force):
        self.acceleration[0] += force[0]
        self.acceleration[1] += force[1]

    # 三个规则：分离、对齐、凝聚
    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)

        # 应用每个行为的加速度
        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)

    # 对齐行为：与邻居的平均速度对齐
    def align(self, boids):
        avg_velocity = [0, 0]
        total = 0
        for boid in boids:
            if boid != self and self.distance(boid) < self.perception_radius:
                avg_velocity[0] += boid.velocity[0]
                avg_velocity[1] += boid.velocity[1]
                total += 1
        if total > 0:
            avg_velocity[0] /= total
            avg_velocity[1] /= total

            # 调整速度差异
            avg_velocity[0] -= self.velocity[0]
            avg_velocity[1] -= self.velocity[1]

            # 限制最大加速度
            speed = math.sqrt(avg_velocity[0] ** 2 + avg_velocity[1] ** 2)
            if speed > self.max_force:
                avg_velocity[0] = (avg_velocity[0] / speed) * self.max_force
                avg_velocity[1] = (avg_velocity[1] / speed) * self.max_force
        return avg_velocity

    # 凝聚行为：向邻居的平均位置靠拢
    def cohere(self, boids):
        avg_position = [0, 0]
        total = 0
        for boid in boids:
            if boid != self and self.distance(boid) < self.perception_radius:
                avg_position[0] += boid.position[0]
                avg_position[1] += boid.position[1]
                total += 1
        if total > 0:
            avg_position[0] /= total
            avg_position[1] /= total

            # 计算向平均位置的方向
            desired = [avg_position[0] - self.position[0], avg_position[1] - self.position[1]]

            # 限制最大加速度
            speed = math.sqrt(desired[0] ** 2 + desired[1] ** 2)
            if speed > self.max_force:
                desired[0] = (desired[0] / speed) * self.max_force
                desired[1] = (desired[1] / speed) * self.max_force
            return desired
        return [0, 0]

    # 分离行为：避免过于靠近邻居
    def separate(self, boids):
        avg_repulsion = [0, 0]
        total = 0
        for boid in boids:
            distance = self.distance(boid)
            if boid != self and distance < self.perception_radius:
                diff = [self.position[0] - boid.position[0], self.position[1] - boid.position[1]]
                diff[0] /= distance
                diff[1] /= distance
                avg_repulsion[0] += diff[0]
                avg_repulsion[1] += diff[1]
                total += 1
        if total > 0:
            avg_repulsion[0] /= total
            avg_repulsion[1] /= total

            # 限制最大加速度
            speed = math.sqrt(avg_repulsion[0] ** 2 + avg_repulsion[1] ** 2)
            if speed > self.max_force:
                avg_repulsion[0] = (avg_repulsion[0] / speed) * self.max_force
                avg_repulsion[1] = (avg_repulsion[1] / speed) * self.max_force
        return avg_repulsion

    # 计算与另一Boid的距离
    def distance(self, boid):
        return math.sqrt((self.position[0] - boid.position[0]) ** 2 + (self.position[1] - boid.position[1]) ** 2)


# 初始化Boids群体
boids = [Boid() for _ in range(100)]

# Pygame设置
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    screen.fill((0, 0, 0))

    for boid in boids:
        boid.edges()  # 边界处理
        boid.flock(boids)  # 应用Boids规则
        boid.update()  # 更新位置和速度

        # 在屏幕上绘制Boid
        pygame.draw.circle(screen, (255, 255, 255), (int(boid.position[0]), int(boid.position[1])), 5)

    pygame.display.flip()
    clock.tick(60)

    # 事件处理（关闭窗口）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
