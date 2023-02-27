import random

class gameMethod:
    verb_dict = {
        "examine": "Examine a creature in the room. Use by typing examine [target].",
        "hit": "Hit a creature in the room. Use by typing hit [target].",
        "help": "Get help about the available commands. Use by typing help [command].",
        "heal": "Heal for an amount of damage. Use by typing heal.",
        "kill": "Immediately kill the target. Use by typing kill [target].",
        "status": "Get your own status. Use by typing status.",
        "repeat": "Repeat your last action. Use by typing repeat or r",
        "r": "Repeat your last action. Use by typing repeat or r"  # IMPLEMENT REPEAT, store last input
    }

    @staticmethod
    def get_input():
        command = input(": ").split()
        verb_word = command[0]
        if verb_word in gameMethod.verb_dict:
            verb = getattr(gameMethod, verb_word)
        else:
            print(f"Unknown verb {verb_word}")
            print("For a list of commands type \"help\"")
            return
    
        if len(command) >= 2:
            noun_word = " ".join(command[1:])
            print(verb(noun_word))
        else:
            print(verb("nothing"))

    @staticmethod
    def hit(noun):
        for creature in character.current_room.creatures:
            if creature.name == noun:
                character.attack(creature)
                if creature.health <= 0:
                    character.current_room.remove_creature(creature)
                    return f"You have killed the {creature.name}!"
                else:
                    creature.attack(character)
                    return f"You prepare for your next move."
        else:
            return f"There is no {noun} to hit."
    
    @staticmethod
    def examine(noun):
        if noun == character.current_room.name or noun == "room":
            return character.current_room.contents
        for creature in character.current_room.creatures:
            if creature.name == noun:
                return creature.get_desc()
        return f"There is no {noun} here."
    
    @staticmethod
    def help(noun):
        if noun == "nothing":
            return list(gameMethod.verb_dict.keys())
        elif noun in gameMethod.verb_dict:
            return gameMethod.verb_dict[noun]
        else:
            return f"Unknown command {noun}"
    
    @staticmethod
    def heal(noun):
        character.heal()
        if len(character.current_room.creatures) > 0:
            for creature in character.current_room.creatures:
                creature.attack(character)
        return f"You prepare for your next move."
    
    @staticmethod
    def kill(noun):
        if noun == character.name or noun == "self":
            character.health = 0
            return "You have killed yourself!"
        for creature in character.current_room.creatures:
            if creature.name == noun:
                character.current_room.remove_creature(creature)
                return f"You have killed the {creature.name}!"
        else:
            return f"There is no {noun} to kill."

    def status(noun):
        return f"Your name is {character.name}, you have {character.health}/{character.max_health} HP.\nInventory: {character.inventory}"

class Dungeon:
    def __init__(self, num_rooms, world_seed=None):
        self.rooms = []
        self.generate(num_rooms, world_seed)

    def generate(self, num_rooms, world_seed=None):
        if world_seed is None:
            world_seed = random.Random()
        starting_room = Entrance()
        self.rooms.append(starting_room)
        unconnected_rooms = [starting_room]

        for i in range(num_rooms - 1):
            new_room = world_seed.choice([Hallway, Prison, TreasureRoom])()
            connected = False
            while not connected:
                parent_room = world_seed.choice(unconnected_rooms)
                if len(parent_room.adjacent_rooms) < 3:
                    # try to connect room to parent room
                    direction = world_seed.choice(["north", "south", "east", "west"])
                    connected = new_room.connect_to(parent_room, direction)
                    if connected:
                        unconnected_rooms.append(new_room)
                        self.rooms.append(new_room)
                        new_room.spawn_monsters()

        #  for room in self.rooms:
            #  print(room.name, [r.name for r in room.adjacent_rooms])

