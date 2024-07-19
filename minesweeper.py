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
    def __init__(self, cells, count, mc):
        self.cells = set(cells)
        self.count = count
        self.mc = mc

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __str__(self):
        return f"\033[90m {self.mc} ---> \033[0m {self.cells} = {self.count}"
    
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
        if self.count <= 0:
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
        
        self.knowledge.append(Sentence(cells, count, cell))
       
        def update_knowledge():
            
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
        print("Checking when does it do extra move!")
        update_knowledge()
        # TODO: Ok so it looks like not all the sentences are giving the correct result, I think at some point some of them get removed without any safes/mines being added
        # TODO: It looks like the sentence with zero still stays, after the run, then it will be removed on next run, but on first run it will be marked as safe/mine

        # Might be only the ones that are in the corner
        print(" ")
        print("____________________________")
        print("New run and these are all the sentences")
        for s in self.knowledge:
            print(s)
        print("Mines: ")
        print(self.mines)
        print("Safes: ")
        print(self.safes)
        # Will run till no new connection found
        finished = False
        # Ok so as of now it will not recuringly add new sentences, this is the plan to keep on adding new inferences till there is no more
        while not finished:
            for sentence in self.knowledge:
                    finished = True
                    for other_sentence in self.knowledge:
                        if sentence.cells != set() and other_sentence.cells != set():
                            if sentence != other_sentence and sentence.cells.issubset(other_sentence.cells):
                                # Currently that is adding same sentece and infinite loop
                                new_cells= sentence.cells - other_sentence.cells
                                all_cells = [item.cells for item in self.knowledge  ]
                               
                                if new_cells not in all_cells:
                                    finished = False
                                    print("New Sentence Inferred")
                                    print(f"\033[94m {sentence.mc} ---> \033[0m",sentence.cells , "--->" , sentence.count)
                                    count = sentence.count - other_sentence.count
                                    new_sentence = Sentence(new_cells, count, sentence.mc)
                                    self.knowledge.append(new_sentence)
                                    update_knowledge()
         
    

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
        if len(not_mine) > 0:
            choice = random.choice(list(not_mine))
            if choice:
                return choice
        else:
            return None
