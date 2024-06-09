import random
from pygame.math import Vector2

class Fish:
    def __init__(self, id, energy, position):
        self.id = id
        self.energy = energy
        self.position = Vector2(position)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.max_speed = 2
        self.max_force = 0.1
        self.change_target_time = random.randint(30, 90)
        self.target = self.random_target()

    def random_target(self):
        return Vector2(random.randint(0, 800), random.randint(0, 600))

    def move(self, fish_population, food_sources):
        if self.energy > 0:
            self.energy -= 1
            self.change_target_time -= 1
            if self.change_target_time <= 0:
                self.target = self.random_target()
                self.change_target_time = random.randint(30, 90)
            acceleration = self.steer(fish_population, food_sources)
            self.velocity += acceleration
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)
            self.position += self.velocity
            self.position.x = max(0, min(self.position.x, 800))
            self.position.y = max(0, min(self.position.y, 600))
        else:
            self.die()

    def steer(self, fish_population, food_sources):
        separation_force = self.separation(fish_population) * 1.5
        alignment_force = self.alignment(fish_population) * 1.0
        cohesion_force = self.cohesion(fish_population) * 1.0
        seek_food_force = self.seek_food(food_sources) * 2.0
        seek_target_force = self.seek(self.target) * 2.0
        return separation_force + alignment_force + cohesion_force + seek_food_force + seek_target_force

    def separation(self, fish_population):
        desired_separation = 20
        steer = Vector2(0, 0)
        count = 0
        for other in fish_population:
            if other != self:
                distance = self.position.distance_to(other.position)
                if 0 < distance < desired_separation:
                    diff = self.position - other.position
                    if diff.length() > 0:
                        diff = diff.normalize() / distance
                    steer += diff
                    count += 1
        if count > 0:
            steer /= count
        if steer.length() > 0:
            steer = steer.normalize() * self.max_speed - self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
        return steer

    def alignment(self, fish_population):
        neighbor_dist = 50
        avg_velocity = Vector2(0, 0)
        count = 0
        for other in fish_population:
            if other != self:
                distance = self.position.distance_to(other.position)
                if 0 < distance < neighbor_dist:
                    avg_velocity += other.velocity
                    count += 1
        if count > 0:
            avg_velocity /= count
            if avg_velocity.length() > 0:
                avg_velocity = avg_velocity.normalize() * self.max_speed
            steer = avg_velocity - self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
            return steer
        return Vector2(0, 0)

    def cohesion(self, fish_population):
        neighbor_dist = 50
        avg_position = Vector2(0, 0)
        count = 0
        for other in fish_population:
            if other != self:
                distance = self.position.distance_to(other.position)
                if 0 < distance < neighbor_dist:
                    avg_position += other.position
                    count += 1
        if count > 0:
            avg_position /= count
            return self.seek(avg_position)
        return Vector2(0, 0)

    def seek(self, target):
        desired = (target - self.position).normalize() * self.max_speed
        steer = desired - self.velocity
        if steer.length() > self.max_force:
            steer = steer.normalize() * self.max_force
        return steer

    def seek_food(self, food_sources):
        if not food_sources:
            return Vector2(0, 0)
        closest_food = min(food_sources, key=lambda food: self.position.distance_to(Vector2(food.position)))
        return self.seek(Vector2(closest_food.position))

    def eat(self, food):
        self.energy += food

    def die(self):
        self.energy = 0
