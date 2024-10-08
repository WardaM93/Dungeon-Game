import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional
from support import *

# Implement the classes, methods & functions described in the task sheet here

def main():
    # Implement your main function here

    Position = tuple[int, int]  # Alias for position coordinates (x, y)

class Weapon():
    def __init__(self):
        self._name = "AbstractWeapon"
        self._symbol = "W"
        self._effect = {}
        self._range = 0
    
    
    def get_name(self) -> str:
        """Returns the name of the weapon."""
        return self._name
    
    
    def get_symbol(self) -> str:
        """Returns the symbol of the weapon."""
        return self._symbol
    
    
    def get_effect(self) -> dict[str, int]:
        """Returns the effect of the weapon as a dictionary."""
        return self._effect
    
    
    def get_targets(self, position: Position) -> list[Position]:
        """Returns a list of positions in range from the given position (cardinal directions only)."""
        x, y = position
        targets = []
        
        # List of possible movements in the four cardinal directions (up, down, left, right)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            for step in range(1, self._range + 1):
                target = (x + dx * step, y + dy * step)
                targets.append(target)
    
        return targets
    
    def __str__(self) -> str:
        """Returns the string representation of the weapon's name."""
        return self.get_name()
    
    def __repr__(self) -> str:
        """Returns a representation of the weapon for REPL use."""
        return f"{self.__class__.__name__}()"


class PoisonDart(Weapon):
    def __init__(self):
        super().__init__()
        self._name = "PoisonDart"
        self._symbol = "D"
        self._effect = {"poison": 2}
        self._range = 2
    
    def get_name(self) -> str:
        return self._name
    
    def get_symbol(self) -> str:
        return self._symbol
    
    def get_effect(self) -> dict[str, int]:
        return self._effect


class PoisonSword(Weapon):
    def __init__(self):
        super().__init__()
        self._name = "PoisonSword"
        self._symbol = "S"
        self._effect = {"damage": 2, "poison": 1}
        self._range = 1
    
    def get_name(self) -> str:
        return self._name
    
    def get_symbol(self) -> str:
        return self._symbol
    
    def get_effect(self) -> dict[str, int]:
        return self._effect


class HealingRock(Weapon):
    def __init__(self):
        super().__init__()
        self._name = "HealingRock"
        self._symbol = "H"
        self._effect = {"healing": 2}
        self._range = 2
    
    def get_name(self) -> str:
        return self._name
    
    def get_symbol(self) -> str:
        return self._symbol
    
    def get_effect(self) -> dict[str, int]:
        return self._effect

class Tile():
    def __init__(self, symbol, is_blocking_tile):
        self._symbol = symbol
        self._is_blocking_tile = is_blocking_tile  # This is the attribute
        self._weapon = None  # Initialize with no weapon

    def is_blocking_tile(self) -> bool:
        """Method to check if the tile is blocking."""
        return self._is_blocking_tile  # Access the attribute
    
    def is_blocking(self) -> bool:
        """Backward-compatible method to check if the tile is blocking."""
        return self.is_blocking_tile()
    
    def set_weapon(self, weapon):
        self._weapon = weapon

    def get_weapon(self):
        return self._weapon
    
    def remove_weapon(self) -> None:
        """Removes the current weapon from the tile."""
        self._weapon = None
    
    def __str__(self) -> str:
        """Returns the symbol of this tile."""
        return self._symbol
    
    def __repr__(self):
        return f"Tile('{self._symbol}', {self._is_blocking_tile})"

    
def create_tile(symbol: str) -> Tile:
    """Constructs and returns a Tile based on the symbol."""
    if symbol == "#":
        return Tile("#", True)
    elif symbol in [" ", "G"]:
        return Tile(symbol, False)
    elif symbol in ["D", "S", "H"]:
        tile = Tile(" ", False)
        if symbol == "D":
            tile.set_weapon(PoisonDart())
        elif symbol == "S":
            tile.set_weapon(PoisonSword())
        elif symbol == "H":
            tile.set_weapon(HealingRock())
        return tile
    else:
        return Tile(" ", False)
    
