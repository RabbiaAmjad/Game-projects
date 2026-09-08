#Python project inpired by the 12 dancing pricesses💃🩰🪭
import json
import os

import random
import time

# -----------------------------------------TEXT EFFECTS-----------------------------------------
def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
# -----------------------------------------COLOR UTIL-----------------------------------------
class Colors:
    RESET = "\033[0m"

    LOCKED = "\033[90m"      # Gray
    AVAILABLE = "\033[95m"   # Pink / light purple
    UNLOCKED = "\033[93m"    # Gold / yellow

    MAGIC = "\033[94m"       # Blue
    CONFIDENCE = "\033[91m"  # Red / pink
    ENERGY = "\033[92m"      # Green
# these are ansi codes no libraries

# -----------------------------------------CREATING THE TILE CLASS---------------------------------------------------------
class Tile:
    """A tile has a name, theme, a challenge, and a locked/unlocked state."""
    def __init__(self, name, theme, play_function, symbol="◇"):
        self.name = name
        self.theme = theme
        self.play_function = play_function
        self.unlocked = False
        self.symbol=symbol

    def play(self, player):
        print(f"\n▶ Entering tile: {self.name}")
        if self.unlocked:
          print(f"\n✨ {self.name} Tile already unlocked ✨")
          return None

        result = self.play_function(player)

        if result:
          self.unlocked = True
        else:
          player.failures += 1
        player.normalize_stats()

        return result

# -----------------------------------------------------PLAYER CLASS-----------------------------------------   
class Player:
    def __init__(self):
        """player stats are stored"""
        self.magic = 50
        self.confidence = 50
        self.energy = 50

        # 🌑☀️ World tracking
        self.failures = 0
        self.visited_lower_world = False

    def show_stats(self):
       print("\n🔮 PLAYER STATS")
       print(f"{Colors.MAGIC}✨ Magic: {self.magic}{Colors.RESET}")
       print(f"{Colors.CONFIDENCE}💖 Confidence: {self.confidence}{Colors.RESET}")
       print(f"{Colors.ENERGY}💫 Energy: {self.energy}{Colors.RESET}")


    def normalize_stats(self):
        """validation if stats go negative"""
        self.magic = max(0, self.magic)
        self.confidence = max(0, self.confidence)
        self.energy = max(0, self.energy)

# saving and loading player game stats
    def to_dict(self):
      return {
        "magic": self.magic,
        "confidence": self.confidence,
        "energy": self.energy,
        "failures": self.failures,
        "visited_lower_world": self.visited_lower_world
    }

    def load_from_dict(self, data):
      self.magic = data.get("magic", 50)
      self.confidence = data.get("confidence", 50)
      self.energy = data.get("energy", 50)
      self.failures = data.get("failures", 0)
      self.visited_lower_world = data.get("visited_lower_world", False)




# ---------------------------------------------------TILE LOGIC FUNCTIONS-----------------------------------
#-------------------------------------------------------🌷TULIP 🌷-------------------------------------------
def tulip_tile(player):
    print("\n🌷 TULIP TILE — CURIOSITY 🌷")
    print("Choose the correct rhythm:")
    print("1) Slow Waltz")
    print("2) Fast Spin")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "2":
        print("✨ Graceful move! ✨")
        player.confidence += 10
        player.magic += 5
        return True
    else:
        print("❌ The rhythm fades.")
        player.energy -= 5
        return False

# --------------------------------------------------------🌸LILY🌸------------------------------------------------
def lily_tile(player):
    print("\n🌸 LILY TILE — GRACE 🌸")
    print("Choose the most graceful response.\n")

    attempts = 0

    while attempts < 3:
        print("a) Rush forward")
        print("b) Pause and step lightly")
        print("c) Turn back")

        choice = input("Enter a, b, or c: ").strip().lower()

        if choice == "b":
            print("✨ Grace unlocks the tile ✨")
            player.confidence += 10
            player.magic += 5
            return True
        elif choice in ["a", "c"]:
            print("❌ Not graceful.")
            player.energy -= 5
            attempts += 1
        else:
            print("⚠️ Invalid input.")
            attempts +=1

    print("❌ Grace lost.")
    return False

# ------------------------------------------------------🔵BLUE IRIS🔵-----------------------------------------------

def iris_tile(player):
    print("\n🔵 IRIS TILE — FOCUS 🔵")

    symbols = {
        "1": "✨",
        "2": "🌸",
        "3": "🌙",
        "4": "💎"
    }

    print("Symbol Guide:")
    for k, v in symbols.items():
        print(f"{k} → {v}", end="   ")
    print("\n")

    sequence = random.sample(list(symbols.keys()), 3)

    print("Remember this sequence:")
    for num in sequence:
        print(f"{num} {symbols[num]}", end="   ")

    time.sleep(4)
    print("\n" * 15)

    user = input("Enter numbers (e.g. 2 4 1): ").strip().split()

    if user == sequence:
        print("✨ Perfect focus! ✨")
        player.magic += 10
        player.confidence += 5
        return True
    else:
        print("❌ Focus lost.")
        player.energy -= 5
        return False
    
