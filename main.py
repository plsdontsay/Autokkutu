from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import time
import pyautogui
import json

# chosung = ['r', 'R', 's', 'e', 'E', 'f', 'a', 'q', 'Q', 't', 'T', 'd', 'w', 'W', 'c', 'z', 'x', 'v', 'g']
# jungsung = ['k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk', 'ho', 'hl', 'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l']
# jongsung = ['', 'r', 'R', 'rt', 's', 'sw', 'sg', 'e', 'f', 'fr', 'fa', 'fq', 'ft', 'fx', 'fv', 'fg', 
#             'a', 'q', 'qt', 't', 'T', 'd', 'w', 'c', 'z', 'x', 'v', 'g']

# # 유니코드 한글 분해 함수
# def decompose_korean(text):
#     result_keys = []

#     for char in text:
#         if '가' <= char <= '힣':
#             code = ord(char) - ord('가')
#             ch = code // 588
#             jung = (code % 588) // 28
#             jong = code % 28

#             result_keys.append(chosung[ch])
#             result_keys.extend(list(jungsung[jung]))
#             if jongsung[jong]:
#                 result_keys.extend(list(jongsung[jong]))
#         else:
#             # 한글 외 문자 (띄어쓰기, 특수문자 등)
#             result_keys.append(char)
    
#     result_keys.append('enter')
#     return result_keys

# 두음법칙 경우 처리
def p(s):
  if len(s)==1:
    return [s]
  else:
    return s[:-1].split('(')

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://kkutu.co.kr/")

sent=False
used={}
while True:
  # print(sent)
  words=[]
  elem=driver.find_elements(By.CLASS_NAME,"game-input")
  if elem and elem[0].value_of_css_property("display")=='none':
    sent=False
    # print('정상작동')
    WebDriverWait(driver,10000).until(
      EC.visibility_of_element_located((By.CLASS_NAME,"game-input"))
    )
  elif not elem:
    continue
  else:
    prefix=driver.find_element(By.CLASS_NAME,"jjo-display")
    # inpbox=driver.find_element(By.CLASS_NAME,"game-input")
    inpbox=driver.find_element(By.CSS_SELECTOR,'input[id^="UserMassage"]')
    # try:
    #   inpbox.click()
    # except:
    #   pass

    if not sent: 
      for i in p(prefix.text):
        try:
          with open('words/'+i+'.json', "r", encoding="utf-8") as f:
            data = json.load(f)  # JSON → 파이썬 딕셔너리/리스트로 변환
            words.extend([item["word"] for item in data])
        except:
          pass
      # with open('words/'+prefix.text+'.json', "r", encoding="utf-8") as f:
      #   data = json.load(f)  # JSON → 파이썬 딕셔너리/리스트로 변환
      #   words.extend([item["word"] for item in data])

      print('로딩 완료: '+prefix.text)

      word=''
      for w in words:
        # print(prefix.text)
        if w in used: continue
        word=str(w)
        used[w]=1
        break

      # pyautogui.write(decompose_korean(word),interval=0.001)
      inpbox.send_keys(word)
      inpbox.send_keys(Keys.ENTER)
      sent=True