class Entity():
    def __init__(self, max_health: int) -> None:
        """Constructs an entity with a given max health."""
        self._max_health = max_health
        self._health = max_health
        self._poison = 0
        self._weapon = None
        self._symbol = ENTITY_SYMBOL
        self._name = "Entity"

    def get_symbol(self) -> str:
        """Returns the symbol of the entity."""
        return self._symbol

    def get_name(self) -> str:
        """Returns the name of the entity."""
        return self._name

    def get_health(self) -> int:
        """Returns the current health of the entity."""
        return self._health

    def get_poison(self) -> int:
        """Returns the poison stat of the entity."""
        return self._poison

    def get_weapon(self) -> Optional['Weapon']:
        """Returns the weapon held by the entity."""
        return self._weapon

    def equip(self, weapon: 'Weapon') -> None:
        """Equips the entity with a weapon."""
        self._weapon = weapon

    def get_weapon_targets(self, position: 'Position') -> list['Position']:
        """Returns the positions the entity can attack with its weapon."""
        if self._weapon:
            return self._weapon.get_targets(position)
        return []

    def get_weapon_effect(self) -> dict[str, int]:
        """Returns the effect of the entity's weapon."""
        if self._weapon:
            return self._weapon.get_effect()
        return {}

    def apply_effects(self, effects: dict[str, int]) -> None:
        """Applies effects to the entity (now public)."""
        self._health = min(self._max_health, max(0, self._health + effects.get("healing", 0) - effects.get("damage", 0)))
        self._poison += effects.get("poison", 0)

    def apply_poison(self) -> None:
        """Applies poison damage to the entity."""
        if self._poison > 0:
            self._health = max(0, self._health - self._poison)
            self._poison -= 1

    def is_alive(self) -> bool:
        """Returns True if the entity is still alive, False otherwise."""
        return self._health > 0

    def __str__(self) -> str:
        return self.get_name()

    def __repr__(self) -> str:
        """Returns a string representation of the entity in the format Entity(health)."""
        return f"{self.__class__.__name__}({self._max_health})"

    
class Player(Entity):
    def __init__(self, max_health: int = 20) -> None:
        """Constructs a player entity with a default max health of 20."""
        super().__init__(max_health)
        self._max_health = max_health
        self._health = max_health
        self._poison = 0
        self._symbol = PLAYER_SYMBOL

    def apply_poison(self) -> None:
        """Applies poison damage to the entity."""
        if self._poison > 0:
            self._health = max(0, self._health - self._poison)
            self._poison -= 1
            
    def get_health(self) -> int:
        """Returns the current health of the entity."""
        return self._health

    def get_poison(self) -> int:
        """Returns the poison stat of the entity."""
        return self._poison
    
    def get_symbol(self) -> str:
        return "P"
    
    def get_name(self) -> str:
        return "Player"
    
class Slug(Entity):
    
    def __init__(self, max_health: int) -> None:
        """Constructs a slug with the given max health."""
        super().__init__(max_health)
        self._can_move_flag = True
        self._symbol = SLUG_SYMBOL
        self._name = 'Slug'
        self._stunned = False
        self._poisoned = False

    
    def choose_move(self, candidates: list['Position'], current_position: 'Position', player_position: 'Position') -> 'Position':
        raise NotImplementedError("Slug subclasses must implement a choose_move method.")
    
    def can_move(self) -> bool:
        """Returns True if the slug can move this turn, otherwise False."""
        return self._can_move_flag

    def set_can_move_flag(self, can_move: bool) -> None:
        """Sets whether the slug can move."""
        self._can_move_flag = can_move
    
    def end_turn(self) -> None:
        """Registers that the slug has completed another turn."""
        self._can_move_flag = not self._can_move_flag

    def is_poisoned(self) -> bool:
        """Returns True if the slug is poisoned (i.e., poison value > 0)."""
        return self._poison > 0

    def is_stunned(self) -> bool:
        """Returns True if the slug is stunned (i.e., cannot move due to stun effect)."""
        return self._stunned
    
    def __str__(self) -> str:
        return "Slug"
    
    def __repr__(self) -> str:
        return f"Slug({self._max_health})"

