import firebase,json,re,requests,bs4
import wikipedia,urllib
from bs4 import BeautifulSoup
firebase = firebase.FirebaseApplication('https://pi-saurus-default-rtdb.firebaseio.com/')
TOKEN = "1732261163:AAH6fDLBs4L321L5AGreZC4RYA2g1srzrkI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)



# page= wikipedia.page("tkm college of engineering")
# print(page.title)
# test = {"ok":True,"result":[{"update_id":937339743,
# "message":{"message_id":205,"from":{"id":863175437,"is_bot":False,"first_name":"SOORAJ","last_name":"TS","username":"soorajts007","language_code":"en"},"chat":{"id":863175437,"first_name":"SOORAJ","last_name":"TS","username":"soorajts007","type":"private"},"date":1622289328,"reply_to_message":{"message_id":193,"from":{"id":1732261163,"is_bot":True,"first_name":"tester1","username":"Agsgegebot"},"chat":{"id":863175437,"first_name":"SOORAJ","last_name":"TS","username":"soorajts007","type":"private"},"date":1622285792,"photo":[{"file_id":"AgACAgUAAxkDAAPBYLIrsB6jO7NNiRttpcC4eQXWOqcAAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADcwAD27AEAAEfBA","file_unique_id":"AQADDsQYb3QAA9uwBAAB","file_size":691,"width":26,"height":90},{"file_id":"AgACAgUAAxkDAAPBYLIrsB6jO7NNiRttpcC4eQXWOqcAAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADbQAD3LAEAAEfBA","file_unique_id":"AQADDsQYb3QAA9ywBAAB","file_size":10243,"width":94,"height":320},{"file_id":"AgACAgUAAxkDAAPBYLIrsB6jO7NNiRttpcC4eQXWOqcAAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADeAAD3bAEAAEfBA","file_unique_id":"AQADDsQYb3QAA92wBAAB","file_size":47338,"width":235,"height":800},{"file_id":"AgACAgUAAxkDAAPBYLIrsB6jO7NNiRttpcC4eQXWOqcAAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADeQAD2rAEAAEfBA","file_unique_id":"AQADDsQYb3QAA9qwBAAB","file_size":71036,"width":376,"height":1280}]},"text":"Delete this"}}]}
# for elements in test["result"]:
#     if "reply_to_message" in elements["message"]:
#         print(elements["message"]["reply_to_message"]['photo'][0]['file_id'])
# test = {"message":{"message_id":206,"from":{"id":863175437,"is_bot":False,"first_name":"SOORAJ","last_name":"TS","username":"soorajts007","language_code":"en"},"chat":{"id":863175437,"first_name":"SOORAJ","last_name":"TS","username":"soorajts007","type":"private"},"date":1622290257,"reply_to_message":{"message_id":196,"from":{"id":1732261163,"is_bot":True,"first_name":"tester1","username":"Agsgegebot"},"chat":{"id":863175437,"first_name":"SOORAJ","last_name":"TS","username":"soorajts007","type":"private"},"date":1622285795,"document":{"file_name":"Armature windings.pptx","mime_type":"application/vnd.openxmlformats-officedocument.presentationml.presentation","file_id":"BQACAgUAAxkDAAPEYLIvUuBDmpNCJRjRP12nD2tplkIAAkcCAALuBzlVTq_rsK91QKcfBA","file_unique_id":"AgADRwIAAu4HOVU","file_size":11694387}},"text":"Delete this"}}
# print(test["message"]["reply_to_message"]['document']['file_id'])
# test_dic = {'DCMT': [[['AgACAgUAAxkBAAOlYLIUwVYH9vtt27o8lwJ0G4u8HV8AAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADcwAD27AEAAEfBA', 'AgACAgUAAxkBAAOmYLIUwd8FUxQ7b39BUWABNsOJGC0AAlGsMRvuBzlV9Wnc7T1P6OSjCU5zdAADAQADAgADcwADcsYBAAEfBA', 'AgACAgUAAxkBAAOqYLIUwVtoEwqJZ107mBTQgPUbPBUAAk6sMRvuBzlVpJVs5w9PWaKcKrpudAADAQADAgADcwADtt8EAAEfBA'], ['BQACAgUAAxkBAAOnYLIUwWZbWAdibeBq9MsPWr2ij6IAAkcCAALuBzlVTq_rsK91QKcfBA', 'BQACAgUAAxkBAAOoYLIUwb5ujh0d_DXliyfRsJfnuNwAAkgCAALuBzlVUKq0udIbqb8fBA', 'BQACAgUAAxkBAAOpYLIUwTAvbFMvrHBrOYKl7ai0UDAAAkkCAALuBzlVcSB_YNvTDssfBA'], [], 'May 29, 2021']], 'DEC': []}
# for one in list(test_dic.values()):
#     if len(one)>0:
#         print(one[0][0])
#         print(one[0][1])
# sample = ["AgACAgUAAxkDAAPYYLI68v0K9Df2792nVcTPNMHDyHQAAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADcwAD27AEAAEfBA",'AgACAgUAAxkBAAOlYLIUwVYH9vtt27o8lwJ0G4u8HV8AAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADcwAD27AEAAEfBA', 'AgACAgUAAxkBAAOmYLIUwd8FUxQ7b39BUWABNsOJGC0AAlGsMRvuBzlV9Wnc7T1P6OSjCU5zdAADAQADAgADcwADcsYBAAEfBA', 'AgACAgUAAxkBAAOqYLIUwVtoEwqJZ107mBTQgPUbPBUAAk6sMRvuBzlVpJVs5w9PWaKcKrpudAADAQADAgADcwADtt8EAAEfBA']
# test = "AgACAgUAAxkDAAPYYLI68v0K9Df2792nVcTPNMHDyHQAAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADcwAD27AEAAEfBA"
# for sam in sample:
#     if test == sam:
#         print(test)
#         ['AgACAgUAAxkBAAOlYLIUwVYH9vtt27o8lwJ0G4u8HV8AAlCsMRvuBzlVvy_oNQymGMIOxBhvdAADAQADAgADcwAD27AEAAEfBA', 'AgACAgUAAxkBAAOmYLIUwd8FUxQ7b39BUWABNsOJGC0AAlGsMRvuBzlV9Wnc7T1P6OSjCU5zdAADAQADAgADcwADcsYBAAEfBA', 'AgACAgUAAxkBAAOqYLIUwVtoEwqJZ107mBTQgPUbPBUAAk6sMRvuBzlVpJVs5w9PWaKcKrpudAADAQADAgADcwADtt8EAAEfBA'], ['BQACAgUAAxkBAAOnYLIUwWZbWAdibeBq9MsPWr2ij6IAAkcCAALuBzlVTq_rsK91QKcfBA', 'BQACAgUAAxkBAAOoYLIUwb5ujh0d_DXliyfRsJfnuNwAAkgCAALuBzlVUKq0udIbqb8fBA', 'BQACAgUAAxkBAAOpYLIUwTAvbFMvrHBrOYKl7ai0UDAAAkkCAALuBzlVcSB_YNvTDssfBA'], [], 'May 29, 2021']]
# uploaded_file_id = "BQACAgUAAxkBAAIBFWCzDtlyB6zOsFu8CWy5XXS3JVPSAALEAgACtVqRVdgXLrHasUhDHwQ"
# "BQACAgUAAxkBAAIBF2CzEEHmDJYfBGm_lSobe_wpN0BsAALEAgACtVqRVdgXLrHasUhDHwQ"
# "BQACAgUAAxkBAAIBF2CzEEHmDJYfBGm_lSobe_wpN0BsAALEAgACtVqRVdgXLrHasUhDHwQ"

