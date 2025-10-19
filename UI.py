from texttable import Texttable
from exceptions import NotInteger,NotWithinBounds,SameShot,InvalidDirection,GameOver,InvalidColumn,OverlappingShip,InvalidCoordinates,ShipSunken
from board import (ShipDirection)
from game import Battleships

class UI:
    def __init__(self):
        self.__game=Battleships()

    def __place_a_ship(self, availableShips, i):
        column = input("The column(A-J):").upper()
        if column == "" or len(column)>1:
            raise InvalidColumn("This column doesn't exist!")
        column_number = ord(column) - ord('A')
        if column_number < 0 or column_number > 9:
            raise NotWithinBounds("The column is not within the right bounds!(A-J)")
        try:
            row = int(input("The row(1-10):"))
            if row<1 or row>10:
                raise NotWithinBounds("The row is not within the right bounds!(1-10)")
        except ValueError:
            raise NotInteger
        direction = input("The direction(LEFT,RIGHT,UP,DOWN):").upper()
        if direction == "DOWN":
            if row+availableShips[i]["size"]>11:
                raise InvalidDirection
            try:
                self.__game.player_board.place_ship(row - 1, column_number, ShipDirection.DOWN, availableShips[i]["size"])
            except OverlappingShip:
                raise OverlappingShip
        elif direction == "UP":
            if row-availableShips[i]["size"]<0:
                raise InvalidDirection
            try:
                self.__game.player_board.place_ship(row - 1, column_number, ShipDirection.UP, availableShips[i]["size"])
            except OverlappingShip:
                raise OverlappingShip
        elif direction == "RIGHT":
            if column_number+availableShips[i]["size"]>10:
                raise InvalidDirection
            try:
                self.__game.player_board.place_ship(row - 1, column_number, ShipDirection.RIGHT, availableShips[i]["size"])
            except OverlappingShip:
                raise OverlappingShip
        elif direction == "LEFT":
            if column_number-availableShips[i]["size"]<-1:
                raise InvalidDirection
            try:
                self.__game.player_board.place_ship(row - 1, column_number, ShipDirection.LEFT, availableShips[i]["size"])
            except OverlappingShip:
                raise OverlappingShip
        else:
            raise InvalidDirection("This direction doesn't exist!")

    def __place_player_ships(self):
        print(self.__game.player_board)
        table=Texttable()
        availableShips=[
            {"name":"Carrier","size":5},
            {"name":"Battleship","size":4},
            {"name":"Cruiser","size":3},
            {"name":"Submarine","size":3},
            {"name":"Destroyer","size":2}
        ]
        header=["No.","Class of ship","Size"]
        table.add_row(header)
        count=1
        for ship in availableShips:
            table.add_row([count,ship["name"],ship["size"]])
            count+=1
        print(table.draw())
        i=0
        while i<5:
            print(f"Place the {availableShips[i]["name"]}")
            try:
                self.__place_a_ship(availableShips,i)
            except (NotInteger,NotWithinBounds,InvalidDirection,OverlappingShip,InvalidColumn) as ve:
                print(ve,"\n")
                continue
            print(self.__game.player_board)
            i+=1


    def start(self):
        pshot=0
        cshot=0
        self.__place_player_ships()
        legend=Texttable()
        header=["Symbol","Description"]
        legend.add_row(header)
        legend.add_row([".","You hit the water"])
        legend.add_row(["X","You hit an enemy ship"])
        print(legend.draw())
        print("My board")
        print(self.__game.player_board)
        print("Targeting board")
        print(self.__game.computer_board)
        while True:
            ok=0
            try:
                fire_coordinates=input("fire>").strip()
                if len(fire_coordinates)<2 or len(fire_coordinates)>3:
                    raise InvalidCoordinates
                if fire_coordinates[0].upper()<'A' or fire_coordinates[0].upper()>'J':
                    raise NotWithinBounds("The column is not within the bounds!(A-J)")
                column=ord(fire_coordinates[0].upper())-ord('A')
                try:
                    row_str=fire_coordinates[1:]
                    row=int(row_str)-1
                    if row<0 or row>9:
                        raise NotWithinBounds("The row is not within the bounds!(1-10)")
                except ValueError:
                    raise NotInteger("The row has to be an integer!")
                pshot += 1
                self.__game.fire_human_player(row,column)
                if self.__game.check_game_over():
                    raise GameOver("You won!")
                cshot += 1
                ok=1
                self.__game.fire_computer_player()
                if self.__game.check_game_over():
                    raise GameOver("The computer won!")
                print("My board")
                print(self.__game.player_board)
                print("Targeting board")
                print(self.__game.computer_board)
            except (NotInteger,NotWithinBounds,InvalidCoordinates,SameShot) as ve:
                print(ve)
                continue
            except ShipSunken as ve:
                cop=ve
                if cshot+1==pshot:
                    cshot+=1
                    try:
                        self.__game.fire_computer_player()
                    except ShipSunken as ve:
                        print("My board")
                        print(self.__game.player_board)
                        print("Targeting board")
                        print(self.__game.computer_board)
                        print("ENEMY SHIP:")
                        print(cop)
                        print("YOUR SHIP:")
                        print(ve)
                        continue
                print("My board")
                print(self.__game.player_board)
                print("Targeting board")
                print(self.__game.computer_board)
                if ok == 0:
                    print("ENEMY SHIP: ")
                else: print("YOUR SHIP:")
                print(ve)
                if self.__game.computer_board.all_ships_sunk():
                    print("You won!")
                    break
                elif self.__game.player_board.all_ships_sunk():
                    print("The computer won!")
                    break
            except GameOver as ve:
                print(ve)
                break


ui=UI()
ui.start()