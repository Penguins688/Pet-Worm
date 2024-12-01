class Neuron:
    def __init__(self, neuron_id, threshold):
        self.id = neuron_id
        self.activation_threshold = threshold
        self.current_signal = 0.0

    def is_activated(self):
        return self.current_signal >= self.activation_threshold

    def receive_input(self, signal):
        self.current_signal += signal

    def reset_signal(self):
        self.current_signal = 0.0