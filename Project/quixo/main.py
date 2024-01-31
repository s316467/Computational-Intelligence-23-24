from game import Game, Player
from players.minMaxPlayer import MinMaxPlayer
from players.geneticPlayer import GeneticPlayer
from players.randomPlayer import RandomPlayer
from players.optimalPlayer import OptimalPlayer
from players.reinforcedPlayer import ReinforcedPlayer
from tournament.genetic_tournament import run_genetic_tournament
from tournament.final_tournament import run_final_tournament

# Define a dictionary of players so that it can be selected in this part of the code as global variable
# Player type selection

def create_player(player_type, game: 'Game' = None) -> 'Player':
    """
    Create and return a player instance based on the player type.
    """
    if player_type == "random":
        return RandomPlayer()
    elif player_type == "genetic":
        return GeneticPlayer()
    elif player_type == "minmax":
        return MinMaxPlayer()
    elif player_type == "reinforcement":
        return ReinforcedPlayer()
    elif player_type == "optimal":
        return OptimalPlayer()
    else:
        raise ValueError(f"Unknown player type: {player_type}")

############################################################## EXECUTION ############################################################################################

if __name__ == '__main__':
    
    # run_genetic_tournament()
    
    # run_final_tournament()
    
    # Create a new game instance and print the initial board
    game = Game()
    game.print()

    # Create two players    
    player1_type = "random"
    player2_type = "minmax"

    player1 = create_player(player1_type, game)
    player2 = create_player(player2_type, game)
    num_wins_player1 = 0
    num_wins_player2 = 0

    # tournament between player1 and player2
    first_tournament_winner, second_tournament_winner = 0 , 0
    draw = False
    for i in range(25):
        game = Game()
        winner = game.play(player1, player2)    # Play the game
        print(f'\nWinner: {winner}')
        if winner == 0:
            num_wins_player1 += 1
        else:
            num_wins_player2 += 1
    
    print( f"Player1: {num_wins_player1} - Player2: {num_wins_player2}")

    if num_wins_player1 > num_wins_player2:
        first_tournament_winner = 0
    elif num_wins_player2 > num_wins_player1:
        first_tournament_winner = 1

    first_tournament_wins_p1 = num_wins_player1
    first_tournament_wins_p2 = num_wins_player2

    num_wins_player1 = 0
    num_wins_player2 = 0
    # switch the two players
    for i in range(25):
        game = Game()
        winner = game.play(player2, player1)        # Play the game
        print(f'\nWinner: {winner}')
        if winner == 0:
            num_wins_player1 += 1
        else:
            num_wins_player2 += 1
    
    print( f"Player1: {num_wins_player1} - Player2: {num_wins_player2}")

    if num_wins_player1 > num_wins_player2:
        second_tournament_winner = 0
    elif num_wins_player2 > num_wins_player1:
        second_tournament_winner = 1

    # Print the result of the tournament
    print("Result of the first tournament: ")
    if first_tournament_winner == 0:
        print("Winner Player1 with", first_tournament_wins_p1, "wins out of 25 games")
    else:
        print("Winner Player2 with", first_tournament_wins_p2, "wins out of 25 games")

    print("Result of the second tournament: ")
    if second_tournament_winner == 0:
        print("Winner Player1 with", num_wins_player1, "wins out of 25 games")
    else:
        print("Winner Player2 with", first_tournament_wins_p2, "wins out of 25 games")

    wins_player1 = first_tournament_wins_p1 + num_wins_player1
    wins_player2 = first_tournament_wins_p2 + num_wins_player2

    if wins_player1 > wins_player2:
        winner = 0
    elif wins_player2 > wins_player1:
        winner = 1
    else:
        draw = True

    print("Final result:")
    if draw:
        print("Draw with:\n Player1 -> ", wins_player1, " wins out of 50 games \n Player2 -> ", wins_player2, " wins out of 50 games")
    elif wins_player1 > wins_player2:
        print("Player1 wins with ", wins_player1, " wins out of 50 games")
    else:
        print("Player2 wins with ", wins_player2, " wins out of 50 games")
    