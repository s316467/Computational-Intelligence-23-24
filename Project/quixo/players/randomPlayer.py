#################### Random Player #################### Random Player#################### Random Player#################### Random Player#################### Random Player 
from game import Player
from simulatedgame import SimulatedGame
import random
from game import Game, Move, Player

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> 'tuple[tuple[int, int], Move]':
        from_pos, direction = random.choice(self.get_possible_moves(game))
        return from_pos, direction

    def get_possible_moves(self, game: 'Game'):
        possible_moves = []
        board = game.get_board()
        player = game.get_current_player()
        tmp = SimulatedGame(board,player)
        for x in range(5):
            for y in range(5):
                for direction in [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]:
                    tmp._board = board
                    if tmp.move((x, y), direction, player):
                        possible_moves.append(((x, y), direction))
        return possible_moves