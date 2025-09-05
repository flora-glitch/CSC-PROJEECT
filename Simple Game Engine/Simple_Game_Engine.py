# Simple Game Engine

class Entity:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def update(self):
        pass

    def render(self):
        print(f"{self.name} at ({self.x}, {self.y})")

class Player(Entity):
    def __init__(self, x, y):
        super().__init__("Player", x, y)

    def update(self):
        move = input("Move (w/a/s/d): ").lower()
        if move == 'w':
            self.y -= 1
        elif move == 's':
            self.y += 1
        elif move == 'a':
            self.x -= 1
        elif move == 'd':
            self.x += 1

class Game:
    def __init__(self):
        self.entities = [Player(0, 0)]

    def update(self):
        for entity in self.entities:
            entity.update()

    def render(self):
        for entity in self.entities:
            entity.render()

    def run(self):
        while True:
            self.update()
            self.render()
            if input("Continue? (y/n): ").lower() != 'y':
                break

if __name__ == "__main__":
    game = Game()
    game.run()