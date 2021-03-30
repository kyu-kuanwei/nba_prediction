from src.algorithm.brute_force import BruteForce
from src.after_game import AfterGame
from src.scrape import Scraper, PlayerStats, load_configs
from src.data_pipeline import DataPipeline


if __name__ == "__main__":
    # Today results.
    after_game = AfterGame()
    today_results = after_game.valid_players
    today_results = BruteForce(maximum_size=2, valid_players=today_results[:50])

    # Tomorrow prediction
    scraper = Scraper()
    all_players_stats = PlayerStats()
    prediction_data_pipeline = DataPipeline(
        player_rating=scraper.results,
        player_stats=all_players_stats.all_players
    )
    prediction_data_pipeline.export_to_csv(mode=load_configs['mode'])
    tomorrow_prediction = BruteForce(
        maximum_size=3,
        valid_players=prediction_data_pipeline.valid_players,
        mode=load_configs['mode']
    )
