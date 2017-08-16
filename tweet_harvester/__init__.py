# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 09:29:11 2017

@author: schro
"""
from flask import Flask, json, request, render_template
import tweepy
import os
import sys
import time
import requests
import re
from py2neo import Graph, Node, Relationship, authenticate

# set up authentication parameters
authenticate("localhost:7474", "neo4j", "neo4jhere")

# connect to authenticated graph database
#graph = Graph()
url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
graph = Graph(url + '/db/data/')

# Instantiate our app...
# Name it the '__name__' of this module (tweet-harvest)
app = Flask(__name__)

# Later, we will store our Twitter tokens/keys
# in config.py...we load our config here.
app.config.from_object('config')

# These config variables come from 'config.py'
auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
                           app.config['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'],
                      app.config['TWITTER_ACCESS_TOKEN_SECRET'])
tweepy_api = tweepy.API(auth)


def get_tweets(username):
    tweets = tweepy_api.user_timeline(screen_name=username)                                                                            
    return [{'tweet': t.text,
              'created_at': t.created_at, 
              'username': username,
              'headshot_url': t.user.profile_image_url}
           for t in tweets]
           
rooms = ["balcony","Green BR", "GBR", "in HOH", " BA ","money room", "Rose BR","rose rm", "SR", "KT"]
names=["Cody","Matt","Raven","Elena","Mark","Alex","Paul", "Christmas", "Josh", "Jason", "Kevin"]

names_room=["Cody","Matt","Raven","Elena","Mark","Alex","Paul", "Christmas", "Josh", "Jason", "Kevin"]
rooms_dic={"balcony":"Balcony","Green BR":"Green Bedroom", "GBR":"Green Bedroom","in HOH":"HOH Room"," BA ":"Bathroom","money room":"Money Room", "Rose BR": "Rose Room","rose rm": "Rose Room", "SR":"Supply Room", "KT":"Kitchen"}
names_dic={}
graph.delete_all()

def take_speech(word_between, word_after):
    if (name+" "+word_between+" "+name2+word_after) in status.text:
        namey = Node("Name", id=name)
        namey2 = Node("Name2", id=name2)
        graph.merge(namey)
        graph.merge(namey2)
        namey.push()
        namey2.push()
        TEXTO = sys.argv[1]
        #my_regex = re.escape(".*?\") + re.escape(name2) + r"\s(.*)[#.].*"

        a = re.search(".*?\:\s(.*)[#.].*",status.text) 
        #if a 
        speech_text=(a.group(1))
        speech = Node("Chit Chat", id=speech_text)
        graph.merge(speech)
        speech["text"] = status.text
        speech.push()
        
        graph.merge(Relationship(namey, ("tells "+name2), speech))
        
def create_tweets():
    page_list=[]
    tweet_list=[]
    #min_time=top20[0].created_at
    n=0
    for page in tweepy.Cursor(tweepy_api.user_timeline, id="JokersBBUpdates", count=200).pages(3):
        page_list.append(page)
        n = n+1

    for page in page_list:
        for status in page:
            for name in names:
                for name2 in names:
                    if (name+" to "+name2+":") in status.text:
                        namey = Node("Name", id=name)
                        namey2 = Node("Name2", id=name2)
                        graph.merge(namey)
                        graph.merge(namey2)
                        namey.push()
                        namey2.push()
                            
                        a=re.search(".*?\:\s(.*)[#.].*",status.text)
                        if a: 
                            speech_text=(a.group(1))
                            speech = Node("Chit Chat", id=speech_text)
                            graph.merge(speech)
                            speech["text"] = status.text
                            speech.push()
                            
                            graph.merge(Relationship(namey, ("told "+name2), speech))
                        
                    
            for room in rooms:
                if room in status.text:
                    hoh = Node(rooms_dic[room], id=rooms_dic[room])
                    graph.merge(hoh)
                    hoh["text"] = status.text
                    hoh.push()
                    together=[]
                    for name in names_room:
                        if name in status.text:
                            
                                
                            jody = Node("Name", id=name)
                            graph.merge(jody)
                            jody["text"] = status.text
                            jody.push()
                                #if similar==1:
                            graph.merge(Relationship(jody, "INSIDE", hoh))
                            together.append(jody)
                            #remove name so they can't be added to a room they were in before
                            names_room.remove(name)
                        if len(together)>1:
                            graph.merge(Relationship(together[0], "WITH", together[1]))
    return tweet_list


test_list=create_tweets()


  
           
# We define our URL route, and the controller to handle requests
@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'
    
    
@app.route('/tweet_harvester/<string:username>')
def tweets(username):
  # 'tweets' is passed as a keyword-arg (**kwargs)
  # **kwargs are bound to the 'tweets.html' Jinja Template context
  return render_template("tweets.html", tweets=get_tweets(username))