# ----------------------------------------------- 🌹ROSE — KINDNESS🌹------------------------------------------------
def rose_tile(player):
    print("\n🌹 ROSE TILE — KINDNESS 🌹")
    print("You see someone struggling.")
    print("a) Ignore them")
    print("b) Help them")
    print("c) Laugh")

    choice = input("Choose a, b, or c: ").lower()

    if choice == "b":
        print("✨ Kindness blooms ✨")
        player.confidence += 10
        player.magic += 5
        return True
    else:
        print("❌ Compassion missed.")
        player.energy -= 5
        return False

# ------------------------------------------------------🌼DAISY — JOY🌼------------------------------------------
def daisy_tile(player):
    print("\n🌼 DAISY TILE — JOY 🌼")
    print("Choose what brings joy:")
    print("1) Competing")
    print("2) Creating")
    print("3) Complaining")

    choice = input("Enter 1, 2, or 3: ")

    if choice == "2":
        print("✨ Joy fills you ✨")
        player.energy += 10
        return True
    else:
        print("❌ Joy fades.")
        player.energy -= 5
        return False

# ------------------------------------------------🌻SUNFLOWER — ENERGY🌻-------------------------------------
def sunflower_tile(player):
    print("\n🌻 SUNFLOWER TILE — ENERGY 🌻")
    print("Quick decision! Type 'rise' in 3 seconds!")

    import time
    start = time.time()
    choice = input("Type here: ").lower()
    end = time.time()

    if choice == "rise" and end - start <= 3:
        print("✨ Energy surges ✨")
        player.energy += 10
        return True
    else:
        print("❌ Too slow or wrong.")
        player.energy -= 5
        return False

# --------------------------------------------------🔵BLUE LILY — COURAGE--------------------------------------
def blue_lily_tile(player):
    print("\n🔵 BLUE LILY — COURAGE 🔵")
    print("You must speak despite fear.")
    print("Type: 'I am brave'")

    choice = input("Say it: ").lower()

    if choice == "i am brave":
        print("✨ Courage unlocked ✨")
        player.confidence += 15
        return True
    else:
        print("❌ Fear wins.")
        return False

# -------------------------------------------------🌸ORCHID — WISDOM 🌸-------------------------------------
def orchid_tile(player):
    print("\n🌸 ORCHID TILE — WISDOM 🌸")
    print("What matters more?")
    print("a) Knowing everything")
    print("b) Understanding deeply")
    print("c) Winning arguments")

    choice = input("Choose a, b, or c: ").lower()

    if choice == "b":
        print("✨ Wisdom grows ✨")
        player.magic += 15
        return True
    else:
        print("❌ Wisdom delayed.")
        return False

# --------------------------------------------------🪷LOTUS — BALANCE🪷--------------------------------------------
def lotus_tile(player):
    print("\n🪷 LOTUS TILE — BALANCE 🪷")
    print("Balance your stats.")
    print("Choose one stat to sacrifice (+5 to others):")
    print("1) Magic  2) Confidence  3) Energy")

    choice = input("Enter 1, 2, or 3: ")

    if choice == "1":
        player.magic -= 5
    elif choice == "2":
        player.confidence -= 5
    elif choice == "3":
        player.energy -= 5
    else:
        return False

    player.magic += 5
    player.confidence += 5
    player.energy += 5
    print("✨ Balance achieved ✨")
    return True

# ------------------------------------------------🌺PEONY — LEADERSHIP🌺-------------------------------------
def peony_tile(player):
    print("\n🌺 PEONY TILE — LEADERSHIP 🌺")
    print("Your team is unsure.")
    print("a) Command loudly")
    print("b) Listen and guide")
    print("c) Walk away")

    choice = input("Choose a, b, or c: ").lower()

    if choice == "b":
        print("✨ Leadership shines ✨")
        player.confidence += 10
        player.magic += 5
        return True
    else:
        print("❌ Leadership fails.")
        return False

# -------------------------------------------🌼JASMINE — UNITY🌼-------------------------------------
def jasmine_tile(player):
    print("\n🌼 JASMINE TILE — UNITY 🌼")
    print("Two paths conflict.")
    print("Type a sentence including BOTH words:")
    print("'listen' and 'together'")

    choice = input("Type here:").lower()  #we should listen and grow together

    if "listen" in choice and "together" in choice:
        print("✨ Unity formed ✨")
        player.confidence += 10
        return True
    else:
        print("❌ Division remains.")
        return False