class NiceSlug(Slug):
    def __init__(self) -> None:
        """Constructs a NiceSlug with a default max health of 10 and a HealingRock weapon."""
        super().__init__(10)
        self.equip(HealingRock())
        self._symbol = NICE_SLUG_SYMBOL
        self._name = "NiceSlug"
        
    
    def choose_move(self, candidates: list['Position'], current_position: 'Position', player_position: 'Position') -> 'Position':
        """Returns the current position since the NiceSlug stays where it is."""
        return current_position
    
    def __str__(self) -> str:
        return "NiceSlug"
    
    def __repr__(self) -> str:
        return "NiceSlug()"

class AngrySlug(Slug):
    def __init__(self) -> None:
        """Constructs an AngrySlug with a default max health of 5 and a PoisonSword weapon."""
        super().__init__(5)
        self.equip(PoisonSword())
        self._symbol = ANGRY_SLUG_SYMBOL
        self._name = "AngrySlug"
    
    def choose_move(self, candidates: list['Position'], current_position: 'Position', player_position: 'Position') -> 'Position':
        """Moves towards the player, choosing the closest position."""
        closest_position = min(candidates + [current_position], key=lambda pos: (self.distance(pos, player_position), pos))
        return closest_position
    
    
    def distance(self, pos1, pos2):
    # Correct version to compute the Euclidean distance
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    
    def __str__(self) -> str:
        return "AngrySlug"
    
    def __repr__(self) -> str:
        return "AngrySlug()"
    
class ScaredSlug(Slug):
    def __init__(self) -> None:
        """Constructs a ScaredSlug with a default max health of 3 and a PoisonDart weapon."""
        super().__init__(3)
        self.equip(PoisonDart())
        self._symbol = SCARED_SLUG_SYMBOL
        self._name = "ScaredSlug"
    
    def choose_move(self, candidates: list['Position'], current_position: 'Position', player_position: 'Position') -> 'Position':
        """Moves away from the player, choosing the furthest position."""
        furthest_position = max(candidates + [current_position], key=lambda pos: (self.distance(pos, player_position), pos))
        return furthest_position
    
    def can_move(self) -> bool:
        """Returns True if the slug can move this turn, otherwise False."""
        return self._can_move_flag
    
    def distance(self, pos1, pos2):
    # Correct version to compute the Euclidean distance
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    
    def is_poisoned(self) -> bool:
        """Returns True if the slug is poisoned (i.e., poison value > 0)."""
        return self._poison > 0

    def is_stunned(self) -> bool:
        """Returns True if the slug is stunned (i.e., cannot move due to stun effect)."""
        return self._stunned
    
    def __str__(self) -> str:
        return "ScaredSlug"
    
    def __repr__(self) -> str:
        return "ScaredSlug()"
    
