import numpy as np

class callCenter():#writing a call center simulation class
    #set random seed
    np.random.seed(0)
    def __init__(self):
        self.maximum_slots = 5
        self.arrival_queue = [] #a queue before others have decided to go to car or other. 
        self.car_stereo_representative_queue = []
        self.others_representative_queue = []
        self.server_state = 0 #0 = idle, 1 = busy
        self.current_time = 0
        # print("Call Center Simulation")
    def arrival (self,customer):
        if self.current_time > 960: #if time is greater than 960, then call center is closed: 16 hours * 60 minutes
            print("Call Center Closed")
            return
        print("Arrival")
        
        if customer < 0.5: #if random number is less than 0.5, then add to car stereo queue
            if len(self.car_stereo_representative_queue) > self.maximum_slots: #if there are no available spots for car stereo
                if self.arrival_queue > self.maximum_slots:
                    print("No available slots")
                    return 
                self.arrival_queue.append(customer)
            #there are availble spots for car stereo 
            print("Add to Car Stereo Queue")
            self.car_stereo_representative_queue.append(customer)
        #if random number is greater than 0.5, then add to others queue
        else:
            if len(self.others_representative_queue) > self.maximum_slots: #if there are no available spots for others
                if self.arrival_queue > self.maximum_slots:
                    print("No available slots")
                    return 
                self.arrival_queue.append(customer)
            print("Add to Others Queue")
            self.others_representative_queue.append(customer)

    def available_signal_checking(self, queue):
        if len(queue) > self.maximum_slots:
            return 0 #0 = no signal
        else:
            return 1 #1 = signal
    
    def run(self,customer):
        self.server_state = 1
        while self.server_state == 1:
            # self.corrent_time += 1
            # print("Time: ", self.time)

            if self.available_signal_checking(self.arrival_queue):
                self.arrival(customer)
            # print(self.car_stereo_representative_queue)

            # self.service()
            # self.departure()
            # print("Car Stereo Queue: ", self.car_stereo_representative_queue)
            # print("Others Queue: ", self.others_representative_queue)
            # print("Server State: ", self.server_state)
            # print("Time: ", self.time)
    


def __main__():
    #implement the simulation clock and the advance of the simulation clock, as well as an event calendar (event list) which is a list of events as they are scheduled. In every simulation, there is only one calendar and it is ordered by the earliest scheduled-time first.
    #generate 100 customers
    customer_list = np.random.uniform(0,1,5)
    print(customer_list)
    test = callCenter()
    test.run(customer_list[4])

if __name__ == "__main__":
    __main__()
