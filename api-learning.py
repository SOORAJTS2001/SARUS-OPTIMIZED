
url_photo = "https://api.telegram.org/bot1864066235:AAESrmaoeD0DKgCyPvXc022CUh7yuDkbZG4/sendDocument"



import requests, json

bot_token = '1864066235:AAESrmaoeD0DKgCyPvXc022CUh7yuDkbZG4'
chat_id = '1143248192'
text = "Choose:"
reply_markup={"InlineKeyboardButton":True,"callback_data":'example'}
data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
url ="https://api.telegram.org/bot" + bot_token + "/sendMessage"

r = requests.get(url, data = data)
results = r.json()
print(results)
# print (results)https://drive.google.com/uc?export=download&id=1_PNuMnRcEFar3A3TUKZ26sYmbdiZd7Md
# import requests
# data = {"chat_id": 1143248192,"caption":'Hi da pizza veno???',"document":"https://drive.google.com/uc?export=download&id=1_PNuMnRcEFar3A3TUKZ26sYmbdiZd7Md"}
# response = requests.post(url_photo, data=data)
# print(response)