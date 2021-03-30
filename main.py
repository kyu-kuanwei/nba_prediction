from src.algorithm.brute_force import BruteForce
from src.after_game import AfterGame
from src.scrape import load_configs
from src.data_lib.data_pipeline import DataPipeline


if __name__ == "__main__":
    # Today results.
    # today_results = BruteForce(maximum_size=2, valid_players=AfterGame().valid_players[:50])

    # Tomorrow prediction
    tomorrow_prediction = BruteForce(
        maximum_size=3,
        valid_players=DataPipeline().valid_players,
        mode=load_configs['mode']
    )
