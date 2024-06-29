"""
Operators for MLRS
"""


class Operator:
    def __init__(self, name, age, position, rank):
        self.name = name
        self.age = age
        self.position = position
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} {self.name}, {self.position}, Age: {self.age}"
