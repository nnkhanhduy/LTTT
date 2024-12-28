from math import log2, ceil

class Shannon:
    def __init__(self, data):
        self.data = data
        self.prob = self.calculate_probability(data)
        self.codes = self.shannon_encoding()

    def calculate_probability(self, data):
        freq = {}
        for char in data:
            freq[char] = freq.get(char, 0) + 1
        total = len(data)
        prob = {char: freq[char] / total for char in freq}
        return prob

    def shannon_encoding(self):
        prob = dict(sorted(self.prob.items(), key=lambda item: item[1], reverse=True))
        cumulative_prob = 0
        codes = {}

        for char, p in prob.items():
            code_length = ceil(-log2(p))
            cumulative_prob_bin = format(int(cumulative_prob * (2 ** code_length)), f'0{code_length}b')
            codes[char] = cumulative_prob_bin
            cumulative_prob += p

        return codes

    def encode(self):
        return ''.join(self.codes[char] for char in self.data)

    def decode(self, encoded_data):
        reverse_codes = {v: k for k, v in self.codes.items()}
        temp = ''
        decoded = ''

        for bit in encoded_data:
            temp += bit
            if temp in reverse_codes:
                decoded += reverse_codes[temp]
                temp = ''

        return decoded