# --------------------------------------🌙🩷PINK ROSE — FINAL TRUTH🌙🩷--------------------------------------
def pink_rose_tile(player):
    print("\n🌹🌙 FINAL TILE — TRUTH 🌙🌹")
    print("Answer honestly.")
    answer = input("Why did you come here?") #I came here to grow and understand myself better

    if len(answer.strip()) > 10:
        print("\n✨ The gate opens ✨")
        print("You sought growth, not victory.")
        return True
    else:
        print("❌ The gate remains closed.")
        return False

# ---------------------------------------------creating lower world----------------------------------------
def lower_world(player):
    print("\n🌑🌫️ YOU HAVE ENTERED THE LOWER WORLD 🌫️🌑")
    print("The ground is cold. The music slows.\n")

    print("A quiet voice asks:")
    print("❝ What do you keep avoiding? ❞\n")

    response = input("Answer honestly (one sentence)").strip() #ans:I keep avoiding my fear of failure and judgment

    if len(response) >= 15:
        print("\n✨ The shadows loosen their grip.")
        print("You feel steadier.\n")

        player.energy += 10
        player.confidence += 5
        player.failures = 0
        player.visited_lower_world = True

        print("🌸 You rise back to the Tile Floor 🌸")
    else:
        print("\n🌑 The silence remains.")
        print("You need more reflection.\n")

        player.energy -= 5

# -----------------------------------------Creating upper world--------------------------------------
def upper_world(player):
    print("\n☀️🌸 YOU HAVE REACHED THE UPPER WORLD 🌸☀️")
    print("Light surrounds you. The air feels open.\n")

    if player.visited_lower_world:
        print("You have known both shadow and light.")
        print("That balance has changed you.\n")
    else:
        print("Your path was steady, yet growth still found you.\n")

    print("The world asks one final question:")
    print("What will guide you forward?\n")

    print("a) Awareness")
    print("b) Kindness")
    print("c) Courage")

    choice = input("Choose a, b, or c: ").strip().lower()

    titles = {
        "a": "The Watchful Dancer",
        "b": "The Gentle Light",
        "c": "The Fearless Heart"
    }

    title = titles.get(choice, "The One Who Is Becoming")

    print(f"\n✨ You are now known as: {title} ✨")
    print("\n🌷 THE JOURNEY IS COMPLETE 🌷")


# -----------------------------------------------------CREATING THE 12 TILES-------------------------------------

tiles = [
    Tile("Tulip", "Curiosity", tulip_tile, "🌷"),
    Tile("Lily", "Grace", lily_tile, "🌸"),
    Tile("Iris", "Focus", iris_tile, "🔵"),
    Tile("Rose", "Kindness", rose_tile, "🌹"),
    Tile("Daisy", "Joy", daisy_tile, "🌼"),
    Tile("Sunflower", "Energy", sunflower_tile, "🌻"),
    Tile("Blue Lily", "Courage", blue_lily_tile, "💙"),
    Tile("Orchid", "Wisdom", orchid_tile, "🌺"),
    Tile("Lotus", "Balance", lotus_tile, "🪷"),
    Tile("Peony", "Leadership", peony_tile, "🌺"),
    Tile("Jasmine", "Unity", jasmine_tile, "🌼"),
    Tile("Pink Rose", "Final Gate", pink_rose_tile, "🌙"),
]
# -------------------------------------------GUI archi for title screen---------------------------------
def title_screen():
    print("\n" * 2)
    print("🌸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌸")
    print("        ✨ THE ENCHANTED TILES ✨        ")
    print("🌸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌸\n")

    print("A journey of growth, reflection, and balance.\n")
    time.sleep(1)

    print("1) 🌷 Begin New Journey")
    print("2) 📂 Continue Journey")
    print("3) ❌ Exit\n")

    choice = input("Choose an option (1–3): ").strip()

    return choice

#------------------------------------------- final polish summary line method------------------------------------
def journey_summary(player):
    print("\n🌸✨ JOURNEY SUMMARY ✨🌸")

    print(f"✨ Magic: {player.magic}")
    print(f"💖 Confidence: {player.confidence}")
    print(f"💫 Energy: {player.energy}")

    if player.visited_lower_world:
        print("\n🌑 You faced your shadow and returned stronger.")
    else:
        print("\n☀️ Your path was steady and bright.")

    print("\n🌷 Thank you for walking the Enchanted Tiles 🌷")

# -----------------------------------------GAME CONTROLLER-----------------------------------------
class Game:
    def __init__(self):
        self.player = Player()
        self.tiles = tiles