# file_unique_id="AgADxAIAArVakVU"
# "AgADxAIAArVakVU"
# tagged_file_id = "BQACAgUAAxkBAAIBFWCzDtlyB6zOsFu8CWy5XXS3JVPSAALEAgACtVqRVdgXLrHasUhDHwQ"
# file_unique_id2 = "AgADxAIAArVakVU"
# if uploaded_file_id == tagged_file_id:
#     print("file_id is true")
# if file_unique_id == file_unique_id2:
#     print("unique_file_id is true")
# urlKeyword = 'baloon'
# url = f'http://www.google.com/search?q={urlKeyword}&tbm=isch'
# response = requests.get(url=url, headers=None)
# soup = BeautifulSoup(response.content,"html.parser")
# images = soup.find_all("img")
# for image in images:
#    image_src = image['src']
#    print(image_src)
# import urllib.request
# url = 'https://google.com/search?q=Where+can+I+get+the+best+coffee'
# request = urllib.request.Request(url)
# request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
# raw_response = urllib.request.urlopen(request).read()
# html = raw_response.decode("utf-8")
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html, 'html.parser')
# divs = soup.select("#search div.g")
# empty = []
# for div in divs:
#     results = div.select("a")
#     if (len(results) >= 1):
#         h3 = results[0]
#         print(h3.get('href'))
#         empty.append(h3.get_text())

