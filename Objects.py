from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):

    @abstractmethod
    def __init__(self):
        pass

    # @abstractmethod
    def draw(self, display):
        pass


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        self.sprite = icon
        self.stats = stats
        self.xp = xp
        self.position = position

    def interact(self, engine, hero):
        # DONE! - TODO interact Enemy
        hero_luck = random.randint(0, engine.hero.stats["luck"])
        hero_safe = engine.hero.stats["endurance"] * engine.hero.stats["intelligence"] * hero_luck

        enemy_luck = random.randint(0, self.stats["luck"])
        enemy_safe = self.stats["endurance"] * self.stats["intelligence"] * enemy_luck

        hero_force = engine.hero.stats["strength"] * engine.hero.stats["intelligence"]
        enemy_force = self.stats["strength"] * self.stats["intelligence"]

        hero_damage = enemy_force - hero_safe
        if hero_damage > 0:
            hero.hp -= hero_damage
            engine.notify("hero damaged!")

        enemy_damage = hero_force - enemy_safe
        if enemy_damage > 0:
            engine.notify("enemy damaged")
            engine.hero.exp += 5
            engine.score += 0.1
            if (self.xp - enemy_damage) < 0:
                engine.hero.exp += 10
                engine.score += 0.2
                engine.notify("enemy destroyed!")

        # engine.notify("hero_damage=" + str(hero_damage))
        # engine.notify('enemy_damage=' + str(enemy_damage))
        # engine.notify("strength=" + str(self.stats["strength"]))
        # engine.notify("endurance=" + str(self.stats["endurance"]))
        # engine.notify("intelligence=" + str(self.stats["intelligence"]))
        # engine.notify("luck=" + str(self.stats["luck"]))
        # engine.notify("experience=" + str(self.stats["experience"]))
        # engine.notify("</Enemy >")
        # delta_strength = (self.stats["strength"] - hero.stats["strength"])
        # delta_endurance = (self.stats["endurance"] - hero.stats["endurance"])
        # delta_luck
        # if delta_strength > 0:
        #     hero.hp -= delta_strength
        engine.hero.exp += 1
        # self.action(engine, hero)


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        # res = f"Ally-{hero.hp}\nSecond str"
        # engine.notify(res)
        # engine.notify("stats="+str(hero.stats))
        self.action(engine, hero)
        engine.hero.exp += 1

        # DONE! - TODO interact Ally


class Effect(Hero):

    def __init__(self, base_stats):
        self.base = base_stats
        self.stats = self.base.stats.copy()
        # self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        # DONE! - TODO apply_effect Berserk
        res = ""
        if random.randint(0, 1):
            self.stats["strength"] *= 2
            res += f'Strength={self.stats["strength"]}\n'
        if random.randint(0, 1):
            self.stats["endurance"] *= 2
            res += f'Endurance={self.stats["endurance"]}\n'
        if random.randint(0, 1):
            self.stats["intelligence"] *= 2
            res += f'Intelligence={self.stats["intelligence"]}\n'
        return res


class Blessing(Effect):
    def apply_effect(self):
        # DONE! - TODO apply_effect Blessing
        self.max_hp *= 2
        self.hp *= 2
        self.stats["luck"] *= 2
        res = f"Luck={self.stats['luck']}\n" \
              f"Max_HP={self.max_hp}\n" \
              f"New HP={self.hp}"
        return res


class Weakness(Effect):
    def apply_effect(self):
        self.stats["strength"] //= 2
        self.stats["luck"] //= 2
        # DONE! - TODO apply_effect Weakness
        res = f"Luck={self.stats['luck']}\n" \
              f"Strength={self.stats['strength']}"
        return res
