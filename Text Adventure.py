import random

class GameObject:
    verb_dict = {
        "examine": "Examine a creature in the room. Use by typing examine [target].",
        "hit": "Hit a creature in the room. Use by typing hit [target].",
        "help": "Get help about the available commands. Use by typing help [command].",
        "heal": "Heal for an amount of damage. Use by typing heal.",
        "kill": "Immediately kill the target. Use by typing kill [target].",
        "status": "Get your own status. Use by typing status."
    }

    @staticmethod
    def get_input():
        command = input(": ").split()
        verb_word = command[0]
        if verb_word in GameObject.verb_dict:
            verb = getattr(GameObject, verb_word)
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
            return list(GameObject.verb_dict.keys())
        elif noun in GameObject.verb_dict:
            return GameObject.verb_dict[noun]
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

class Room:
    def __init__(self, name):
        self.name = name
        self.creatures = []
        self.adjacent_rooms = []

    def add_creature(self, creature):
        self.creatures.append(creature)

    def remove_creature(self, creature):
        if creature in self.creatures:
            self.creatures.remove(creature)

    @property
    def contents(self):
        if len(self.creatures) == 0:
            return "There is nothing in this room"
        return f"In this room is {[str(i) for i in self.creatures]}."

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
    possible_names = ["green goblin", "angry goblin", "sticky goblin", "bloody goblin", "warted goblin", "goblin"]
    def __init__(self):
        super().__init__(
            random.choice(Goblin.possible_names),
            Slime,
            "A slimy, amorphous creature with a glowing gem at its core.",
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

entrance = Room("entrance")
goblin1 = Goblin()
entrance.add_creature(goblin1)

hallway = Room("hallway")
slime1 = Slime()
hallway.add_creature(slime1)

dungeon = Room("dungeon")
troll1 = Troll()
dungeon.add_creature(troll1)

treasure_room = Room("treasure_room")
dragon1 = Dragon()
treasure_room.add_creature(dragon1)

entrance.adjacent_rooms.append(hallway)
hallway.adjacent_rooms.append(entrance)
hallway.adjacent_rooms.append(dungeon)
hallway.adjacent_rooms.append(treasure_room)
dungeon.adjacent_rooms.append(hallway)
treasure_room.adjacent_rooms.append(hallway)

name = input("What is your name? ")
character = Player(name, entrance)

while character.health > 0:
    if not character.current_room.creatures:
        print("You have defeated all the creatures in this room.")
        room_options = [room.name for room in character.current_room.adjacent_rooms]
        print(f"Adjacent rooms: {room_options}")
        next_room = input("Which room would you like to move to? ")
        character.move_to_room(next_room)
        character.current_room.contents
    else:
        GameObject.get_input()
else:
    print("You have 0 HP.")
    print("Game Over!")