import json
from src.brain.Connection import Connection
from src.brain.Input import Input
from src.brain.Neuron import Neuron
from src.brain.Output import Output
from src.simulation.Wall import Wall

class Simulation:
    global walls
    walls = []

    def __init__(self, json_file):
        self.load_brain(json_file)
        self.load_walls("data/wall_config.json")

    def load_brain(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)

        self.inputs = [
            Input(input_data["type"], input_data["id"], input_data["weight"], input_data["active"])
            for input_data in data["inputs"]
        ]

        self.neurons = [
            Neuron(neuron_data["id"], neuron_data["threshold"])
            for neuron_data in data["neurons"]
        ]

        self.outputs = [
            Output(output_data["type"], output_data["strength"], output_data["id"])
            for output_data in data["outputs"]
        ]

        self.input_to_neuron_connections = [
            Connection(conn_data["from_id"], conn_data["to_id"], conn_data["weight"])
            for conn_data in data["connections"]["input_to_neuron"]
        ]

        self.neuron_to_output_connections = [
            Connection(conn_data["from_id"], conn_data["to_id"], conn_data["weight"])
            for conn_data in data["connections"]["neuron_to_output"]
        ]
    
    def load_walls(self, json_file):
        with open(json_file, 'r') as file:
            wall_data = json.load(file)
            for data in wall_data:
                walls.append(Wall(data['x'], data['y'], data['width'], data['height']))

    def update_positions(self):
        for neuron in self.neurons:
            neuron.reset_signal()
        for output in self.outputs:
            output.reset_weight()

        for input_data in self.inputs:
            if input_data.active:
                for conn in self.input_to_neuron_connections:
                    if conn.from_id == input_data.id:
                        self.neurons[conn.to_id - 1].receive_input(input_data.weight * conn.weight)

        for neuron in self.neurons:
            if neuron.is_activated():
                for conn in self.neuron_to_output_connections:
                    if conn.from_id == neuron.id:
                        output = self.outputs[conn.to_id - 1]
                        signal = neuron.current_signal * conn.weight
                        output.update_weight(signal)

        for input_data in self.inputs:
            input_data.active = False

    def draw(self, screen, worm_x, worm_y, treats):
        highest_weight = max(output.current_weight for output in self.outputs)
        
        for output in self.outputs:
            worm_position = output.display(screen, worm_x, worm_y, treats, highest_weight)
            worm_x = worm_position[0]
            worm_y = worm_position[1]
        
        for wall in walls:
            Wall.draw(wall, screen)

        return worm_position

    def handle_user_input(self, input_types):
        if not isinstance(input_types, list):
            input_types = [input_types]

        for input_type in input_types:
            for input_data in self.inputs:
                if input_data.type == input_type:
                    input_data.active = True
                    print(f"Input activated: {input_type}")
    
    def get_walls(self):
        return walls
