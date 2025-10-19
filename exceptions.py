class UserValidationError(Exception):
    def __init__(self, message:str):
        super().__init__(message)

class NotInteger(UserValidationError):
    def __init__(self, message="The provided input is not valid! Please enter an integer."):
        super().__init__(message)

class InvalidCoordinates(UserValidationError):
    def __init__(self, message="The coordinates are not right!"):
        super().__init__(message)

class NotWithinBounds(UserValidationError):
    def __init__(self, message="The provided input it not within the right bounds!"):
        super().__init__(message)

class InvalidDirection(UserValidationError):
    def __init__(self, message="This direction will get the ship out of bounds!"):
        super().__init__(message)

class InvalidColumn(UserValidationError):
    def __init__(self, message="This column is not good!"):
        super().__init__(message)

class OverlappingShip(Exception):
    def __init__(self, message="The ship overlaps with another one!"):
        super().__init__(message)

class GameInfo(Exception):
    def __init__(self, message:str):
        super().__init__(message)

class ShipSunken(GameInfo):
    def __init__(self, message="An enemy ship sank!"):
        super().__init__(message)

class GameOver(GameInfo):
    def __init__(self, message="The game is over!"):
        super().__init__(message)

class SameShot(GameInfo):
    def __init__(self, message="You hit a cell that has already been hit!"):
        super().__init__(message)