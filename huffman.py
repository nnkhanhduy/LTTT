import heapq

class Huffman:
    def __init__(self, data):
        # Constructor nhận một dictionary `data` chứa các ký tự và tần suất xuất hiện của chúng.
        self.codes = {}  # Dictionary để lưu trữ mã Huffman.
        self.data = data  # Dữ liệu đầu vào.

    def huffman(self):
        """
        Phương thức chính để xây dựng mã Huffman.
        """
        self.codes.clear()  # Xóa mọi mã cũ.
        # Tạo một heap (hàng đợi ưu tiên) từ danh sách các ký tự và tần suất.
        heap = [[freq, [char, ""]] for char, freq in self.data.items()]
        heapq.heapify(heap)  # Biến danh sách thành heap.

        # Lặp cho đến khi chỉ còn một nút trong heap.
        while len(heap) > 1:
            # Lấy hai nút có tần suất nhỏ nhất từ heap.
            low1 = heapq.heappop(heap)
            low2 = heapq.heappop(heap)

            # Gán mã "0" cho tất cả các ký tự trong nút đầu tiên và "1" cho nút thứ hai.
            for pair in low1[1:]:
                pair[1] = "0" + pair[1]
            for pair in low2[1:]:
                pair[1] = "1" + pair[1]

            # Gộp hai nút thành một nút mới với tổng tần suất và đẩy lại vào heap.
            heapq.heappush(heap, [low1[0] + low2[0]] + low1[1:] + low2[1:])

        # Sắp xếp kết quả và lưu các mã Huffman vào dictionary.
        for char, code in sorted(heap[0][1:], key=lambda x: (len(x[1]), x[0])):
            self.codes[char] = code

    def decode(self, encoded_text):
        """
        Giải mã một chuỗi nhị phân được mã hóa bằng thuật toán Huffman.
        Args:
            encoded_text: Chuỗi nhị phân được mã hóa.
        Returns:
            Chuỗi ký tự đã giải mã.
        """
        # Đảo ngược dictionary mã hóa để tra cứu ký tự nhanh.
        reverse_codes = {v: k for k, v in self.codes.items()}
        decoded_text = ""  # Kết quả giải mã.
        buffer = ""  # Bộ đệm lưu tạm chuỗi nhị phân.

        for bit in encoded_text:  # Lặp qua từng bit trong chuỗi mã hóa.
            buffer += bit  # Thêm bit vào bộ đệm.
            if buffer in reverse_codes:  # Kiểm tra nếu bộ đệm khớp với mã nào đó.
                decoded_text += reverse_codes[buffer]  # Lấy ký tự tương ứng.
                buffer = ""  # Xóa bộ đệm để tiếp tục.

        return decoded_text  # Trả về chuỗi đã giải mã.
