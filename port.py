import os
import pymongo
from pymongo import MongoClient
import mongo_creds

username = f'{mongo_creds.username}'
password = f'{mongo_creds.password}'
cluster = f'{mongo_creds.clustername}'
auth = f'{mongo_creds.auth}'

uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + "." + auth + '.mongodb.net'

client = pymongo.MongoClient(uri)
portfolio_ports_db = client["portfolio_ports"]
portfolios_col = portfolio_ports_db["portfolios"]

def create_portfolio(username, portfolio_name, stocks, bonds, cash, api_key):

    
    portfolio = {"portfolio_name": portfolio_name, "stocks": stocks, "bonds": bonds, "cash": cash}

    try:
        portfolios_col.update_one( {"username" : username, "APIkey": api_key, "portfolio_name" : portfolio_name }, 
                {"$set": portfolio}, upsert=True)
        results = {"success": 1}
    except:
        results = {"success": 0, "error_msg": "Something has gone wrong"}
    
    return results

def return_portfolios(username, api_key):

    portfolios = list(portfolios_col.find({"username": username, "APIkey": api_key}))

    for portfolio in portfolios:
        del portfolio["_id"]

    return portfolios

def return_portfolio(username, portfolio_name, api_key):

  
    portfolio = portfolios_col.find_one({"username": username, "APIkey": api_key, "portfolio_name": portfolio_name})

    del portfolio["_id"]

    return portfolio

def delete_portfolio(username, portfolio_name, api_key):

    try:
        portfolios_col.delete_one({"username": username,  "APIkey": api_key, "portfolio_name": portfolio_name})
        results = {"success": 1}
    except:
        error_msg = "something has gone wrong"
        results = {"success": 0, "error_msg": error_msg}

    return results
    
