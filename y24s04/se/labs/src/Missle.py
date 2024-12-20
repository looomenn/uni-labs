"""
Missile module for MLRS
"""


class Missile:
    def __init__(self, missile_id, missile_type, missile_range,
                 weight, caliber, accuracy, warhead_weight, chamber_position):
        self.missile_id = missile_id
        self.type = missile_type
        self.range = missile_range
        self.weight = weight
        self.caliber = caliber
        self.accuracy = accuracy
        self.warhead_weight = warhead_weight
        self.chamber_position = chamber_position
        self.status = "unloaded"

    def load(self):
        self.status = "loaded"

    def launch(self):
        if self.status == "loaded":
            self.status = "launched"
            return "[!] Missile launched 🚀"
        return "[!] Missile not loaded"
