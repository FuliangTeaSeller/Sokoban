import pygame
from gameobjects import load_image, BasicObject, Player, Box, Wall, Target, Air, Background

class Game:
    def __init__(self, game_map) -> None:
        pygame.init()
        self.screen_size = (400, 300)
        self.screen = pygame.display.set_mode(self.screen_size)  # 初始化屏幕大小
        self.clock = pygame.time.Clock()  # 控制游戏帧率
        self.map = game_map  # 存储游戏地图数据

    def init(self) -> None:
        self.tile_size = 30  # 设置地图中每块的大小
        self.objects = []  # 所有游戏对象列表
        self.walls = []  # 墙对象列表
        self.boxes = []  # 箱子对象列表
        self.targets = []  # 目标位置列表
        self.airs = []  # 空地对象列表
        self.parse_map(self.map)  # 解析地图

    def parse_map(self, game_map):
        for row_index, row in enumerate(game_map):
            for col_index, col in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if col == 'P':
                    self.player = Player(x, y, 'images/Bmp6.gif')
                    self.airs.append(Air(x, y, 'images/Bmp2.gif'))
                elif col == 'B':
                    self.boxes.append(Box(x, y, 'images/Bmp3.gif'))
                    self.airs.append(Air(x, y, 'images/Bmp2.gif'))
                elif col == 'W':
                    self.walls.append(Wall(x, y, 'images/Bmp1.gif'))
                elif col == 'T':
                    self.targets.append(Target(x, y, 'images/Bmp5.gif'))
                elif col == 'A':
                    self.airs.append(Air(x, y, 'images/Bmp2.gif'))

    def handle_player_movement(self, key):
        dx, dy = 0, 0
        if key == pygame.K_LEFT:
            dx = -self.tile_size
        elif key == pygame.K_RIGHT:
            dx = self.tile_size
        elif key == pygame.K_UP:
            dy = -self.tile_size
        elif key == pygame.K_DOWN:
            dy = self.tile_size

        new_x, new_y = self.player.x + dx, self.player.y + dy

        if any(wall.x == new_x and wall.y == new_y for wall in self.walls):
            return  # 阻止玩家移动到墙上

        for box in self.boxes:
            if box.x == new_x and box.y == new_y:
                box_new_x = box.x + dx
                box_new_y = box.y + dy
                if any((b.x == box_new_x and b.y == box_new_y) or (w.x == box_new_x and w.y == box_new_y) for b in self.boxes for w in self.walls):
                    return  # 箱子移动到墙上或其他箱子上时停止
                box.x = box_new_x
                box.y = box_new_y

        self.player.x, self.player.y = new_x, new_y

    def run(self):
        while True:
            self.init()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.handle_player_movement(key=event.key)

                self.render()
                running = self.check_win_condition()

                pygame.display.flip()
                self.clock.tick(60)

            # 显示重启游戏提示
            font = pygame.font.Font(None, 36)
            text = font.render("Press R to restart", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT :
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        break
                else:
                    continue
                break

    def check_win_condition(self):
        # 检查所有箱子是否都移动到目标位置
        sorted_boxes = sorted(self.boxes, key=lambda box: (box.x, box.y))
        sorted_targets = sorted(self.targets, key=lambda target: (target.x, target.y))
        return not all(box.x == target.x and box.y == target.y for box, target in zip(sorted_boxes, sorted_targets))

    def render(self):
        self.screen.fill((0, 0, 0))
        # 绘制背景图案
        background = Background(0, 0, 'images/Bmp0.gif')
        for i in range(0, self.screen_size[0], 37):
            for j in range(0, self.screen_size[1], 37):
                background.x = i
                background.y = j
                background.draw(self.screen)

        for air in self.airs:
            air.draw(self.screen)
        for wall in self.walls:
            wall.draw(self.screen)
        for target in self.targets:
            target.draw(self.screen)
        for box in self.boxes:
            box.draw(self.screen)
        self.player.draw(self.screen)

if __name__ == "__main__":
    game_map = [
        "WWWWWWWWWW",
        "WAAAAAAAAW",
        "WATBAAAAAW",
        "WATBAAPAAW",
        "WAAAAAAAAW",
        "WWWWWWWWWW"
    ]
    game = Game(game_map)
    game.run()
