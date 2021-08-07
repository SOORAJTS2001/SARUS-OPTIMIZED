import firebase,requests,json,re,urllib,time,wikipedia,urllib.request,traceback
#https://api.telegram.org/bot1732261163:AAH6fDLBs4L321L5AGreZC4RYA2g1srzrkI/sendMessage?text=Hello%20%3Cb%3Ehai%3C/b%3E&chat_id=863175437&parse_mode=HTML
from datetime import date
from bs4 import BeautifulSoup
now = date.today()
today_date = now.strftime("%B %d, %Y")
firebase = firebase.FirebaseApplication('https://pi-saurus-default-rtdb.firebaseio.com/')
TOKEN = "1732261163:AAH6fDLBs4L321L5AGreZC4RYA2g1srzrkI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
url_photo = "https://api.telegram.org/bot{}/sendPhoto".format(TOKEN)
url_doc = "https://api.telegram.org/bot{}/sendDocument".format(TOKEN)
url_sticker = "https://api.telegram.org/bot{}/sendSticker".format(TOKEN)
material_uploaders = {}
text_uploaders = {}
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
def send_images(mat_list,chat_id):
    for lis in mat_list:
        data = {"chat_id": chat_id,"caption":'',"photo":lis[1]}
        print(type(lis[1]))
        print(lis[1])
        response = requests.post(url_photo, data=data)#to send photo files={"photo": image_file}
        print(response)
def send_images_url(image_list,chat_id):
    for image in image_list:
        data = {"chat_id": chat_id,"caption":'',"photo":image}
        response = requests.post(url_photo, data=data)#to send photo files={"photo": image_file}
    print(response)
def send_message_html(title,summary,chat_id):
    url = URL + "sendMessage?text=<b>{}</b>\n<I>{}</I>&chat_id={}&parse_mode=HTML".format(title,summary,chat_id)
    get_url(url)
def send_doc(mat_list,chat_id):
    for lis in mat_list:
        data = {"chat_id": chat_id,"document":lis[1]}
        response = requests.post(url_doc, data=data)
        print(response)
def send_doc_url(mat_list,chat_id):
    for lis in mat_list:
        data = {"chat_id": chat_id,"document":lis}
        response = requests.post(url_doc, data=data)
        print(response)
def send_text(mat_list,chat_id):
    all_text = 'These are the text materials/links \n'
    for lis in mat_list:
        lis = '\n' +lis +'\n'
        all_text = all_text + lis 
    url = URL + "sendMessage?text={}&chat_id={}".format(all_text, chat_id)
    response = requests.get(url)
    print(response)
def send_reply(message_id,chat_id,text):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&reply_to_message_id={}&chat_id={}".format(text,message_id,chat_id)
    get_url(url)
def scrap_images(query):
    url = f'http://www.google.com/search?q={query}&tbm=isch'
    response = requests.get(url=url, headers=None)
    soup = BeautifulSoup(response.content,"html.parser")
    images = soup.find_all("img")
    image_list = []
    count = 0
    for image in images:
        count +=1
        image_list.append(image['src'])
        if count == 6:
            break
    return image_list
def scrap_google(query):
    empty = []
    query = query.replace(' ', '+')
    url = f'https://google.com/search?q={query}'
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    raw_response = urllib.request.urlopen(request).read()
    html = raw_response.decode("utf-8")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.select("#search div.g")
    for div in divs:
        results = div.select("a")
        if (len(results) >= 1):
            details = results[0].get('href')
            empty.append(details)
        else:
            empty = 200
            return empty
    return empty
