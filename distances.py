import csv

# Insert distance data into list of lists (two-dimensional array)
distanceArray = []
with open('distanceTable.csv', 'r') as d:
    distanceData = csv.reader(d, delimiter=',')
    for row in distanceData:
        distanceArray.append(row)

addressList = []
with open('addressTable.csv', 'r') as a:
    addressData = csv.reader(a, delimiter=',')
    for row in addressData:
        addressList.append(row)

indexedAddresses = {}  # Empty dictionary
allAddresses = 27

# Load data into dictionary with address strings from addressList
def load_address_dict():
    for i in range(allAddresses):
        address = str(addressList[i]).replace('[\' ', '').replace('\']', '')
        indexedAddresses[i] = address
    return indexedAddresses


# Function to get distance between two locations
def get_distance(depart, arrive):
    # compare address strings and get index of address
    dkey = 0
    akey = 0
    for key, value in indexedAddresses.items():
        if depart == value:
            dkey = key

    for key, value in indexedAddresses.items():
        if arrive == value:
            akey = key

    # get distance from distanceArray[index1][index2]
    if dkey < akey:
        edge_distance = distanceArray[akey][dkey]
    else:
        edge_distance = distanceArray[dkey][akey]
    return float(edge_distance)


all_distances = []

# Sum of all distances traveled
def add_distances():
    total = sum(all_distances)
    print("Total distance traveled: %s" % round(total, 1))
    return total


total_distance = add_distances()
