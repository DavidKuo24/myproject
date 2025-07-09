import pytesseract
from PIL import Image

# 指定 Tesseract 的路徑
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\David.Kuo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# 圖片絕對路徑 ← 重點來了
image_path = r"C:\Users\David.Kuo\python\silentreaper\zefg.png"

# 開啟圖片並辨識
img = Image.open(image_path)
text = pytesseract.image_to_string(img)

print("辨識結果：", text.strip())
