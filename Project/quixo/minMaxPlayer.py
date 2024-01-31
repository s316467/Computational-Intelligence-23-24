#################### MinMax Player #################### MinMax Player #################### MinMax Player #################### MinMax Player #################### MinMax Player 
from game import Player, Game, Move
from simulatedgame import SimulatedGame
import random

# The MinMaxPlayer is designed to make strategic decisions by intelligently exploring the game tree using the Minimax algorithm 
# while incorporating a heuristic evaluation function to guide its decision-making process.
# The heuristic evaluation function is based on the optimalPlayer strategy for the evaluation of the score
# For each possible move a tree is generated alternating 
class MinMaxPlayer(Player):
    def __init__(self, depth=3):
        super().__init__()
        self.depth = depth
        self.new_game = None
    
    # Recursive function that implements the MinMax algorithm (tree generation, leaf evaluation, back propagation e move selection)
    # maximazing is a flag that indicates if we are in the maximazing player or in the minimazing (we start as maximazier) 
    def alphabeta(self, simgame: 'SimulatedGame', alpha, beta, depth, player_id, maximazing = True):
        endGame = simgame.check_winner() != -1      # check if we arrived to a winning state of the board
        if endGame == True or depth == 0:
            score = self.evaluate(simgame, depth)   # Leaf valutation 
            return score, None
        
        bestMove = None
        if maximazing:       # maximizer player
            for _move in self.get_possible_moves(simgame):
                s = SimulatedGame(simgame.get_board(), player_id)       # create a deepcopy version of the game to simulate the moves
                sim_from_pos, sim_slide = _move
                s.move((sim_from_pos[0], sim_from_pos[1]), sim_slide, player_id)        # make the move
                val, _ = self.alphabeta(s, alpha, beta, depth-1, ((player_id + 1) % 2), False)
                if val > alpha:     # back propagation
                    alpha = val     
                    bestMove = _move
                if alpha >= beta:   # pruning
                    break
            return alpha, bestMove
        else:               # minimazer player
            for _move in self.get_possible_moves(simgame):
                s = SimulatedGame(simgame.get_board(), player_id)       # create a deepcopy version of the game to simulate the moves
                sim_from_pos, sim_slide = _move
                s.move((sim_from_pos[0], sim_from_pos[1]), sim_slide, player_id)        # make the move
                val, _ = self.alphabeta(s, alpha, beta, depth-1, ((player_id + 1) % 2), True)
                if val < beta:      # back propagation
                    beta = val
                    bestMove = _move
                if alpha >= beta:   # pruning
                    break
            return beta, bestMove

    # Adapting evaluate function from the optimalPlayer code
    # prioioritize the move that lead you to a state in which you have 4 consecutive pieces e no opponent piece in at least one row, colum or diagonal
    # increasing the score using the count variable (number of rows, columns, diagonal and anti diagonal in priority state) 
    def evaluate(self, simgame: 'SimulatedGame', depth):
        endGame = simgame.check_winner()
        if endGame == 0:  # Maximizer won
            return 100 + depth
        elif endGame == 1:  # Minimizer won
            return -100 - depth
        else:
            score = 0                               
            board = simgame.get_board()
            player_id = simgame.get_current_player()

            results = self.check_board(board, player_id)        # count the pieces of the player_id

            num_elements_rows, num_elements_columns, num_elements_diagonal, num_elements_anti_diagonal = results[0]

            opponent_rows, opponent_columns, opponent_diagonal, opponent_anti_diagonal = results[1]
        
            count = 0   # count indicates the number of rows, columns, diagonl and anti diagonal 
                        # that are in a state in which we have 4 consecutive pieces of the player_id and no opponent piece

            # count the number of rows, columns, diagonl and anti diagonal 
            # that are in a state in which we have 4 consecutive pieces of the player_id and no opponent piece
            for i in range(board.shape[0]):
                if num_elements_rows[i] == board.shape[0] - 1 and opponent_rows[i] == 0:
                    count += 1
                if num_elements_columns[i] == board.shape[0] - 1 and opponent_columns[i] == 0:
                    count += 1

            if num_elements_diagonal == board.shape[0] - 1 and opponent_diagonal == 0:
                count += 1
            if num_elements_anti_diagonal == board.shape[0] - 1 and opponent_anti_diagonal == 0:
                count += 1
           
            # evaluate the score as the sum of the product of the element for each row, column, diagonal and anti diagonal
            for i in range(board.shape[0]):
                score += (num_elements_rows[i] * num_elements_rows[i])
                score += (num_elements_columns[i] * num_elements_columns[i])
                
            score += (num_elements_diagonal * num_elements_diagonal)               
            score += (num_elements_anti_diagonal * num_elements_anti_diagonal)

            if count != 0:
                if count == 1:
                    count += 0.5
                score *= count

            return score

    # function that count every piece of player_id along the board
    def check_board(self, board, player_id):
        opponent_id = (player_id + 1) % 2

        num_elements_rows = [0] * board.shape[0]
        opponent_rows = [0] * board.shape[0]
        opponent_columns = [0] * board.shape[0]
        num_elements_columns = [0] * board.shape[0]
        num_elements_diagonal = 0
        opponent_diagonal = 0
        opponent_anti_diagonal = 0
        num_elements_anti_diagonal = 0
        
        for i in range(board.shape[0]):
            for j in range(board.shape[0]):
                if board[i, j] == player_id:
                    num_elements_rows[i] += 1
                    num_elements_columns[j] += 1
                    if i == j:
                        num_elements_diagonal += 1
                    if i + j == board.shape[0] - 1:
                        num_elements_anti_diagonal += 1
                elif board[i, j] == opponent_id:
                    opponent_rows[i] += 1
                    opponent_columns[j] += 1
                    if i == j:
                        opponent_diagonal += 1
                    if i + j == board.shape[0] - 1:
                        opponent_anti_diagonal += 1

        results = []
        results.append((num_elements_rows, num_elements_columns, num_elements_diagonal, num_elements_anti_diagonal))
        results.append((opponent_rows, opponent_columns, opponent_diagonal, opponent_anti_diagonal))

        return results

    def make_move(self, game: 'Game') -> 'tuple[tuple[int, int], Move]':
        simulated = SimulatedGame(game.get_board(), game.get_current_player())
        _, best_move = self.alphabeta(simulated, float('-inf'), float('inf'), self.depth, game.get_current_player())
        if best_move is not None:
            best_from_pos, best_direction = best_move
        else:
            # Fallback to a random move if no best move is found
            best_from_pos, best_direction = random.choice(self.get_possible_moves(simulated))

        return best_from_pos, best_direction

    # get the list of all the possible moves
    def get_possible_moves(self, simgame: 'SimulatedGame'):
        possible_moves = []
        for x in range(5):
            for y in range(5):
                for direction in [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]:
                    simulated = SimulatedGame(simgame.get_board(),simgame.get_current_player())
                    ok = simulated.move((x, y), direction, simgame.get_current_player())
                    if ok:
                        possible_moves.append(((x, y), direction))
        return possible_moves