class Room:
    num_rooms = {}  # class variable to keep track of number of rooms of each subclass

    def __init__(self, name, x=0, y=0):
        self.name = name
        self.creatures = []
        self.adjacent_rooms = []
        self.monster_types = []
        self.num_monsters = 0
        if name not in Room.num_rooms:
            Room.num_rooms[name] = 1
        else:
            Room.num_rooms[name] += 1
        self.name += f" {Room.num_rooms[name]}"
        self.x = x
        self.y = y

    def connect_to(self, other, direction):
        if len(self.adjacent_rooms) >= 3 or len(other.adjacent_rooms) >= 3:
            return False
        if direction == "north":
            if other.y == 0 or self.y == other.y + 1:
                self.adjacent_rooms.append(other)
                other.adjacent_rooms.append(self)
                self.y = other.y - 1
                return True
        elif direction == "south":
            if other.y == 0 or self.y == other.y - 1:
                self.adjacent_rooms.append(other)
                other.adjacent_rooms.append(self)
                self.y = other.y + 1
                return True
        elif direction == "east":
            if other.x == 0 or self.x == other.x - 1:
                self.adjacent_rooms.append(other)
                other.adjacent_rooms.append(self)
                self.x = other.x + 1
                return True
        elif direction == "west":
            if other.x == 0 or self.x == other.x + 1:
                self.adjacent_rooms.append(other)
                other.adjacent_rooms.append(self)
                self.x = other.x - 1
                return True
        return False

    def add_creature(self, creature):
        self.creatures.append(creature)

    def spawn_monsters(self):
        for monster_number in range(self.num_monsters):
            monster_type = random.choice(self.monster_types)
            monster = monster_type()
            self.add_creature(monster)

    def remove_creature(self, creature):
        if creature in self.creatures:
            self.creatures.remove(creature)

    @property
    def contents(self):
        if len(self.creatures) == 0:
            return "There is nothing in this room"
        return f"In this room is {[str(i) for i in self.creatures]}."

class Entrance(Room):
    def __init__(self):
        super().__init__("entrance")
        self.monster_types = [Goblin, Slime]
        self.num_monsters = world_seed.randint(1, 3)

class Hallway(Room):
    def __init__(self):
        super().__init__("hallway")
        self.monster_types = [Goblin, Slime]
        self.num_monsters = world_seed.randint(1, 4)

class Prison(Room):
    def __init__(self):
        super().__init__("prison")
        self.monster_types = [Orc, Troll]
        self.num_monsters = world_seed.randint(1, 3)

class TreasureRoom(Room):
    def __init__(self):
        super().__init__("treasure room")
        self.monster_types = [Dragon]
        self.num_monsters = world_seed.randint(1, 2)

class Player:
    def __init__(self, name, starting_room, health=25, damage_multiplier=1, damage_range=(1,4), inventory=["Sword"]):
        self.name = name
        self.current_room = starting_room
        self.max_health = health
        self.health = health
        self.damage_multiplier = damage_multiplier
        self.damage_range = damage_range
        self.inventory = inventory
        print(f"You enter {self.current_room.name}. {self.current_room.contents}")

    def attack(self, target):
        damage_randomized = self.damage_multiplier * random.randrange(*self.damage_range)
        target.health -= damage_randomized
        print(f"You hit the {target.name} for {damage_randomized} damage!")

    def move_to_room(self, room_name):
        for room in self.current_room.adjacent_rooms:
            if room.name == room_name:
                self.current_room = room
                print(f"You have moved to {room_name}.")
                print(self.current_room.contents)
                return
        print(f"{room_name} is not adjacent to your current room.")
    
    def heal(self):
        heal_amount = random.randrange(3,5)
        if self.health + heal_amount > self.max_health:
            heal_amount = self.max_health - self.health
        self.health += heal_amount
        print(f"You have healed for {heal_amount} HP.")

class Creature:
    def __init__(self, name, class_name, desc, health, damage_multiplier, damage_range):
        self.name = name
        self.class_name = class_name
        self.desc = desc
        self.max_health = health
        self.health = health
        self.damage_multiplier = damage_multiplier
        self.damage_range = damage_range
    
    def attack(self, target):
        damage_randomized = self.damage_multiplier * random.randrange(*self.damage_range)
        target.health -= damage_randomized
        print(f"The {self.name} hit you for {damage_randomized} damage!")

    def __str__(self):
        return self.name

    def get_desc(self):
        if self.health >= self.max_health:
            return self.name + "\n" + self.desc
        else:
            health_line = f"{self.health}/{self.max_health} HP"
            return self.name + "\n" + self.desc + "\n" + health_line

class Goblin(Creature):
    possible_names = ["green goblin", "angry goblin", "sticky goblin", "bloody goblin", "warted goblin", "goblin"]
    def __init__(self):
        super().__init__(
            random.choice(Goblin.possible_names),
            Goblin,
            "A small green creature",
            random.randrange(5,11),
            1,
            (1,3)
        )

