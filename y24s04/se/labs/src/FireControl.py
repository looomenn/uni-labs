"""
Fire control systems
"""


class FireControlSystem:
    def __init__(self, launch_rate, delay):
        self.ready = False
        self.firing = False
        self.safety_on = True
        self.lever_in_fire_position = False
        self.launch_rate = launch_rate
        self.delay = delay
        self.status = "idle"

    def prepare_fire(self):
        self.ready = True

    def fire(self):
        if self.ready and not self.safety_on and self.lever_in_fire_position:
            self.firing = True
            self.status = "firing"
            return "Missile launched"
        return "Cannot fire"

    def cease_fire(self):
        self.firing = False
        self.ready = False
        self.safety_on = True
        self.lever_in_fire_position = False
        self.status = "idle"
        return "[!] Fire ceased\n"

    def remove_safety(self):
        self.safety_on = False

    def set_fire_position(self):
        self.lever_in_fire_position = True

    def reset_fire_position(self):
        self.lever_in_fire_position = False


class Launcher:
    def __init__(self, max_missiles):
        self.missiles = []
        self.loaded_missiles = 0
        self.max_missiles = max_missiles

    def load_missile(self, missile):
        if self.loaded_missiles < self.max_missiles:
            if missile.status == "unloaded":
                missile.load()
                self.missiles.append(missile)
                self.loaded_missiles += 1
                return f"[Launcher] Missile loaded: id: {missile.missile_id}, slot: {missile.chamber_position}"
            return "[!] Missile already loaded"
        return "[!] Launcher is full"

    def launch_missile(self):
        if self.loaded_missiles > 0:
            missile = self.missiles.pop(0)
            self.loaded_missiles -= 1
            return missile.launch()
        return "No missiles loaded"
