import numpy as np

class callCenter():#writing a call center simulation class
    #set random seed
    np.random.seed(0)
    def __init__(self):
        self.car_stereo_representative_queue = []
        self.others_representative_queue = []
        self.server_state = [0,1]
        self.time = 0
        # print("Call Center Simulation")
    def run(self):
        while self.time < 100:
            self.time += 1
            # print("Time: ", self.time)
            self.arrival()
            self.service()
            self.departure()
            # print("Car Stereo Queue: ", self.car_stereo_representative_queue)
            # print("Others Queue: ", self.others_representative_queue)
            # print("Server State: ", self.server_state)
            # print("Time: ", self.time)


def __main__():
    test = callCenter()

if __name__ == "__main__":
    __main__()
