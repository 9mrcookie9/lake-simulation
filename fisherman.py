import random

class Fisherman:
    def __init__(self, probability, fishing_area):
        self.probability = probability
        self.fishing_area = fishing_area

    def fish(self, lake):
        if random.random() < self.probability:
            fish_in_area = [fish for fish in lake.fish_population if self.is_in_fishing_area(fish.position)]
            if fish_in_area:
                caught_fish = random.choice(fish_in_area)
                lake.fish_population.remove(caught_fish)
                lake.caught_fish_positions.append((caught_fish.position, 30))
                lake.record_fish_caught()
                print(f"Fisherman caught fish: {caught_fish.id}")

    def is_in_fishing_area(self, position):
        x, y = position
        x1, y1, x2, y2 = self.fishing_area
        return x1 <= x <= x2 and y1 <= y <= y2