class Slime(Creature):
    possible_names = ["slime", "yellow slime", "purple slime", "red slime", "orange slime", "purple slime", "blue slime", "green slime"]
    def __init__(self):
        super().__init__(
            random.choice(Slime.possible_names),
            Slime,
            "A slimy, amorphous creature with a glowing gem at its core.",
            random.randrange(2,4),
            1,
            (1,2)
        )

class Ghost(Creature):  # TO MODIFY
    possible_names = ["ghost", "angry ghost", "red ghost", "bloody goblin", "warted goblin", "goblin"]
    def __init__(self):
        super().__init__(
            random.choice(Ghost.possible_names),
            Slime,
            "BOOOOOOOOOOOOO",
            random.randrange(2,4),
            1,
            (1,2)
        )

class Skeleton(Creature):  # TO MODIFY
    possible_names = ["skeleton", "broken skeleton", "shattered skeleton", "dark skeleton", "cloaked skeleton", "bloody skeleton", "angry skeleton"]
    def __init__(self):
        super().__init__(
            random.choice(Skeleton.possible_names),
            Slime,
            "CLACKCLACKCLACK",
            random.randrange(2,4),
            1,
            (1,2)
        )

class Zombie(Creature):  # TO MODIFY
    possible_names = ["zombie", "broken zombie", "hungry zombie", "pale zombie", "bloody zombie", "decayed zombie", "angry zombie"]
    def __init__(self):
        super().__init__(
            random.choice(Zombie.possible_names),
            Slime,
            "GRRRRRRRRR",
            random.randrange(2,4),
            1,
            (1,2)
        )

class GiantSpider(Creature):  # TO MODIFY
    possible_names = ["spider", "angry spider", "bloody spider", "hairy spider", "slimy spider", "fanged spider"]
    def __init__(self):
        super().__init__(
            random.choice(GiantSpider.possible_names),
            Slime,
            "HISSSSSSSSSSSSSS",
            random.randrange(2,4),
            1,
            (1,2)
        )

class Orc(Creature):  # TO MODIFY
    possible_names = ["orc", "green orc", "war orc", "bloody orc", "angry orc", "bearded orc", "large orc"]
    def __init__(self):
        super().__init__(
            random.choice(Orc.possible_names),
            Slime,
            "OINKOINKOINK",
            random.randrange(2,4),
            1,
            (1,2)
        )

class Troll(Creature):
    possible_names = ["green troll", "angry troll", "limping troll", "troll", "bloody troll"]
    def __init__(self):
        super().__init__(
            random.choice(Troll.possible_names),
            Troll,
            "An enormous, lumbering beast with green skin and glowing eyes.",
            random.randrange(15,20),
            1,
            (2,5)
        )

class Ogre(Creature):
    possible_names = ["bloody ogre", "ogre", "angry ogre", "careful ogre", "black ogre"]
    def __init__(self):
        super().__init__(
            random.choice(Ogre.possible_names),
            Ogre,
            "A massive, brutish creature with a club the size of a tree trunk.",
            random.randrange(30,35),
            1,
            (4,7)
        )

class Dragon(Creature):
    possible_names = ["great dragon", "dragon", "red dragon", "gold dragon"]
    def __init__(self):
        super().__init__(
            random.choice(Dragon.possible_names),
            Dragon,
            "A massive, fire-breathing beast with razor-sharp claws and scales as hard as steel.",
            random.randrange(70,75),
            1,
            (6,10)
        )

seed = input("Enter a seed: ")
world_seed = random.Random(seed)

size = world_seed.randint(5,10)

dungeon = Dungeon(size, world_seed)

name = input("What is your name? ")
character = Player(name, dungeon.rooms[0])

while character.health > 0:
    if not character.current_room.creatures:
        print("There are no enemies in this room.")
        room_options = [room.name for room in character.current_room.adjacent_rooms]
        print(f"Adjacent rooms: {room_options}")
        next_room = input("Which room would you like to move to? ")
        character.move_to_room(next_room)
        character.current_room.contents
    else:
        gameMethod.get_input()
else:
    print("You have 0 HP.")
    print("Game Over!")