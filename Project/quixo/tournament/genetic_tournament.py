from game import Game
from players.geneticPlayer import GeneticPlayer
from players.randomPlayer import RandomPlayer
from itertools import product

# Tournament between GeneticPlayer and RandomPlayer made in order to
# determine the best strategy combination among:
# selection_strategies = ["roulette_wheel", "tournament_selection"]
# crossover_strategies = ["single_point", "two_points"]
# mutation_strategies = ["random_reset", "swap", "shift"]
# that fits the best for the GeneticPlayer, along with setting hyperparameters such as:
# population_size = from 10 to 100 (closer to 50)
# number_of_generations = from 2 to 20 (closer to 10)
# mutation_rate from 0.1 to 0.5 (closer to 0.15)


# Function to generate combinations of selection, crossover, and mutation strategies
def strategies_combinations():
    selection_strategies = ["roulette_wheel", "tournament_selection"]
    crossover_strategies = ["single_point", "two_points"]
    mutation_strategies = ["random_reset", "swap", "shift"]

    combinations = list(product(selection_strategies, crossover_strategies, mutation_strategies))

    return combinations

def run_genetic_tournament():
    # Get all possible strategy combinations for GeneticPlayer
    genetic_strategies = strategies_combinations()

    # Number of games for each combination of GeneticPlayer and RandomPlayer
    num_games_per_matchup = 10

    # Create a list of initial participants using strategy combinations for GeneticPlayer
    # genetic_players = [GeneticPlayer(None, True, 10, 5, 0.1, selection_strategy, crossover_strategy, mutation_strategy)
                      # for (selection_strategy, crossover_strategy, mutation_strategy) in genetic_strategies]

    # Create RandomPlayer
    random_player = RandomPlayer()

    # Dictionary to store tournament statistics
    tournament_stats = {}

    for strategy_combination in genetic_strategies:
        # for parameter_combination in parameters_values:
        # Initialize statistics for this strategy combination
        tournament_stats[strategy_combination] = {"total_wins": 0, "total_games": 0}
        # tournament_stats[strategy_combination][parameter_combination] = {"total_wins": 0, "total_games": 0}

        # Play num_games_per_matchup games against the RandomPlayer
        for _ in range(num_games_per_matchup):
            # Create a new game
            game = Game()

            # Play the game with GeneticPlayer as Player1 and RandomPlayer as Player2
            winner = game.play(GeneticPlayer(None, True, 50, 10, 0.15, *strategy_combination), random_player)
            # winner = game.play(GeneticPlayer(None, True, *parameter_combination, *strategy_combination), random_player)

            # Update tournament statistics
            tournament_stats[strategy_combination]["total_games"] += 1
            # tournament_stats[strategy_combination][parameter_combination]["total_games"] += 1
            if winner == 0:
                tournament_stats[strategy_combination]["total_wins"] += 1
                # tournament_stats[strategy_combination][parameter_combination]["total_games"] += 1

        # Play additional num_games_per_matchup games with RandomPlayer as Player1 and GeneticPlayer as Player2
        for _ in range(num_games_per_matchup):
            # Create a new game
            game = Game()

            # Play the game with RandomPlayer as Player1 and GeneticPlayer as Player2
            winner = game.play(random_player, GeneticPlayer(None, True, 50, 10, 0.15, *strategy_combination))
            # winner = game.play(GeneticPlayer(None, True, *parameter_combination, *strategy_combination), random_player)

            # Update tournament statistics
            tournament_stats[strategy_combination]["total_games"] += 1
            # tournament_stats[strategy_combination][parameter_combination]["total_games"] += 1
            if winner == 1:
                tournament_stats[strategy_combination]["total_wins"] += 1
                # tournament_stats[strategy_combination][parameter_combination]["total_wins"] += 1

    # Find the strategy combination with the highest total wins
    best_strategy_combination = max(tournament_stats, key=lambda k: tournament_stats[k]["total_wins"])
    # best_combination = max(tournament_stats, key=lambda k: tournament_stats[k][k]["total_wins"])

    # Print the final winner
    print("\nTournament Winner:")
    print(f"Best Strategy Combination: {best_strategy_combination} with {tournament_stats[best_strategy_combination]['total_wins']} wins out of {tournament_stats[best_strategy_combination]['total_games']} games")
    ## print(f"Best Combination: {best_combination} with {tournament_stats[best_combination[0]][best_combination[1]]['total_wins']} wins out of {tournament_statsbest_combination[0]][best_combination[1]]['total_games']} games")

    print(f"\nTournament stats: ")
    for strategy_combination in genetic_strategies:
        # for parameter_combination in parameters_values:
        print(f"Strategy Combination: {strategy_combination} -> {tournament_stats[strategy_combination]['total_wins']} wins out of {tournament_stats[strategy_combination]['total_games']} games")
        # print(f"Combination: {strategy_combination}{parameter_combination} -> {tournament_stats[strategy_combination][parameter_combination]['total_wins']} wins out of {tournament_stats[strategy_combination][parameter_combination]['total_games']} games")