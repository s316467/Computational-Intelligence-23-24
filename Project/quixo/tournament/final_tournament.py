# Import necessary classes from other modules
from game import Game
from players.randomPlayer import RandomPlayer
from players.minMaxPlayer import MinMaxPlayer
from players.geneticPlayer import GeneticPlayer
from players.reinforcedPlayer import ReinforcedPlayer
from players.optimalPlayer import OptimalPlayer

"""
This code comprises a function run_final_tournament() that orchestrates a tournament 
among various player types in a game environment. It includes RandomPlayer, MinMaxPlayer, 
GeneticPlayer, ReinforcedPlayer, and OptimalPlayer, each embodying different strategies 
or AI algorithms. The tournament involves each player competing against the RandomPlayer, 
with the function meticulously tracking statistics like total wins, wins as player 1 or 2, 
and total games for each participant. Post-matchups, these statistics are calculated 
and displayed, highlighting win percentages and identifying the top-performing player(s). 
The Game class is used for simulating games, and the Move class for game moves. 
Notably, GeneticPlayer is initialized with specific genetic algorithm parameters. 
Overall, run_final_tournament() serves as an extensive framework for evaluating 
and comparing different player types or AI strategies in a simulated competitive environment.
"""

# Function definition for running the final tournament among different player types
def run_final_tournament():
    # Initialize the list of player instances
    players = [
        RandomPlayer(),
        MinMaxPlayer(),
        GeneticPlayer(None, True, 50, 10, 0.15, 'roulette_wheel', 'two_points', 'random_reset'),
        ReinforcedPlayer(),
        OptimalPlayer()
    ]

    # Initialize a dictionary to keep track of tournament statistics for each player
    tournament_stats = {player: {"total_wins": 0, "total_games": 0, "wins_as_player1": 0, "wins_as_player2": 0} for player in players}

    # Define the number of games to be played in each matchup
    num_games_per_matchup = 10

    # Loop through each player as player1
    for player in players:
            # Create a RandomPlayer instance
            random_player = RandomPlayer()
            # Play the specified number of games with player and random player
            for _ in range(num_games_per_matchup):
                game1 = Game()
                winner1 = game1.play(player, random_player)
                tournament_stats[player]["total_games"] += 1
                tournament_stats[player]["wins_as_player1"] += 1 if winner1 == 0 else 0
                if winner1 == 0:
                    tournament_stats[player]["total_wins"] += 1

                # Play the specified number of games with random player starting as first player
                game2 = Game()
                winner2 = game2.play(random_player, player)
                tournament_stats[player]["total_games"] += 1
                tournament_stats[player]["wins_as_player2"] += 1 if winner2 == 1 else 0
                if winner2 == 1:
                    tournament_stats[player]["total_wins"] += 1

    # Print the statistics of the tournament
    print("\nTournament Statistics:")
    for player in players:
        print(f"\nPlayer: {player}")
        print(f"Total Wins: {tournament_stats[player]['total_wins']}")
        print(f"Total Games: {tournament_stats[player]['total_games']}")
        print(f"Wins as Player1: {tournament_stats[player]['wins_as_player1']}")
        print(f"Wins as Player2: {tournament_stats[player]['wins_as_player2']}")
        print(f"Win Percentage: {tournament_stats[player]['total_wins'] / tournament_stats[player]['total_games'] * 100}%")

    # Determine the player(s) with the highest number of total wins
    best_player = max(tournament_stats, key=lambda player: tournament_stats[player]["total_wins"])

    # Check if there are multiple players with the highest number of wins
    best_players = [player for player in tournament_stats if tournament_stats[player]["total_wins"] == tournament_stats[best_player]["total_wins"]]

    # If there's only one best player
    if not best_players:
        print("\nThe best player is: ", best_player, "con ", tournament_stats[best_player]["total_wins"],
              " vitcories out of ", tournament_stats[best_player]["total_games"], " games")
    else:
        # If there's a tie, print all the best players
        print(f"\nThe best playera are:")
        i = 1
        for player in best_players:
            print(i, ") ", player, "con ", tournament_stats[player]['total_wins'], 
                  " vitcories out of ", tournament_stats[player]["total_games"], " games")
            i += 1
        
        print("\nPlayers with highest total number of victories: ", best_players)
