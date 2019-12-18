from PIL import Image
import pytesseract

print(pytesseract.image_to_string(Image.open('rewe.jpg'), lang='deu'))
