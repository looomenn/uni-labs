"""
Event logging module
"""
import datetime

NOW = datetime.datetime.now()
PREF = {
    'error': '[Error]',
    'success': '[Success]',
    'warn': '[Warning]',
}


class EventLog:
    def __init__(self):
        self.log = []

    def add_event(self, event):
        self.log.append(f'[Logger] - {NOW} - {event}')

    def get_prefix(self, event, status):
        return f'{PREF[status]} {event}'

    def get_log(self):
        return self.log


class DiagnosticSystem:
    def __init__(self, param_count, update_frequency, power_consumption):
        self.status = "All systems operational"
        self.param_count = param_count
        self.update_frequency = update_frequency
        self.power_consumption = power_consumption

    def run_diagnostics(self):
        return self.status
