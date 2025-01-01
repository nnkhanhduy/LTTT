from math import log2, ceil

class Shannon:
    def __init__(self, data):
        """
        Constructor nhận chuỗi dữ liệu `data` để mã hóa.
        Tính toán xác suất của các ký tự và xây dựng mã Shannon.
        """
        self.data = data  # Dữ liệu đầu vào.
        self.prob = self.calculate_probability(data)  # Tính xác suất xuất hiện của từng ký tự.
        self.codes = self.shannon_encoding()  # Sinh mã Shannon cho từng ký tự.

    def calculate_probability(self, data):
        """
        Tính toán xác suất xuất hiện của từng ký tự trong dữ liệu.
        Args:
            data: Chuỗi dữ liệu đầu vào.
        Returns:
            Dictionary chứa xác suất của từng ký tự.
        """
        freq = {}  # Dictionary lưu tần suất xuất hiện của từng ký tự.
        for char in data:
            freq[char] = freq.get(char, 0) + 1
        total = len(data)  # Tổng số ký tự trong chuỗi dữ liệu.
        prob = {char: freq[char] / total for char in freq}  # Xác suất = tần suất / tổng số ký tự.
        return prob

    def shannon_encoding(self):
        """
        Sinh mã Shannon cho từng ký tự dựa trên xác suất của chúng.
        Returns:
            Dictionary chứa mã Shannon của từng ký tự.
        """
        # Sắp xếp các ký tự theo xác suất giảm dần.
        prob = dict(sorted(self.prob.items(), key=lambda item: item[1], reverse=True))
        cumulative_prob = 0  # Biến lưu xác suất tích lũy.
        codes = {}  # Dictionary lưu mã Shannon của từng ký tự.

        for char, p in prob.items():
            code_length = ceil(-log2(p))  # Độ dài mã dựa trên xác suất.
            # Chuyển xác suất tích lũy thành mã nhị phân có độ dài tương ứng.
            cumulative_prob_bin = format(int(cumulative_prob * (2 ** code_length)), f'0{code_length}b')
            codes[char] = cumulative_prob_bin
            cumulative_prob += p  # Cập nhật xác suất tích lũy.

        return codes

    def encode(self):
        """
        Mã hóa chuỗi dữ liệu đầu vào thành chuỗi nhị phân.
        Returns:
            Chuỗi nhị phân đã mã hóa.
        """
        return ''.join(self.codes[char] for char in self.data)

    def decode(self, encoded_data):
        """
        Giải mã chuỗi nhị phân thành chuỗi ký tự gốc.
        Args:
            encoded_data: Chuỗi nhị phân đã mã hóa.
        Returns:
            Chuỗi ký tự đã giải mã.
        """
        reverse_codes = {v: k for k, v in self.codes.items()}  # Đảo ngược dictionary mã hóa để tra cứu nhanh.
        temp = ''  # Bộ đệm tạm thời để lưu chuỗi nhị phân đang xét.
        decoded = ''  # Kết quả giải mã.

        for bit in encoded_data:  # Duyệt qua từng bit trong chuỗi mã hóa.
            temp += bit  # Thêm bit vào bộ đệm.
            if temp in reverse_codes:  # Kiểm tra nếu bộ đệm khớp với mã nào đó.
                decoded += reverse_codes[temp]  # Lấy ký tự tương ứng.
                temp = ''  # Xóa bộ đệm để tiếp tục.

        return decoded
