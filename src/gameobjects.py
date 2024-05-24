import pygame

def load_image(filename):
    return pygame.image.load(filename)

class BasicObject:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = load_image(image)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
class Player(BasicObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Box(BasicObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Wall(BasicObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Target(BasicObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Background(BasicObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Air(BasicObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
