from math import floor, ceil, log10, pow

class Bands(object):

    def round_up(self, x):
        self.get_base(x)

    def get_base(self, x):
        # Note: this will not work for decimal places
        return len(str(int(x))) - 1

    def nicen_number(self, x):
        base = self.get_base(x)
        first_digits = int(str(x)[0])
        if first_digits <= 3:
            first_digits = 1
        elif 3 < first_digits <= 6:
            first_digits = 5
        else:
            first_digits = 10
        return first_digits * pow(10, base)

    def get_chunk_size(self, x1, x2):
        diff = abs(x2 - x1)
        chunk_size = self.nicen_number(diff * 0.1)
        return chunk_size

    def get_min_value(self, x, chunk_size):
        if chunk_size == 1:
            x = int(x)
        else:
            cb = self.get_base(chunk_size)
            if str(chunk_size)[0] == '5':
                cb += 1
            last = int(str(x)[-cb:])
            if last > chunk_size:
                last -= chunk_size
            x -= last
        return x

    def get_band(self, mn, mx, cs):
        x = mn
        bands = [x]
        while x < mx:
            x += cs
            bands.append(x)
        return bands


    def get_labels(self, bands):
        labels = {}
        mid = (bands[1] - bands[0]) / 2
        for i in range(0,len(bands)):
            labels[i] = '{:,}'.format(int((bands[i]+mid)))

        return labels

    def get_banding(self, mn, mx):
        cs = self.get_chunk_size(mn, mx)
        mn = self.get_min_value(mn, cs)
        bands = self.get_band(mn, mx, cs)
        labels = self.get_labels(bands)
        return bands, labels



    '''
    def find_band_size(self, x1, x2):
        max_value = self.get_base(x2)
        print(max_value)
        no_of_bands = str(max_value)[0:2]
        size_of_bands = int(pow(10, max_base - 1))
        bands = [e for e in range(0, max_value + size_of_bands, size_of_bands)]

    def round_to_n(self, x, n, b):
        if b == 'd':
            return int(str(x)[0:n]) * pow(10, n-1)
        else:
            return (int(str(x)[0:n])+1) * pow(10, n-1)

    def round_up(self, x):
        return x[0]+1

    def find_bands(self, x1, x2):
        # round the number
        max = self.round_up(x2, 1)
        no_of_bands = str(max)[0:2]
        size_of_bands = int(pow(10, self.get_base(x1) - 1))
        bands = [e for e in range(0, max_value + size_of_bands, size_of_bands)]


    def determine_banding(self, max, min):
        bands = []
        band_labels = {}
        max_base = floor(log10(max))
        min_base = floor(log10(min))
        min_value = self.round_to_n(min, 1)
        if max_base > min_base:
            max_value = self.round_to_n(max, 1)
            print(max_value)
            no_of_bands = str(max_value)[0:2]
            size_of_bands = int(pow(10, max_base - 1))
            bands = [e for e in range(0, max_value + size_of_bands, size_of_bands)]
            print(bands)
        if min_base == max_base:
            # We need to determine at what point the numbers diverge
            diverge = max - min
            # Div bas determine what level of base to we are going to go up in.
            div_base = floor(log10(abs(diverge)))
            dull = int(str(min)[0:max_base - div_base])
            max = int(str(max)[div_base + 2:])
            min = int(str(min)[div_base + 2:])
            print(max)
            print(min)
            print(dull)

            size_of_bands = int(pow(10, div_base))
            no_of_bands = int(ceil((max - min) / size_of_bands))
            print('um:' + str(no_of_bands))
            print(min_value)
            # print(max_value)
            # bands = [e for e in range(min_value, max_value + size_of_bands, size_of_bands)]
            # print(bands)#
        '''

