class Plant:
    def __init__(self, position):
        self.position = position
        self.food_amount = 10

    def generate_food(self):
        self.food_amount += 0.5