# adding helper function for UI purpose
    def tile_visual(self, tile, index):
       if tile.unlocked:
         return f"{Colors.UNLOCKED}✨ UNLOCKED{Colors.RESET}"
       elif index == 0 or self.tiles[index - 1].unlocked:
         return f"{Colors.AVAILABLE}🌸 AVAILABLE{Colors.RESET}"
       else:
         return f"{Colors.LOCKED}🔒 LOCKED{Colors.RESET}"

# tile reveal animation for text based game-helper method
    def reveal_tiles(self):
       print("\n🌫️ The tiles begin to glow...\n")
       time.sleep(0.6)

       for i, tile in enumerate(self.tiles, start=1):
         status = self.tile_visual(tile, i - 1)
         print(
            f"{Colors.AVAILABLE}{i:>2}.{Colors.RESET} "
            f"{tile.symbol} {tile.name:<12} | {status}"
        )
         time.sleep(0.25)  # ✨ animation speed

#modifying show tile floor method
    def show_tile_floor(self):
      print("\n" + "═" * 50)
      print("🌷✨        THE ENCHANTED TILE FLOOR        ✨🌷")
      print("═" * 50)

      self.reveal_tiles()

      print("─" * 50)
      self.player.show_stats()
      print("═" * 50)

# adding animations like barbie effects
    def unlock_animation(self, tile):
      print("\n🌸 The tile begins to shimmer...")
      time.sleep(0.5)

      for _ in range(3):
        print("✨✨✨")
        time.sleep(0.2)

      print(f"\n{Colors.UNLOCKED}{tile.symbol} {tile.name} AWAKENS! ✨{Colors.RESET}")
      time.sleep(0.4)

# checkking tile locking status
    def get_tile_status(self, index):
        tile = self.tiles[index]

        if tile.unlocked:
          return f"{Colors.UNLOCKED}UNLOCKED ✨{Colors.RESET}"

        elif index == 0 or self.tiles[index - 1].unlocked:
          return f"{Colors.AVAILABLE}AVAILABLE 🌸{Colors.RESET}"

        else:
          return f"{Colors.LOCKED}LOCKED 🔒{Colors.RESET}"


    def play_turn(self):
        # 🌑 Lower World check
        if self.player.failures >= 3 and not self.player.visited_lower_world:
            lower_world(self.player)

        self.show_tile_floor()

# save and load choices in game controller
        choice = input(
    "\nChoose tile number | (s) Save | (l) Load | (q) Quit: "
).strip().lower()

        if choice == "q":
         return False

        if choice == "s":
          self.save_game()
          return True

        if choice == "l":
          self.load_game()
          return True

        if not choice.isdigit():
          return True


        index = int(choice) - 1
        if index < 0 or index >= len(self.tiles):
            return True

        # progression rule
        if index > 0 and not self.tiles[index - 1].unlocked:
            print("🚪 This tile is still sealed.")
            return True

        result = self.tiles[index].play(self.player)

        if result:
           self.unlock_animation(self.tiles[index])


        # ☀️ Upper World check
        if all(tile.unlocked for tile in self.tiles):
            upper_world(self.player)
            return False
    
        journey_summary(self.player)

    # ATMOSPHERIC FEEDBACK
        if self.player.energy <= 15:
            print("\n🌫️ You feel weak… the tiles feel heavier beneath your feet.")

        if self.player.failures == 2:
            print("\n🌑 The shadows are close. Be mindful.")

        return True

    def run(self):
      while True:
        choice = title_screen()

        if choice == "1":
            print("\n🌷 A new journey begins...\n")
            time.sleep(1)
            break

        elif choice == "2":
            if os.path.exists(self.SAVE_FILE):
                self.load_game()
                print("\n📂 Journey restored.\n")
                time.sleep(1)
                break
            else:
                print("\n📂 No saved journey found.\n")
                time.sleep(1)

        elif choice == "3":
            print("\n🌙 Until next time...\n")
            return

        else:
            print("\n⚠️ Invalid choice.\n")
            time.sleep(1)

    # 🎮 MAIN GAME LOOP
      running = True
      while running:
        running = self.play_turn()


    
    SAVE_FILE = "game_save.json"
#adding save load methods to save in json
    SAVE_FILE = "game_save.json"

    def save_game(self):
      data = {
        "player": self.player.to_dict(),
        "tiles": [tile.unlocked for tile in self.tiles]
    }

      with open(self.SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

      print("💾 Game saved successfully!")

    def load_game(self):
      if not os.path.exists(self.SAVE_FILE):
        print("📂 No saved game found.")
        return

      with open(self.SAVE_FILE, "r") as f:
        data = json.load(f)

      self.player.load_from_dict(data["player"])

      for tile, unlocked in zip(self.tiles, data["tiles"]):
        tile.unlocked = unlocked

      print("📂 Game loaded successfully!")

# -----------------------------------------START GAME-----------------------------------------
game = Game()
game.run()
