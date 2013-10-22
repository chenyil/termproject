#-------------------------------------------------------------------------------
# Name:        chartCaculation
# Purpose:
#
# Author:      Chenyi Liu
#
# Created:     21/10/2013
# Copyright:   (c) Chenyi Liu 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
from GChartWrapper import *
import sys
import json
import string
img_number=0
flag=0
filenames = [".\Images\image.jpg"]
scores= {} # initialize an empty dictionary

hoursen =[0.0]*24
hourcount=[0.0]*24
houremo = [0.0]*24
hours=[0]*24
hoursa=[0]*24

def InitiatDictionary():
    fp="AFINN-111.txt"
    afinnfile = open(fp)

    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    # print scores.items() # Print every (term, score) pair in the dictionary

    for i in range(len(hours)):
        hours[i]=i
        hoursa[i]=i*5

def clearIMGBuffer():
    global filenames
    for name in filenames:
        if (name!=".\Images\image.jpg"):
            os.remove(name)
            filenames.remove(name)

def drawbarchart():
    #Tweets Sentiment
    data = [hours,hoursen]
    min_value = float(min(data[1]))
    max_value = float(max(data[1]))

    G = Line( hoursen, encoding='text' )
    G.axes.type('xxyy')
    G.axes.label( 0, *data[0] )
    G.axes.label( 1, 'Hour' )
    G.axes.label( 3, 'Score' )
    G.axes.range( 2, min_value, max_value )
    G.scale( min_value, max_value )
    G.size ( 500, 200 )
    G.title( "Tweets Sentiment" )
    G.save(".\Images\\0")
    G.show()

    #Tweets Emotional
    data1=[hours,houremo]
    min_value = float(min(data1[1]))
    max_value = float(max(data1[1]))
    G1 = Line( houremo, encoding='text' )
    G1.axes.type('xxyy')
    G1.axes.label( 0, *data1[0] )
    G1.axes.label( 1, 'Hour' )
    G1.axes.label( 3, 'emotional' )
    G1.axes.range( 2, min_value, max_value )
    G1.scale( min_value, max_value )
    G1.size ( 500, 200 )
    G1.title( "Tweets Emotional" )
    G1.save(".\Images\\1")
    G1.show()

    #Number of Tweets
    data2=[hours,hourcount]
    min_value = float(min(data2[1]))
    max_value = float(max(data2[1]))
    G2 = Line( hourcount, encoding='text' )
    G2.axes.type('xxyy')
    G2.axes.label( 0, *data1[0] )
    G2.axes.label( 1, 'Hour' )
    G2.axes.label( 3, 'Count' )
    G2.axes.range( 2, min_value, max_value )
    G2.scale( min_value, max_value )
    G2.size ( 500, 200 )
    G2.title( "Tweets Counts" )
    G2.save(".\Images\\2")
    G2.show()

def HandleHour(hour,sen):
    hourcount[hour]+=1
    hoursen[hour]+=sen
    if sen<0:
        houremo[hour]-=sen
    else:
        houremo[hour]+=sen

def TraceTime(time,sen):
    weekday=time[0:3]
    month=time[4:7]
    day= int(time[8:10])
    hour=int(time[11:13])
    year=int(time[-4:])
    print("%s %d %s %d %d" %(weekday,year,month,day,hour))
    HandleHour(hour,sen)

def finalCal():
    for i in range(len(hourcount)):
        if hourcount[i]!=0:
            hoursen[i]=hoursen[i]/hourcount[i]
            houremo[i]=houremo[i]/hourcount[i]
        #print("%2d %.2f" %(i,hoursen[i]))

def lines(gp):

    twi=open(gp)
    sentiment=[]
    strr=[]
    twii=json.loads(twi.read())
    i=0
    for object in twii:
        #tweet= json.loads(object)
        tweet=object
        sentiment.append(0)
        if tweet.has_key('text'):
            s=tweet['text']
            es = s.lower().encode('utf-8')
            strr=es.split(' ')
            #print strr
            for term in scores.keys():
                for word in strr:
                    if(word==term):
                        #print term
                        sentiment[i]=sentiment[i]+scores[term]

            # sample:Wed Aug 27 13:08:45 +0000 2008

            time=tweet['created_at']
            time=time.encode('utf-8')
            TraceTime(time,sentiment[i])

            print float(sentiment[i])
        i=i+1

    finalCal()
    drawbarchart()
