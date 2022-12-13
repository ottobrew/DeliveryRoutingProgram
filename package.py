# Package class

class Package:
    def __init__(self, package_id, address, city, state, zip, delivery_deadline, mass_kgs, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.mass_kgs = mass_kgs
        self.status = status

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.package_id, self.address, self.city, self.state, self.zip, self.delivery_deadline, self.mass_kgs,
            self.status)


