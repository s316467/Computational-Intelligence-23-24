#################### Genetic Player #################### Genetic Player #################### Genetic Player #################### Genetic Player #################### Genetic Player  
from game import Player
from simulatedgame import SimulatedGame
import random
from game import Game, Move, Player
import numpy as np
from players.randomPlayer import RandomPlayer
from tqdm import tqdm  # Import tqdm

# The GeneticPlayer is a player in a game that evolves its strategy using a genetic algorithm. 
# It begins with a randomly generated strategy (genotype) and improves it over multiple generations. 
# The strategy undergoes mutations and crossovers, and the player's fitness is evaluated based on its performance in the game. 
# The genetic player selects parents based on their fitness, applies genetic operations to create a new generation, and repeats 
# this process for a specified number of generations. The ultimate goal is to produce a genotype with a high fitness score, 
# representing an effective and evolved strategy for playing the game.
# Once the player with the best genotype is obtained, the make_move function, to perform a move, will choose the one among 
# the possible moves that has the highest value of the product between the move's score and the move's count.

class GeneticPlayer(Player):
    def __init__(self, genotype=None, training = True, population_size=10, generations=10, mutation_rate=0.1,
                selection_strategy='tournament_selection', crossover_strategy='two_points', mutation_strategy='shift'):
        super().__init__()
        self.fitness_score = 0
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.selection_strategy = selection_strategy
        self.crossover_strategy = crossover_strategy
        self.mutation_strategy = mutation_strategy

        # Initialize genotype randomly or with a provided one
        if genotype:
            self.genotype = genotype
        else:
            self.genotype = self.generate_random_genotype()
        if training: 
            self.genotype = self.genetic_algorithm()


    def make_move(self, game: 'Game') -> 'tuple[tuple[int, int], Move]':
        # List to store possible moves with their weights
        possible_moves = []
        
        # Iterate over each element in the genotype
        for element in self.genotype:
            # Create a simulated game based on the current game state
            simulated = SimulatedGame(game.get_board(), game.get_current_player())
            
            # Extract move, weight, and count from the genotype element
            _move, weight, count = element

            # Check if the move is valid in the simulated game
            if simulated.move(_move[0], _move[1], game.current_player_idx):
                # If valid, add the move and its weighted count to the list
                possible_moves.append((_move, weight * count))

        # Sort possible moves based on their weighted counts in descending order
        sorted_possible_moves = sorted(possible_moves, key=lambda x: x[1], reverse=True)

        # Extract the top move and its weight from the sorted list
        top_move, top_weight = sorted_possible_moves[0]

        # Return the top move
        return top_move


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

    # Generate a random genotype: a list of (move, weight, countMove)
    def generate_random_genotype(self):
        # Create a simulated game with an initial board
        initialBoard = SimulatedGame(np.ones((5, 5), dtype=np.uint8) * -1, 0)
        
        # Get a list of possible moves on the initial board (should return 44 possible moves)
        moves = self.get_possible_moves(initialBoard)

        random_genotype = []
        for move in moves:
            # Generate a random weight for the move (between 0 and 100)
            random_weight = np.random.randint(0, 101)

            # Append the move, random weight, and count (initialized to 0)
            random_genotype.append((move, random_weight, 0))

        # Return the generated random genotype
        return random_genotype


    def calculate_fitness(self, factor = 1.2):
        # Create a new game instance for each fitness calculation
        game = SimulatedGame(np.ones((5, 5), dtype=np.uint8) * -1, 1)
        winner = -1
        opponent = RandomPlayer() 
        count_moves = 0

        # Continue the game until a winner is determined
        while winner < 0:
            game.current_player_idx += 1 
            game.current_player_idx %= 2
            ok = False

            # While the current player's move is not valid
            while not ok:
                if game.current_player_idx == 0:
                    # If the current player is the opponent, get a move from the opponent
                    from_pos, slide = opponent.make_move(game)
                    ok = game.move(from_pos, slide, 0)
                else: 
                    # If the current player is the genetic player, select a move based on the genotype
                    possible_moves = self.get_possible_moves(game)
                    returned = []

                    # Filter possible moves based on the genotype
                    for _move, _weight, _count in self.genotype:
                        if _move in possible_moves:
                            returned.append((_move,_weight,_count))
                    
                    # Sort the filtered moves based on weights in descending order
                    returned.sort(key=lambda x: x[1],reverse=True)

                    # If a move is selected from the genotype, update the genotype counts
                    if returned:
                        selected_move, selected_weight, selected_count = returned[0]
                        self.genotype = [(move, weight, count + 1) if move == selected_move else (move, weight, count) for move, weight, count in self.genotype]
                    
                    # Move the genetic player
                    ok = game.move(selected_move[0],selected_move[1],1)
                    count_moves += 1
            winner = game.check_winner()

        # Update fitness score based on the game result
        if winner:
            self.fitness_score += 1 + (1/count_moves) * factor 

        # Return the updated fitness score
        return self.fitness_score

    @staticmethod 
    def crossover(parent1, parent2, crossover_strategy='single_point'):
        # Get the length of the genotype
        len_gen = len(parent1)

        # Check the crossover strategy
        if crossover_strategy == 'single_point':
            # Choose a random crossover point
            crossover_point = random.randint(0, len_gen - 1)

            # Perform single-point crossover
            cross = parent1[:crossover_point] + parent2[crossover_point:]
            return cross
        
        if crossover_strategy == 'two_points':
            # Choose two distinct random crossover points
            point1 = random.randint(0, len_gen - 1)
            point2 = random.randint(0, len_gen - 1)

            # Ensure the two points are distinct
            while point1 == point2:
                point2 = random.randint(0, len_gen - 1)

            # Determine the start and end points for two-point crossover
            start, end = sorted([point1, point2])
            
            # Perform two-point crossover
            cross = parent1[:start] + parent2[start:end] + parent1[end:]
            return cross 

    @staticmethod 
    def mutate(child, mutation_rate=0.1, mutation_strategy='swap'):
        # Get the length of the genotype
        len_gen = len(child)
                

        # Check the mutation strategy
        if mutation_strategy == 'random_reset':
            # Randomly reset weights in the genotype with a certain probability
            for i in range(len_gen):
                if random.random() < mutation_rate:
                    _move, _weight, _count = child[i]
                    _weight += np.random.randint(-19, 20)
                    child[i] = (_move,_weight,_count)
            return child
                
        if mutation_strategy == 'swap':
            # Swap the weights of pairs of elements in the genotype with a certain probability
            for i in range(len_gen - 1):
                if np.random.rand() < mutation_rate:
                    j = np.random.randint(i + 1, len_gen)
                    _move_i, _weight_i, _count_i = child[i]
                    _move_j, _weight_j, _count_j = child[j]
                    _weight_i, _weight_j = _weight_j, _weight_i
                    child[i] = (_move_i, _weight_i, _count_i)
                    child[j] = (_move_j, _weight_j, _count_j)
            return child
        
        if mutation_strategy == 'shift':
            # Shift a portion of weights in the genotype with a certain probability
            for i in range(len_gen - 1):
                if np.random.rand() < mutation_rate:
                    # Randomly select start and end indices for the shifted portion
                    start_index = np.random.randint(1, len_gen - 3)
                    end_index = np.random.randint(start_index + 1, len_gen - 2)
                    selected_weight = []
                    
                    # Extract weights from portions before and after the selected portion
                    portion2_weight = []
                    for i in range(start_index, end_index + 1):
                        move, weight, count = child[i]
                        portion2_weight.append(weight)

                    portion1_weight = []
                    for i in range(0, start_index):
                        move, weight, count = child[i]
                        portion1_weight.append(weight)

                    portion3_weight = []
                    for i in range(end_index + 1, len_gen):
                        move, weight, count = child[i]
                        portion3_weight.append(weight)

                    # Combine and shuffle the weights to form the shifted portion
                    selected_weight = portion2_weight + portion3_weight + portion1_weight

                    # Update the weights in the genotype
                    for i in range(len_gen):
                        move, weight, count = child[i]
                        weight = selected_weight[i]
                        child[i] = move, weight, count

            return child
      
    def genetic_algorithm(self, population_size=100, generations=10, mutation_rate=0.1):
        # Initialize the population with randomly generated players
        population = [GeneticPlayer(training=False) for _ in range(population_size)]

        # Evolve the population over a specified number of generations
        for generation in tqdm(range(generations), desc="Evolving Generations"):
            
            # Calculate fitness scores for each player in the population
            fitness_scores = [s.calculate_fitness() for s in tqdm(population, desc=f"Gen {generation+1} Fitness Eval", leave=False)]
            
            # Select individuals for the mating pool based on fitness scores
            mating_pool = [population[i] for i in self.select_based_on_fitness(self, fitness_scores)]
           
            # Create next generation using crossover and mutation
            new_population = []
            while len(new_population) < population_size:
                # Select two parents randomly from the mating pool
                parents = random.sample(mating_pool, 2)

                # Perform crossover on the parents' genotypes
                child_genotype = GeneticPlayer.crossover(parents[0].genotype, parents[1].genotype, self.crossover_strategy)
                
                # Perform mutation on the child genotype
                child_genotype = GeneticPlayer.mutate(child_genotype, self.mutation_rate, self.mutation_strategy)
                
                # Add the child with the new genotype to the new population
                new_population.append(GeneticPlayer(genotype=child_genotype,training=False))
            
            # Update the population with the new generation
            population = new_population
        
        # Return the best genotype found in the final population
        best_player = max(population, key=lambda player: player.fitness_score)
        return best_player.genotype
    
    @staticmethod
    def select_based_on_fitness(self, fitness_scores):
        # Check the selection strategy
        if self.selection_strategy == 'roulette_wheel':
            # Calculate total fitness and ensure it's not zero
            total_fitness = sum(fitness_scores)
            if total_fitness == 0:
                total_fitness = 1
            
            # Calculate selection probabilities based on fitness scores
            selection_probs = [f / total_fitness for f in fitness_scores]
            
            # Select indices based on roulette wheel selection
            best_indices = np.random.choice(len(fitness_scores), size=len(fitness_scores), replace=True, p=selection_probs)
            return best_indices
        
        if self.selection_strategy == 'tournament_selection':
            # Initialize lists to store selected players and tournament winners
            winners = []

            # Set the tournament size as a percentage of the population size
            tournament_size = int(self.population_size * 0.2)

            # Perform tournament selection for the entire population
            for _ in range(self.population_size):
                # Randomly choose tournament indices without replacement
                tournament_indices = np.random.choice(int(self.population_size/2), tournament_size, replace=False)

                # Retrieve tournament fitness scores
                tournament_scores = [fitness_scores[i] for i in tournament_indices]

                # Determine the winner index based on the highest fitness score in the tournament
                winner_index = tournament_indices[np.argmax(tournament_scores)]
                winners.append(winner_index)

            return winners