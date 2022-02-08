import pyglet


class Tower:
    def __init__(self, pos):
        super().__init__()
        self.pos = pos


class TownHall(Tower):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pyglet.image.load('./Assets/town hall.png')
        self.image.anchor_x = self.image.width // 2
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.pos[0], y=self.pos[1])
        self.size = [3, 3]
        self.tiles = [[(x + self.pos[0], y + self.pos[1]) for x in range(3)] for y in range(3)]
        print(self.tiles)