def scrap_youtube(query):
    query = query.replace(' ','+')
    response = requests.get(f"https://www.youtube.com/results?search_query={query}")
    soup = BeautifulSoup(response.text,'lxml')
    script = soup.find_all("script")[32]
    json_text = re.search('var ytInitialData = (.+)[,;]{1}',str(script)).group(1)
    json_data = json.loads(json_text)
    content = (
        json_data
        ['contents']['twoColumnSearchResultsRenderer']
        ['primaryContents']['sectionListRenderer']
        ['contents'][0]['itemSectionRenderer']
        ['contents'])
    tube_data = []
    count = 0
    for data in content:
        for key,value in data.items():
            if type(value) is dict and count<5:
                empty = []
                for k,v in value.items(): 
                    """
                        https://www.youtube.com/watch?v=J2npVg9ONFo
                        https://i.ytimg.com/vi/J2npVg9ONFo/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLBsvSjLFmd8SfSKut7NXhiUm0zMFg
                        Ford F150 Lightning Impressions: Better Than I Thought!
                        5,635,927 views
                        Marques Brownlee 
                    """
                    # Gets the title for the video the title prints as 3rd object in the group
                    try:
                        if k == "title": 
                            empty.append(v["runs"][0]["text"])
                    except: 
                        pass
                    #  Gets video id and appends it to make a clickable link
                    if k == "videoId" and len(v) == 11:
                        empty.append("https://www.youtube.com/watch?v="+v)
                    # Youtube channel owner text
                    if k == "ownerText":
                        empty.append(v["runs"][0]["text"])
                    # Thumbnail link 
                    # Shows the views as a string like: "123 views"
                    if k == "viewCountText":
                        empty.append(v["simpleText"])
                tube_data.append(empty)
            count +=1
    return tube_data
def ktu_notes_scraper(query):
    result = requests.get(f"https://www.ktunotes.in/?s={query}")
    #  Giving time for website to load
    time.sleep(1)
    src= result.content
    soup = BeautifulSoup(src,'lxml')
    links = soup.find_all(rel = "bookmark")
    go_list = [links[0].attrs['href']]
    print(links[0].attrs['href'].split("/")[3])
    for go_link in go_list:
        empty = []
        result = requests.get(go_link)
        src = result.content
        soup = BeautifulSoup(src,'lxml')
        links = soup.find_all("a", {"class": "maxbutton-2 maxbutton maxbutton-main-buttons"})
        count = 0
        for link in links:
            count += 1
            # print(link.attrs['href'])
            glink = link.attrs['href']
            hey = glink.split('=')
            # print(hey[1])
            if count <=3:
                try:
                    download_link = f"https://drive.google.com/uc?export=download&id={hey[1]}"
                    empty.append(download_link)
                except:
                    empty.append(' ')
        return empty
def send_inlineKeyBoard_All(chat_id,text,option_list):
    reply_markup={"keyboard":option_list,"one_time_keyboard":False}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    url ="https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    r = requests.get(url, data = data)
    print(f"Tried to send an inline button,but result is{r}")
