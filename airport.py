import heapq
from collections import deque
import time


# Passenger class encapsulates the data for each passenger.
class Passenger:
    def __init__(self, name, priority, is_late=False, is_frequent_flyer=False):
        self.name = name
        # Frequent flyers get a priority boost
        self.priority = priority + (1 if is_frequent_flyer else 0)
        self.is_late = is_late


    def __lt__(self, other):
        # Late passengers take priority; then frequent flyers; then regular passengers by priority level.
        if self.is_late != other.is_late:
            return self.is_late > other.is_late
        return self.priority > other.priority


    def __repr__(self):
        return f"Passenger({self.name}, Priority: {self.priority}, Late: {self.is_late})"


# Process class manages the queuing and processing of passengers at each stage (check-in, security, boarding).
class Process:
    def __init__(self, name, available_resources):
        self.name = name
        self.queue = deque()
        self.available_resources = available_resources


    def add_passenger(self, passenger):
        self.queue.append(passenger)
        print(f"{passenger.name} added to {self.name} queue.")


    def process(self):
        # Process passengers using available resources
        while self.available_resources > 0 and self.queue:
            passenger = self.queue.popleft()
            print(f"{passenger.name} is being processed at {self.name}.")
            self.available_resources -= 1
            time.sleep(1)  # Simulate processing time
            self.available_resources += 1
            print(f"{passenger.name} finished {self.name}.")


    def is_queue_empty(self):
        return not self.queue


# Scheduler class manages the overall scheduling for check-in, security, and boarding stages.
class AirportScheduler:
    def __init__(self, check_in_resources, security_resources, boarding_resources):
        self.check_in_process = Process("Check-in", check_in_resources)
        self.security_process = Process("Security", security_resources)
        self.boarding_process = Process("Boarding", boarding_resources)
        self.check_in_queue = [ ]  # Priority Queue for Check-in


    def add_passenger_to_check_in(self, passenger):
        heapq.heappush(self.check_in_queue, passenger)
        print(f"{passenger.name} added to priority-based check-in queue with priority {passenger.priority}.")


    def process_check_in(self):
        same_priority_queue = deque()  # For round-robin scheduling
        while self.check_in_process.available_resources > 0 and self.check_in_queue:
            passenger = heapq.heappop(self.check_in_queue)
           
            # If the queue contains passengers with equal priority, use round-robin.
            if same_priority_queue and passenger.priority ==same_priority_queue[0].priority:
                same_priority_queue.append(passenger)
                passenger = same_priority_queue.popleft()  # Round-robin among equal priorities
           
            print(f"Processing {passenger.name} at check-in.")
            self.check_in_process.add_passenger(passenger)
            self.check_in_process.process()  # Process passenger at check-in
            self.security_process.add_passenger(passenger)  # Move passenger to security


    def process_security(self):
        self.security_process.process()  # Process passengers at security
        # After security, move passengers to boarding queue
        while not self.security_process.is_queue_empty():
            passenger = self.security_process.queue.popleft()
            self.boarding_process.add_passenger(passenger)


    def process_boarding(self):
        self.boarding_process.process()  # Process passengers at boarding gate


    def run_scheduler(self):
        # Continuously process all stages in a loop
        while self.check_in_queue or not self.security_process.is_queue_empty() or not self.boarding_process.is_queue_empty():
            print("\nStarting check-in process...")
            self.process_check_in()


            print("\nStarting security process...")
            self.process_security()


            print("\nStarting boarding process...")
            self.process_boarding()


            print("\nAll passengers processed for this cycle. Waiting for the next cycle...\n")
            time.sleep(3)  # Pause before next cycle


# Function to get user input for passenger details
def get_passenger_details():
    num_passengers = int(input("Enter the number of passengers: "))
    passengers = [ ]
   
    for i in range(num_passengers):
        print(f"\nEnter details for Passenger {i + 1}:")
        name = input("Name: ")
        priority = int(input("Priority (1-5, where 5 is highest): "))
        is_late_input = input("Is the passenger late? (yes/no): ").strip().lower()
        is_late = True if is_late_input == 'yes' else False
        is_frequent_flyer_input = input("Is the passenger a frequent flyer? (yes/no): ").strip().lower()
        is_frequent_flyer = True if is_frequent_flyer_input == 'yes' else False


        passenger = Passenger(name, priority, is_late, is_frequent_flyer)
        passengers.append(passenger)


    return passengers


# Example usage with user input
def main():
    print("Welcome to the Airport Scheduler System!")


    # Input for number of available resources
    check_in_resources = int(input("\nEnter the number of check-in counters: "))
    security_resources = int(input("Enter the number of security lanes: "))
    boarding_resources = int(input("Enter the number of boarding gates: "))


    scheduler = AirportScheduler(check_in_resources, security_resources, boarding_resources)


    # Get passenger details
    passengers = get_passenger_details()


    # Add passengers to the scheduler's check-in queue
    for passenger in passengers:
        scheduler.add_passenger_to_check_in(passenger)


    # Run the airport scheduler
    scheduler.run_scheduler()


if __name__ == "__main__":
    main()