class SlugDungeonModel():
    def __init__(self, tiles: list[list[Tile]], slugs: dict[Position, Slug], player: Player, player_position: Position) -> None:
        self._tiles = tiles
        self._slugs = slugs
        self._player = player
        self._player_position = player_position
        self._previous_player_position = player_position

    def get_tiles(self) -> list[list[Tile]]:
        """Returns the tiles for this game in the same format provided to __init__."""
        return self._tiles

    def get_slugs(self) -> dict[Position, Slug]:
        """Returns a dictionary mapping slug positions to the Slug instances at those positions."""
        return self._slugs

    def get_player(self) -> Player:
        """Returns the player instance."""
        return self._player

    def get_player_position(self) -> Position:
        """Returns the player's current position."""
        return self._player_position

    def get_tile(self, position: Position) -> Tile:
        """Returns the tile at the given position."""
        x, y = position
        return self._tiles[x][y]

    def get_dimensions(self) -> tuple[int, int]:
        """Returns the dimensions of the board as (#rows, #columns)."""
        return len(self._tiles), len(self._tiles[0])

    def get_valid_slug_positions(self, slug: Slug) -> list[Position]:
        """Returns valid positions that the slug can move to from its current position."""
        # Find the current position of the slug
        current_position = next((pos for pos, s in self._slugs.items() if s == slug), None)
        
        # If no valid position is found or the slug cannot move, return only the current position
        if not current_position or not slug.can_move():
            return [current_position]
        
        valid_positions = []
        x, y = current_position
        
        # Possible moves (up, down, left, right)
        possible_moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

        for move in possible_moves:
            # Check if the move is within the bounds of the board
            if (0 <= move[0] < len(self._tiles) and
                0 <= move[1] < len(self._tiles[0]) and
                not self.get_tile(move).is_blocking_tile() and
                move not in self._slugs and  # No other slug is at the new position
                move != self._player_position):  # No player is at the new position
                valid_positions.append(move)

        # If no valid move is available, the slug stays in place
        return valid_positions if valid_positions else [current_position]


    def perform_attack(self, entity: Entity, position: Position) -> None:
        """Performs an attack from the given position based on the entity's weapon."""
        if not entity.get_weapon():
            return
        
        targets = entity.get_weapon_targets(position)
        if isinstance(entity, Player):
            for target in targets:
                slug = self._slugs.get(target)
                if slug:
                    slug.apply_effects(entity.get_weapon_effect())
        else:
            if self._player_position in targets:
                self._player.apply_effects(entity.get_weapon_effect())

    def end_turn(self) -> None:
        """Handles end-of-turn activities for the player and slugs."""
        # Apply poison to player
        self._player.apply_poison()
        
        # Apply poison and remove dead slugs
        dead_slugs = []
        for pos, slug in self._slugs.items():
            slug.apply_poison()
            if not slug.is_alive():
                dead_slugs.append(pos)
                self.get_tile(pos).set_weapon(slug.get_weapon())
        
        for pos in dead_slugs:
            del self._slugs[pos]

        # Move remaining slugs
        for slug_position, slug in self._slugs.items():
            # Update slug movement abilities based on their status or effects
            if slug.is_poisoned() or slug.is_stunned():  # Check for poison or stun
                slug.set_can_move_flag(False)  # Disable movement for poisoned or stunned slugs
            else:
                slug.set_can_move_flag(True)

            # Perform slug attacks if they can move
            if slug._can_move_flag:
                self.perform_attack(slug, slug_position)

            slug.end_turn()

        # Update player's previous position
        self._previous_player_position = self._player_position

    def handle_player_move(self, position_delta: Position) -> None:
        """Handles the player's movement and associated actions."""
        new_position = (self._player_position[0] + position_delta[0],
                        self._player_position[1] + position_delta[1])
        
        # Check if the move is valid
        if (0 <= new_position[0] < len(self._tiles) and
            0 <= new_position[1] < len(self._tiles[0]) and
            not self.get_tile(new_position).is_blocking_tile() and
            new_position not in self._slugs):
            
            # Update player position
            self._player_position = new_position

            # Check for weapon pickup
            tile = self.get_tile(new_position)
            if tile.get_weapon():
                self._player.equip(tile.get_weapon())
                tile.remove_weapon()

            # Player attacks
            self.perform_attack(self._player, self._player_position)

            # End the turn
            self.end_turn()
            
    def has_lost(self) -> bool:
        """Returns True if the player has lost the game."""
        return not self._player.is_alive()

    def has_won(self) -> bool:
        """Returns True if the player has won the game."""
        goal_reached = self.get_tile(self._player_position).__str__() == "G"
        return goal_reached and len(self._slugs) == 0
    
def load_level(filename: str) -> SlugDungeonModel:

    # Extract the player's max_health from the first line
    max_health = int(lines[0].strip())
    
    # Initialize the tiles, slugs, and player variables
    tiles = []
    slugs = {}
    player = None
    player_position = None

    # Process the grid lines (starting from the second line)
    for row_idx, line in enumerate(lines[1:], start=0):
        line = line.strip()  # Remove extra whitespace
        tile_row = []  # Create a new row for tiles
        
        for col_idx, char in enumerate(line):
            position = (row_idx, col_idx)
            
            # Create Tile objects based on character ('#' for blocking, ' ' for empty)
            if char == '#':
                tile_row.append(Tile(blocking=True))  # Assuming Tile class has a blocking attribute
            else:
                tile_row.append(Tile(blocking=False))

            # If the character is a slug (non-wall entity), add it to the slugs dictionary
            if char == 'P':
                # Create the player at the corresponding position
                player = Player(max_health=max_health)  # Assuming Player class takes max_health as parameter
                player_position = position
            elif char not in '# ':
                # Create a slug and add it to the dictionary
                slug = Slug()  # Assuming Slug class exists
                slugs[position] = slug
        
        tiles.append(tile_row)

    # Return an instance of SlugDungeonModel with the parsed data
    return SlugDungeonModel(tiles=tiles, slugs=slugs, player=player, player_position=player_position)

