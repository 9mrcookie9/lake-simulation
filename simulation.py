# import numpy as np
# import random
# import pygame
# import sys
# from pygame.math import Vector2
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#
#
# class Fish:
#     def __init__(self, id, energy, position):
#         self.id = id
#         self.energy = energy
#         self.position = Vector2(position)
#         self.velocity = Vector2(random.uniform(-1, 1),
#                                 random.uniform(-1, 1)).normalize()
#         self.max_speed = 2
#         self.max_force = 0.1
#         self.change_target_time = random.randint(
#             30, 90)  # Time to change target
#         self.target = self.random_target()
#
#     def random_target(self):
#         return Vector2(random.randint(0, 800), random.randint(0, 600))
#
#     def move(self, fish_population, food_sources):
#         # Fish moves based on steering behaviors
#         if self.energy > 0:
#             self.energy -= 1  # Each movement costs 1 energy unit
#             self.change_target_time -= 1
#             if self.change_target_time <= 0:
#                 self.target = self.random_target()
#                 self.change_target_time = random.randint(30, 90)
#             acceleration = self.steer(fish_population, food_sources)
#             self.velocity += acceleration
#             if self.velocity.length() > self.max_speed:
#                 self.velocity.scale_to_length(self.max_speed)
#             self.position += self.velocity
#             # Ensure fish stays within bounds
#             self.position.x = max(0, min(self.position.x, 800))
#             self.position.y = max(0, min(self.position.y, 600))
#         else:
#             self.die()  # Fish dies if it has no energy
#
#     def steer(self, fish_population, food_sources):
#         # Implement steering behaviors
#         separation_force = self.separation(fish_population) * 1.5
#         alignment_force = self.alignment(fish_population) * 1.0
#         cohesion_force = self.cohesion(fish_population) * 1.0
#         seek_food_force = self.seek_food(food_sources) * 2.0
#         seek_target_force = self.seek(self.target) * 2.0  # Increased weight
#
#         # Combine forces
#         return separation_force + alignment_force + cohesion_force + seek_food_force + seek_target_force
#
#     def separation(self, fish_population):
#         # Steer to avoid crowding local fish
#         desired_separation = 20
#         steer = Vector2(0, 0)
#         count = 0
#         for other in fish_population:
#             if other != self:
#                 distance = self.position.distance_to(other.position)
#                 if 0 < distance < desired_separation:
#                     diff = self.position - other.position
#                     if diff.length() > 0:
#                         diff = diff.normalize() / distance
#                     steer += diff
#                     count += 1
#         if count > 0:
#             steer /= count
#         if steer.length() > 0:
#             steer = steer.normalize() * self.max_speed - self.velocity
#             if steer.length() > self.max_force:
#                 steer = steer.normalize() * self.max_force
#         return steer
#
#     def alignment(self, fish_population):
#         # Steer towards the average heading of local fish
#         neighbor_dist = 50
#         avg_velocity = Vector2(0, 0)
#         count = 0
#         for other in fish_population:
#             if other != self:
#                 distance = self.position.distance_to(other.position)
#                 if 0 < distance < neighbor_dist:
#                     avg_velocity += other.velocity
#                     count += 1
#         if count > 0:
#             avg_velocity /= count
#             if avg_velocity.length() > 0:
#                 avg_velocity = avg_velocity.normalize() * self.max_speed
#             steer = avg_velocity - self.velocity
#             if steer.length() > self.max_force:
#                 steer = steer.normalize() * self.max_force
#             return steer
#         return Vector2(0, 0)
#
#     def cohesion(self, fish_population):
#         # Steer to move towards the average position of local fish
#         neighbor_dist = 50
#         avg_position = Vector2(0, 0)
#         count = 0
#         for other in fish_population:
#             if other != self:
#                 distance = self.position.distance_to(other.position)
#                 if 0 < distance < neighbor_dist:
#                     avg_position += other.position
#                     count += 1
#         if count > 0:
#             avg_position /= count
#             return self.seek(avg_position)
#         return Vector2(0, 0)
#
#     def seek(self, target):
#         # Seek a target position
#         desired = (target - self.position).normalize() * self.max_speed
#         steer = desired - self.velocity
#         if steer.length() > self.max_force:
#             steer = steer.normalize() * self.max_force
#         return steer
#
#     def seek_food(self, food_sources):
#         # Steer to move towards the nearest food source
#         if not food_sources:
#             return Vector2(0, 0)
#         closest_food = min(food_sources, key=lambda food: self.position.distance_to(
#             Vector2(food.position)))
#         return self.seek(Vector2(closest_food.position))
#
#     def eat(self, food):
#         self.energy += food  # Fish gains energy from food
#
#     def die(self):
#         self.energy = 0
#         # Implement death logic
#
#
# class Plant:
#     def __init__(self, position):
#         self.position = position
#         self.food_amount = 10  # Initial amount of food the plant generates
#
#     def generate_food(self):
#         # Plant generates food around itself
#         self.food_amount += 0.5  # Reduced food generation
#
#
# class Fisherman:
#     def __init__(self, probability, fishing_area):
#         self.probability = probability
#         self.fishing_area = fishing_area
#
#     def fish(self, lake):
#         if random.random() < self.probability:
#             fish_in_area = [fish for fish in lake.fish_population if self.is_in_fishing_area(fish.position)]
#             if fish_in_area:
#                 caught_fish = random.choice(fish_in_area)
#                 lake.fish_population.remove(caught_fish)
#                 lake.caught_fish_positions.append((caught_fish.position, 30))
#                 lake.record_fish_caught()
#                 print(f"Fisherman caught fish: {caught_fish.id}")
#
#     def is_in_fishing_area(self, position):
#         x, y = position
#         x1, y1, x2, y2 = self.fishing_area
#         return x1 <= x <= x2 and y1 <= y <= y2
#
#
# class Lake:
#     def __init__(self, width, height, initial_fish, initial_food, plants, reproduction_interval):
#         self.width = width
#         self.height = height
#         self.fish_population = initial_fish
#         self.food_amount = initial_food
#         self.plants = plants
#         self.oxygen_level = 100
#         self.generation_count = 0
#         self.reproduction_interval = reproduction_interval
#         self.caught_fish_positions = []
#         self.season_length = 50
#         self.current_season = 0
#
#         # Tracking fish born and caught
#         self.fish_born_per_season = {"Spring": 0, "Summer": 0, "Fall": 0, "Winter": 0}
#         self.fish_caught_per_season = {"Spring": 0, "Summer": 0, "Fall": 0, "Winter": 0}
#         self.total_fish_born = []
#         self.total_fish_caught = []
#
#         # Data logging
#         self.time_steps = []
#         self.fish_population_log = []
#         self.food_amount_log = []
#         self.oxygen_level_log = []
#
#     def update(self):
#         self.generation_count += 1
#         self.current_season = (self.generation_count // self.season_length) % 4
#         season_names = ["Spring", "Summer", "Fall", "Winter"]
#         season_name = season_names[self.current_season]
#
#         if self.current_season == 0:
#             reproduction_chance = 0.04
#             food_generation = 1
#             oxygen_generation = 0.2
#         elif self.current_season == 1:
#             reproduction_chance = 0.05
#             food_generation = 1.2
#             oxygen_generation = 0.3
#         elif self.current_season == 2:
#             reproduction_chance = 0.03
#             food_generation = 0.8
#             oxygen_generation = 0.1
#         else:
#             reproduction_chance = 0.02
#             food_generation = 0.5
#             oxygen_generation = 0.05
#
#         self.oxygen_level -= len(self.fish_population) * 0.05
#
#         for plant in self.plants:
#             plant.generate_food()
#             self.food_amount += food_generation
#             self.oxygen_level += oxygen_generation
#
#         self.food_amount = max(self.food_amount, 0)
#         self.oxygen_level = max(self.oxygen_level, 0)
#
#         for fish in self.fish_population:
#             fish.move(self.fish_population, self.plants)
#             if self.food_amount > 0:
#                 fish.eat(1)
#                 self.food_amount -= 1
#
#             if fish.energy <= 0:
#                 self.fish_population.remove(fish)
#
#         if self.generation_count % self.reproduction_interval == 0 and self.food_amount > 10 and self.oxygen_level > 10:
#             new_fish = []
#             if len(self.fish_population) >= 2:
#                 for fish in self.fish_population:
#                     if random.random() < reproduction_chance:
#                         parent1, parent2 = random.sample(self.fish_population, 2)
#                         new_position = (parent1.position + parent2.position) / 2
#                         new_fish.append(
#                             Fish(id=len(self.fish_population) + len(new_fish), energy=50, position=new_position))
#             self.fish_population.extend(new_fish)
#             self.fish_born_per_season[season_name] += len(new_fish)
#
#         self.caught_fish_positions = [(pos, ticks - 1) for pos, ticks in self.caught_fish_positions if ticks > 0]
#
#         # Log data
#         self.time_steps.append(self.generation_count)
#         self.fish_population_log.append(len(self.fish_population))
#         self.food_amount_log.append(self.food_amount)
#         self.oxygen_level_log.append(self.oxygen_level)
#
#     def record_fish_caught(self):
#         season_names = ["Spring", "Summer", "Fall", "Winter"]
#         season_name = season_names[self.current_season]
#         self.fish_caught_per_season[season_name] += 1
#
#     def get_stats(self):
#         season_names = ["Spring", "Summer", "Fall", "Winter"]
#         return {
#             'Fish count': len(self.fish_population),
#             'Food amount': self.food_amount,
#             'Oxygen level': self.oxygen_level,
#             'Season': season_names[self.current_season]
#         }
#
#     def plot_stats(self):
#         seasons = ["Spring", "Summer", "Fall", "Winter"]
#         fish_born = [self.fish_born_per_season[season] for season in seasons]
#         fish_caught = [self.fish_caught_per_season[season] for season in seasons]
#
#         x = np.arange(len(seasons))
#
#         fig, ax = plt.subplots()
#         bar_width = 0.35
#
#         bar1 = ax.bar(x - bar_width / 2, fish_born, bar_width, label='Fish Born')
#         bar2 = ax.bar(x + bar_width / 2, fish_caught, bar_width, label='Fish Caught')
#
#         ax.set_xlabel('Season')
#         ax.set_ylabel('Count')
#         ax.set_title('Fish Born and Caught per Season')
#         ax.set_xticks(x)
#         ax.set_xticklabels(seasons)
#         ax.legend()
#
#         for bar in bar1 + bar2:
#             height = bar.get_height()
#             ax.annotate('{}'.format(height),
#                         xy=(bar.get_x() + bar.get_width() / 2, height),
#                         xytext=(0, 3),
#                         textcoords="offset points",
#                         ha='center', va='bottom')
#
#         plt.show()
#
#     def plot_time_series(self):
#         fig, axs = plt.subplots(3, 1, figsize=(10, 15))
#
#         # Plot fish population over time
#         axs[0].plot(self.time_steps, self.fish_population_log, label='Fish Population', color='b')
#         axs[0].set_xlabel('Time Step')
#         axs[0].set_ylabel('Fish Population')
#         axs[0].set_title('Fish Population Over Time')
#         axs[0].legend()
#
#         # Plot food amount over time
#         axs[1].plot(self.time_steps, self.food_amount_log, label='Food Amount', color='g')
#         axs[1].set_xlabel('Time Step')
#         axs[1].set_ylabel('Food Amount')
#         axs[1].set_title('Food Amount Over Time')
#         axs[1].legend()
#
#         # Plot oxygen level over time
#         axs[2].plot(self.time_steps, self.oxygen_level_log, label='Oxygen Level', color='r')
#         axs[2].set_xlabel('Time Step')
#         axs[2].set_ylabel('Oxygen Level')
#         axs[2].set_title('Oxygen Level Over Time')
#         axs[2].legend()
#
#         for ax in axs:
#             ax.grid(True)
#
#         plt.tight_layout()
#         plt.show()
#
# # Initialize Pygame
# pygame.init()
#
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption('Lake Ecosystem Simulation')
#
# # Define the fishing area (x1, y1, x2, y2)
# fishing_area = (200, 150, 400, 350)
#
# # Initialize lake, fish, plants, and fisherman
# lake = Lake(width, height, [Fish(id=i, energy=100, position=(random.randint(0, width), random.randint(0, height))) for i in range(
#     10)], 500, [Plant(position=(random.randint(0, width), random.randint(0, height))) for _ in range(20)], reproduction_interval=10)
# # Fisherman has a 5% chance of catching a fish in each iteration
# fisherman = Fisherman(probability=0.05, fishing_area=fishing_area)
#
# clock = pygame.time.Clock()
# font = pygame.font.SysFont(None, 24)
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             lake.plot_stats()
#             lake.plot_time_series()
#             sys.exit()
#
#     lake.update()
#     fisherman.fish(lake)  # Fisherman tries to catch a fish
#
#     screen.fill((0, 0, 255))  # Color of the lake
#     pygame.draw.rect(screen, (0, 0, 0), fishing_area,
#                      2)  # Draw the fishing area
#     for fish in lake.fish_population:
#         pygame.draw.circle(screen, (255, 255, 255), (int(
#             fish.position.x), int(fish.position.y)), 5)
#     for plant in lake.plants:
#         # Representing plants
#         pygame.draw.circle(screen, (0, 255, 0), plant.position, 10)
#     for pos, _ in lake.caught_fish_positions:
#         # Red dot at the position of caught fish
#         pygame.draw.circle(screen, (255, 0, 0), (int(pos.x), int(pos.y)), 5)
#
#     # Display simulation stats
#     stats = lake.get_stats()
#     stats_surface = font.render(
#         f"Fish: {stats['Fish count']} | Food: {stats['Food amount']} | Oxygen: {stats['Oxygen level']:.2f} | Season: {stats['Season']}", True, (255, 255, 255))
#     screen.blit(stats_surface, (10, 10))
#
#     pygame.display.flip()
#     clock.tick(60)
