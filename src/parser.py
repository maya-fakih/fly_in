from typing import Dict

class GraphParser():
    def __init__(self, config: str):
        self.config_file = config
        self.configs = Dict

    def load_file(self):
        first_line = True
        configs = Dict
        try:
            with open(self.config_file, "r") as config_file:
                
                for line in config_file:
                    if line.startswith('#'):
                        continue
                    if first_line:
                        # call check 1st line
                        pass

        except Exception as e:
            print(f"[Parsing]: {e}")

    def check_first_line(self, line):
        try:
            line.split(":")
        except:
            pass