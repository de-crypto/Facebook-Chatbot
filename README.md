# Making a basic echo bot in python & Django

1) `git clone` the code for the bot
```
git clone https://github.com/botshala/basic_echo_bot.git
```

2) Every messenger bot must be associated with a facebook page, Add your page access token to [this line](https://github.com/botshala/basic_echo_bot/blob/master/fb_chatbot/views.py#L13)
![alt text](http://i.imgur.com/0KsbwnA.jpg "fb dashboard img")

3) Next we need to activate the webhook, we will use [heroku](heroku.com) to deploy our bot. Sign up for it and download the [cmd-line toolbelt](https://toolbelt.heroku.com/)
```
#make sure you're in the parent directory
cd basic_echo_bot
#login to your account using the toolbelt
heroku login
heroku create
#commit your changes
git add .
git commit -m 'pushing code to heroku'
git push heroku master
#run your code on heroku servers
heroku ps:scale web=1
#see the logs for debugging
heroku logs -t 
```

4) Verify if your project is deployed correctly by viewing the logs and going to the public url of your app (e.g arcane-retreat-27414.herokuapp.com) 

5) Activate your webhook ![alt text](http://g.recordit.co/SCF7NVNxot.gif "fb dashboard gif 1")

6) Make sure the VERIFY_TOKEN you enter on the fb dashboard is the same as [in your code](https://github.com/botshala/basic_echo_bot/blob/master/fb_chatbot/views.py#L14) 
![alt text](http://i.imgur.com/acIAODB.png "fb dashboard gif 1")


7) Once the webhook is activated and verfified, go to the fb dashboard and subscribe to the facebook page you want your webhook to listen to. 
![alt text](http://g.recordit.co/3Hz6sZlKRs.gif "fb dashboard gif")

8) Send a message to your page, and view the logs `heroku logs -t` to debug any errors

9) make changes to your code and re-deploy it on heroku as follows
```
git add .
git commit -m 'made some changes'
git push heroku master
#now re-run it on heroku
heroku ps:scale web=1
#now see the logs, to check whether the error still persists
heroku logs -t
```
10) FAQs
+ `sudo pip install requests`
+ `heroku config:set DISABLE_COLLECTSTATIC=1`
+ `heroku git:remote -a {{YOUR heroku_app_id}}`
+ `heroku ps:scale web=0`
