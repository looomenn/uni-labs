"""
Course: SE
Lab: 04
"""

import time

from EventLog import (
    EventLog,
    DiagnosticSystem
)

from Missle import Missile
from Operator import Operator

from FireControl import (
    FireControlSystem,
    Launcher
)

from Vehicle import (
    Vehicle,
    PowerSystem,
    FuelSystem,
    HydraulicSystem,
    NavigationSystem,
    SafetySystem
)


class ControlPanel:
    def __init__(self, event_log):
        self.hydraulic_system = HydraulicSystem(5000, 10, 200)
        self.fire_control_system = FireControlSystem(5, 50)
        self.launcher = Launcher(20)
        self.fuel_system = FuelSystem(500, "Diesel", 30)
        self.power_system = PowerSystem(100, 200, 4)
        self.navigation_system = NavigationSystem(5000, 5, "AES")
        self.diagnostic_system = DiagnosticSystem(50, 60, 10)
        self.safety_system = SafetySystem(2, 10, ["Armor", "Jamming"], 2)
        self.vehicle = Vehicle(20, "Hydraulic", ["All-Terrain"], "3 G", "8x8")
        self.missiles = []
        self.event_log = event_log
        self.system_active = False
        self.autofire_lever = False
        self.autofire_count = 0
        self.autofire_count_set = False
        self.error = False

    def initiate_preparation(self):
        print('\nPreparation started....')
        if not self.missiles:
            self.event_log.add_event("[PrepSystem] No missiles in chamber. preparation aborted ")
            self.error = True
            return "[!] There is no missiles to lunch! Preparation aborted!"

        if self.system_active:
            self.event_log.add_event("[PrepSystem] Attempt to prepare system while already active.")
            return "[!] System is already active. Preparation not needed."

        self.fire_control_system.prepare_fire()

        for missile in self.missiles:
            self.launcher.load_missile(missile)

        self.event_log.add_event("[PrepSystem] System prepared for firing.")
        self.system_active = True
        return self.event_log.get_prefix("Preparation completed\n", 'success')

    def set_autofire_count(self, count):
        missiles_loaded = self.launcher.loaded_missiles
        if count > missiles_loaded:
            self.event_log.add_event(f"[AutoFire] Tried to set autofire count {count} when {missiles_loaded} loaded")
            return self.event_log.get_prefix("Not enough missiles loaded", 'error')

        self.autofire_count_set = True
        self.autofire_count = count
        self.event_log.add_event("[AutoFire] Set {count} to fire with autofire")
        return self.event_log.get_prefix(f"Set {count} to autofire", 'success')

    def start_fire(self):
        if self.error:
            self.event_log.add_event("[Launcher] Error already occurred. Starting fire aborted!")
            return "[!] Start fire aborted"

        if not self.system_active:
            self.event_log.add_event("[Launcher] Attempt to fire without preparation.")
            return "[!] System is not active. Prepare the system first."

        if self.autofire_lever:
            return self.autofire()

        self.fire_control_system.remove_safety()
        self.fire_control_system.set_fire_position()

        launch_status = self.launcher.launch_missile()

        if self.launcher.loaded_missiles == 0:
            self.event_log.add_event("[Launcher] All missiles launched.")
            self.system_active = False
            return f"{launch_status}, Missiles left: 0"

        self.event_log.add_event(f"[Launcher] Missile fired, missiles left: {self.launcher.loaded_missiles}")
        return f"{launch_status}, Missiles left: {self.launcher.loaded_missiles}"

    def autofire(self):

        if not self.autofire_count_set:
            return self.event_log.get_prefix("Set amount of missiles to lunch!", 'error')

        count = self.autofire_count

        self.fire_control_system.remove_safety()
        self.fire_control_system.set_fire_position()

        for _ in range(count):
            launch_status = self.launcher.launch_missile()
            self.event_log.add_event(f"Missile fired: {launch_status}")
            time.sleep(self.fire_control_system.delay / 1000)

        if self.launcher.loaded_missiles == 0:
            self.event_log.add_event("[Launcher] All missiles launched.")
            self.system_active = False

        self.fire_control_system.reset_fire_position()
        return self.event_log.get_prefix("Autofired {count} missiles", 'success')

    def cease_fire(self):
        if not self.system_active:
            self.event_log.add_event("Attempt to cease fire when system is not active.")
            return "[!] System is not active. No fire to cease."

        self.fire_control_system.reset_fire_position()
        cease_status = self.fire_control_system.cease_fire()

        self.system_active = False
        self.event_log.add_event("Firing ceased.")
        return cease_status

    def system_status(self):
        fuel_status = self.fuel_system.check_fuel()
        power_status = self.power_system.check_power()
        status_report = {
            "fuel_status": fuel_status,
            "power_status": power_status
        }
        self.event_log.add_event("System status checked.")
        return status_report

    def move_vehicle(self, distance):
        if not self.hydraulic_system.stabilized:
            self.fuel_system.fuel_consumption(distance)
            move_report = f"Vehicle moved {distance} km"
            self.event_log.add_event(move_report)
            return move_report

        self.event_log.add_event("Cannot move, stabilizers are deployed.")
        return "Cannot move, stabilizers are deployed"

    def release_stabilizers(self):

        if not self.hydraulic_system.stabilized:
            self.event_log.add_event("[Stabilization] Attempt to release stabilizers when system is "
                                     "not stabilised yet")
            return '[!] No active stabilizers to release'

        self.hydraulic_system.release_stabilizers()
        self.event_log.add_event("Stabilizers released.")
        return self.event_log.get_prefix("[HydraulicSystem] Stabilizers released", 'success')

    def activate_stabilizers(self):
        if self.hydraulic_system.stabilized:
            self.event_log.add_event("[Stabilization] Attempt to already activated stabilizers")
            return '[!] Stabilizers already activated'

        self.hydraulic_system.stabilize()
        self.event_log.add_event("[HydraulicSystem] Stabilizer activated")
        return self.event_log.get_prefix("[HydraulicSystem] Stabilizers activated", 'success')

    def start_engine(self):
        if self.vehicle.engine_running:
            self.event_log.add_event("Attempt to start engine when already running")
            return "Engine is already running"
        engine_status = self.vehicle.start_engine()
        self.event_log.add_event(engine_status)
        return self.event_log.get_prefix(engine_status, 'success')

    def stop_engine(self):
        if not self.vehicle.engine_running:
            self.event_log.add_event("[Vehicle] Attempt to stop engine when already stopped.")
            return self.event_log.get_prefix("Engine is not running", 'error')
        engine_status = self.vehicle.stop_engine()
        self.event_log.add_event(engine_status)
        return engine_status

    def load_missile(self, missile):
        load_status = self.launcher.load_missile(missile)
        self.event_log.add_event(load_status)
        return self.event_log.get_prefix("Missiles loaded", 'success')


