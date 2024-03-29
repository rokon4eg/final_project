import pygame
import collections
import Logic

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


class ScreenHandle(pygame.Surface):
    game_engine: Logic.GameEngine

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])
        self.game_engine = Logic.GameEngine()

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    # DONE! - FIXME - connect_engine
    def connect_engine(self, engine):
        self.game_engine = engine
        if not self.successor is None:
            self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):
    def connect_engine(self, engine):
        self.game_engine = engine
        if not self.successor is None:
            self.successor.connect_engine(engine)
        # DONE! - FIXME - save engine and send it to next in chain

    def draw_hero(self):
        min_x, min_y = self._calculate_min_x_y()

        screen_size = self.get_size()
        size = self.game_engine.sprite_size
        hero = self.game_engine.hero
        self.blit(hero.sprite, ((hero.position[0] - min_x) * size, (hero.position[1] - min_y) * size))

    def draw_map(self):
        size = self.game_engine.sprite_size
        # DONE! - FIXME || calculate (min_x,min_y) - left top corner
        min_x, min_y = self._calculate_min_x_y()

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - min_x):
                for j in range(len(self.game_engine.map) - min_y):
                    self.blit(self.game_engine.map[min_y + j][min_x + i][0],
                              (i * size, j * size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.game_engine.sprite_size
        # DONE! - FIXME || calculate (min_x,min_y) - left top corner
        min_x, min_y = self._calculate_min_x_y()

        self.blit(sprite, ((coord[0] - min_x) * size,
                           (coord[1] - min_y) * size))

    def draw(self, canvas):
        self.fill(colors["wooden"])
        size = self.game_engine.sprite_size
        # DONE! - FIXME || calculate (min_x,min_y) - left top corner
        min_x, min_y = self._calculate_min_x_y()

        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - min_x) * size,
                                      (obj.position[1] - min_y) * size))
        self.draw_hero()

        if self.successor is not None:
            self.successor.draw(canvas)
            canvas.blit(self.successor, self.next_coord)
        # DONE! - FIXME - draw next surface in chain

    def _calculate_min_x_y(self):
        min_x, min_y = 0, 0
        screen_size = self.get_size()
        size = self.game_engine.sprite_size
        pos = self.game_engine.hero.position
        max_x = screen_size[0] // size
        max_y = screen_size[1] // size
        if pos[0] >= max_x:
            min_x = max_x * (pos[0] // max_x)
        if pos[1] >= max_y:
            min_y = max_y * (pos[1] // max_y)
        return min_x, min_y


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        # DONE! - FIXME - save engine and send it to next in chain
        self.game_engine = engine
        if not self.successor is None:
            self.successor.connect_engine(engine)

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
            "red"], (50, 30, 200 * self.game_engine.hero.hp / self.game_engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70,
                                                 200 * self.game_engine.hero.exp / (
                                                             100 * (2 ** (self.game_engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.game_engine.hero.position}', True, colors["black"]),
                  (250, 0))

        self.blit(font.render(f'{self.game_engine.level} floor', True, colors["black"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(f'{self.game_engine.hero.hp}/{self.game_engine.hero.max_hp}', True, colors["black"]),
                  (60, 30))
        self.blit(font.render(f'{self.game_engine.hero.exp}/{(100 * (2 ** (self.game_engine.hero.level - 1)))}', True,
                              colors["black"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.game_engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.game_engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render(f'Intel', True, colors["black"]),
                  (420, 0))
        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 21))
        self.blit(font.render(f'Endur', True, colors["black"]),
                  (420, 45))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.game_engine.hero.stats["intelligence"]}', True, colors["black"]),
                  (480, 0))
        self.blit(font.render(f'{self.game_engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 21))
        self.blit(font.render(f'{self.game_engine.hero.stats["endurance"]}', True, colors["black"]),
                  (480, 45))
        self.blit(font.render(f'{self.game_engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.game_engine.score:.4f}', True, colors["black"]),
                  (550, 70))

        # DONE! - TODO - draw next surface in chain
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        for s in str(value).split("\n"):
            self.data.append(f"> {s}")

    def draw(self, canvas):
        self.fill(colors["wooden"])
        size = self.get_size()
        font = pygame.font.SysFont("comicsansms", 14)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)
        # DONE! - FIXME -  draw next surface in chain

    def connect_engine(self, engine):
        self.game_engine = engine
        engine.subscribe(self)
        if not self.successor is None:
            self.successor.connect_engine(engine)
        # DONE! - FIXME set this class as Observer to engine and send it to next in chain


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
        # DONE! - FIXME You can add some help information
        self.data.append(["ESC", "Stop Game and Exit"])

    def connect_engine(self, engine):
        self.game_engine = engine
        if not self.successor is None:
            self.successor.connect_engine(engine)
        # DONE! - FIXME - save engine and send it to next in chain

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.game_engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)
    # DONE! - FIXME - draw next surface in chain
