import os
import random
import shutil
import sys
import tkinter as tk
from tkinter import messagebox

import pygame

from fish import Fish
from fisherman import Fisherman
from lake import Lake
from plant import Plant


def start_simulation(initial_fish_count, initial_plant_count, fishing_area, fisherman_probability, reproduction_interval, season_length):
    # Initialize pygame
    pygame.init()

    # Set up screen dimensions
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Lake Ecosystem Simulation')

    # Clear the /analyze folder
    if os.path.exists('analyze'):
        shutil.rmtree('analyze')
    os.makedirs('analyze')

    # Initialize lake and fisherman
    lake = Lake(
        width,
        height,
        [Fish(id=i, energy=100, position=(random.randint(0, width), random.randint(0, height))) for i in range(initial_fish_count)],
        500,
        [Plant(position=(random.randint(0, width), random.randint(0, height))) for _ in range(initial_plant_count)],
        reproduction_interval=reproduction_interval,
        season_length=season_length  # Include season_length parameter
    )
    fisherman = Fisherman(probability=fisherman_probability, fishing_area=fishing_area)

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
            f"Fish: {stats['Fish count']} | Food: {stats['Food amount']:.2f} | Oxygen: {stats['Oxygen level']:.2f} | Season: {stats['Season']}",
            True, (255, 255, 255)
        )
        screen.blit(stats_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

def on_confirm():
    try:
        initial_fish_count = int(fish_count_entry.get())
        initial_plant_count = int(plant_count_entry.get())
        fishing_area_x = int(fishing_area_x_entry.get())
        fishing_area_y = int(fishing_area_y_entry.get())
        fishing_area_width = int(fishing_area_width_entry.get())
        fishing_area_height = int(fishing_area_height_entry.get())
        fisherman_probability = float(fishing_probability_entry.get())
        reproduction_interval = int(reproduction_interval_entry.get())
        season_length = int(season_length_entry.get())

        fishing_area = (fishing_area_x, fishing_area_y, fishing_area_width, fishing_area_height)

        root.destroy()
        start_simulation(initial_fish_count, initial_plant_count, fishing_area, fisherman_probability, reproduction_interval, season_length)

    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

# GUI
root = tk.Tk()
root.title("Lake Simulation Configuration")

tk.Label(root, text="Initial Fish Count:").grid(row=0, column=0)
fish_count_entry = tk.Entry(root)
fish_count_entry.insert(0, "10")
fish_count_entry.grid(row=0, column=1)

tk.Label(root, text="Initial Plant Count:").grid(row=1, column=0)
plant_count_entry = tk.Entry(root)
plant_count_entry.insert(0, "20")
plant_count_entry.grid(row=1, column=1)

tk.Label(root, text="Fishing Area Top-Left X Coordinate:").grid(row=2, column=0)
fishing_area_x_entry = tk.Entry(root)
fishing_area_x_entry.insert(0, "200")
fishing_area_x_entry.grid(row=2, column=1)

tk.Label(root, text="Fishing Area Top-Left Y Coordinate:").grid(row=3, column=0)
fishing_area_y_entry = tk.Entry(root)
fishing_area_y_entry.insert(0, "150")
fishing_area_y_entry.grid(row=3, column=1)

tk.Label(root, text="Fishing Area Width:").grid(row=4, column=0)
fishing_area_width_entry = tk.Entry(root)
fishing_area_width_entry.insert(0, "400")
fishing_area_width_entry.grid(row=4, column=1)

tk.Label(root, text="Fishing Area Height:").grid(row=5, column=0)
fishing_area_height_entry = tk.Entry(root)
fishing_area_height_entry.insert(0, "350")
fishing_area_height_entry.grid(row=5, column=1)

tk.Label(root, text="Fisherman's Probability of Catching a Fish:").grid(row=6, column=0)
fishing_probability_entry = tk.Entry(root)
fishing_probability_entry.insert(0, "0.05")
fishing_probability_entry.grid(row=6, column=1)

tk.Label(root, text="Fish Reproduction Interval:").grid(row=7, column=0)
reproduction_interval_entry = tk.Entry(root)
reproduction_interval_entry.insert(0, "10")
reproduction_interval_entry.grid(row=7, column=1)

tk.Label(root, text="Season Length:").grid(row=8, column=0)
season_length_entry = tk.Entry(root)
season_length_entry.insert(0, "50")
season_length_entry.grid(row=8, column=1)

confirm_button = tk.Button(root, text="Confirm", command=on_confirm)
confirm_button.grid(row=9, columnspan=2)

root.mainloop()