class FireControlUnit:
    def __init__(self, commander):
        self.commander = commander
        self.operators = []
        self.event_log = EventLog()
        self.control_panel = ControlPanel(self.event_log)

    def add_operator(self, operator):
        if len(self.operators) < 4:
            self.operators.append(operator)
            self.event_log.add_event(f"[FireControlUnit] Operator added: {operator}")
        else:
            self.event_log.add_event("Attempt to add more than 4 operators.")
            return "Cannot add more than 4 operators."

    def execute_fire_mission(self):
        print(self.control_panel.start_engine())
        print(self.control_panel.activate_stabilizers())
        print(self.control_panel.initiate_preparation())
        print(self.control_panel.start_fire())
        print(self.control_panel.cease_fire())
        print(self.control_panel.release_stabilizers())
        print(self.control_panel.move_vehicle(5))
        print(self.control_panel.stop_engine())

    def refuel_vehicle(self, amount):
        refuel_status = self.control_panel.fuel_system.refuel(amount)
        self.event_log.add_event(f"Vehicle refueled: {refuel_status} litres")
        print(f"Refueled: {refuel_status} litres")

    def check_systems(self):
        diagnostics = self.control_panel.diagnostic_system.run_diagnostics()
        safety = self.control_panel.safety_system.monitor_surroundings()
        status = self.control_panel.system_status()
        print("Diagnostics:", diagnostics)
        print("Safety Status:", safety)
        print("System Status:", status)

    def print_event_log (self):
        log = self.event_log.get_log()
        for event in log:
            print(event)


def main():
    # ініціалізація операторів
    commander = Operator(name="John Doe", age=40, position="Commander", rank="Captain")
    operator1 = Operator(name="Jane Smith", age=30, position="Operator", rank="Lieutenant")
    operator2 = Operator(name="Robert Brown", age=28, position="Operator", rank="Sergeant")
    operator3 = Operator(name="Emily Davis", age=35, position="Operator", rank="Lieutenant")
    operator4 = Operator(name="Michael Wilson", age=32, position="Operator", rank="Sergeant")

    # створення команди розрахунку
    fire_control_unit = FireControlUnit(commander)

    # додавання операторів до команди
    fire_control_unit.add_operator(operator1)
    fire_control_unit.add_operator(operator2)
    fire_control_unit.add_operator(operator3)
    fire_control_unit.add_operator(operator4)

    # завантаження ракет
    fire_control_unit.control_panel.load_missile(Missile("9М221Ф «Тайфун-1»",
                                                         "HEI",
                                                         40, 500, 122,
                                                         200, 18, 1))
    fire_control_unit.control_panel.missiles.append(Missile("9М221Ф «Тайфун-1»",
                                                            "HEI",
                                                            40, 500, 122,
                                                            200, 18, 2))

    # виконання місії
    fire_control_unit.execute_fire_mission()

    # заправка транспортного засобу
    fire_control_unit.refuel_vehicle(100)

    # перевірка систем
    fire_control_unit.check_systems()

    # подивитися лог
    fire_control_unit.print_event_log()


if __name__ == "__main__":
    main()
