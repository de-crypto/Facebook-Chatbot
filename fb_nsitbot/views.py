from django.shortcuts import render
# Create your views here.
# yomamabot/fb_yomamabot/views.py
import json , re, random
import requests
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import sqlite3


#database connectivity
dbconect=sqlite3.connect('db.sqlite3')
#create a database cursor
cur=dbconect.cursor()
#creating table in the database
cur.execute('DROP TABLE IF EXISTS Reply ')
cur.execute('CREATE TABLE Reply (recieve TEXT PRIMARY KEY, send TEXT );')
cur.close()

#TOKEN provided from FB to access the local server
PAGE_ACCESS_TOKEN = "EAAIySNmDLe0BAFCjxHDZBbg7wIVdxytOvq45vWjF3D5AVqF9rZCamwZBtthmBzNAzKqLyHStlNpCcFi7eGITZCFfpZAswSFUkHuQtNVJ5HTDQ72xg1N537pnPaFZBaYLU44ynZAngevXN1hvmAhto47gZBq56Sniq4IZD"

#fun facts
funfact = [
           ' The first electronic computer ENIAC weighed more than 27 tons and took up 1800 square feet!',
           ' There are more than 5000 new computer viruses are released every month ! ',
           ' The password for the computer controls of nuclear tipped missiles of the U.S was 00000000 for eight years. damnnnn',
           ' HP, Microsoft and Apple have one very interesting thing in common, they were all started in a garage ',
           ' The first ever hard disk drive was made in 1979, and could hold only 5MB of data ',
           ' The original name of windows was Interface Manager.',
           ' An average person normally blinks 20 times a minute, but when using a computer he/she blinks only 7 times a minute !'
         ]
#Pre-defined jokes
jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                    """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""],
         'chutiya': ["""Tera baap chutiya ! Bhancho!"""],
         'chutiye': ["""Tera baap chutiya ! Bhancho!"""],
         'hey': ["""Hey ! how can i help you ? :)"""],
         'hello': ["""Hello ! how can i help you ? :)"""],
         'hiii': ["""Hi ! how can i help you ? :)"""],
         'hi': ["""Hi   ! how can i help you ? :)"""],
         'created': ["""The Almighty Decrypto! """ ],
         'creator': ["""The Almighty Decrypto! """],
         'haha' : ["""I'm glad you find me amusing! """],
         'fuck' : ["""is that what you say to your mom? ""","""please don't use the F word"""],
         'Thanks' : ["""My pleasure ;) """],
         'thank' : ["""My pleasure ;) """],
         'thanks' : ["""My pleasure ;) """]
         }
# Create your views here.
class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('hub.verify_token') == '2318934571':
            return HttpResponse(self.request.GET.get('hub.challenge'))
        else:
            return HttpResponse('Error, invalid token')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()

#simple helper function that will make this POST call with the received text.
def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    #print(ans)
    joke_text1 = ''
    joke_text2 = ''
    #reply_ans=get_reply_table(recevied_message)
    reply_ans="$"
    if reply_ans=="$":
        tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
        for token in tokens:
            if token in jokes:
                joke_text1 = random.choice(jokes[token])
                break
        if not joke_text1:
            joke_text1 = "Sorry I didn't undertand that ! I'm still under the development process :) "
            secure_random = random.SystemRandom()
            joke_text2 = "Here's a Fun fact !" + secure_random.choice(funfact)
        #insert_reply_table(recevied_message,joke_text1)
    else :
        joke_text1=reply_ans
            #joke_text1=ans[0]
        #joke_text2=ans[0]
        #joke_text1 = joke_text1 + "\n" + joke_text2
    #user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    #user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    #user_details = requests.get(user_details_url, user_details_params).json()
    #joke_text = 'Yo '+user_details['first_name']+'..! ' + joke_text
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token="+PAGE_ACCESS_TOKEN
    response_msg1 = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text1}})
    response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text2}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg1)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg2)
    pprint(status.json())

#to get the output string for the recevied message if it's present in the database
def get_reply_table(recevied_message):
    send_ans = ''
    dbconect2 = sqlite3.connect('db.sqlite3')
    cur2 = dbconect2.cursor()
    #query1="SELECT send FROM Reply WHERE recieve" + " = '" + recevied_message + "';"
    #cur2.execute(query1)
    cur2.execute("SELECT send FROM Reply WHERE recieve = 'hey'")
    if cur2.fetchone() is not None:
        ans=cur2.fetchone()
        send_ans=ans[0]
        print("#############################################")
        print(ans[0])
        print("#############################################")
        print(send_ans)
    else :
        send_ans="$"
        print("#############################################")
        print(send_ans)
    return send_ans

#to insert the replies in the database
def insert_reply_table(recevied_message,send_message):
    dbconect1=sqlite3.connect('db.sqlite3')
    cur1=dbconect1.cursor()
    #query="INSERT INTO Reply (recieve,send) VALUES " + "( '" + recevied_message + "' , '" + send_message + "')"
    #cur1.execute(query)
    cur1.execute('INSERT INTO Reply (recieve,send) VALUES ( ?,? ) ', ( recevied_message,send_message) )
    dbconect1.commit()
    cur1.close()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("INSERTED IN THE  DATABASE")
    print("VALUE ARE : " + recevied_message + " , " + send_message)
