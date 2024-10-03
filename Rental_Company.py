from datetime import date

# Helper function to parse dates
def parse_date(date_str):
    try:
        return date(*map(int, date_str.split('-')))
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return None

# Custom exception classes
class RentalError(Exception):
    pass

class VehicleNotAvailableError(RentalError):
    def __init__(self, message="Vehicle is not available for the selected dates"):
        self.message = message
        super().__init__(self.message)

class VehicleNotFoundError(RentalError):
    def __init__(self, message="Vehicle not found in the system"):
        self.message = message
        super().__init__(self.message)

class Vehicle:
    def __init__(self, vehicle_id, make, model, year, rental_price_per_day):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.rental_price_per_day = rental_price_per_day
        self.is_available = True
        self.current_rentals = []

    def check_availability(self, start_date, end_date):
        for rental in self.current_rentals:
            if not (end_date < rental.start_date or start_date > rental.end_date):
                return False
        return True

    def assign_rental(self, rental):
        self.current_rentals.append(rental)
        self.is_available = False

    def release_rental(self, rental_id):
        self.current_rentals = [r for r in self.current_rentals if r.rental_id != rental_id]
        self.is_available = True

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - ${self.rental_price_per_day}/day"

class Car(Vehicle):
    def __init__(self, vehicle_id, make, model, year, rental_price_per_day, number_of_doors, seating_capacity, transmission_type):
        super().__init__(vehicle_id, make, model, year, rental_price_per_day)
        self.number_of_doors = number_of_doors
        self.seating_capacity = seating_capacity
        self.transmission_type = transmission_type

    def __str__(self):
        return f"Car: {super().__str__()} | {self.seating_capacity}-seater | {self.transmission_type} Transmission"

class Bike(Vehicle):
    def __init__(self, vehicle_id, make, model, year, rental_price_per_day, bike_type, has_gear):
        super().__init__(vehicle_id, make, model, year, rental_price_per_day)
        self.bike_type = bike_type
        self.has_gear = has_gear

    def __str__(self):
        return f"Bike: {super().__str__()} | Type: {self.bike_type} | Gear: {'Yes' if self.has_gear else 'No'}"

class Truck(Vehicle):
    def __init__(self, vehicle_id, make, model, year, rental_price_per_day, max_load_capacity, number_of_axles):
        super().__init__(vehicle_id, make, model, year, rental_price_per_day)
        self.max_load_capacity = max_load_capacity
        self.number_of_axles = number_of_axles

    def __str__(self):
        return f"Truck: {super().__str__()} | Capacity: {self.max_load_capacity} tons | Axles: {self.number_of_axles}"

class Customer:
    def __init__(self, customer_id, name, driver_license_number):
        self.customer_id = customer_id
        self.name = name
        self.driver_license_number = driver_license_number
        self.rentals = []

    def make_reservation(self, rental):
        self.rentals.append(rental)

    def return_vehicle(self, rental_id):
        self.rentals = [r for r in self.rentals if r.rental_id != rental_id]

    def get_rentals(self):
        return self.rentals

    def __str__(self):
        return f"Customer: {self.name} | ID: {self.customer_id}"

class Rental:
    def __init__(self, rental_id, customer_id, vehicle_id, start_date, end_date):
        self.rental_id = rental_id
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = "Reserved"
        self.total_price = 0

    def update_status(self, new_status):
        self.status = new_status

    def calculate_total_price(self, rental_price_per_day):
        rental_days = (self.end_date - self.start_date).days + 1
        self.total_price = rental_days * rental_price_per_day

    def __str__(self):
        return f"Rental {self.rental_id}: Vehicle {self.vehicle_id} | Customer {self.customer_id} | Price: ${self.total_price:.2f} | Status: {self.status}"

