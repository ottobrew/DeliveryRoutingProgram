# Ryan Otto
# Student ID #001465704


import math
from datetime import timedelta
import csv
import hash as h
import distances as d
import package as p
import truck as t

track_packages_out = []  # Track packages which left Hub
delivered_packages = []  # Track packages already delivered
to_be_delivered = []  # Track packages on active truck
time_tracker = timedelta(hours=int(8), minutes=int(0), seconds=int(0))


# Function to load package data from csv file into hash table
def load_package_data(file_name):
    with open(file_name) as importPackageData:
        package_data = csv.reader(importPackageData, delimiter=',')
        for i in package_data:
            pId = int(i[0])
            pAddress = i[1]
            pCity = i[2]
            pState = i[3]
            pZip = i[4]
            pDeadline = i[5]
            pMass = i[6]
            pStatus = "At Hub"

            # instantiate Package object
            package = p.Package(pId, pAddress, pCity, pState, pZip, pDeadline, pMass, pStatus)
            # print(package)

            # insert package objects into instance of hash table
            all_packages.insert(pId, package)


# Function to update time for truck
def update_time(truck):
    # t = d / s
    # Calc trip time in minutes
    trip_in_sec = (current_trip / truck.speed) * 3600
    trip_min = math.floor(trip_in_sec / 60)
    leftover_sec = trip_in_sec % 60
    truck.clock += timedelta(minutes=int(trip_min), seconds=int(leftover_sec))

# Function to load packages onto truck
def load_truck(truck):
    deliver_others = False  # When True, leave package for now and deliver others
    full = False  # Boolean to mark when truck.inventory is full or not
    sorted_list = []

    # Sort packages by delivery deadline before loading onto truck
    for i in truck.package_list:
        package = all_packages.search(i)
        if package.delivery_deadline == "9:00 AM":
            sorted_list.insert(0, package.package_id)

        elif package.delivery_deadline == "10:30 AM":
            sorted_list.insert(0, package.package_id)

        else:
            sorted_list.append(package.package_id)

    # Set parameters to load until truck is full and package delivery list is empty
    while len(truck.package_list) > 0 and not full and not deliver_others:
        for i in sorted_list:
            if not full:
                deliver = True  # Add package to truck.inventory for delivery
                package = all_packages.search(i)

                # Packages 6,25,28,32 delayed until 9:05am.  Deliver 25 & 26 together to same address
                if truck.clock < timedelta(hours=int(9), minutes=int(5)) and package.package_id in (6, 25, 26, 28, 32):
                    # Skip loading
                    deliver = False

                # Package 9 wrong address.
                # Update address for package 9 after 10:20am. If load attempted prior, package will not be loaded and
                # package address will not be updated. Also deliver 5 & 9 together to same address.
                elif truck.clock < timedelta(hours=int(10), minutes=int(20)) and package.package_id in (5, 9):
                    # Skip loading
                    deliver = False
                    deliver_others = True

                # If after 10:20am, update address for package 9
                if truck.clock >= timedelta(hours=int(10), minutes=int(20)) and package.package_id == 9:
                    package.address = "410 S State St"
                    package.city = "Salt Lake City"
                    package.state = "UT"
                    package.zip = "84111"

                # Add package to truck.inventory for delivery
                if deliver:
                    truck.inventory.append(package)
                    package.status = "En route on {}".format(truck.name)
                    track_packages_out.append(i)
                    to_be_delivered.append(i)
                    truck.package_list.remove(i)

                # If inventory is full, update flag
                if len(truck.inventory) >= 16:
                    full = True

# Function to loop through package list and deliver packages, updating truck and package attributes.
# Use Greedy Algorithm to determine next delivery by shortest distance from current location
def deliver_packages(truck, time=timedelta(hours=int(23), minutes=int(59))):
    global current_trip  # distance in miles
    global current_package  # package object from truck.inventory
    global current_location  # package address
    global last_location  # previous delivery address
    global last_delivered  # package object already removed from truck.inventory

    hub = "4001 South 700 East"
    current_location = hub
    continue_delivery = True  # Complete deliveries.  False if needed to stop according to user-entered time

    while len(truck.inventory) > 0 and continue_delivery:
        global next_package_id  # Package id whose delivery location has the shortest distance
        trip_distances = {}  # Dictionary of key-value pairs of package ids with distances from current address

        # --- Determine Next Delivery --- #
        # --- Greedy Algorithm ---#
        # Self-adjusting element looks for shortest distance from truck object's current delivery location
        for package in truck.inventory:
            # Get distance from current location to package's delivery address
            trip_length = d.get_distance(current_location, package.address)
            # Populate dictionary of package ids with corresponding trip lengths
            trip_distances.update({package.package_id: trip_length})

        # Shortest trip from current location
        shortest = min(trip_distances.values())

        # For packages left in truck inventory, save package_id as key and delivery distance as value
        for key, value in trip_distances.items():
            if value == shortest:
                next_package_id = key
                current_trip = value
                break

        # Get package object with corresponding package id
        for package in truck.inventory:
            if package.package_id == next_package_id:
                current_package = truck.inventory.pop(truck.inventory.index(package))
                break

        # update current location to package address
        current_location = current_package.address

        # update truck location to current address
        truck.location = current_location

        # update time / save timestamp
        update_time(truck)

        # Ensure output of status data is accurate according to input time
        if truck.clock <= time:
            # update delivered package status with timestamp
            current_package.status = "Delivered at {}".format(truck.clock)

            # update total distance
            d.all_distances.append(current_trip)

            # update lists to track delivered packages
            to_be_delivered.remove(current_package.package_id)
            delivered_packages.append(current_package)

            if len(truck.inventory) == 0:
                # Deliver last package and return truck to Hub
                distance_to_hub = d.get_distance(current_location, hub)
                current_location = hub

                # update total distance
                d.all_distances.append(distance_to_hub)

                # Re-load truck for next set of deliveries if more packages are waiting at Hub
                if len(track_packages_out) < 40:
                    load_truck(truck)
        else:
            continue_delivery = False