# #to add button
# import requests, json

# bot_token = '1824370628:AAHrVNB7lz4iR0Txy9Ugd5Ek2uu6NK1APsc'
# chat_id = '863175437'
# text = "Choose:"
# reply_markup={"keyboard":[["Yes","No"],["Maybe"],["1","2","3"]],"one_time_keyboard":True}
# data = {'chat_id': chat_id, 'text': text, 'user_id': 863175437}
# url ="https://api.telegram.org/bot" + bot_token + "/peerUser"

# r = requests.get(url, data = data)
# results = r.json()
# print (results)

import requests, json

# bot_token = '1824370628:AAHrVNB7lz4iR0Txy9Ugd5Ek2uu6NK1APsc'
# chat_id = '863175437'
# text = "Choose:"
# reply_markup={"keyboard":[["Yes"],["Yes"],["Yes"],["Yes"],["Yes"],["Yes"],["Yes"],["Yes"],["Yes"]],"one_time_keyboard":True}
# data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
# url ="https://api.telegram.org/bot" + bot_token + "/sendMessage"

# r = requests.get(url, data = data)
# results = r.json()
# print (results)

url_doc = 'https://api.telegram.org/bot1732261163:AAH6fDLBs4L321L5AGreZC4RYA2g1srzrkI/sendDocument'
data = {"chat_id": 863175437,"document":"https://drive.google.com/uc?export=download&id=1_PNuMnRcEFar3A3TUKZ26sYmbdiZd7Md"}
response = requests.post(url_doc, data=data)
print(response)
# #<div class="btn boxmen2" onclick="window.location.href='https://docs.google.com/uc?id=0B5-XmFIN8sjKQ2JxZWVUSDAxUlU&amp;export=download'"><i class="material-icons"></i>&nbsp; Download File</div>]
# "https://drive.google.com/uc?export=download&id=0B9ojglPaasIEWi11eFhRZW9GM0E"
#<button onclick="window.location.href = 'https://drive.google.com/file/d/1jRrVkqhzOvjnbTk71HBXq0trkBZHbwEs/view?usp=sharing'">DOWNLOAD <i aria-hidden="true" class="fa fa-download"></i></button>



# response = requests.get(url='https://www.ktunotes.in/?s=s3+eee', headers=None)
# print(response)
# soup = BeautifulSoup(response.content,"html.parser")
# li = soup.find("li")
# print(li)
#<a class="maxbutton-2 maxbutton maxbutton-main-buttons" href="https://drive.google.com/open?id=1_PNuMnRcEFar3A3TUKZ26sYmbdiZd7Md"><span class="mb-text">University Question Paper</span></a>
# from bs4 import BeautifulSoup
# import requests
  
# # Website URL
# URL = 'https://www.ktunotes.in/?s=s3+eee'
# response = requests.get(url='https://www.ktunotes.in/?s=s3+eee', headers=None)
# print(response)
# soup = BeautifulSoup(response.content,"html.parser")
# div = soup.find_all('li',{'class':'infinite-post'})
# print(div)
# val = requests.get("https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key=AIzaSyAFcqlPYJXtZI8YnchDuXXylCRoIi723rI")
# print(val.json())
#Your B-TECH with EC branch and 2019-2023th batch has been registered on MEC THRIKAKARA Please Note the codes for Students : MECSTU19-23EC1936 StudentRepresentative : MECREP19-23EC4700 Teacher : MECTEAC19-23EC3405



