# for Delta Arm TOF sensors
# written by bkenndpngieering and JPZ

# custom weighted moving average sensor filter
# gives precidence to newest readings
# larger array size (n) means smoother readings but slower update times

class WMA:
    def __init__(self, n=10):
        # array length
        self.n = n

        # previous sensor readings are stored in memory
        self.array = []

    def update(self, current_value):
        self.array.append(current_value)
        if len(self.array) < self.n+1:
            pass
        else:
            del self.array[0]
        
        base_weight = 0
        for i in range(len(self.array)):
            base_weight += i+1
        base_weight = 1/base_weight

        total = 0
        for i in range(len(self.array)):
            total += self.array[i]*base_weight*(i+1)

        return total

