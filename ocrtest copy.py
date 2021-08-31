from paddleocr import PaddleOCR

ocr = PaddleOCR()  # need to run only once to download and load model into memory
result = ocr.ocr('./images/coor0.jpg', det=False)
for line in result:
    print(line)