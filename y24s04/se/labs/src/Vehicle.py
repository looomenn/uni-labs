"""
Vehicle class for MLRS
"""


class Vehicle:
    def __init__(self, max_load, suspension_type, terrain_capability, overload_protection, chassis_format):
        self.engine_running = False
        self.max_load = max_load
        self.suspension_type = suspension_type
        self.terrain_capability = terrain_capability
        self.overload_protection = overload_protection
        self.chassis_format = chassis_format

    def start_engine(self):
        self.engine_running = True
        return "Engine started"

    def stop_engine(self):
        self.engine_running = False
        return "Engine stopped"



class PowerSystem:
    def __init__(self, generator_power, battery_capacity, battery_count):
        self.generator_power = generator_power
        self.battery_capacity = battery_capacity
        self.battery_count = battery_count
        self.generator_status = "operational"
        self.battery_status = "fully charged"

    def check_power(self):
        return {
            "generator_status": self.generator_status,
            "battery_status": self.battery_status
        }


class FuelSystem:
    def __init__(self, capacity, fuel_type, consumption):
        self.capacity = capacity
        self.fuel_type = fuel_type
        self.current_level = capacity
        self.consumption = consumption

    def check_fuel(self):
        return self.current_level

    def refuel(self, amount):
        self.current_level = min(self.capacity, self.current_level + amount)
        return self.current_level

    def fuel_consumption(self, distance):
        self.current_level -= distance * (self.consumption / 100)


class HydraulicSystem:
    def __init__(self, max_load, lift_time, pressure):
        self.stabilized = False
        self.max_load = max_load
        self.lift_time = lift_time
        self.pressure = pressure

    def stabilize(self):
        self.stabilized = True

    def release_stabilizers(self):
        self.stabilized = False


class NavigationSystem:
    def __init__(self, radius, update_interval, encryption):
        self.current_location = (0, 0)
        self.radius = radius
        self.update_interval = update_interval
        self.encryption = encryption

    def set_location(self, latitude, longitude):
        self.current_location = (latitude, longitude)

    def get_location(self):
        return self.current_location


class SafetySystem:
    def __init__(self, activation_time, threat_count, protection_types, duck_count):
        self.monitoring_status = "No threats detected"
        self.activation_time = activation_time
        self.threat_count = threat_count
        self.protection_types = protection_types
        self.duck_count = duck_count

    def monitor_surroundings(self):
        return self.monitoring_status
