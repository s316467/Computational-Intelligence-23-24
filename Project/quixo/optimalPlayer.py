import random
from game import Game, Move, Player
from simulatedgame import SimulatedGame
import sys

# Just the rappresentation of a human (so optimal) player that makes the best possible moves based on 3 factors:
# 1) if there is a move that lead you to the victory, done it
# 2) if there are moves that lead your opponent to win (and they are not winning moves), don't do it (create like a black list of moves that mustn't be done)
# 3) Among all the others possible moves, do the one that lead you to a state in which you have more consecutives pieces for each row, column or diagonal
# In particular, prioioritize the move that lead you to a state in which you have 4 consecutive pieces e no opponent piece in at least one row, colum or diagonal
# Among all these moves, select the one that has more rows, columns or diagonal with that state
# Otherwise choose the move with highest score among all the possible moves that are not in the black list (#Rule 2)
# Pretty similar to the minMaxPlayer but it doesn't require any training or tree generation
class OptimalPlayer(Player):

    def make_move(self, game: Game) -> "tuple[tuple[int, int], Move]":
        # Get the current state of the board
        board = game.get_board()
        player_id = game.get_current_player()
        # print("Player_id: ", player_id)

        # Rule 1: Check for a winning move
        winning_move = self.find_winning_move(game, player_id)
        if winning_move:     # if there's a winning move, do it
            # print("Winning move: ", winning_move)
            return winning_move

        # Rule 2: Check for a move that bring you to an opponent's winning move
        # like a black list of moves that mustn't be executed
        losing_moves = []
        losing_moves = self.find_losing_moves(game, player_id)
        if len(losing_moves) != 0:
            print("Losing moves: ", losing_moves)

        # Rule 3: Make a move that improves the player's position and hinders the opponent
        best_moves = []
        best_moves = self.find_best_move(game, player_id, losing_moves)     
        if len(best_moves) != 0:
            best_move = random.choice(best_moves)       # select randomly one of the best_moves, if there are more than one,
            print("Selected_move: ", best_move)         # otherwise you will select the only move present in the list
            return best_move    
        else: 
            selected_move = random.choiche(self.get_possible_moves(game, player_id))     # if there are no possible moves it means that
            print("Selected_move: ", best_move)                                          # every move bring you to a losing position so select
            return selected_move                                                         # randomly one of the possible_move because you are gonna lose (o7 GG WP)

    # check if among all the possible moves there's one that bring you to the victory
    def find_winning_move(self, game, player_id):
        possible_moves = self.get_possible_moves(game, player_id)
        
        for moves in possible_moves:
            x, y = moves[0]
            direction = moves[1]
            if self.is_winning_move(game, x, y, direction, player_id):
                return moves

        return None


    # check if among all the possible moves there's at least one that leads to a state in which the opponent can make a winning_move
    def find_losing_moves(self, game, player_id):
        possible_moves = self.get_possible_moves(game, player_id)
        opponent_id = (player_id + 1) % 2
        losing_moves = []

        for moves in possible_moves:
            x, y = moves[0]
            direction = moves[1]
            simulated = SimulatedGame(game.get_board(), player_id)      # create a simulatedGame to check the state of the move
            ok = simulated.move((x, y), direction, player_id)           # make the move with the simulated board (deepcopy)
            if ok: 
                opponent_winning_move = self.find_winning_move(simulated, opponent_id)
                if opponent_winning_move:
                    losing_moves.append(moves)

        return losing_moves

    # check if the move is the one that leads you to the win
    def is_winning_move(self, game, x, y, direction, player_id):
        # Check if the move creates a winning position for the player
        winning_move = False
        simulated = SimulatedGame(game.get_board(), player_id)
        ok = simulated.move((x, y), direction, player_id)
        if ok:
            if simulated.check_winner() == player_id:
                winning_move = True
        return winning_move
    
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

    # Find the best possible moves based on the Score
    # the moves that leads you to a state in which you have at least one row/column/diagonal/anti diagonal with 4 equal pieces in sequence
    # and no opponent piece is considerated as the best possible beacause it leads to a state in which the opponent has to block you from winning
    # so the number of moves that he can make are fewer. So you are actually blocking your opponent from playing as he want and forcing him to 
    # make a move that blocks you and for that reason the score associated to that move will be tha maximum possible (system.)
    # the score is calculated as the sum of product of all the consecutive pieces among each row/column/diagonal/anti diagonal
    def find_best_move(self, game, player_id, losing_moves):
        possible_moves = self.get_possible_moves(game, player_id)

        best_move = None
        best_score = float('-inf')
        best_count = 0
        best_moves = []

        for move in possible_moves:
            if move in losing_moves:    # if the considerated move is in the black list of moves, jump to the next iteration of the for 
                continue                # and don't consider the move as a "possible" move
            x, y = move[0]
            direction = move[1]
            score, count = self.evaluate_move(game, x, y, direction, player_id)
            # print("Score, count: ", score, count)
            if score >= best_score:         
                if score == best_score:             
                    if count >= best_count:            
                        if count == best_count:     # if the score and the count are the same as the previous we have two prioritized moves and we update the list of best moves
                            best_moves.append((move, score, count))
                            if best_move != None:   # reset the previous best move
                                best_move = None
                            # print("New element added: ", move, score, count)
                        else:
                            if len(best_moves) != 0:    # if we are in this else we have a move with the same score but an higher count
                                best_moves.clear()      # reset the list of best moves
                            best_score = score          # update the new best score
                            best_move = move            # update the new best move
                            best_count = count          # update the new best count
                            # print("Best score updated: ", best_score)
                            # print("Best move updated: ", best_move)
                            # print("Best count updated: ", best_count)
                else:
                    if len(best_moves) != 0:    # if we are in this else we have a new best move with an higher score and count
                        best_moves.clear()      # reset the list of best moves
                    best_score = score          # update the new best score
                    best_move = move            # update the new best move
                    best_count = count          # update the new best count
                    # print("Best score updated: ", best_score)
                    # print("Best move updated: ", best_move)
                    # print("Best count updated: ", best_count)

        m = []
        
        if len(best_moves) != 0:
            for elem in best_moves:
                m.append(elem[0])                   # append the move to the list of moves
            return m                # return the list of moves
        else:
            m.append(best_move)             # otherwise select the best move
            return m

    # function to evaluate the score associated with each move
    # Among all the possible moves that are not the winning ones and that are not in the black list,
    # prioioritize the move that lead you to a state in which you have 4 consecutive pieces e no opponent piece in at least one row, colum or diagonal
    # associating the maximum score possible to it (sys.float_info.max) 
    # Among all these moves, select the one that has more rows, columns or diagonal with that state
    # Otherwise choose the move with highest score among all the possible moves that are not in the black list (#Rule 2)
    def evaluate_move(self, game, x, y, direction, player_id):
        # Evaluate a move based on proximity to victory and hindrance to opponent
        score = 0

        simulated = SimulatedGame(game.get_board(), player_id)      # simulate the move
        ok = simulated.move((x, y), direction, player_id)
        board = simulated.get_board()                               # get the updated board

        results = self.check_board(simulated.get_board(), player_id)    # count the pieces of the player_id

        num_elements_rows, num_elements_columns, num_elements_diagonal, num_elements_anti_diagonal = results[0]

        opponent_rows, opponent_columns, opponent_diagonal, opponent_anti_diagonal = results[1]
    
        count = 0       # count indicates the number of rows, columns, diagonl and anti diagonal 
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
            
        if count != 0:
            return sys.float_info.max, count     # assign the maximun value possible to give priority to this move
        else:
            # evaluate the score as the sum of the product of the element for each row, column, diagonal and anti diagonal
            for i in range(board.shape[0]):     
                score += (num_elements_rows[i] * num_elements_rows[i])
                score += (num_elements_columns[i] * num_elements_columns[i])
                
            score += (num_elements_diagonal * num_elements_diagonal)
            score += (num_elements_anti_diagonal * num_elements_anti_diagonal)

        return score, count

    # get the list of all the possible moves
    def get_possible_moves(self, game, player_id):
        possible_moves = []
        for x in range(5):
            for y in range(5):
                for direction in [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]:
                    simulated = SimulatedGame(game.get_board(), player_id)
                    ok = simulated.move((x, y), direction, player_id)
                    if ok:
                        possible_moves.append(((x, y), direction))
        return possible_moves