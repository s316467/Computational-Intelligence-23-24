import random
import numpy as np
from game import Game, Move, Player
from simulatedgame import SimulatedGame
from players.randomPlayer import RandomPlayer

"""
The ReinforcedPlayer class, inheriting from Player, is an AI agent designed for a board game environment. 
It utilizes Q-learning, a form of reinforcement learning, to learn optimal strategies through gameplay. 
The agent employs an epsilon-greedy approach for action selection, balancing between exploring new moves and 
exploiting known strategies. It maintains a Q-table for storing the utility of actions in different game states. 
The agent undergoes a training phase against either a random player or another instance of itself, adjusting 
its strategy based on the outcomes of these games. Post-training, it relies on the learned Q-values to make 
decisions, significantly reducing exploration. This approach allows the agent to adaptively improve its gameplay, 
aiming to increase its chances of winning in the simulated game environment.
"""

# Training matches constant for the ReinforcedPlayer
TRAINING_MATCHES = 1000

class ReinforcedPlayer(Player):
    def __init__(self, trained = False):
        super().__init__()                      # Calls the constructor of the base class Player
        self.epsilon = 0.3                      # Sets the exploration rate for the epsilon-greedy strategy
        self.alpha = 0.3                        # Sets the learning rate for Q-learning updates
        self.trajectory = []                    # Initializes the trajectory list to store state sequences
        self.q_table = {}                       # Initializes the Q-table as an empty dictionary
        self.trained = trained                  # Indicates whether the player is already trained

    def updateReward(self, reward):
        # Update Q-values based on the reward received
        for state in self.trajectory:
            if self.q_table.get(state) is None:
                self.q_table[state] = 0          # Initialize unseen state's Q-value to 0
            # Update the Q-value for the state based on the received reward
            self.q_table[state] += self.alpha * (reward - self.q_table[state])

    def reset(self):
        # Resets the trajectory list for a new game
        self.trajectory = []

    def get_hash(self, state):
        # Converts the game state into a hashable representation
        hash = []
        for row in state:
            for cell in row:
                hash.append(cell)
        return str(hash)

    def get_possible_moves(self, simgame: 'SimulatedGame'):
        # Generates all possible moves from the current state
        my_pos = []   # Stores the player's own positions
        free_pos = [] # Stores the free positions on the board
        for x in range(5):
            for y in range(5):
                for direction in [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]:
                    simulated = SimulatedGame(simgame.get_board(),simgame.get_current_player())
                    ok = simulated.move((x, y), direction, simgame.get_current_player())
                    # Check if the move is valid
                    if ok:
                        # Classify the move based on whether it's taking a free spot or not
                        if simulated.get_board()[x][y] == simulated.get_current_player():
                            my_pos.append(((x, y), direction))
                        else:
                            free_pos.append(((x, y), direction))
        return my_pos,free_pos
    
    def make_move(self, game: 'Game') -> 'tuple[tuple[int, int], Move]':
        # Decides on the best move to make, based on Q-learning
        if not self.trained:
            # If not trained, undergo training
            self.q_table = self.training(game.get_current_player())
            self.trained = True
            self.epsilon = 0.0    # Set exploration rate to 0 after training
        simulated = SimulatedGame(game.get_board(), game.get_current_player())
        my_pos,free_pos = self.get_possible_moves(simulated)
    
        if np.random.uniform(0, 1) > self.epsilon:
            # Choosing the best move based on Q-values if not exploring
            value_max = float('-inf')

            for possible_move in my_pos + free_pos:
                simulated = SimulatedGame(game.get_board(), game.get_current_player())
                ok = simulated.move(possible_move[0],possible_move[1],simulated.get_current_player())
                next_board_hash = self.get_hash(simulated.get_board())
                # Get the Q-value of the resulting state
                value = 0 if self.q_table.get(next_board_hash) is None else self.q_table.get(next_board_hash)
                # Update the best move if this move has a higher Q-value
                if value > value_max:
                    value_max = value
                    best_hash = next_board_hash
                    from_pos = possible_move[0]
                    slide = possible_move[1]
         
        else: 
            # If exploring, choose a random move
            from_pos, slide = random.choice(free_pos) if len(free_pos)>0 else random.choice(my_pos)
            best_hash = self.get_hash(simulated.get_board())

        # Add the chosen state to the trajectory
        self.trajectory.append(best_hash)
        return from_pos, slide

    def training(self, player_id):
        # Training the agent by playing games against a random or reinforced player
        # Decide opponent based on player_id
        player0 = RandomPlayer() if player_id==1 else ReinforcedPlayer(trained=True)
        player1 = ReinforcedPlayer(trained=True) if player_id==1 else RandomPlayer()

        for match in range(TRAINING_MATCHES):
            g = Game()
            winner = g.play(player0, player1)
            # Update rewards based on the outcome of the game
            if winner == player_id:
                player1.updateReward(10) if player_id==1 else player0.updateReward(10)
            else:
                player1.updateReward(0) if player_id==1 else player0.updateReward(0)

            # Reset the players for the next game
            player1.reset() if player_id==1 else player0.reset()
        return player1.q_table if player_id==1 else player0.q_table
