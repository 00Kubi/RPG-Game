import random
import os
import time
from colorama import Fore, Style, init

# Inicjalizuj colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(duration=1):
    print(f"{Fore.YELLOW}Ładowanie", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(duration / 3)
    print(f"{Style.RESET_ALL}")

class SkillTree:
    def __init__(self):
        self.skills = {
            "Atak": 0,
            "Obrona": 0,
            "Magia": 0,
            "Skradanie się": 0,
            "Zwinność": 0
        }

    def upgrade_skill(self, skill):
        if skill in self.skills:
            self.skills[skill] += 1
            print(f"{Fore.GREEN}Ulepszono {skill} do poziomu {self.skills[skill]}!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Nieznana umiejętność.{Style.RESET_ALL}")

    def show_skills(self):
        print(f"{Fore.CYAN}Umiejętności:")
        for skill, level in self.skills.items():
            print(f"{skill}: Poziom {level}")
        print(Style.RESET_ALL)

class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.experience = 0
        self.level = 1
        self.skill_tree = SkillTree()
        self.inventory = []
        self.items_per_level = {
            2: "Miecz",
            3: "Zbroja",
            4: "Mikstura many",
            5: "Tarcza",
            6: "Mikstura życia",
            7: "Złoty pierścień",
            8: "Czarna księga magii"
        }

    def level_up(self):
        if self.experience >= 100:
            self.level += 1
            self.experience = 0
            self.health += 20
            print(f"{Fore.GREEN}{self.name} awansował na poziom {self.level}! Zdrowie wzrosło do {self.health}.{Style.RESET_ALL}")
            self.give_item()
            self.show_skill_upgrade_option()

    def give_item(self):
        if self.level in self.items_per_level:
            item = self.items_per_level[self.level]
            self.add_item(item)

    def show_skill_upgrade_option(self):
        if self.level > 1:
            print(f"{Fore.YELLOW}Otrzymujesz punkt umiejętności!{Style.RESET_ALL}")
            self.skill_tree.show_skills()
            skill = input("Wybierz umiejętność do ulepszenia (Atak, Obrona, Magia, Skradanie się, Zwinność): ").strip()
            self.skill_tree.upgrade_skill(skill)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            print(f"{Fore.RED}{self.name} został pokonany!{Style.RESET_ALL}")

    def heal(self, amount):
        self.health += amount
        print(f"{Fore.CYAN}{self.name} wyleczył się o {amount} zdrowia. Aktualne zdrowie: {self.health}.{Style.RESET_ALL}")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{Fore.YELLOW}{item} został dodany do ekwipunku.{Style.RESET_ALL}")

    def use_item(self, item_name):
        for item in self.inventory:
            if item == item_name:
                if item_name == "Mikstura życia":
                    self.heal(30)
                    self.inventory.remove(item)
                    break
                elif item_name == "Złoty pierścień":
                    print(f"{Fore.GREEN}{self.name} aktywował Złoty Pierścień, zwiększając szansę na krytyczny atak!{Style.RESET_ALL}")
                break
        else:
            print(f"{Fore.RED}Nie masz takiego przedmiotu.{Style.RESET_ALL}")

    def attack_animation(self):
        print(f"{Fore.CYAN}Atakujesz...", end="", flush=True)
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.5)
        print(f"{Style.RESET_ALL}")

