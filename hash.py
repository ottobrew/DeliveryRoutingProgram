# Create Chaining Hash Table class with insert and search functions
# to access table of lists.

class ChainingHashTable:
    # Constructor. Empty list is added to all buckets
    def __init__(self):
        self.table = []
        for i in range(10):
            self.table.append([])

    # insert method
    def insert(self, id, item):
        # get list where package will be located
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]

        for i in bucket_list:
            if i[0] == id:
                i[1] = item
                return True

        # insert package ID (key) and package (value) to end of bucket_list
        id_package = [id, item]
        bucket_list.append(id_package)
        return True

    # search method for item by id, then return associated item
    def search(self, id):
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]

        for i in bucket_list:
            if i[0] == id:
                return i[1]  # return item
        return None
