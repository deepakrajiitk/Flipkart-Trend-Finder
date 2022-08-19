# -*- coding: utf-8 -*-
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Importing requiredlibraries
import numpy as np
from datetime import *
import pandas as pd
import json
from pytrends.request import TrendReq
from googlesearch import search   
from serpapi import GoogleSearch
import math

# Function to get date with given offset
def getDate(offset=0):
  curr_time=datetime.utcnow() + timedelta(hours=5, minutes=30)
  date = curr_time + timedelta(days = offset)
  return str(date.date())

# Opening file
file = open('./DataSet/Categories.json');
dataset = json.load(file);

def getFlipkartLink(query):
    query = query
    for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
        if "flipkart" in j:
            return j

def getImage(query,api_key="293db784785353787a027b83533e3d0011714662cee89aca8b6717e7ef8fd845"):
    params = {
      "q": query,
      "tbm": "isch",
      "ijn": "0",
      "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results["images_results"]
    image = []
    for i in range(0,3):
        image.append(images_results[i]['thumbnail'])
    return image

def getGoogleTrendResult(category, subcategory, count):
  res = {}
  startingDate = getDate(-30)
  endingDate = getDate()
  data = list(set(dataset[category][1][subcategory][1]))
  categoryID = dataset[category][1][subcategory][0]
  # initializing pytrends object
  pytrends = TrendReq(retries=20, backoff_factor=0.1, requests_args={'verify':False})
  # splitting data into chunks of size of 5 each
  kw_list = np.array_split(data, math.ceil(len(data)/5))
  for kw in kw_list:
    pytrends.build_payload(kw, cat = categoryID, timeframe = startingDate + " " + endingDate, geo = 'IN')
    df = pytrends.interest_over_time()
    # df may be empty for some keywords
    if(not df.empty):
      df.drop('isPartial', axis = 1, inplace = True)
    # getting average of the popularity
    temp_dic = df.mean().to_dict();
    res = {**res, **temp_dic}
  return res;

def createDictionary(name, category, subcategory):
  d = {}
  d['Name'] = name
  d['Category'] = category
  d['Subcategory'] = subcategory
  d['Image Url'] = getImage(name+" "+subcategory+" "+category)[:]
  d['Flipkart Url'] = getFlipkartLink(name+" "+subcategory+" "+category+" Flipkart")
  return d

# this function return top trending product in specific subcategory
def getTrendByCatAndSub(category, subcategory, count):
  response = getGoogleTrendResult(category, subcategory, count)
  # print(response)
  response = sorted(response, key=response.get, reverse=True)[:count]
  result = []
  for name in response:
    d = createDictionary(name, category, subcategory)
    result.append(d)

  with open(f"./DataSet/{category}_{subcategory}_data.json","w") as f:
      json.dump(result,f)
  return result;

# this function return top trending product in specific category
def getAllTrendOfCategory(category, count):
  data = dataset[category][1]
  res = []
  for subcategory in data:
    print(subcategory)
    response = getGoogleTrendResult(category, subcategory, count)
    temp = []
    for i in response:
       res.append([i, response[i], category, subcategory])
  # print(result)
  # response = sorted(res, key=res.get, reverse=True)[:count]
  res = sorted(res, key = lambda x: x[1], reverse = True)[:count]
  result = []
  for i in res:
    d = createDictionary(i[0], i[2], i[3])
    result.append(d)

  with open(f"./DataSet/{category}_data.json","w") as f:
      json.dump(result,f)

  return result;

# this function return top trending products in all categories
def getAllTrend(count):
  result = {}
  for category in dataset:
    response = getAllTrendOfCategory(category, count)
    result[category] = response
  with open("./DataSet/all_categories.json") as f:
    json.dump(result,f)
  return result

# getTrendByCatAndSub("Women Fashion", "Western Wear", 5)

# getAllTrendOfCategory("Men Fashion", 10)

# getAllTrend(10)

