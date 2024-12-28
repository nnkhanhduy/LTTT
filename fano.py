class Fano:
    def __init__(self, data):
        self.codes = {}
        self.data = data

    def fano(self):
        self.codes.clear()
        sorted_data = sorted(self.data.items(), key=lambda x: x[1], reverse=True)
        self._build_codes(sorted_data, "")

    def _build_codes(self, data, prefix):
        if len(data) == 1:
            self.codes[data[0][0]] = prefix or "0"
            return

        total = sum([x[1] for x in data])
        running_sum, split_idx = 0, 0

        for i, (char, freq) in enumerate(data):
            running_sum += freq
            if running_sum >= total / 2:
                split_idx = i + 1
                break

        self._build_codes(data[:split_idx], prefix + "0")
        self._build_codes(data[split_idx:], prefix + "1")

    def decode(self, encoded_text):
        reverse_codes = {v: k for k, v in self.codes.items()}
        decoded_text = ""
        buffer = ""

        for bit in encoded_text:
            buffer += bit
            if buffer in reverse_codes:
                decoded_text += reverse_codes[buffer]
                buffer = ""

        return decoded_text