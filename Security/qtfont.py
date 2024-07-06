import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QFont

app = QApplication(sys.argv)

# 定义中文字体路径和字号
font_path = 'fonts/OPPOSans-R.ttf'  # 替换为你下载的中文字体文件路径
font = QFont()
font.setFamily(font_path)
font.setPointSize(12)  # 设置字号

# 创建一个 QLabel 来显示中文
label = QLabel('你好，世界！')
label.setFont(font)
label.show()

sys.exit(app.exec_())
