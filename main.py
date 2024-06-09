import pygame
import sys
import random
import shutil
import os
from fish import Fish
from plant import Plant
from fisherman import Fisherman
from lake import Lake

# Initialize pygame
pygame.init()

# Set up screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Lake Ecosystem Simulation')

# Define fishing area
fishing_area = (200, 150, 400, 350)

# Clear the /analyze folder
if os.path.exists('analyze'):
    shutil.rmtree('analyze')
os.makedirs('analyze')

# Initialize lake and fisherman
lake = Lake(
    width,
    height,
    [Fish(id=i, energy=100, position=(random.randint(0, width), random.randint(0, height))) for i in range(10)],
    500,
    [Plant(position=(random.randint(0, width), random.randint(0, height))) for _ in range(20)],
    reproduction_interval=10
)
fisherman = Fisherman(probability=0.05, fishing_area=fishing_area)

# Initialize clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            lake.plot_stats()
            lake.plot_time_series()
            sys.exit()

    lake.update()
    fisherman.fish(lake)

    screen.fill((0, 0, 255))
    pygame.draw.rect(screen, (0, 0, 0), fishing_area, 2)
    for fish in lake.fish_population:
        pygame.draw.circle(screen, (255, 255, 255), (int(fish.position[0]), int(fish.position[1])), 5)
    for plant in lake.plants:
        pygame.draw.circle(screen, (0, 255, 0), plant.position, 10)
    for pos, _ in lake.caught_fish_positions:
        pygame.draw.circle(screen, (255, 0, 0), (int(pos[0]), int(pos[1])), 5)

    stats = lake.get_stats()
    stats_surface = font.render(
        f"Fish: {stats['Fish count']} | Food: {stats['Food amount']} | Oxygen: {stats['Oxygen level']:.2f} | Season: {stats['Season']}",
        True, (255, 255, 255)
    )
    screen.blit(stats_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)