def bot_respond(updates):
    try:
        for update in updates["result"]:
            if 'message' in update:
                chat_id = update["message"]["chat"]["id"]
                if 'text' in update['message']:
                    print("Identified as text")
                    student_codes = firebase.get('SPECIALCODES','Student-codes')
                    student_dict_codes = eval(student_codes)
                    text = update["message"]["text"]
                    upload_match = re.match(r'^(UP-|UPL-|UPLOA-|UPLOAD-)',text,re.I)
                    delete_media = re.match(r'^(PLEASE-DELETE-THIS)',text,re.I)
                    delete_module = re.match(r'^(DELETE-)',text,re.I)
                    all_students = eval(firebase.get('MYSTUDENTS','AllStudents'))
                    if text in  student_dict_codes:
                        print("So not for uploading")  
                        students_dic = all_students
                        if  chat_id in students_dic:
                            send_message("Hey!You have been already registered",chat_id)
                        else:
                            print("New registration")
                            if 'Admin' in student_dict_codes[text]:
                                college_name = student_dict_codes[text][0]
                            else:
                                college_name = student_dict_codes[text][0]
                                course = student_dict_codes[text][1]
                                branch_name = student_dict_codes[text][2]
                                batch = student_dict_codes[text][3]
                                division_name = student_dict_codes[text][4]
                                students_in_class = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','Students-in-class'))
                            students_dic_val = student_dict_codes[text]
                            if students_dic_val[len(students_dic_val)-1] =='Admin':
                                students_dic[chat_id] = students_dic_val
                                send_message(f"Congragulations!!You have been Registered to {students_dic_val[0]},You have access of Admin",chat_id)
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do?",[['send to all in college'],["create form free registration"],["form free registration status"],['send me updates'],['Cancel']])
                            elif students_dic_val[len(students_dic_val)-1] =='Student':
                                students_dic[chat_id] = students_dic_val
                                students_in_class[chat_id]=[college_name,course,branch_name,batch,division_name]
                                send_message(f"Congragulations!!You have been Registered to {students_dic_val[0]} in {students_dic_val[1]} course of {students_dic_val[2]} branch  in {students_dic_val[3]} batch of {students_dic_val[4]} class \n You have access of {students_dic_val[len(students_dic_val)-1]}",chat_id)
                                send_message("Now please send your name,phone-no and email address seperated by commas",chat_id)
                                text_uploaders[chat_id] = [college_name,course,branch_name,batch,division_name,[],'Data-Collection']
                                firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','Students-in-class',str(students_in_class))
                            elif students_dic_val[len(students_dic_val)-1] =='Representative':
                                students_dic[chat_id] = students_dic_val
                                students_in_class[chat_id]=[college_name,course,branch_name,batch,division_name]
                                send_message(f"Congragulations!!You have been Registered to {students_dic_val[0]} in {students_dic_val[1]} course of {students_dic_val[2]} branch in {students_dic_val[3]} batch of {students_dic_val[4]} class \n You have access of {students_dic_val[len(students_dic_val)-1]}",chat_id)
                                send_message("Now please send your name,phone-no and email address seperated by commas",chat_id)
                                text_uploaders[chat_id] = [college_name,course,branch_name,batch,division_name,[],'Data-Collection']
                                firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','Students-in-class',str(students_in_class))
                            elif students_dic_val[len(students_dic_val)-1] =='Teacher':
                                students_dic[chat_id] = students_dic_val
                                send_message(f"Congragulations!!You have been Registered to {students_dic_val[0]} in {students_dic_val[1]} course of {students_dic_val[2]} branch in {students_dic_val[3]} batch of {students_dic_val[4]} class \n You have access of {students_dic_val[len(students_dic_val)-1]}",chat_id)
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do?",[['get materials'],['get material form web'],["add subject"],["send to your class"],['google doubt'],['clear my doubt'],['youtube my doubt'],['Cancel']])
                                firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','Students-in-class',str(students_in_class))
                            firebase.put('MYSTUDENTS','AllStudents',str(students_dic))
                        #'TKMSTU19-23EEE2627': ['TKM COLLEGE OF ENGINEERING,KOLLAM', 'B-TECH', 'EEE', '2019-2023', 'B', 'Student']
                    elif text not in student_dict_codes and chat_id not in all_students:
                        send_message("Hey!!Your are not authorized to chat with me,kindly give the code or leave",chat_id)
                    elif chat_id in all_students:
                        print("Verified as in the pool of registered students")
                        if 'Admin' in all_students[chat_id]:
                            college_name = all_students[chat_id][0]
                        else:
                            college_name = all_students[chat_id][0]
                            course = all_students[chat_id][1]
                            branch_name = all_students[chat_id][2]
                            batch = all_students[chat_id][3]
                            division_name = all_students[chat_id][4]
                            subject_dic = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data'))
                        Session = eval(firebase.get(f'STORED-DATA/{college_name}/','Sessions'))
                        if text=='Done' and chat_id in material_uploaders:
                            #[college_name,course,branch_name,batch,division_name,subject,module,[[],[],[]],[[],[]],'Study-Materials']
                            #for study materials [college_name,course,branch_name,batch,division_name,subject,module,[[],[],[]],[[],[]],'Study-Materials']
                            if 'Study-Materials' in material_uploaders[chat_id]:
                                subject = material_uploaders[chat_id][5]
                                module = int(material_uploaders[chat_id][6])
                                meta_data = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','meta-data'))
                                data = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data'))
                                for images in material_uploaders[chat_id][7][0]:
                                    if material_uploaders[chat_id][7][0] != '':
                                        data[subject][module-1][0].append(images)
                                        meta_data['photo_size'] += material_uploaders[chat_id][8][0]
                                        print("added images")
                                for doc in material_uploaders[chat_id][7][1]:
                                    if material_uploaders[chat_id][7][1] != '':
                                        data[subject][module-1][1].append(doc)
                                        meta_data['doc_size'] += material_uploaders[chat_id][8][1]
                                        print("docs added")
                                for text in material_uploaders[chat_id][7][2]:
                                    if material_uploaders[chat_id][7][2] != '':
                                        data[subject][module-1][2].append(text)
                                        print("added text")
                                data[subject][module-1].pop()
                                data[subject][module-1].append(today_date)
                                firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data',str(data))
                                photo_no = material_uploaders[chat_id][8][2]
                                doc_no = material_uploaders[chat_id][8][3]
                                text_no = material_uploaders[chat_id][8][4]
                                del material_uploaders[chat_id]
                                print("You have been deleted from chat backup")
                                send_message(f"Materials has been updated..and received {photo_no} photo(s),{doc_no} file(s) and {text_no} text or links",chat_id)
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do",[["Command Me"]])
                            elif 'Send-To-Class' in material_uploaders[chat_id]: 
                                #for send to class [college_name,course,branch_name,batch,division_name,[[],[],[],''],[0,0,0,0,0],'Send-To-Class']                        
                                students_in_class = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','Students-in-class'))
                                images = material_uploaders[chat_id][5][0]
                                files = material_uploaders[chat_id][5][1]
                                text = material_uploaders[chat_id][5][2]
                                for chat in students_in_class:
                                    send_message("Hi there,You got a message form the teacher",chat)
                                    send_images(images,chat)
                                    send_doc(files,chat)
                                    send_text(text,chat)
                                send_message("Successfully send all the materials to students in class",chat_id)
                                del material_uploaders[chat_id]
                                print("You have been deleted from chat backup") 
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do",[["Command Me"]])  
                            elif 'Send-To-All' in material_uploaders[chat_id]:
                                # for send to all [college_name,[[],[],[],''],[0,0,0,0,0],'Send-To-All']
                                images = material_uploaders[chat_id][1][0]
                                files = material_uploaders[chat_id][1][1]
                                text = material_uploaders[chat_id][1][2]
                                for chat in all_students:
                                    if 'Admin' not in all_students[chat]:
                                        send_message("Hi there,You got a message from the college admin",chat)
                                        send_images(images,chat)
                                        send_doc(files,chat)
                                        send_text(text,chat)
                                send_message("Successfully send all the materials to the whole college",chat_id)
                                del material_uploaders[chat_id]
                                print("You have been deleted from chat backup") 
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do",[["Command Me"]])
                            elif 'Form Free Registration' in material_uploaders[chat_id]:
                                print("trying to send form free reg")
                                print(material_uploaders)
                                images = material_uploaders[chat_id][2][0]
                                files = material_uploaders[chat_id][2][1]
                                text = material_uploaders[chat_id][2][2]
                                event_name = material_uploaders[chat_id][1]
                                Session =  eval(firebase.get(f'STORED-DATA/{college_name}/','Sessions'))
                                Session[event_name] = [[images,files,text],[]]
                                firebase.put(f'STORED-DATA/{college_name}/','Sessions',str(Session))
                                for chat in all_students:
                                    if 'Admin' not in all_students[chat]:
                                        send_message("Hi there,You got an event registration from college",chat)
                                        send_images(images,chat)
                                        send_doc(files,chat)
                                        send_text(text,chat)
                                        send_inlineKeyBoard_All(chat,"Do you want to register for this event",[[f"Yes I Want To Register For {event_name}"],["Cancel"]])
                                send_message("Successfully send all the materials to the whole college for event",chat_id)
                                del material_uploaders[chat_id]
                                print("You have been deleted from chat backup") 
                        elif text == 'Cancel':
                            if chat_id in material_uploaders:
                                del material_uploaders[chat_id]
                                send_message("Ohk materials deleted",chat_id)
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do",[["Command Me"]])
                            else:    
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do",[["Command Me"]])   
                        elif re.match(r'^(Yes I Want To Register For)',text):
                            event_name = text.split(' ')[6]
                            students_in_class = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','Students-in-class'))
                            name = students_in_class[chat_id][len(students_in_class[chat_id])-3]
                            phone_no = students_in_class[chat_id][len(students_in_class[chat_id])-2]
                            email = students_in_class[chat_id][len(students_in_class[chat_id])-1]
                            Session =  eval(firebase.get(f'STORED-DATA/{college_name}/','Sessions'))
                            Session[event_name][1].append([name,phone_no,email,batch,branch_name,college_name])
                            send_message("You have been registered",chat_id)
                            send_inlineKeyBoard_All(chat_id,"What do you want me to do",[["Command Me"]])
                            firebase.put(f'STORED-DATA/{college_name}/','Sessions',str(Session))
                        elif chat_id in material_uploaders and text!='Done':
                            if 'Study-Material' in material_uploaders[chat_id]:
                                material_uploaders[chat_id][7][2].append(text)
                            elif 'Send-To-Class' in material_uploaders[chat_id]:
                                material_uploaders[chat_id][5][2].append(text)
                            elif 'Form Free Reg' in material_uploaders[chat_id]:
                                material_uploaders[chat_id] = [college_name,text,[[],[],[]],'Form Free Registration']
                                print("got the event name")
                                send_inlineKeyBoard_All(chat_id,"Now you can upload what to send",[["Done"],["Cancel"]])
                            elif 'Form Free Registration' in material_uploaders[chat_id]:
                                material_uploaders[chat_id][2][2].append(text) 
                        elif chat_id in text_uploaders and text!='Done':
                            if 'Data-Collection' in text_uploaders[chat_id]:
                                print("trying to give name")
                                students_in_class = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','Students-in-class'))
                                #name
                                students_in_class[chat_id].append(text.split(',')[0])
                                #mobile no
                                students_in_class[chat_id].append(text.split(',')[1])
                                #email address
                                students_in_class[chat_id].append(text.split(',')[2])
                                print("deleted from temp list")
                                del text_uploaders[chat_id]
                                firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','Students-in-class',str(students_in_class))
                                send_message("This is for form free registration,Thank you!!",chat_id)  
                                send_inlineKeyBoard_All(chat_id,"What should i do??",[["Command Me"]])
                            elif 'Add-Subject' in text_uploaders[chat_id]:
                                try:
                                    subject_name = text.split('-')[0].upper()
                                    subject_abbreviation = text.split('-')[1].upper()
                                    print("Teacher or Representative is trying to add subject")
                                    stored_data = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data'))
                                    if subject_name in stored_data:
                                        send_message("Hey!!Seems that it is already in the subject list...",chat_id)
                                    else:
                                        stored_data[subject_name] = []
                                        code_abbreviation = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','code-abbreviations'))
                                        code_abbreviation[subject_name] = subject_abbreviation
                                        firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data',str(stored_data))
                                        firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','code-abbreviations',str(code_abbreviation))
                                        send_message("Cool!!I have created the subject in my database..",chat_id)
                                        del text_uploaders[chat_id]
                                        print("Successfully deleted from temp list")
                                except:
                                    send_message(f"Please make sure that the format is same",chat_id)
                            elif 'Get-Material' in text_uploaders[chat_id] and text.isdigit():
                                subject_name = text_uploaders[chat_id][0]
                                module_no = int(text)
                                if module_no > 0:
                                    try:
                                        print(f"Got a request of {subject_name} module {module_no} ")
                                        send_images(subject_dic[subject_name][module_no-1][0],chat_id)
                                        send_doc(subject_dic[subject_name][module_no-1][1],chat_id)
                                        send_text(subject_dic[subject_name][module_no-1][2],chat_id)
                                        send_message(f"These materials was last updated on {subject_dic[subject_name][module_no-1][3]}",chat_id)
                                        del text_uploaders[chat_id]
                                        print("deleted from the temp")
                                    except:
                                        send_message("Seems that this module is not registered",chat_id)
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do now",[["Command Me"]])
                            elif 'Doubt-Clearance'  in text_uploaders[chat_id]:
                                query = text
                                data = ''
                                print(f"Got a help request of {query}")
                                send_images_url(scrap_images(query),chat_id)
                                try:
                                    page = wikipedia.page(query)
                                    send_message_html(page.title,wikipedia.summary(query,sentences=5),chat_id)
                                except Exception as e: 
                                    print(f"{query} query got an exception of {e}") 
                                    send_message(f"Your description for {query} is not found at this moment,please try another",chat_id)
                                del text_uploaders[chat_id]
                            elif 'Google-Doubt'  in text_uploaders[chat_id]:
                                query = text
                                print(f"Trying to google {query}")
                                results = scrap_google(query)
                                print(f"Got the result of {query}")
                                for result in results:
                                    send_message(result,chat_id)
                                del text_uploaders[chat_id]
                            elif 'Youtube-Doubt'in text_uploaders[chat_id]:
                                query = text
                                data = ''
                                print(f"Trying to youtube {query}")
                                for you_list in scrap_youtube(query):
                                    for details in you_list:
                                        details = details + '\n'
                                        data = data + details
                                    send_message(data,chat_id)
                                    data = ''
                                del text_uploaders[chat_id]
                            elif 'Web-Material' in text_uploaders[chat_id]:
                                query = text
                                send_doc_url(ktu_notes_scraper(query),chat_id)
                                del text_uploaders[chat_id]
                        elif text in Session and 'Admin' in all_students[chat_id]:
                                data = ''
                                print(Session[text][1])
                                for all_details in Session[text][1]:
                                    for detail in all_details:
                                        detail = detail+ '\n'
                                        data = data + detail
                                    data = data + '\n'+ '\n'
                                send_message(data,chat_id)
                        elif upload_match and len(text.split('-'))>=3:
                            meta_data = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','meta-data'))
                            print("Trying to upload")
                            subject = text.split('-')[1].upper()
                            module = [letters for letters in text.split('-')[2] if letters.isdigit()][0]
                            if subject in subject_dic:
                                if len(subject_dic[subject])-1 >= int(module):
                                    material_uploaders[chat_id] = [college_name,course,branch_name,batch,division_name,subject,module,[[],[],[],''],[0,0,0,0,0],'Study-Materials']
                                else:
                                    print("So need to create module")
                                    for sub in range(len(subject_dic[subject]),int(module)):
                                        empty_sub = [[],[],[],'']
                                        subject_dic[subject].append(empty_sub)
                                firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data',str(subject_dic))
                                print("extended the modules")
                                material_uploaders[chat_id] = [college_name,course,branch_name,batch,division_name,subject,module,[[],[],[],''],[0,0,0,0,0],'Study-Materials']    
                                send_inlineKeyBoard_All(chat_id,"Hey,You can upload materials now,press Done when it is done!!",[["Done"],["Cancel"]])
                            #send_message(f"Succesfully Created {int(module_no[0])} module of {subject} subject \n recieved {photo} photo(s) {file} files and {textes} text or links",chat_id)
                            else:
                                send_message("Hey seems that this subject has not been registered by your Teacher or Representative..",chat_id)
                        elif text=='Command Me':
                            if 'Admin' in all_students[chat_id]:
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do?",[['send to all in college'],["create form free registration"],["form free registration status"],['send me updates'],['Cancel']])
                            elif 'Teacher' in all_students[chat_id]:
                                send_inlineKeyBoard_All(chat_id," want me to do?",[['get materials'],['get material form web'],["add subject"],["send to your class"],['google doubt'],['clear my doubt'],['youtube my doubt'],['Cancel']])
                            elif 'Representative' in all_students[chat_id]:
                                send_inlineKeyBoard_All(chat_id,"What do you want me to do?",[['get materials'],['get material form web'],["add subject"],['google doubt'],['clear my doubt'],['youtube my doubt'],['Cancel']])
                            elif 'Student' in all_students[chat_id]:
                                send_inlineKeyBoard_All(chat_id," want me to do?",[['get materials'],['get material from web'],['google doubt'],['clear my doubt'],['youtube my doubt'],['Cancel']])
                        elif text =='send to your class' and 'Teacher' in all_students[chat_id]:
                            material_uploaders[chat_id] = [college_name,course,branch_name,batch,division_name,[[],[],[],''],[0,0,0,0,0],'Send-To-Class']
                            send_inlineKeyBoard_All(chat_id,"Hey,You can upload messages now,where there it is images files etc,please press done at last",[["Done"],["Cancel"]])
                        elif text =='send to all in college' and 'Admin' in all_students[chat_id]:
                            material_uploaders[chat_id] = [college_name,[[],[],[],''],[0,0,0,0,0],'Send-To-All']
                            send_inlineKeyBoard_All(chat_id,"Hey,You can upload messages now,where there it is images files etc,please press done at last",[["Done"],["Cancel"]])
                        elif text == 'create form free registration'and 'Admin' in all_students[chat_id]:
                            material_uploaders[chat_id] = ['Form Free Reg']
                            send_message("please send the evet name",chat_id)
                            print(material_uploaders)
                        elif text == 'form free registration status' and 'Admin' in all_students[chat_id]:
                            college_name = all_students[chat_id][0]
                            Session =  eval(firebase.get(f'STORED-DATA/{college_name}/','Sessions'))
                            print("asked about the form free reg status")
                            empty = []
                            session_names = list(Session.keys())
                            for names in session_names:
                                empty.append([names])
                            empty.append(['Cancel'])    
                            print(empty)
                            send_inlineKeyBoard_All(chat_id,"These are the sessions I have",empty)
                        elif text == "add subject" and ('Teacher' in all_students[chat_id] or 'Representative' in all_students[chat_id]):   
                            text_uploaders[chat_id] = [college_name,course,branch_name,batch,division_name,'Add-Subject']
                            send_message("Sure!!,Now please tell the subject name along with its abbreviation like mat-maths",chat_id)
                        elif text == 'get materials':
                            empty = []
                            for key in subject_dic:
                                empty.append([key])
                            empty.append(['Cancel'])
                            send_inlineKeyBoard_All(chat_id,"Sure Please select a subject",empty)
                        elif text == 'clear my doubt':
                            text_uploaders[chat_id] = ['Doubt-Clearance']
                            send_message("Sure!!,what is your doubt??",chat_id)
                        elif text == 'google doubt':
                            text_uploaders[chat_id] = ['Google-Doubt']
                            send_message("Sure!!,what is your doubt to google??",chat_id)
                        elif text =='youtube my doubt':
                            text_uploaders[chat_id] = ['Youtube-Doubt']
                            send_message("Sure!!,what is your doubt??",chat_id)
                        elif text == 'get material from web':
                            text_uploaders[chat_id] = ['Web-Material']
                            send_message("Which portion do you want??",chat_id)
                        elif text in subject_dic:
                            empty = []
                            for key in range(1,len(subject_dic[text])+1):
                                empty.append([str(key)])
                                print(key)
                            empty.append(['Cancel']) 
                            print(empty)   
                            send_inlineKeyBoard_All(chat_id,"Sure Please select the module",empty)
                            text_uploaders[chat_id] = [text,'Get-Material']
                        elif text == 'send me updates':
                            meta_data = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','meta-data'))
                            #'photo_size':0,'doc_size':0,'photo_no':0,'doc_no':0,'nsfw_alerts':0,'customers':0,'buzzword':''}"
                            send_message(f"So far I have {len(all_students)} registered members.. {meta_data['photo_no']} Photos,size of {meta_data['photo_size']} MB and {meta_data['doc_no']} Files of size {meta_data['doc_size']} MB and {meta_data['links']} links",chat_id)
                        elif delete_module and len(text.split('-'))==3:
                            print("Trying to delete the module")    
                            module_no = int([ letter for letter in text.split('-')[2] if letter.isdigit()][0])
                            subject = text.split('-')[1].upper()
                            if module_no and module_no > 0:
                                student_data = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data'))
                                if subject in student_data:
                                    student_data[subject].pop(module_no-1)
                                    firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data',str(student_data))
                                    send_message(f"Successfully deleted {module_no} module of {subject} subject",chat_id)
                                else:
                                    send_message(f"subject is not found!!",chat_id)
                        elif delete_module and len(text.split('-'))==2:
                            print("delete the subject")
                            subject = text.split('-')[1].upper()
                            student_data = eval(firebase.get(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data'))
                            if subject in student_data:
                                student_data.pop(subject)
                                firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data',str(student_data))
                                send_message(f"Sucessfully deleted the {subject} subject ",chat_id)
                            else:
                                send_message("Subject not found!!",chat_id)
                        elif delete_media:
                            print("Into deletion")
                            if all_students[chat_id][len(all_students[chat_id])-1] == 'Representative' or all_students[chat_id][len(all_students[chat_id])-1] == 'Teacher':
                                print("Acess given to deletion")
                                if "reply_to_message" in update['message']:
                                    print("Identified the message")
                                    if "photo" in update['message']['reply_to_message']:
                                        print("Identified the photo")
                                        delete_photo_unique_id = update["message"]["reply_to_message"]['photo'][0]['file_unique_id']
                                        print("this is the photo to be deleted")
                                        print(delete_photo_unique_id)
                                        for key,value in subject_dic.items():
                                            if len(value)>0:
                                                for val in value:
                                                    print("This is the pool of values\n")
                                                    print("\n")
                                                    for id in val[0]:
                                                        if delete_photo_unique_id in id:
                                                            val[0].remove(id)
                                                            firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data',str(subject_dic))
                                                            send_message("Successfully removed the photo!!",chat_id)                                                       
                                    elif "document" in update['message']['reply_to_message']:
                                        print("Identified the document")
                                        delete_doc_unique_id = update["message"]["reply_to_message"]['document']["file_unique_id"]
                                        print("this is the doc to be deleted")
                                        print(delete_doc_unique_id)
                                        for key,value in subject_dic.items():
                                            if len(value)>0:
                                                for val in value:
                                                    print("This is the pool of values\n")
                                                    print("\n")
                                                    for id in val[1]:
                                                        if delete_doc_unique_id in id:
                                                            val[1].remove(id)
                                                            firebase.put(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}','stored-data',str(subject_dic))
                                                            send_message("Successfully removed the document!!",chat_id)                 
                                    else:
                                        send_message("Please tag any images or docs",chat_id)
                            else:
                                send_message("Hey!!You dont have permission to delete any media!!",chat_id)
                        else:
                            (chat_id,"Please choose one",[["What do you want me to do"]]) 
                elif 'photo' in update['message'] and chat_id in material_uploaders:
                    Photo_id = update['message']['photo'][0]['file_id']
                    Photo_unique_id = update['message']['photo'][0]["file_unique_id"]
                    photo_size = update['message']['photo'][0]["file_size"]
                    if 'Study-Materials' in material_uploaders[chat_id]:
                        print("trying to upload images")
                        #[college_name,course,branch_name,batch,division_name,subject,module,[[],[],[]],[[],[],[],[],[]],'Study-Materials']
                        material_uploaders[chat_id][7][0].append((Photo_unique_id,Photo_id))
                        material_uploaders[chat_id][8][0]+=round(photo_size/10**6,2)
                        material_uploaders[chat_id][8][2]+=1
                        print(material_uploaders)
                    elif 'Send-To-Class' in material_uploaders[chat_id]:
                        print("trying to upload images to send to class")
                        #[college_name,course,branch_name,batch,division_name,subject,module,[[],[],[]],[[],[],[],[],[]],'Study-Materials']
                        material_uploaders[chat_id][5][0].append((Photo_unique_id,Photo_id))
                        material_uploaders[chat_id][6][0]+=round(photo_size/10**6,2)
                        material_uploaders[chat_id][6][2]+=1
                        print(material_uploaders)
                    elif 'Send-To-All'in material_uploaders[chat_id]:
                        print("trying to upload images to send to all")
                        material_uploaders[chat_id][1][0].append((Photo_unique_id,Photo_id))
                        material_uploaders[chat_id][2][0]+=round(photo_size/10**6,2)
                        material_uploaders[chat_id][2][2]+=1
                    elif 'Form Free Registration'in material_uploaders[chat_id]:
                        material_uploaders[chat_id][2][0].append((Photo_unique_id,Photo_id))
                elif 'document' in update['message'] and chat_id in material_uploaders:
                    Doc_id = update['message']['document']['file_id']
                    Doc_unique_id= update['message']['document']["file_unique_id"]
                    doc_size = update['message']['document']["file_size"]
                    if 'Study-Materials' in material_uploaders[chat_id]:
                        print("trying to upload docs")
                        #[college_name,course,branch_name,batch,division_name,subject,module,[[],[],[]],[[],[],[],[],[]],'Study-Materials']
                        material_uploaders[chat_id][7][1].append((Doc_unique_id,Doc_id))
                        material_uploaders[chat_id][8][1]+=round(doc_size/10**6,2)
                        material_uploaders[chat_id][8][3]+=1
                        print(material_uploaders)
                    elif 'Send-To-Class' in material_uploaders[chat_id]:
                        print("trying to upload docs to send to class")
                        #[college_name,course,branch_name,batch,division_name,subject,module,[[],[],[]],[[],[],[],[],[]],'Study-Materials']
                        material_uploaders[chat_id][5][1].append((Doc_unique_id,Doc_id))
                        material_uploaders[chat_id][6][1]+=round(doc_size/10**6,2)
                        material_uploaders[chat_id][6][3]+=1
                        print(material_uploaders)
                    elif 'Send-To-All' in material_uploaders[chat_id]:
                        print("trying to upload docs to send to all")
                        #[college_name,course,branch_name,batch,division_name,subject,module,[[],[],[]],[[],[],[],[],[]],'Study-Materials']
                        material_uploaders[chat_id][1][1].append((Doc_unique_id,Doc_id))
                        material_uploaders[chat_id][2][1]+=round(doc_size/10**6,2)
                        material_uploaders[chat_id][2][3]+=1
                        print(material_uploaders)
                    elif 'Form Free Registration'in material_uploaders[chat_id]:
                        material_uploaders[chat_id][2][1].append((Doc_unique_id,Doc_id))
    except Exception as a:
        print(f"Error!!!:I have been crashed due to {a} at {traceback.format_exc()}")
        send_message(f"Error!!!:I have been crashed due to {a} at {traceback.format_exc()}",863175437)
def main():
    last_update_id = None
    while 1:
        print("Running")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            bot_respond(updates)
if __name__ == '__main__':
    main()