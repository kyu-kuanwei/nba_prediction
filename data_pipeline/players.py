class Players:
    def __init__(self, name, rating, score, position):
        self.name = name
        self.rating = rating
        self.score = score
        self.position = position

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.name}  {self.position}  {self.rating}"