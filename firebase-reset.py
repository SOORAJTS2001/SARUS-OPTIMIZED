from __future__ import division
import firebase,requests
firebase = firebase.FirebaseApplication('https://pi-saurus-default-rtdb.firebaseio.com/', None)
subject_details = "{'MAT':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],''],'DCMT':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],'AgACAgUAAxkBAAIFYGCifOPndbOiNrbiq2jUM2o1UH2ZAAKgrDEbh6YRVfBpemrqMDvFMgKxbnQAAwEAAwIAA20ABAUFAAEfBA'],'EMT':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],'AgACAgUAAxkBAAIFYWCifPgi-43KMDetRf8GhGmcrnLsAAKhrDEbh6YRVR2AMBXotxb_dcQYb3QAAwEAAwIAA20AAyylBAABHwQ'],'DEC':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],'AgACAgUAAxkBAAIFYmCifPhdwa7hww1NddZUiWzTiuFyAAKirDEbh6YRVf9CA6kiF-VkHJ5Sc3QAAwEAAwIAA20AA9XBAQABHwQ'],'PFET':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],'AgACAgUAAxkBAAIFXmCifB3zQhwFcYq5IP2WF2Ij-ZgQAAKdrDEbh6YRVYEY-syxkxJk7johbXQAAwEAAwIAA20AA8I-BgABHwQ'],'COI':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],'AgACAgUAAxkBAAIFX2CifONqzFL9SS6ADZfNQgy2rd-iAAKfrDEbh6YRVbtkCVUZBM_fRJFPc3QAAwEAAwIAA20AAwytAQABHwQ'],'EML':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],'AgACAgUAAxkBAAIFY2CifPj9EUcTAXJv3Qj77VKUHZ6WAAKjrDEbh6YRVSszmxWdLo5m7vHnbnQAAwEAAwIAA3kAA563BAABHwQ'],'DECL':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],'AgACAgUAAxkBAAIFZGCifPhEc5TJKvzfAkQ-Rxw3VKXfAAKkrDEbh6YRVW952gbPfqSVplYdb3QAAwEAAwIAA3kAA7C-BAABHwQ'],'HONO':[[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],''],[[],[],[],'']],'KTU':[[[],[],[],'']]}"
TOKEN = "1743202476:AAE4D2DLPFoMWKpl5jfWEuKpLCJko6DskVA"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
url_photo = "https://api.telegram.org/bot{}/sendPhoto".format(TOKEN)
data ={
    'dict_data':subject_details
}
#sended = firebase.post('/python-example-1/Students',data)
# recieved = firebase.get('/python-example-1/Students/-M_eqP9DM5qA1ElTxk2d', '')
# print(recieved['dict_data'],"Recieved")
# subject_dic = eval(recieved['dict_data'])
# subject_dic['MAT'][0][0].append("This is the file location")
# firebase.put('/python-example-1/Students/-M_eqP9DM5qA1ElTxk2d','dict_data',subject_details)
# print("Database resetted!!!!")
data = {
'stored-data':"{}"
}
college_name ='TKM COLLEGE OF ENGINEERING,KOLLAM'
course = 'B'
branch_name = 'C'
batch = 'D'
division_name = 'E'
print(firebase.patch(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}',data))
# subject_dic = eval(subject_details)
# print(subject_dic.keys())
# recieved = firebase.get('/python-example-1/Students/-M_eqP9DM5qA1ElTxk2d', '')
# subject_dic = eval(recieved['dict_data'])
# def send_images(mat_list,chat_id):
#     for lis in mat_list:
#         data = {"chat_id": chat_id,"caption":'',"photo":lis}
#         response = requests.post(url_photo, data=data)#to send photo files={"photo": image_file}
#         #print(response)
#         print(response)
# send_images(subject_dic['DCMT'][0][0],863175437)