class Monster:
    def __init__(self, name, health, damage, special_ability=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.special_ability = special_ability

    def attack(self, character):
        print(f"{Fore.MAGENTA}{self.name} atakuje {character.name} zadając {self.damage} obrażeń!{Style.RESET_ALL}")
        character.take_damage(self.damage)
        if self.special_ability:
            self.special_ability.use(character)

class HealingPotion:
    def __init__(self):
        self.name = "Mikstura życia"
        self.health_restore = 30

    def use(self, character):
        if character.health < 100:
            restore_amount = min(self.health_restore, 100 - character.health)
            character.health += restore_amount
            print(f"{Fore.GREEN}{character.name} używa {self.name}, przywracając {restore_amount} zdrowia. Aktualne zdrowie: {character.health}.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}{character.name} jest już w pełni zdrowy!{Style.RESET_ALL}")

class Quest:
    def __init__(self, description, reward):
        self.description = description
        self.reward = reward
        self.completed = False

    def complete(self):
        self.completed = True
        print(f"{Fore.GREEN}Quest '{self.description}' został zakończony! Otrzymujesz {self.reward} doświadczenia.{Style.RESET_ALL}")
        return self.reward

class NPC:
    def __init__(self, name):
        self.name = name
        self.quests = []

    def give_quest(self, quest):
        self.quests.append(quest)
        print(f"{Fore.CYAN}{self.name} daje ci quest: {quest.description}{Style.RESET_ALL}")

class Game:
    def __init__(self):
        self.player = None
        self.locations = ["Wioska", "Las", "Góra", "Zamek", "Podziemia", "Ruiny"]
        self.monsters = [
            Monster("Goblin", 30, 10),
            Monster("Ork", 50, 15, HealingPotion()),
            Monster("Smok", 80, 25),
            Monster("Wilk", 40, 12),
            Monster("Szkielet", 45, 10),
            Monster("Troll", 60, 20),
            Monster("Czarny Mag", 70, 18),
            Monster("Złodziej", 30, 25)
        ]
        self.npcs = [NPC("Starzec"), NPC("Wojownik"), NPC("Czarodziej")]
        self.quests = [
            Quest("Zabij 3 gobliny", 50),
            Quest("Zabij orka", 100),
            Quest("Zabij 2 wilki", 75),
            Quest("Zbierz 5 ziół", 30),
            Quest("Zabij trola", 150),
            Quest("Zabij czarnego maga", 200)
        ]

    def start_game(self):
        clear_screen()
        player_name = input("Wprowadź imię swojej postaci: ")
        self.player = Character(player_name)
        print(f"{Fore.GREEN}Witaj, {self.player.name}! Rozpoczynasz swoją przygodę.{Style.RESET_ALL}")

        while True:
            print("\nDostępne lokalizacje:", ', '.join(self.locations))
            action = input("Wybierz akcję: [lokacja, walka, quest, interakcja, przedmioty, zapis, zakończ]: ").strip().lower()
            clear_screen()

            if action == "lokacja":
                self.change_location()
            elif action == "walka":
                self.fight()
            elif action == "quest":
                self.complete_quest()
            elif action == "interakcja":
                self.interact_with_npc()
            elif action == "przedmioty":
                self.manage_items()
            elif action == "zapis":
                self.save_game()
            elif action == "zakończ":
                print(f"{Fore.RED}Dziękujemy za grę!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Nieznana akcja. Spróbuj ponownie.{Style.RESET_ALL}")

    def change_location(self):
        print("Wybierz lokalizację:", ', '.join(self.locations))
        location = input("Wpisz nazwę lokalizacji: ").strip()
        if location in self.locations:
            print(f"{Fore.YELLOW}Przenosisz się do {location}.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Nieznana lokalizacja.{Style.RESET_ALL}")

    def fight(self):
        monster = random.choice(self.monsters)
        print(f"{Fore.RED}Napotkałeś {monster.name}!{Style.RESET_ALL}")
        loading_animation()

        while monster.health > 0 and self.player.health > 0:
            self.player.attack_animation()
            monster.health -= 20  # Zadaj 20 obrażeń
            print(f"{Fore.CYAN}Zadajesz {20} obrażeń {monster.name}. Jego zdrowie: {monster.health}.{Style.RESET_ALL}")

            if monster.health > 0:
                monster.attack(self.player)
            else:
                print(f"{Fore.GREEN}Pokonałeś {monster.name}!{Style.RESET_ALL}")
                self.player.experience += monster.health // 10  # Zwiększ doświadczenie
                self.player.level_up()  # Sprawdź, czy poziom się zwiększył

    def complete_quest(self):
        quest_completed = False
        for quest in self.quests:
            if not quest.completed:
                quest_completed = True
                print(f"{Fore.GREEN}Kompletny quest: {quest.description}.{Style.RESET_ALL}")
                reward = quest.complete()
                self.player.experience += reward
                break
        if not quest_completed:
            print(f"{Fore.YELLOW}Nie masz żadnych questów do ukończenia.{Style.RESET_ALL}")

    def interact_with_npc(self):
        print("Dostępni NPC:", ', '.join(npc.name for npc in self.npcs))
        npc_name = input("Wybierz NPC do interakcji: ").strip()
        for npc in self.npcs:
            if npc.name.lower() == npc_name.lower():
                quest = random.choice(self.quests)
                accept = input(f"{Fore.CYAN}Zadajesz pytanie do {npc.name}: '{quest.description}'. Chcesz przyjąć ten quest? [tak/nie]: ").strip().lower()
                if accept == "tak":
                    npc.give_quest(quest)
                    break
        else:
            print(f"{Fore.YELLOW}Nie ma żadnych NPC w pobliżu.{Style.RESET_ALL}")

    def manage_items(self):
        print("Twoje przedmioty:", ', '.join(item for item in self.player.inventory))
        item_name = input("Wpisz nazwę przedmiotu, aby go użyć: ").strip()
        self.player.use_item(item_name)

    def save_game(self):
        with open("save_game.txt", "w") as f:
            f.write(f"{self.player.name},{self.player.level},{self.player.experience},{self.player.health}\n")
            f.write(",".join(self.player.inventory) + "\n")
            f.write(",".join(f"{skill}:{level}" for skill, level in self.player.skill_tree.skills.items()))
            print(f"{Fore.GREEN}Gra została zapisana!{Style.RESET_ALL}")

# Uruchomienie gry
if __name__ == "__main__":
    game = Game()
    game.start_game()
