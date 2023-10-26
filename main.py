import numpy as np
import random
import pandas as pd
# Simulate two dice being rolled and their resulting rolls being summed
def DICE():
    x1 = random.randint(1,6)
    x2 = random.randint(1,6)
    return x1 + x2
def generate_event_type():
    if DICE() <= 4:
        return "car_stereo"
    else:
        return "others"
# Delay at IVR unit
def delay(minutes):
    # Simulate delay for given number of minutes
    pass

def generate_statistic(event:pd.DataFrame) -> float:
    #=========Mean===========
    average_waiting_time = sum(event['arrival'])/len(event)
    total_waiting_time = sum(event['waiting_time']) # or sum(event['departure_time'] - event['arrival'] - event['service_time'])
    average_waiting_time = total_waiting_time/len(event)
    #=========Variance===========
    variance_waiting_time = sum((event['waiting_time'] - average_waiting_time)**2)/len(event)
    #=========Standard Deviation===========
    standard_deviation_waiting_time = variance_waiting_time**(1/2)
    #=========Confidence Interval===========
    # 95% confidence interval
    confidence_interval_waiting_time = [average_waiting_time - 1.96*(standard_deviation_waiting_time/(len(event)**(1/2))),average_waiting_time + 1.96*(standard_deviation_waiting_time/(len(event)**(1/2)))]
    # for i in range(len(event)):
    #     event.iloc[i]['waiting_time'] = event.iloc[i]['departure_time'] - event.iloc[i]['arrival'] - event.iloc[i]['service_time']
    return average_waiting_time, variance_waiting_time, standard_deviation_waiting_time, confidence_interval_waiting_time
# Class specifics:
# - time is measured in minutes
# - customers refer to callers

# Random variables:
#1. Time between arrivals of calls at the center = (DICE * 0.333) minutes.
#2. The delay at the IVR unit = (DICE * 0.3) minutes.
#3. The delay for car-stereo call processing = (DICE * 2) minutes.
#4. The delay for other-product call processing= (DICE) minutes. 

# Main class
## To do:
## Timing and calendar
class event_calendar():
    def schedule_event(self,event_time,event_type):
        self.event_calendar.append([event_time,event_type])
        self.event_calendar = sorted(self.event_calendar, key=lambda x: x[0])
    
    def next_event(self):
        event_time,event_type = self.event_calendar.pop(0)
        self.current_time = event_time

        if event_type == "arrival":
            customer = random.randint(1,12)
            self.arrival(customer)
        elif event_type == "departure":
            # self.departure()
            pass
## delay(), service() and removing customers from queue
class callCenter():# a call center simulation class
    #set random seed
    np.random.seed(0)
    def __init__(self):
        self.maximum_slots = 5 # maximum queue length for call arrivals to splitter
        self.arrival_queue = [] #a queue before others have decided to go to car or other.
        self.car_stereo_representative_queue = []
        self.others_representative_queue = []
        self.server_state = 0 #0 = idle, 1 = busy
        self.current_time = 0
        self.event_calendar = []
        self.customer_df = pd.DataFrame(columns = ['customer_id','event_time','service_time','event_type','product_type','departure_time','waiting_time'])
        # print("Call Center Simulation")
        
    # Input: customer - a random number generated representing if a customer is calling for car stereo or others
    # Assumption: Because the run function already handles the arrival queue busy signaling, we do not need to here
    def arrival (self,customer:int): #customer id 
        # 11am to 4pm - 5 hours of peak time
        if self.current_time > 300: #if time is greater than 5*60 = 300 minutes, then call center is closed
            print("Call Center Closed")
            return
        
        print("Arrival")
        #adding product type to customer
        # print(f'arrival {customer}')
        # print(f'{self.customer_df}')
        self.customer_df.loc[self.customer_df['customer_id']== customer, 'product_type'] = generate_event_type()
        current_customer = self.customer_df.loc[self.customer_df['customer_id']== customer]
        print(current_customer["product_type"])
        print(f'{self.customer_df}')  

        if current_customer['product_type'].iloc[0] == 'car_stereo': #if random DICE number is <= 4, then add to car-stereo queue
            if len(self.car_stereo_representative_queue) > self.maximum_slots: #if there are no available spots for car stereo
                if len(self.arrival_queue) > self.maximum_slots:
                    print("No available slots")
                    return
                self.arrival_queue.append(current_customer)
                
                # Delay for car-stereo call processing
                delay(DICE() * 2)
                
            #there are availble spots for car stereo
            print("Add to Car Stereo Queue")
            self.car_stereo_representative_queue.append(current_customer)
        #if random number is greater than 4, then add to others queue
        else:
            if len(self.others_representative_queue) > self.maximum_slots: #if there are no available spots for others
                if len(self.arrival_queue) > self.maximum_slots:
                    print("No available slots")
                    return 
                self.arrival_queue.append(current_customer)
                
                # Delay for other-product call processing
                delay(DICE())
            print("Add to Others Queue")
            self.others_representative_queue.append(current_customer)

    def available_signal_checking(self, queue)-> bool:
        if len(queue) > self.maximum_slots:
            return 0 #0 = no signal
        else:
            return 1 #1 = signal
 
    def run(self,event_calendar:pd.DataFrame) -> None: 
        self.server_state = 1   

        while self.server_state == 1:
            # self.current_time += 1
            # print("Time: ", self.time)
    
            if self.available_signal_checking(self.arrival_queue):
                for i in range(len(event_calendar)):
                    if event_calendar.iloc[i]['event_type'] == "arrival":
                        customer_id = event_calendar.iloc[i]['customer_id']
                        self.customer_df = self.customer_df.append(event_calendar.iloc[i])
                        # event_calendar = event_calendar.drop(i)
                        self.arrival(customer_id)
                        # print(event_calendar.iloc[i])
            # self.service()
            # self.departure()
            # print("Car Stereo Queue: ", self.car_stereo_representative_queue)
            # print("Others Queue: ", self.others_representative_queue)
            # print("Server State: ", self.server_state)
            # print("Time: ", self.time)
            else:
                print("No available slots")          

    


def __main__():
    #implement the simulation clock and the advance of the simulation clock, as well as an event calendar (event list) which is a list of events as they are scheduled. In every simulation, there is only one calendar and it is ordered by the earliest scheduled-time first.

    # creating event calendar list
    event_calendar_list = pd.DataFrame(columns = ['customer_id','event_time','service_time','event_type'])
    event_calendar_list['customer_id'] = np.random.randint(1,6,5)
    event_calendar_list['event_time'] = np.random.randint(0,300,5)
    event_calendar_list['service_time'] = np.random.randint(0,300,5)
    event_calendar_list['event_type'] = np.random.choice(["arrival"],5)
    
    event_calendar_list = event_calendar_list.sort_values(by=['event_time'])

    # for col in event_calendar_list.columns:
    #     print(event_calendar_list[col])
    # print(event_calendar_list.iloc[0])
    #initialize call center simulation
    test = callCenter()
    #run simulation
    test.run(event_calendar_list)
    
if __name__ == "__main__":
    __main__()
