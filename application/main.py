import random

# обект който представлява картата
class WorldMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = []

        for i in range(height):
            row = []
            
            for j in range(width):
                row.append(None)

            self.map.append(row)

#обект който представлява нещо живо
class Entity(object):
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.world.map[x][y] = self

#обект който представлява някакъв герой, било то твоят герой или противник
class Character(Entity):
    def __init__(self, x, y, world, hp, damage):
        Entity.__init__(self, x, y, world)
        self.hp = hp
        self.items = []
        self.damage = damage

    def move(self, direction):
        [x, y] = self.get_coordinates_to_direction(direction)

        self.world.map[self.x][self.y] = None
        self.world.map[x][y] = self
        self.x = x
        self.y = y

    def attack(self, direction):
        [x, y] = self.get_coordinates_to_direction(direction)
        enemy = self.world.map[x][y]
        if self.can_attack(enemy):
            enemy.hp -= self.damage
            self.hp -= enemy.damage
            return enemy

    def can_attack(self, direction):
        [x, y] = self.get_coordinates_to_direction(direction)
            
        return self.world.map[x][y] is not None

    def get_coordinates_to_direction(self, direction):
        x, y = 0, 0

        if direction == 'наляво':
            x = -1
        elif direction == 'надясно':
            x = 1
        elif direction == 'нагоре':
            y = -1
        elif direction == 'надолу':
            y = 1
        
        return [self.x + x, self.y + y]

    def distance(self, other):
        return [abs(other.x-self.x), abs(other.y-self.y)]

class Enemy(Character):
    def __init__(self, x, y, world):
        Character.__init__(self, x, y, world, 100, 10)

class Player(Character):
    def __init__(self, x, y, world):
        Character.__init__(self, x, y, world, 200, 30)

if __name__ == "__main__":
    world = WorldMap(100, 100)
    player = Player(10, 10, world)

    enemies = [Enemy(11, 11, world)]

    for i in range(5):
        enemies.append(Enemy(10 + random.randint(1, 60), 10 + random.randint(1, 60), world))

    while player.hp > 0:
        print('\n--------------')
        print(f'Позиция на играча: x: {player.x} y: {player.y}')
        move_direction = input('На къде искаш да отидеш (нагоре, надолу, наляво, надясно): ')

        if player.can_attack(move_direction):
            enemy = player.attack(move_direction)
            print(f'\nТи се сби с враг. Твоя кръв: {player.hp}. Кръв на врага: {enemy.hp}')

            if (enemy.hp < 0):
                world.map[enemy.x][enemy.y] = None
                print(f'Ти победи врага. Имаш оставащ живот {player.hp} \n')
        else:
            player.move(move_direction)