class RentalCompany:
    def __init__(self):
        self.vehicles = {}
        self.customers = {}
        self.rentals = {}
        self.rental_counter = 1

    def add_customer(self, customer):
        self.customers[customer.customer_id] = customer
        print(f"Customer {customer.name} added to system.")

    def add_vehicle(self, vehicle):
        self.vehicles[vehicle.vehicle_id] = vehicle
        print(f"Vehicle {vehicle.make} {vehicle.model} added to system.")

    def find_available_vehicles(self, vehicle_type, start_date, end_date):
        available_vehicles = [v for v in self.vehicles.values() if isinstance(v, vehicle_type) and v.check_availability(start_date, end_date)]
        if available_vehicles:
            print("Available Vehicles:")
            for vehicle in available_vehicles:
                print(vehicle)
        else:
            print("No vehicles available for the selected dates.")

    def create_rental(self, customer_id, vehicle_id, start_date, end_date):
        customer = self.customers.get(customer_id)
        vehicle = self.vehicles.get(vehicle_id)

        if not vehicle:
            raise VehicleNotFoundError()

        if not vehicle.check_availability(start_date, end_date):
            raise VehicleNotAvailableError()

        rental_id = f"R{self.rental_counter:03}"
        rental = Rental(rental_id, customer_id, vehicle_id, start_date, end_date)
        rental.calculate_total_price(vehicle.rental_price_per_day)

        vehicle.assign_rental(rental)
        customer.make_reservation(rental)
        self.rentals[rental_id] = rental
        self.rental_counter += 1

        print(f"Rental {rental_id} created for customer {customer.name}.")
        return rental

    def return_vehicle(self, rental_id):
        rental = self.rentals.get(rental_id)
        if rental:
            vehicle = self.vehicles[rental.vehicle_id]
            vehicle.release_rental(rental_id)
            rental.update_status("Completed")
            print(f"Vehicle {rental.vehicle_id} returned and rental {rental_id} completed.")
        else:
            print(f"Rental {rental_id} not found.")

    def list_rentals(self):
        for rental in self.rentals.values():
            print(rental)

    def list_customers(self):
        for customer in self.customers.values():
            print(customer)

    def list_vehicles(self):
        for vehicle in self.vehicles.values():
            print(vehicle)

# Menu-based interaction
def main_menu():
    rental_company = RentalCompany()

    while True:
        print("\n--- Vehicle Rental System ---")
        print("1. Add a Customer")
        print("2. Add a Vehicle")
        print("3. Find Available Vehicles")
        print("4. Create Rental")
        print("5. Return Vehicle")
        print("6. View All Rentals")
        print("7. View All Customers")
        print("8. View All Vehicles")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            customer_id = input("Enter Customer ID: ")
            name = input("Enter Customer Name: ")
            driver_license = input("Enter Driver License Number: ")
            customer = Customer(customer_id, name, driver_license)
            rental_company.add_customer(customer)

        elif choice == '2':
            vehicle_type = input("Enter Vehicle Type (Car, Bike, Truck): ").lower()
            vehicle_id = input("Enter Vehicle ID: ")
            make = input("Enter Make: ")
            model = input("Enter Model: ")
            year = int(input("Enter Year: "))
            price_per_day = float(input("Enter Rental Price per Day: "))

            if vehicle_type == 'car':
                doors = int(input("Enter Number of Doors: "))
                seating = int(input("Enter Seating Capacity: "))
                transmission = input("Enter Transmission Type (Automatic/Manual): ")
                vehicle = Car(vehicle_id, make, model, year, price_per_day, doors, seating, transmission)
            elif vehicle_type == 'bike':
                bike_type = input("Enter Bike Type (Mountain, Road, Hybrid): ")
                has_gear = input("Does it have gears? (yes/no): ").lower() == 'yes'
                vehicle = Bike(vehicle_id, make, model, year, price_per_day, bike_type, has_gear)
            elif vehicle_type == 'truck':
                capacity = float(input("Enter Max Load Capacity (in tons): "))
                axles = int(input("Enter Number of Axles: "))
                vehicle = Truck(vehicle_id, make, model, year, price_per_day, capacity, axles)
            else:
                print("Invalid vehicle type!")
                continue

            rental_company.add_vehicle(vehicle)

        elif choice == '3':
            vehicle_type = input("Enter Vehicle Type to Search (Car, Bike, Truck): ").lower()
            start_date = parse_date(input("Enter Start Date (YYYY-MM-DD): "))
            end_date = parse_date(input("Enter End Date (YYYY-MM-DD): "))
            if not start_date or not end_date:
                continue

            if vehicle_type == 'car':
                rental_company.find_available_vehicles(Car, start_date, end_date)
            elif vehicle_type == 'bike':
                rental_company.find_available_vehicles(Bike, start_date, end_date)
            elif vehicle_type == 'truck':
                rental_company.find_available_vehicles(Truck, start_date, end_date)
            else:
                print("Invalid vehicle type!")

        elif choice == '4':
            customer_id = input("Enter Customer ID: ")
            vehicle_id = input("Enter Vehicle ID: ")
            start_date = parse_date(input("Enter Start Date (YYYY-MM-DD): "))
            end_date = parse_date(input("Enter End Date (YYYY-MM-DD): "))
            if not start_date or not end_date:
                continue

            try:
                rental_company.create_rental(customer_id, vehicle_id, start_date, end_date)
            except RentalError as e:
                print(e)

        elif choice == '5':
            rental_id = input("Enter Rental ID: ")
            rental_company.return_vehicle(rental_id)

        elif choice == '6':
            rental_company.list_rentals()

        elif choice == '7':
            rental_company.list_customers()

        elif choice == '8':
            rental_company.list_vehicles()

        elif choice == '9':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