class DungeonMap(AbstractGrid):
    def __init__(self, master, dimensions, size):
        super().__init__(master, dimensions, size)
        self.tiles = []
    
    def redraw(self, tiles: list[list[str]], player_position: Position, slugs: dict[Position, str]) -> None:
        # Clear the previous map
        self.clear()

        # Redraw the dungeon tiles and entities
        for row_idx, row in enumerate(tiles):
            for col_idx, tile in enumerate(row):
                position = (row_idx, col_idx)
                self.draw_tile(position, tile)
        
        # Draw the player
        self.draw_entity(player_position, PLAYER_SYMBOL, PLAYER_COLOUR)

        # Draw the slugs
        for slug_position, slug_type in slugs.items():
            self.draw_entity(slug_position, SLUG_SYMBOL, SLUG_COLOUR)

    def draw_tile(self, position: Position, tile_type: str):
        x_min, y_min, x_max, y_max = self.get_bbox(position)
        color = self.get_tile_color(tile_type)
        self.create_rectangle(x_min, y_min, x_max, y_max, fill=color)

    def draw_entity(self, position: Position, symbol: str, color: str):
        x_min, y_min, x_max, y_max = self.get_bbox(position)
        self.create_oval(x_min, y_min, x_max, y_max, fill=color)
        self.annotate_position(position, symbol)
    
    def get_tile_color(self, tile_type: str) -> str:
        if tile_type == "#":
            return "gray"  # Wall tile
        elif tile_type == " ":
            return "white"  # Floor tile
        elif tile_type == "G":
            return "yellow"  # Goal tile
        return "black"  # Default tile color


class DungeonInfo(AbstractGrid):
    def __init__(self, master, dimensions, size):
        super().__init__(master, dimensions, size)
    
    def redraw(self, entities: dict[Position, 'Entity']) -> None:
        self.clear()
        headers = ["Name", "Position", "Weapon", "Health", "Poison"]
        for col_idx, header in enumerate(headers):
            self.annotate_position((0, col_idx), header, font=("Arial", 12, "bold"))

        for row_idx, (position, entity) in enumerate(entities.items(), start=1):
            self.annotate_position((row_idx, 0), entity.name)
            self.annotate_position((row_idx, 1), str(position))
            self.annotate_position((row_idx, 2), entity.weapon.symbol if entity.weapon else "")
            self.annotate_position((row_idx, 3), str(entity.health))
            self.annotate_position((row_idx, 4), str(entity.poison))


class ButtonPanel(tk.Frame):
    def __init__(self, root: tk.Tk, on_load: callable, on_quit: callable):
        super().__init__(root)
        self.pack(side="bottom", fill="x", padx=10, pady=10)
        
        self.load_button = tk.Button(self, text="Load Game", command=on_load)
        self.load_button.pack(side="left", padx=5)
        
        self.quit_button = tk.Button(self, text="Quit", command=on_quit)
        self.quit_button.pack(side="right", padx=5)




if __name__ == "__main__":
    main()
    root = tk.Tk()
    root.title("Dungeon Game")

    # Instantiate DungeonMap, DungeonInfo, and ButtonPanel
    dungeon_map = DungeonMap(root, dimensions=(5, 5), size=(500, 500))
    dungeon_map.pack(side="left", padx=10, pady=10)
    dungeon_map.redraw(sample_tiles, player_pos, slugs)

    dungeon_info = DungeonInfo(root, dimensions=(6, 5), size=(400, 200))
    dungeon_info.pack(side="right", padx=10, pady=10)
    # Example entities can be added to the redraw method
    
    button_panel = ButtonPanel(root, on_load=lambda: print("Load game"), on_quit=root.quit)
    root.mainloop()
