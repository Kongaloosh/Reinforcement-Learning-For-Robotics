"""
Creates an instance of a file loader. Takes in a file and parses it into a stream of experience
where each step is a dictionary in an array. The dictionary keys are as specified in the header of
the file.
"""
__author__ = 'alex'


class Max_Min_Finder(object):

    def __init__(self, file_loc):
        """Initializes a file-loader given a file-location"""
        f = open(file_loc, 'r')                 # open the file for reading
        self.data_stream = []                   # this is where we store the stream of experience
        self.elements = f.readline().rstrip().split(',')  # extracts the header of the file

        for line in f:
            vals = line.rstrip().split(',')              # separate all the values in an observation
            self.data_stream.append(dict([(self.elements[i], float(vals[i])) for i in range(len(vals)-1)]))
            # we -1 because there's another comma at the end of every line but the header
            # todo: generalize this to work with cleaned obs
        self.i = 0

        self.max_v = dict([(k, 0) for k in self.elements])
        self.min_v = dict([(k, 0) for k in self.elements])

        for state in self.data_stream:
            for e in self.elements:
                if state[e] > self.max_v[e]:
                    self.max_v[e] = state[e]
                if state[e] < self.min_v[e]:
                    self.min_v[e] = state[e]

        for e in self.elements:
            print('{e}: max: {max}, min: {min}'.format(e=e, max=self.max_v[e], min=self.min_v[e]))

def main():
    print('starting')
    file = 'results/prosthetic-data/EdwardsPOIswitching_s1a1.txt'
    m = Max_Min_Finder(file)

if __name__ == "__main__":
    main()