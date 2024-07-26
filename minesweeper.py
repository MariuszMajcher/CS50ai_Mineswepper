import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = [[False for _ in range(width)] for _ in range(height)]

        # Add mines randomly
        while len(self.mines) != mines:
            i, j = random.randrange(height), random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                print("|X" if self.board[i][j] else "| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width and self.board[i][j]:
                    count += 1
        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count, mc):
        self.cells = set(cells)
        self.count = count
        self.mc = mc

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"\033[92m {self.mc} --> \033[0m{self.cells} = {self.count}"

    def known_mines(self):
        return self.cells if len(self.cells) == self.count else set()

    def known_safes(self):
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:
                    cells.add((i, j))

        new_sentence = Sentence(cells, count, cell)
        self.knowledge.append(new_sentence)

        self.update_knowledge()
        self.infer_knowledge()

    def update_knowledge(self):
        updated = True
        while updated:
            updated = False
            safes = set()
            mines = set()

            for sentence in self.knowledge:
                safes.update(sentence.known_safes())
                mines.update(sentence.known_mines())

            if safes:
                updated = True
                for safe in safes:
                    self.mark_safe(safe)
            if mines:
                updated = True
                for mine in mines:
                    self.mark_mine(mine)

            self.knowledge = [s for s in self.knowledge if s.cells]

    def infer_knowledge(self):
        new_inferences = True
        while new_inferences:
            new_inferences = False
            new_knowledge = []

            for sentence in self.knowledge:
                for other_sentence in self.knowledge:
                    if sentence != other_sentence:
                        if sentence.cells.issubset(other_sentence.cells):
                            new_cells = other_sentence.cells - sentence.cells
                            count_diff = other_sentence.count - sentence.count
                            new_sentence = Sentence(new_cells, count_diff, sentence.mc)
                            if new_sentence not in self.knowledge and new_sentence not in new_knowledge:
                                new_knowledge.append(new_sentence)
                                new_inferences = True

            self.knowledge.extend(new_knowledge)
            self.update_knowledge()

    def make_safe_move(self):
        moves = self.safes - self.moves_made
        return random.choice(list(moves)) if moves else None

    def make_random_move(self):
        all_cells = set(itertools.product(range(self.height), range(self.width)))
        possible_moves = list(all_cells - self.moves_made - self.mines)
        return random.choice(possible_moves) if possible_moves else None


# Example usage
ai = MinesweeperAI()
ai.add_knowledge((0, 0), 1)
ai.add_knowledge((0, 1), 1)

print("Knowledge after adding sentences and inferring:")
for sentence in ai.knowledge:
    print(sentence)