import sys
from PyQt5 import QtWidgets, uic


def read_txt(file_path):
    try:
        with open(f"data/txt/{file_path}", "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Файл не найден."
    except Exception as e:
        return f"Произошла ошибка: {e}"


class CryptoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CryptoApp, self).__init__()
        uic.loadUi("data/ui/form.ui", self)

        self.ceasar_pushButton.clicked.connect(self.ceasar_dialog)
        self.vigener_pushButton.clicked.connect(self.vigenere_dialog)
        self.dif_hel_pushButton.clicked.connect(self.diffie_hellman_dialog)

    def ceasar_dialog(self):
        self.ceasar_window = CeasarCode()
        self.ceasar_window.show()

    def vigenere_dialog(self):
        self.vigener_window = VigeneerCode()
        self.vigener_window.show()

    def diffie_hellman_dialog(self):
        self.diff_hell_alg = DiffiHellmanAlg()
        self.diff_hell_alg.show()


class CeasarCode(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("data/ui/ceasar_mode.ui", self)
        self.generate_pushButton.clicked.connect(self.generate)
        self.setWhatsThis(read_txt("ceasar_info.txt"))

    def generate(self):
        input_text = self.input_data_textEdit.toPlainText()
        shift_value = self.shift_number_lineEdit.text()
        if self.code_radioButton.isChecked():
            output_text = self.caesar_cipher(input_text, int(shift_value))
        elif self.uncode_radioButton.isChecked():
            output_text = self.caesar_cipher(input_text, -int(shift_value))
        self.output_data_textBrowser.setText(output_text)

    def caesar_cipher(self, text, shift):
        def shift_char(char, alphabet):
            if char in alphabet:
                return alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            else:
                return char

        lower_latin = "abcdefghijklmnopqrstuvwxyz"
        upper_latin = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower_cyrillic = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        upper_cyrillic = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        result = ""

        for char in text:
            if char in lower_latin or char in upper_latin:
                if char.islower():
                    result += shift_char(char, lower_latin)
                else:
                    result += shift_char(char, upper_latin)
            elif char in lower_cyrillic or char in upper_cyrillic:
                if char.islower():
                    result += shift_char(char, lower_cyrillic)
                else:
                    result += shift_char(char, upper_cyrillic)
            else:
                result += char

        return result


class VigeneerCode(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("data/ui/vigener_mode.ui", self)
        self.generate_pushButton.clicked.connect(self.generate)
        self.setWhatsThis(read_txt("vigener_info.txt"))

    def generate(self):
        input_text = self.input_data_textEdit.toPlainText()
        shift_value = self.codeword_lineEdit.text()
        if self.code_radioButton.isChecked():
            output_text = self.vigener_cipher(input_text, shift_value, 1)
        elif self.uncode_radioButton.isChecked():
            output_text = self.vigener_cipher(input_text, shift_value, 0)
        self.output_data_textBrowser.setText(output_text)

    def vigener_cipher(self, text, key, mode):
        def rotate_char(char, shift_char, mode):
            if char.islower():
                alphabet = lower_cyrillic if char in lower_cyrillic else lower_latin
            else:
                alphabet = upper_cyrillic if char in upper_cyrillic else upper_latin

            shift = alphabet.index(shift_char.lower() if char.islower() else shift_char)
            shift *= -1 if mode == 0 else 1
            return alphabet[(alphabet.index(char) + shift) % len(alphabet)]

        def full_key(text, key):
            key_index = 0
            full = ""

            for char in text:
                if char.isalpha():
                    if char.islower():
                        full += key[key_index % len(key)].lower()
                    else:
                        full += key[key_index % len(key)].upper()
                    key_index += 1
                else:
                    full += char

            return full

        lower_latin = "abcdefghijklmnopqrstuvwxyz"
        upper_latin = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower_cyrillic = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        upper_cyrillic = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        key = full_key(text, key)
        result = ""

        key_index = 0

        for char in text:
            if char.isalpha():
                shift_char = key[key_index]
                shifted_char = rotate_char(char, shift_char, mode)
                result += shifted_char
                key_index += 1
            else:
                result += char

        return result


class DiffiHellmanAlg(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("data/ui/diffi-hellman_alg.ui", self)
        self.generate_pushButton.clicked.connect(self.get_values)
        self.setWhatsThis(read_txt("diffi_hellman_info.txt"))

    def get_values(self):
        try:
            a = int(self.a_number_lineEdit.text())
            b = int(self.b_number_lineEdit.text())
            p = int(self.p_number_lineEdit.text())
            g = int(self.g_number_lineEdit.text())
            self.algoritm(a, b, p, g)
        except:
            self.error_label.setText("!ВВЕДИТЕ ЦЕЛЫЕ ЧИСЛОВЫЕ ЗНАЧЕНИЯ!")

    def algoritm(self, a_sec, b_sec, p, g):
        public_a = g**a_sec % p
        public_b = g**b_sec % p

        self.b_pub_key_textBrowser.setText(str(public_b))
        self.a_pub_key_textBrowser.setText(str(public_a))

        key_s_from_a = public_b**a_sec % p
        key_s_from_b = public_a**b_sec % p

        self.s_number1_textBrowser.setText(str(key_s_from_a))
        self.s_number2_textBrowser.setText(str(key_s_from_b))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec_())
