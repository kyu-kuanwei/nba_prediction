from src.algorithm.brute_force import BruteForce
from src.after_game import AfterGame
from src.scrape import Scraper, PlayerStats, load_configs
from src.data_pipeline import DataPipeline


if __name__ == "__main__":
    # Today results.
    today_results = BruteForce(maximum_size=2, valid_players=AfterGame().valid_players[:50])

    # Tomorrow prediction
    scraper = Scraper()
    all_players_stats = PlayerStats()
    prediction_data_pipeline = DataPipeline(
        player_rating=scraper.results,
        player_stats=all_players_stats.all_players
    )
    prediction_players = prediction_data_pipeline.valid_players
    prediction_data_pipeline.export_to_csv(valid_players=prediction_players, mode=load_configs['mode'])
    tomorrow_prediction = BruteForce(
        maximum_size=3,
        valid_players=prediction_players,
        mode=load_configs['mode']
    )
