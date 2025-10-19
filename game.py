from random import randint,choice
from exceptions import OverlappingShip,InvalidDirection
from board import PlayerBoard,ComputerBoard,ShipDirection


#The idea is to put the alogirthm in their own class
#We instatiante the class that corresponds to the alogirthm we want
#ex: easy diff-> random moves from computer
#hard diff-> once a hit recorded, the computer bombs the area to the oblivion

class ComputerStrategy:
    def __init__(self, computer_board:ComputerBoard, player_board:PlayerBoard):
        self.__computer_board=computer_board
        self.__player_board=player_board
        self.__nr_shots=0
        self.place_ships()
        self.__hit_cells=[]
        self.__targeting=[]
        self.__mode_activated=False
        self.__once=False
        self.__remaining_position=0

    def place_ships(self):
        """
        Computer's strategy for placing ships on its own board
        return: none
        """
        directions=[ShipDirection.RIGHT,ShipDirection.LEFT,ShipDirection.UP,ShipDirection.DOWN]
        sizes=[5,4,3,3,2]
        i=0
        while i<5:
            row = randint(0, 9)
            column = randint(0, 9)
            direction=choice(directions)
            try:
                self.__computer_board.place_ship(row,column,direction,sizes[i])
            except (OverlappingShip,InvalidDirection):
                continue
            i+=1

    def _random_mode(self):
        """
        Firing in random mode
        :return: the row and column of the available cell where the fire will take place
        """
        row = randint(0, 9)
        column = randint(0, 9)
        while not self.__player_board.available_shot(row, column):
            row = randint(0, 9)
            column = randint(0, 9)
        return row,column

    def _around_cells(self, row, column):
        """
        A function that gets all the cells around a cell that contains a part of a ship
        :param row: the row of that cell
        :param column: the column of that cell
        :return: none
        """
        directions=[(-1,0),(0,1),(1,0),(0,-1)]
        for direction in directions:
            new_row=row+direction[0]
            new_column=column+direction[1]
            if 0 <= new_row <= 9 and 0 <= new_column <= 9 and self.__player_board.available_shot(new_row,new_column):
                self.__targeting.append((new_row,new_column))

    def _process_targeting(self):
        """
        A function that checks around the cell that was fired upon and contained a part of a ship
        :return: the row and column of the next fire
        """
        target=self.__targeting.pop(0)
        row1=target[0]
        col1=target[1]
        row2,col2=self.__hit_cells[0]
        #print((row1,col1),(row2,col2))
        #print(row1,col1,row2,col2)
        if self.__player_board.check_equal(row1,col1,row2,col2):
            self.__hit_cells[0]=(row1,col1)
            self.__mode_activated=True
        elif self.__player_board.get_cell(row1,col1)>0:
            self.__hit_cells.append((row1,col1))
        return row1,col1

    def _sure_mode(self):
        """
        A function that will fire upon a ship, knowing exactly its location
        :return: the row and column where the next fire will take place
        """
        the_row,the_col=self.__hit_cells[0]
        the_value=self.__player_board.get_cell(the_row,the_col)
        new_row,new_col=self.__player_board.find_next_ship(the_value)
        self.__hit_cells[0]=(new_row,new_col)
        """
        if self.__player_board.check_equal(the_row,the_col,the_row+1,the_col):
            self.__hit_cells[0]=(the_row+1,the_col)
            return the_row+1,the_col
        if self.__player_board.check_equal(the_row,the_col,the_row-1,the_col):
            self.__hit_cells[0]=(the_row-1,the_col)
            return the_row-1,the_col
        if self.__player_board.check_equal(the_row,the_col,the_row,the_col+1):
            self.__hit_cells[0]=(the_row,the_col+1)
            return the_row,the_col+1
        if self.__player_board.check_equal(the_row,the_col,the_row,the_col-1):
            self.__hit_cells[0]=(the_row,the_col-1)
            return the_row,the_col-1
        """
        return new_row, new_col


    def fire(self):
        """
        Computer's strategy to fire, combining all the strategies together
        :return none
        """
        if self.__hit_cells:
            if not self.__mode_activated:
                row,column=self._process_targeting()
            else: row,column=self._sure_mode()
            if row==None:
                self.__hit_cells.clear()
                self.__targeting.clear()
                #if self.__hit_cells:
                #    r,c=self.__hit_cells[0]
                #    self.__around_cells(r,c)
                row,column=self._random_mode()
                self.__mode_activated=False
                self.__nr_shots=1
        else:
            if self.__nr_shots == 4:
                row, column = self.__player_board.find_next_ship()
                self.__nr_shots = 0
            else:
                self.__nr_shots += 1
                row,column=self._random_mode()
        hit_result=self.__player_board.fire(row,column)
        #print(self.__mode_activated)
        if hit_result<0 and not self.__targeting: #hit a ship
            self.__hit_cells.append((row,column))
            self._around_cells(row,column)

    def get_targeting(self):
        return list(self.__targeting)

    @property
    def hit_cells(self):
        return list(self.__hit_cells)

    @hit_cells.setter
    def hit_cells(self, value:tuple):
        self.__hit_cells.append(value)

class Battleships:
    def __init__(self):
        self.__player_board=PlayerBoard()
        self.__computer_board=ComputerBoard()
        self.__strategy=ComputerStrategy(self.__computer_board,self.__player_board)

    @property
    def computer_board(self):
        return self.__computer_board

    @property
    def player_board(self):
        return self.__player_board

    def fire_human_player(self, row:int, column:int):
        self.__computer_board.fire(row,column)

    def fire_computer_player(self):
        #NOTE this method does not need to know about the computer's actual strategy
        self.__strategy.fire()

    def check_game_over(self):
        """
        A function that checks if the game is over or not
        :return: True/False
        """
        print(self.__player_board)
        if self.__player_board.all_ships_sunk()==True or self.__computer_board.all_ships_sunk()==True:
            return True
        return False

if __name__=="__main__":
    playerB=PlayerBoard()
    compB=ComputerBoard()
    compStr=ComputerStrategy(compB,playerB)
    print(compB)