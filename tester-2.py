#to send location
#https://api.telegram.org/bot1864066235:AAESrmaoeD0DKgCyPvXc022CUh7yuDkbZG4/sendLocation?chat_id=1143248192&latitude=9.995002&longitude=76.305746
#to delete message
#https://api.telegram.org/bot1864066235:AAESrmaoeD0DKgCyPvXc022CUh7yuDkbZG4/deleteMessage?chat_id=1143248192&message_id=22
# import urllib.request
# import urllib.parse
import firebase
firebase = firebase.FirebaseApplication('https://pi-saurus-default-rtdb.firebaseio.com/')
fireget = firebase.get('STORED-DATA/',None)
for key in fireget:
    print(key)
    for key_1 in fireget[key]:
        print(key_1)
        for key_2 in fireget[key][key_1]:
            print(key_2)
            for key_3 in fireget[key][key_1][key_2]:
                print(fireget[key][key_1][key_2])
                print(key_3)
                for key_4 in fireget[key][key_1][key_2][key_3]:
                    print(key_4)
                    break

# def sendSMS(apikey, numbers, sender, message):
#     data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
#         'message' : message, 'sender': sender})
#     data = data.encode('utf-8')
#     request = urllib.request.Request("https://api.txtlocal.com/send/?")
#     f = urllib.request.urlopen(request, data)
#     fr = f.read()
#     return(fr)

# resp =  sendSMS('Nzg3MTZhNzk1NjRkNDM1MTQ4NGU3OTMwNjg2ZTc5NGI=', '+91-94470 01453',
#     'Jims Autos', 'This is your message')
# print (resp)
# importing the client from the twilio
# from twilio.rest import Client
# # Your Account Sid and Auth Token from twilio account
# account_sid = "AC375bb213484a56d4d54654bbdfd7005c"
# auth_token = "3bd26b894fbee4f09c7b17c55235fc4e"
# # instantiating the Client
# client = Client(account_sid, auth_token)
# # sending message
# message = client.messages.create(body='Hi there! How are you?', from_=+17738393836, to=+916282143473)
# # printing the sid after success
# print(message.sid)