# Get package status from all_packages chaining hash table
def all_package_statuses():
    for i in range(40):
        p = all_packages.search(i + 1)

        print("Package ID: {} | Address: {}, {} {} | Delivery Deadline: {} | "
              "Weight: {}kgs | Delivery Status: {}".format(p.package_id, p.address,
                p.city, p.zip, p.delivery_deadline, p.mass_kgs, p.status))
    d.add_distances()

# Get package status for single package by package_id input by user
def package_status_by_id(id_in):

    p = all_packages.search(int(id_in))

    print("Package ID: {}\nAddress: {}, {} {}\nDelivery Deadline: {}\n"
      "Weight: {}kgs\nDelivery Status: {}\n".format(p.package_id, p.address,
        p.city, p.zip, p.delivery_deadline, p.mass_kgs, p.status))


# main - START
if __name__ == '__main__':
    print("\nWelcome to WGUPS Delivery Program")

    # loop until user is satisfied
    isActive = True

    while isActive:
        # --- Load Data --- #
        # Instantiate package list hash table
        all_packages = h.ChainingHashTable()

        # Load package data
        load_package_data('packageData.csv')

        # Populate address dictionary
        d.load_address_dict()

        # Manually load truck inventories and update package status
        # Truck 1: (15 has 9:00am deadline)
        # Packages 13,14,15,16,19,20 must be delivered together
        truck1_package_list = [5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 25, 26, 28, 30, 39]

        # Truck 2:  Packages 3,18,36,38 must be on truck 2
        truck2_package_list = [1, 2, 3, 4, 6, 18, 22, 23, 24, 27, 29, 31, 32, 33, 34, 35, 36, 37, 38, 40]

        # Instantiate truck objects
        truck1 = t.Truck("Truck 1", "At Hub", 18, timedelta(hours=int(8), minutes=int(0), seconds=int(0)), [], truck1_package_list)
        truck2 = t.Truck("Truck 2", "At Hub", 18, timedelta(hours=int(8), minutes=int(0), seconds=int(0)), [], truck2_package_list)


        print("\nOptions:")
        print("1. View Status of All Packages and Total Mileage")
        print("2. View Status by Package ID.")
        print("3. View Status of All Packages by Time")
        print("4. Exit the Program")
        option = input("Chose an option (1,2,3 or 4): ")
        if option == "1":
            d.all_distances.clear()
            delivered_packages.clear()
            track_packages_out.clear()
            load_truck(truck1)
            load_truck(truck2)
            deliver_packages(truck1)
            deliver_packages(truck2)
            all_package_statuses()

        elif option == "2":
            d.all_distances.clear()
            track_packages_out.clear()
            load_truck(truck1)
            load_truck(truck2)
            deliver_packages(truck1)
            deliver_packages(truck2)

            input_id = input("Enter Package ID: ")
            if int(input_id) > 40 or int(input_id) < 1:
                print("Invalid Package ID")
            else:
                package_status_by_id(input_id)
        elif option == "3":
            d.all_distances.clear()
            delivered_packages.clear()
            track_packages_out.clear()
            input_time = input("Enter time (hh:mm): ")
            t_in = input_time.split(":")
            print(timedelta(hours=int(t_in[0]), minutes=int(t_in[1])))

            load_truck(truck1)
            load_truck(truck2)
            deliver_packages(truck1, timedelta(hours=int(t_in[0]), minutes=int(t_in[1])))
            deliver_packages(truck2, timedelta(hours=int(t_in[0]), minutes=int(t_in[1])))
            all_package_statuses()
        elif option == "4":
            isActive = False
        else:
            print("Not an option. Please try again!")
        # main - END