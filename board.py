from enum import Enum
from exceptions import OverlappingShip,InvalidDirection,ShipSunken,SameShot
from texttable import Texttable

"""
0-empty
1,2,3.... ship
1 1 1- ship
2 2 2- ship
100-hit empty
If we hit a ship, we take a ship's number and we minus it

"""

class ShipDirection(Enum):
    UP=0
    DOWN=1
    LEFT=2
    RIGHT=3

class BattleshipsBoard:

    #Tye rules are not tied to any single board, so they don't need the self parameter
    #this is a general placement rule
    __placement_rules={ShipDirection.UP:(-1,0), ShipDirection.DOWN:(1,0), ShipDirection.LEFT:(0,-1)
        , ShipDirection.RIGHT:(0,1)}

    __ship_length=3

    def __init__(self):
        self._data=[]
        for i in range(10):
            self._data.append([0]*10)
        self._current_ship=1 #we represent the next added ship using 1's
        self._ship_parts=[5,4,3,3,2]

    def place_ship(self, row:int, column:int, direction:ShipDirection, length=__ship_length):
        """
        A function that places A SHIP on the board
        :param row: the row of board
        :param column:  the column of board
        :param direction: the direction of the ship
        :param length: the length of the ship
        :return: none
        """
        move_x=BattleshipsBoard.__placement_rules[direction][0]
        move_y=BattleshipsBoard.__placement_rules[direction][1]
        current_x,current_y=row,column
        for cell in range(length):
            if current_x<0 or current_x>9 or current_y<0 or current_y>9:
                raise InvalidDirection
            if self._data[current_x][current_y]!=0:
                raise OverlappingShip
            current_x+=move_x
            current_y+=move_y
        #if self._data[row][column]!=0:
        #    raise OverlappingShip
        #if column-length<-1 and direction==ShipDirection.LEFT:
        #    raise InvalidDirection
        #if column+length>10 and direction==ShipDirection.RIGHT:
        #    raise InvalidDirection
        #if row+length>10 and direction==ShipDirection.DOWN:
        #    raise InvalidDirection
        #if row-length<0 and direction==ShipDirection.UP:
        #    raise InvalidDirection
        self._data[row][column]=self._current_ship
        current_x=row
        current_y=column
        for cell in range(1,length):
            #if self._data[current_x+move_x][current_y+move_y]!=0:
            #    raise OverlappingShip
            self._data[current_x+move_x][current_y+move_y]=self._current_ship
            current_x+=move_x
            current_y+=move_y

        self._current_ship+=1

    def get_cell(self, row, col):
        return self._data[row][col]

    def fire(self, row:int, column:int):
        """
        A function that makes a ship fire on the enemy board
        :param row: the row where the shot takes place
        :param column: the column where the shot takes place
        :return: the element that takes the fire
        """
        if self._data[row][column]==0:
            self._data[row][column]=100
        elif self._data[row][column]>0 and self._data[row][column]!=100:
            ship_id=self._data[row][column]
            self._data[row][column]=-1*self._data[row][column]
            #print(ship_id-1)
            self._ship_parts[ship_id-1]-=1
            if self._ship_parts[ship_id-1]==0:
                raise ShipSunken(f"The ship {ship_id} sank!")
        elif self._data[row][column]==100 or self._data[row][column]<0:
            raise SameShot
        return self._data[row][column]

    def all_ships_sunk(self):
        """
        A function that checks if all ships sank
        :return: True/False
        """
        for ship_parts_count in self._ship_parts:
            if ship_parts_count!=0:
                return False
        return True

    def check_equal(self, row1, col1, row2, col2):
        if abs(self._data[row1][col1])==abs(self._data[row2][col2]):
            return True
        return False

    def __str__(self):
        t=Texttable()
        t.header(['/','A','B','C','D','E','F','G','H','I','J']) #easier with ord(), chr()
        #for ascii_code in range(ord('A'), ord('G')):
        #    print(chr(ascii_code))
        for row in range(10):
            row_data=[row+1]+[' ']*10 #initialize an empty row
            for column in range(10):
                symbol=' '
                if self._data[row][column]==100:
                    symbol='.'
                elif self._data[row][column]>0:
                    symbol=self._data[row][column]
                elif self._data[row][column]<0:
                    symbol='X'
                row_data[column+1]=symbol
                #row_data[column+1]=' ' if self.__data[row][column]==0 else self.__data[row][column]
            t.add_row(row_data)
        return t.draw()

class PlayerBoard(BattleshipsBoard):
    def __init__(self):
        super().__init__()
        self._positions=[]

    def find_next_ship(self, value=1000):
        """
        A function that finds the next ,,alive'' ship on the table
        :param value: A value based on which an additional check happens(so the same function is used in 2 places)
        :return: the row and column
        """
        if value==1000:
            for row in range(10):
                for column in range(10):
                    if self._data[row][column]>0 and self._data[row][column]!=100:
                        return row,column
        else:
            for row in range(10):
                for column in range(10):
                    if self._data[row][column]==abs(value):
                        return row,column
        return None,None

    def available_shot(self, row, column):
        """
        A function that checks if a shot can take place or not
        :param row: the row of the cell
        :param column: the column of the cell
        :return: True/False
        """
        if self._data[row][column]<0 or self._data[row][column]==100:
            return False
        return True

    def __str__(self):
        t=Texttable()
        t.header(['/','A','B','C','D','E','F','G','H','I','J']) #easier with ord(), chr()
        #for ascii_code in range(ord('A'), ord('G')):
        #    print(chr(ascii_code))
        for row in range(10):
            row_data=[row+1]+[' ']*10 #initialize an empty row
            for column in range(10):
                symbol=' '
                if self._data[row][column]==100:
                    symbol='.'
                elif self._data[row][column]>0:
                    symbol=self._data[row][column]
                elif self._data[row][column]<0:
                    symbol='X'
                row_data[column+1]=symbol
            t.add_row(row_data)
        return t.draw()

class ComputerBoard(BattleshipsBoard):
    def __init__(self):
        super().__init__()

    def __str__(self):
        t=Texttable()
        t.header(['/','A','B','C','D','E','F','G','H','I','J']) #easier with ord(), chr()
        #for ascii_code in range(ord('A'), ord('G')):
        #    print(chr(ascii_code))
        for row in range(10):
            row_data=[row+1]+[' ']*10 #initialize an empty row
            for column in range(10):
                symbol=' '
                if self._data[row][column]==100:
                    symbol='.'
                elif self._data[row][column]>0:
                    symbol=self._data[row][column]
                elif self._data[row][column]<0:
                    symbol='X'
                row_data[column+1]=symbol
            t.add_row(row_data)
        return t.draw()


if __name__=="__main__":
    """
    bb=ComputerBoard()
    print(bb)
    bb.place_ship(1,1,ShipDirection.DOWN)
    bb.place_ship(1,2,ShipDirection.RIGHT)
    bb.place_ship(5,5,ShipDirection.UP)
    bb.fire(1,2)
    bb.fire(3,4)    
    print(bb)
    """