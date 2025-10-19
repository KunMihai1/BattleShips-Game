import unittest

from exceptions import OverlappingShip,ShipSunken
from board import PlayerBoard,ComputerBoard,ShipDirection,SameShot
from game import ComputerStrategy

class Tests(unittest.TestCase):
    def setUp(self):
        self.__playerBoard=PlayerBoard()
        self.__computerBoard=ComputerBoard()
        self.__computerStrategy=ComputerStrategy(self.__computerBoard,self.__playerBoard)

    def test_place_ship(self):
        self.__playerBoard.place_ship(1,1,ShipDirection.RIGHT,5)
        self.assertEqual(self.__playerBoard.get_cell(1,1),1)
        self.assertEqual(self.__playerBoard.get_cell(1,2),1)
        self.assertEqual(self.__playerBoard.get_cell(1, 3), 1)
        self.assertEqual(self.__playerBoard.get_cell(1, 4), 1)
        self.assertEqual(self.__playerBoard.get_cell(1, 5), 1)
        self.__playerBoard.place_ship(5,6,ShipDirection.UP,2)
        self.assertEqual(self.__playerBoard.get_cell(5,6),2)
        self.assertEqual(self.__playerBoard.get_cell(4,6),2)
        with self.assertRaises(OverlappingShip):
            self.__playerBoard.place_ship(3,2,ShipDirection.UP,3)

    def test_fire(self):
        self.__playerBoard.place_ship(2, 2, ShipDirection.RIGHT, 5)
        result = self.__playerBoard.fire(1, 1)
        self.assertEqual(result, 100)
        with self.assertRaises(SameShot):
            self.__playerBoard.fire(1,1)
        result = self.__playerBoard.fire(2, 2)
        self.assertEqual(result, -1)
        self.__playerBoard.fire(2, 3)
        self.__playerBoard.fire(2,4)
        self.__playerBoard.fire(2,5)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(2, 6)

    def test_all_ships_sunk(self):
        self.__playerBoard.place_ship(1, 1, ShipDirection.RIGHT, 5)
        self.__playerBoard.place_ship(6, 3, ShipDirection.UP, 4)
        self.__playerBoard.place_ship(9,8,ShipDirection.UP,3)
        self.__playerBoard.place_ship(7,4,ShipDirection.RIGHT,3)
        self.__playerBoard.place_ship(2,9,ShipDirection.DOWN,2)
        self.__playerBoard.fire(1,1)
        self.__playerBoard.fire(1, 2)
        self.__playerBoard.fire(1, 3)
        self.__playerBoard.fire(1, 4)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(1, 5)

        self.__playerBoard.fire(6, 3)
        self.__playerBoard.fire(5, 3)
        self.__playerBoard.fire(4, 3)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(3, 3)

        self.__playerBoard.fire(9,8)
        self.__playerBoard.fire(8,8)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(7,8)

        self.__playerBoard.fire(7,4)
        self.__playerBoard.fire(7,5)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(7,6)

        self.__playerBoard.fire(2,9)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(3,9)

        self.assertTrue(self.__playerBoard.all_ships_sunk())

    def test_find_next_ship(self):
        self.__playerBoard.place_ship(3,3,ShipDirection.RIGHT,5)
        self.__playerBoard.fire(3,3)
        row,column=self.__playerBoard.find_next_ship()
        self.assertEqual(row,3)
        self.assertEqual(column,4)

    def test_available_shot(self):
        self.assertTrue(self.__playerBoard.available_shot(0,0))
        self.__playerBoard.fire(0, 0)
        self.assertFalse(self.__playerBoard.available_shot(0, 0))

    def test_computer_strategy_place_ships(self):
        ship_sizes=[5,4,3,3,2]
        found_ship_sizes=[0,0,0,0,0]
        for row in range(10):
            for col in range(10):
                cell_value=self.__computerBoard.get_cell(row,col)
                if cell_value>0:
                    found_ship_sizes[cell_value-1]+=1
        for i in range(5):
            self.assertEqual(found_ship_sizes[i],ship_sizes[i])

    def test_computer_strategy_random_mode(self):
        self.__playerBoard.fire(0, 0)
        self.__playerBoard.fire(1, 1)
        self.__playerBoard.fire(2, 2)
        for i in range(100):
            row, column = self.__computerStrategy._random_mode()
            self.assertGreaterEqual(row, 0, "Row is out of bounds")
            self.assertLessEqual(row, 9, "Row is out of bounds")
            self.assertGreaterEqual(column, 0, "Column is out of bounds")
            self.assertLessEqual(column, 9, "Column is out of bounds")
            self.assertTrue(self.__playerBoard.available_shot(row,column))

    def test_computer_strategy_process_targeting(self):
        self.__playerBoard.place_ship(5, 5, ShipDirection.RIGHT, 3)
        self.__playerBoard.fire(5,3)
        self.__playerBoard.fire(5,5)
        self.__computerStrategy._around_cells(5,5)
        self.__computerStrategy.hit_cells=(5,5)
        row, col = self.__computerStrategy._process_targeting()
        self.__playerBoard.fire(4,5)
        self.assertEqual(row,4)
        self.assertEqual(col,5)
        row1,col1=self.__computerStrategy._process_targeting()
        self.__playerBoard.fire(5,6)
        self.assertEqual(row1,5)
        self.assertEqual(col1,6)

    def test_computer_strategy_sure_mode(self):
        self.__playerBoard.place_ship(5, 5, ShipDirection.RIGHT, 3)
        self.__playerBoard.fire(5, 3)
        self.__playerBoard.fire(5, 5)
        self.__computerStrategy._around_cells(5, 5)
        self.__computerStrategy.hit_cells = (5, 5)
        row, col = self.__computerStrategy._process_targeting()
        self.__playerBoard.fire(4,5)
        self.assertEqual(row, 4)
        self.assertEqual(col, 5)

        row, col = self.__computerStrategy._process_targeting()
        self.__playerBoard.fire(5,6)
        self.assertEqual(row, 5)
        self.assertEqual(col, 6)

        row1,col1=self.__computerStrategy._sure_mode()
        self.assertEqual(row1,5)
        self.assertEqual(col1,7)

    def test_computer_strategy_fire(self):
        self.__playerBoard.place_ship(3, 3, ShipDirection.DOWN, 5)
        self.__playerBoard.place_ship(9, 0, ShipDirection.RIGHT, 4)
        self.assertFalse(self.__playerBoard.all_ships_sunk())
        self.__computerStrategy.fire()
        self.__computerStrategy.fire()
        self.__computerStrategy.fire()
        self.__computerStrategy.fire()
        self.__computerStrategy.fire()
        c=0
        for row in range(10):
            for col in range(10):
                if self.__playerBoard.get_cell(row,col)<0:
                    c+=1
        self.assertGreaterEqual(c,1)

    def test_check_game_over(self):
        self.__playerBoard.place_ship(3,3,ShipDirection.DOWN,5)
        self.__playerBoard.place_ship(9,0,ShipDirection.RIGHT,4)
        self.__playerBoard.place_ship(8,0,ShipDirection.RIGHT,3)
        self.__playerBoard.place_ship(2,0,ShipDirection.RIGHT,3)
        self.__playerBoard.place_ship(1,0,ShipDirection.RIGHT,2)
        self.__playerBoard.fire(3,3)
        self.__playerBoard.fire(4,3)
        self.__playerBoard.fire(5,3)
        self.__playerBoard.fire(6,3)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(7,3)

        self.__playerBoard.fire(9,0)
        self.__playerBoard.fire(9,1)
        self.__playerBoard.fire(9,2)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(9,3)

        self.__playerBoard.fire(8,0)
        self.__playerBoard.fire(8,1)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(8,2)

        self.__playerBoard.fire(2,0)
        self.__playerBoard.fire(2,1)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(2,2)

        self.__playerBoard.fire(1,0)
        with self.assertRaises(ShipSunken):
            self.__playerBoard.fire(1,1)
        #print(self.__playerBoard)
        self.assertTrue(self.__playerBoard.all_ships_sunk() or self.__computerBoard.all_ships_sunk())

if __name__=="__main__":
    unittest.main()