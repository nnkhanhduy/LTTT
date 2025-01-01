class Fano:
    def __init__(self, data):
        # Constructor nhận một dictionary `data` chứa các ký tự và tần suất xuất hiện của chúng.
        self.codes = {}  # Dictionary để lưu trữ mã hóa Fano.
        self.data = data  # Dữ liệu đầu vào.

    def fano(self):
        """
        Phương thức chính để xây dựng mã Fano.
        """
        self.codes.clear()  # Xóa mọi mã cũ.
        # Sắp xếp các ký tự theo tần suất giảm dần.
        sorted_data = sorted(self.data.items(), key=lambda x: x[1], reverse=True)
        # Gọi phương thức đệ quy để xây dựng mã.
        self._build_codes(sorted_data, "")

    def _build_codes(self, data, prefix):
        """
        Hàm đệ quy để xây dựng mã Fano.
        Args:
            data: Danh sách các ký tự cùng với tần suất (đã sắp xếp giảm dần).
            prefix: Chuỗi mã tiền tố.
        """
        if len(data) == 1:  # Nếu chỉ còn một ký tự, gán mã cho ký tự đó.
            self.codes[data[0][0]] = prefix or "0"  # Trường hợp ký tự đơn lẻ, mã mặc định là "0".
            return

        # Tính tổng tần suất của các ký tự trong danh sách.
        total = sum([x[1] for x in data])
        running_sum, split_idx = 0, 0

        # Tìm vị trí tách danh sách sao cho tổng tần suất hai nửa gần bằng nhau.
        for i, (char, freq) in enumerate(data):
            running_sum += freq
            if running_sum >= total / 2:
                split_idx = i + 1
                break

        # Gọi đệ quy cho nửa đầu với tiền tố "0" và nửa sau với tiền tố "1".
        self._build_codes(data[:split_idx], prefix + "0")
        self._build_codes(data[split_idx:], prefix + "1")

    def decode(self, encoded_text):
        """
        Giải mã một chuỗi nhị phân được mã hóa bằng thuật toán Fano.
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
