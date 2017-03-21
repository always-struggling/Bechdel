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
            labels[i] = int((bands[i]+mid))

        return labels

    def get_banding(self, mn, mx):
        cs = self.get_chunk_size(mn, mx)
        mn = self.get_min_value(mn, cs)
        bands = self.get_band(mn, mx, cs)
        labels = self.get_labels(bands)
        return bands, labels


