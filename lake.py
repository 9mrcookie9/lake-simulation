import random
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime
from fish import Fish
from plant import Plant

class Lake:
    def __init__(self, width, height, initial_fish, initial_food, plants, reproduction_interval):
        self.width = width
        self.height = height
        self.fish_population = initial_fish
        self.food_amount = initial_food
        self.plants = plants
        self.oxygen_level = 100
        self.generation_count = 0
        self.reproduction_interval = reproduction_interval
        self.caught_fish_positions = []
        self.season_length = 50
        self.current_season = 0

        self.fish_born_per_season = {"Spring": 0, "Summer": 0, "Fall": 0, "Winter": 0}
        self.fish_caught_per_season = {"Spring": 0, "Summer": 0, "Fall": 0, "Winter": 0}
        self.total_fish_born = []
        self.total_fish_caught = []

        self.time_steps = []
        self.fish_population_log = []
        self.food_amount_log = []
        self.oxygen_level_log = []

        # Create log files
        self.create_log_files()

    def create_log_files(self):
        """Initialize CSV log files."""
        self.fish_population_file = 'analyze/fish_population_log.csv'
        self.food_amount_file = 'analyze/food_amount_log.csv'
        self.oxygen_level_file = 'analyze/oxygen_level_log.csv'

        # Write headers to log files
        with open(self.fish_population_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time_step', 'fish_population'])

        with open(self.food_amount_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time_step', 'food_amount'])

        with open(self.oxygen_level_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time_step', 'oxygen_level'])

    def log_data(self):
        """Append data to CSV log files."""
        with open(self.fish_population_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.generation_count, len(self.fish_population)])

        with open(self.food_amount_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.generation_count, self.food_amount])

        with open(self.oxygen_level_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.generation_count, self.oxygen_level])

    def update(self):
        self.generation_count += 1
        self.current_season = (self.generation_count // self.season_length) % 4
        season_names = ["Spring", "Summer", "Fall", "Winter"]
        season_name = season_names[self.current_season]

        day_time = (self.generation_count % self.season_length) < (self.season_length // 2)

        if self.current_season == 0:
            reproduction_chance = 0.04
            food_generation = 1
            oxygen_generation = 0.2 if day_time else -0.1
        elif self.current_season == 1:
            reproduction_chance = 0.05
            food_generation = 1.2
            oxygen_generation = 0.3 if day_time else -0.1
        elif self.current_season == 2:
            reproduction_chance = 0.03
            food_generation = 0.8
            oxygen_generation = 0.1 if day_time else -0.1
        else:
            reproduction_chance = 0.02
            food_generation = 0.5
            oxygen_generation = 0.05 if day_time else -0.1

        self.oxygen_level -= len(self.fish_population) * 0.05  # Fish respiration

        decay_factor = 0.02
        self.oxygen_level -= decay_factor * (len(self.fish_population) + len(self.plants))

        for plant in self.plants:
            plant.generate_food()
            self.food_amount += food_generation
            self.oxygen_level += oxygen_generation

        self.food_amount = max(self.food_amount, 0)
        self.oxygen_level = max(self.oxygen_level, 0)

        for fish in self.fish_population:
            fish.move(self.fish_population, self.plants)
            if self.food_amount > 0:
                fish.eat(1)
                self.food_amount -= 1

            if fish.energy <= 0:
                self.fish_population.remove(fish)

        if self.generation_count % self.reproduction_interval == 0 and self.food_amount > 10 and self.oxygen_level > 10:
            new_fish = []
            if len(self.fish_population) >= 2:
                for fish in self.fish_population:
                    if random.random() < reproduction_chance:
                        parent1, parent2 = random.sample(self.fish_population, 2)
                        new_position = (parent1.position + parent2.position) / 2
                        new_fish.append(Fish(id=len(self.fish_population) + len(new_fish), energy=50, position=new_position))
            self.fish_population.extend(new_fish)
            self.fish_born_per_season[season_name] += len(new_fish)

        self.caught_fish_positions = [(pos, ticks - 1) for pos, ticks in self.caught_fish_positions if ticks > 0]

        self.time_steps.append(self.generation_count)
        self.fish_population_log.append(len(self.fish_population))
        self.food_amount_log.append(self.food_amount)
        self.oxygen_level_log.append(self.oxygen_level)

        self.ensure_oxygen_level()

        # Log data to CSV files
        self.log_data()

    def ensure_oxygen_level(self):
        if self.oxygen_level < 10:
            # Boost plant oxygen production
            for plant in self.plants:
                self.oxygen_level += 0.5
            # Reduce fish oxygen consumption
            for fish in self.fish_population:
                self.oxygen_level += 0.01

    def record_fish_caught(self):
        season_names = ["Spring", "Summer", "Fall", "Winter"]
        season_name = season_names[self.current_season]
        self.fish_caught_per_season[season_name] += 1

    def get_stats(self):
        season_names = ["Spring", "Summer", "Fall", "Winter"]
        return {
            'Fish count': len(self.fish_population),
            'Food amount': self.food_amount,
            'Oxygen level': self.oxygen_level,
            'Season': season_names[self.current_season]
        }

    def plot_stats(self):
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        fish_born = [self.fish_born_per_season[season] for season in seasons]
        fish_caught = [self.fish_caught_per_season[season] for season in seasons]

        x = np.arange(len(seasons))

        fig, ax = plt.subplots()
        bar_width = 0.35

        bar1 = ax.bar(x - bar_width / 2, fish_born, bar_width, label='Fish Born')
        bar2 = ax.bar(x + bar_width / 2, fish_caught, bar_width, label='Fish Caught')

        ax.set_xlabel('Season')
        ax.set_ylabel('Count')
        ax.set_title('Fish Born and Caught per Season')
        ax.set_xticks(x)
        ax.set_xticklabels(seasons)
        ax.legend()

        for bar in bar1 + bar2:
            height = bar.get_height()
            ax.annotate('{}'.format(height), xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                        textcoords="offset points", ha='center', va='bottom')

        plt.savefig('analyze/fish_born_and_caught_per_season.png')
        plt.close()

    def plot_time_series(self):
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))

        axs[0].plot(self.time_steps, self.fish_population_log, label='Fish Population', color='b')
        axs[0].set_xlabel('Time Step')
        axs[0].set_ylabel('Fish Population')
        axs[0].set_title('Fish Population Over Time')
        axs[0].legend()

        axs[1].plot(self.time_steps, self.food_amount_log, label='Food Amount', color='g')
        axs[1].set_xlabel('Time Step')
        axs[1].set_ylabel('Food Amount')
        axs[1].set_title('Food Amount Over Time')
        axs[1].legend()

        axs[2].plot(self.time_steps, self.oxygen_level_log, label='Oxygen Level', color='r')
        axs[2].set_xlabel('Time Step')
        axs[2].set_ylabel('Oxygen Level')
        axs[2].set_title('Oxygen Level Over Time')
        axs[2].legend()

        for ax in axs:
            ax.grid(True)

        plt.tight_layout()
        plt.savefig('analyze/overtime_stats.png')
        plt.close()

