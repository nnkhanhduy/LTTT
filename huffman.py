import heapq

class Huffman:
    def __init__(self, data):
        self.codes = {}
        self.data = data

    def huffman(self):
        self.codes.clear()
        heap = [[freq, [char, ""]] for char, freq in self.data.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            low1 = heapq.heappop(heap)
            low2 = heapq.heappop(heap)
            for pair in low1[1:]:
                pair[1] = "0" + pair[1]
            for pair in low2[1:]:
                pair[1] = "1" + pair[1]
            heapq.heappush(heap, [low1[0] + low2[0]] + low1[1:] + low2[1:])

        for char, code in sorted(heap[0][1:], key=lambda x: (len(x[1]), x[0])):
            self.codes[char] = code

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