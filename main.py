from src.algorithm.brute_force import BruteForce
from src.after_game import AfterGame
from src.scrape import Scraper, PlayerStats


if __name__ == "__main__":
    after_game = AfterGame()
    today_results = after_game.valid_players
    recommand = BruteForce(maximum_size=1, valid_players=today_results[:50])

    # scraper = Scraper()
    # all_players_stats = PlayerStats()

    # prediction_data_pipeline = DataPipeline(
    #     player_rating=scraper.results,
    #     player_stats=all_players_stats.all_players
    # )
    # # Export to csv files.
    # prediction_data_pipeline.export_to_csv(mode=load_configs['mode'])

    # valid_players = prediction_data_pipeline.valid_players
    # # Recommand tomorrow fantasy prediction
    # brute_force.recommand(valid_players=valid_players)

