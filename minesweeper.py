import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    # For testing purposes, will add the middle cell, that will help me to undersand the board better
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
       

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()
        
        
    
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #If i remove a cell will it mark it with flag?
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            # Seems like count does not change

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
    

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    cells.add((i,j))
        # How to create a difference of the sentences, 
        # Dont want to create to many, and not repeating 
        print("new iteration")
        self.knowledge.append(Sentence(cells, count))
       
        for se in self.knowledge:

            print(se)
        print("safes")
        print(self.safes)
        print("mines")
        print(self.mines)
        for sentence in self.knowledge:
            safe_moves = sentence.known_safes()
            mines = sentence.known_mines()
            if safe_moves:
                for move in safe_moves:
                    self.safes.add(move)
            if mines:
                for mine in mines:
                    self.mines.add(mine)
       
        for sentence in self.knowledge:
           
            for move in self.safes:
                sentence.mark_safe(move)
            for mine in self.mines:
                sentence.mark_mine(mine)        

        for sentence in self.knowledge:
              if sentence.cells == set():
                    self.knowledge.remove(sentence)  

        
        finished = False
        while not finished:
            finished = True
            for sentence in self.knowledge:

                if sentence.cells != set():
                    for other_sentence in self.knowledge:
                
                        if sentence != other_sentence:
                            if sentence.cells.issubset(other_sentence.cells):
                                print(sentence.cells)
                                new_cells= sentence.cells - other_sentence.cells
                                all_cells = [item.cells for item in self.knowledge  ]
                                if new_cells not in all_cells:
                                    finished = False
                                    count = sentence.count - other_sentence.count
                                    new_sentence = Sentence(new_cells, count)
                                    need_checking = True
                                    while need_checking:
                                        need_checking = False
                                        safe_moves = new_sentence.known_safes()
                                        mines = new_sentence.known_mines()
                                        if safe_moves or mines:
                                            need_checking = True
                                        if safe_moves:
                                            for move in safe_moves:
                                                self.safes.add(move)
                                                new_sentence.mark_safe(move)
                                        if mines:
                                            for mine in mines:
                                                self.mines.add(mine)
                                                new_sentence.mark_mine(mine)
                                        self.knowledge.append(new_sentence)
              
       

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > 0:
            moves = (self.safes - self.moves_made)
            if len(moves) > 0:
                choice = random.choice(list(moves))
                if choice:
                    return choice
                else:
                    return None
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        board = set()
        for i in range(self.width):
            for j in range(self.height):
                board.add((i,j))
        not_mine = (board - self.mines - self.moves_made)
        choice = random.choice(list(not_mine))
        if choice:
            return choice
        else:
            return None
