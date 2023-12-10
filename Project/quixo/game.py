from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
import numpy as np

# Enum class for representing possible moves in the game.
class Move(Enum):
    TOP = 0    # Move to the top
    BOTTOM = 1 # Move to the bottom
    LEFT = 2   # Move to the left
    RIGHT = 3  # Move to the right

# Abstract base class for a player.
class Player(ABC):
    def __init__(self) -> None:
        '''Constructor for the Player class.'''
        pass

    @abstractmethod
    def make_move(self, game: 'Game') -> 'tuple[tuple[int, int], Move]':
        '''
        Abstract method that each player class must implement.
        This method should return a tuple containing a coordinate (x,y) and a Move (TOP, BOTTOM, LEFT, RIGHT).
        '''
        pass

# Class representing the game logic.
class Game(object):
    def __init__(self) -> None:
        '''Constructor for the Game class, initializes the game board as a 5x5 grid with -1 (indicating neutral pieces).'''
        self._board = np.ones((5, 5), dtype=np.uint8) * -1

    def print(self):
        '''Prints the current state of the game board.'''
        print(self._board)

    def check_winner(self) -> int:
        '''Checks for a winner in the current game state.'''
        # Check each row for a winner
        for x in range(self._board.shape[0]):
            if all(self._board[x, :] == self._board[x, 0]):
                return self._board[x, 0]
        # Check each column for a winner
        for y in range(self._board.shape[0]):
            if all(self._board[:, y] == self._board[0, y]):
                return self._board[0, y]
        # Check diagonal from top-left to bottom-right
        if all([self._board[x, x] for x in range(self._board.shape[0])] == self._board[0, 0]):
            return self._board[0, 0]
        # Check diagonal from top-right to bottom-left
        if all([self._board[x, -x] for x in range(self._board.shape[0])] == self._board[-1, -1]):
            return self._board[0, -1]
        return -1  # No winner found

    def play(self, player1: Player, player2: Player) -> int:
        '''Starts and manages the game play between two players.'''
        players = [player1, player2]
        current_player_idx = 1
        winner = -1
        while winner < 0:
            # Alternating turns between the two players
            current_player_idx += 1
            current_player_idx %= len(players)
            ok = False
            while not ok:
                # Get the move from the current player
                from_pos, slide = players[current_player_idx].make_move(self)
                # Attempt to execute the move
                ok = self.__move(from_pos, slide, current_player_idx)
            # Check for a winner after the move
            winner = self.check_winner()
        return winner  # Return the ID of the winning player

    def __move(self, from_pos: 'tuple[int, int]', slide: Move, player_id: int) -> bool:
        '''Private method to perform a move in the game.'''
        # Check if the player ID is valid
        if player_id > 2:
            return False
        # Take a deepcopy of the current value at the from_pos
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        # Try to take the piece at the given position
        acceptable = self.__take((from_pos[1], from_pos[0]), player_id)
        if acceptable:
            # If taking the piece is acceptable, try to slide it
            acceptable = self.__slide(from_pos, slide)
            if not acceptable:
                # If sliding is not acceptable, revert to the previous value
                self._board[(from_pos[1], from_pos[0])] = deepcopy(prev_value)
        return acceptable

    def __take(self, from_pos: 'tuple[int, int]', player_id: int) -> bool:
        '''Private method to take a piece from the board.'''
        # Check if the position is on the border and if the current piece is neutral or belongs to the player
        acceptable: bool = (from_pos[0] == 0 and from_pos[1] < 5) or (from_pos[0] == 4 and from_pos[1] < 5) or (
            from_pos[1] == 0 and from_pos[0] < 5) or (from_pos[1] == 4 and from_pos[0] < 5) and (self._board[from_pos] < 0 or self._board[from_pos] == player_id)
        if acceptable:
            # If taking the piece is acceptable, assign it to the current player
            self._board[from_pos] = player_id
        return acceptable

    def __slide(self, from_pos: 'tuple[int, int]', slide: Move) -> bool:
        '''Private method to slide the pieces after a piece has been taken.'''
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]  # Corner positions on the board
        # Determine if the move is acceptable based on the current position and the desired slide direction
        if from_pos not in SIDES:
            # For non-corner positions
            acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT)
            acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT)
            acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT)
            acceptable_right: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT)
        else:
            # For corner positions
            acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            acceptable_right: bool = from_pos == (4, 0) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            acceptable_left: bool = from_pos == (0, 4) and (
                slide == Move.TOP or slide == Move.RIGHT)
            acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        if acceptable:
            # If the slide is acceptable, move the pieces accordingly
            piece = self._board[from_pos]
            # Slide operations based on the chosen direction
            if slide == Move.TOP:
                for i in range(from_pos[1], 0, -1):
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], 1 - 1)]
                self._board[(from_pos[0], 0)] = piece
            elif slide == Move.BOTTOM:
                for i in range(from_pos[1], self._board.shape[1], 1):
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], 1 + 1)]
                self._board[(from_pos[0], self._board.shape[1] - 1)] = piece
            elif slide == Move.LEFT:
                for i in range(from_pos[0], 0, -1):
                    self._board[(i, from_pos[1])] = self._board[(
                        1 - 1, from_pos[1])]
                self._board[(0, from_pos[1])] = piece
            elif slide == Move.RIGHT:
                for i in range(from_pos[0], self._board.shape[0], 1):
                    self._board[(i, from_pos[1])] = self._board[(
                        1 + 1, from_pos[1])]
                self._board[(self._board.shape[0] - 1, from_pos[1])] = piece
        return acceptable
