import easyocr
import os
import re

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

result = reader.readtext('./images/imgTem/rw_jyl_wc.JPG', detail=0)

res = re.findall(r"\d+", result[0])

print(result[0])
print(res[0], res[1])