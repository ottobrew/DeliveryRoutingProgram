from datetime import timedelta

# Truck class

class Truck:
    def __init__(self, name, location, speed, clock, inventory, package_list):
        self.name = name
        self.location = location
        self.speed = speed    # 18 mph
        self.clock = clock
        self.inventory = inventory
        self.package_list = package_list

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.name, self.location, self.speed, self.clock, self.inventory, self.package_list)
