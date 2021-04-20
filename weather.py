#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:30:02 2020

@author: yuyara
"""

import requests as rq
import PySimpleGUI as gui
from datetime import datetime


#AIzaSyBStwZGDooSga5dsl0pg4vczeqVTd_jIE8
    
def locate(location):
    parameter = {"address":location,"key":"GOOGLE_API_KEY"}
    result = rq.get("https://maps.googleapis.com/maps/api/geocode/json",params=parameter)
    resultText = eval(result.text)
    find = resultText["results"][0]["geometry"]["location"]
    return(find["lat"],find["lng"])


def callweather(location):
    lat, lon = locate(location)
    condition = {"lat":lat,"lon":lon,"appid":"OPENWEATHERMAP_API_KEY"}
    response = rq.get('https://api.openweathermap.org/data/2.5/onecall',params=condition)
    responsetext = eval(response.text)
    return(responsetext)



def search():
    layout = [
        [gui.Text("This is Yuya's Weather Forecast yeet!")],
        [gui.Text("You want to know your weather for "), gui.Combo(["now","tomorrow","today"])],
        [gui.Text("Your current location: "),gui.InputText(),gui.OK()]
        ]
    
    window = gui.Window("Know Your Weather",layout)
    
    while True:
        event,values = window.read()
        if event == gui.WINDOW_CLOSED:
            break
        elif event == "OK":
            raWeather = callweather(values[1])
            display(values[0],values[1],raWeather)
            break
    window.Close()

def display(time,place,weatherdata):
    #print(weatherdata)
    if time == "now":
        icon = weatherdata["current"]["weather"][0]["main"]
        layout = [
            [gui.Image("./" + icon + ".png")],
            [gui.Text("The weather in " + place + " " + time + " is " + icon + ", the temperature is " + str(round((float(weatherdata["current"]["temp"])-273.15),2)) + " °C.")],
            [gui.OK()]
            ]
    elif time == "tomorrow":
        icon = weatherdata["daily"][1]["weather"][0]["main"]
        layout = [
            [gui.Image("./" + icon + ".png")],
            [gui.Text("The weather of " + place + " for tomorrow is " + icon + ", the average temperature is " + str(round((float(weatherdata["daily"][1]["temp"]["day"])-273.15),2)) + " °C.")],
            [gui.OK()]
            ]
    elif time == "today":
        end = None
        t = 0
        while end != "23" and t  < (len(weatherdata["hourly"])):
            hourly = weatherdata["hourly"][t]
            hour = hourly["dt"]
            hourweather = hourly["weather"][0]["main"]
            end = datetime.fromtimestamp(hour).strftime("%H")
            print(hourweather)
            t+=1
                
        layout = [
            [gui.Text("The rest of the day will be " + hourweather)]
            ]
        
        
        
    window = gui.Window("Result",layout)
    
    while True:
        event,values = window.read()
        if event == gui.WINDOW_CLOSED:
            break
        elif event == "OK":
            search()
            break
    window.Close()
    

gui.theme("DarkTeal5")

search()


