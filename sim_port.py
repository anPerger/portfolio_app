import random
import numpy as np
import scipy
from scipy import stats
import pymongo
from pymongo import MongoClient
import mongo_creds

username = f'{mongo_creds.username}'
password = f'{mongo_creds.password}'
cluster = f'{mongo_creds.clustername}'
auth = f'{mongo_creds.auth}'

uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + "." + auth + '.mongodb.net'

client = pymongo.MongoClient(uri)

portfolio_sims_db = client["portfolio_sims"]
sims_col = portfolio_sims_db["sims"]

def analysis(sim_results):
        
    inflation_results = sim_results["Inflation"]

    nominal_bonds_results = sim_results["bond_vals_nominal"]
    real_bonds_results = sim_results["bond_vals_real"]

    nominal_cash_results = sim_results["cash_vals_nominal"]
    real_cash_results = sim_results["cash_vals_real"]

    nominal_stock_results = sim_results["stock_vals_nominal"]
    real_stock_results = sim_results["stock_vals_real"]

    nominal_portfolio_results = sim_results["portfolio_vals_nominal"]
    real_portfolio_results = sim_results["portfolio_vals_real"]


    inflation_mean_list = []
    inflation_std_list = []

    stocks_nominal_mean_list = []
    stocks_nominal_std_list = []
    stocks_real_mean_list = []
    stocks_real_std_list = []

    bonds_nominal_mean_list = []
    bonds_nominal_std_list = []
    bonds_real_mean_list = []
    bonds_real_std_list = []

    cash_nominal_mean_list = []
    cash_nominal_std_list = []
    cash_real_mean_list = []
    cash_real_std_list = []

    portfolio_nominal_mean_list = []
    portfolio_nominal_std_list = []
    portfolio_real_mean_list = []
    portfolio_real_std_list = []

    year = []

    for x in range(len(inflation_results)):

        # inflation 
        year_inflation = np.array(inflation_results[x])
        year_inflation_mean = np.mean(year_inflation)
        year_inflation_std = np.std(year_inflation)

        inflation_mean_list.append(year_inflation_mean)
        inflation_std_list.append(year_inflation_std)

        # stocks nominal
        year_stocks_nominal = np.array(nominal_stock_results[x])
        year_stocks_nominal_mean = np.mean(year_stocks_nominal)
        year_stocks_nominal_std = np.std(year_stocks_nominal)

        stocks_nominal_mean_list.append(year_stocks_nominal_mean)
        stocks_nominal_std_list.append(year_stocks_nominal_std)


        # stocks real
        year_stocks_real = np.array(real_stock_results[x])
        year_stocks_real_mean = np.mean(year_stocks_real)
        year_stocks_real_std = np.std(year_stocks_real)

        stocks_real_mean_list.append(year_stocks_real_mean)
        stocks_real_std_list.append(year_stocks_real_std)

        # bonds nominal
        year_bonds_nominal = np.array(nominal_bonds_results[x])
        year_bonds_nominal_mean = np.mean(year_bonds_nominal)
        year_bonds_nominal_std = np.std(year_bonds_nominal)

        bonds_nominal_mean_list.append(year_bonds_nominal_mean)
        bonds_nominal_std_list.append(year_bonds_nominal_std)

        # bonds real
        year_bonds_real = np.array(real_bonds_results[x])
        year_bonds_real_mean = np.mean(year_bonds_real)
        year_bonds_real_std = np.std(year_bonds_real)

        bonds_real_mean_list.append(year_bonds_real_mean)
        bonds_real_std_list.append(year_bonds_real_std)

        # cash nominal
        year_cash_nominal = np.array(nominal_cash_results[x])
        year_cash_nominal_mean = np.mean(year_cash_nominal)
        year_cash_nominal_std = np.std(year_cash_nominal)

        cash_nominal_mean_list.append(year_cash_nominal_mean)
        cash_nominal_std_list.append(year_cash_nominal_std)

        # cash real
        year_cash_real = np.array(real_cash_results[x])
        year_cash_real_mean = np.mean(year_cash_real)
        year_cash_real_std = np.std(year_cash_real)

        cash_real_mean_list.append(year_cash_real_mean)
        cash_real_std_list.append(year_cash_real_std)

        # portfolio nominal
        year_portfolio_nominal = np.array(nominal_portfolio_results[x])
        year_portfolio_nominal_mean = np.mean(year_portfolio_nominal)
        year_portfolio_nominal_std = np.std(year_portfolio_nominal)

        portfolio_nominal_mean_list.append(year_portfolio_nominal_mean)
        portfolio_nominal_std_list.append(year_portfolio_nominal_std)

        # portfolio real
        year_portfolio_real = np.array(real_portfolio_results[x])
        year_portfolio_real_mean = np.mean(year_portfolio_real)
        year_portfolio_real_std = np.std(year_portfolio_real)

        portfolio_real_mean_list.append(year_portfolio_real_mean)
        portfolio_real_std_list.append(year_portfolio_real_std)

        year.append(x+1)

    
    dash_prep = {
                    "year": year,
                    "Inflation": inflation_mean_list,
                    "Inflation_std": inflation_std_list,

                    "Stocks Nominal": stocks_nominal_mean_list,
                    "Stocks Nominal_std": stocks_nominal_std_list,
                    "Stocks Real": stocks_real_mean_list,
                    "Stocks Real_std": stocks_real_std_list,
                    
                    "Bonds Nominal": bonds_nominal_mean_list,
                    "Bonds Nominal_std": bonds_nominal_std_list,
                    "Bonds Real": bonds_real_mean_list,
                    "Bonds Real_std": bonds_real_std_list,
                    
                    "Cash Nominal": cash_nominal_mean_list,
                    "Cash Nominal_std": cash_nominal_std_list,
                    "Cash Real": cash_real_mean_list,
                    "Cash Real_std": cash_real_std_list,
                    
                    "Portfolio Nominal": portfolio_nominal_mean_list,
                    "Portfolio Nominal_std": portfolio_nominal_std_list,
                    "Portfolio Real": portfolio_real_mean_list,
                    "Portfolio Real_std": portfolio_real_std_list}
    
    return dash_prep

def sim_portfolio(args):

    username = args["username"]
    portfolio_name = args["portfolio_name"]
    api_key = args["key"]
    user_stocks = args["user_stocks"]
    user_bonds = args["user_bonds"]
    user_cash = args["user_cash"]

    stock_ret = args["stock_ret"]
    stock_std = args["stock_std"]
    stock_div = args["stock_div"]

    bond_ret = args["bond_ret"]
    bond_std = args["bond_std"]
    bond_div = args["bond_div"]

    inflation_rate = args["inflation_rate"]
    inflation_std = args["inflation_std"]
    horizon = args["user_horizon"]
    num_sims = args["sims"]
    principal = args["principal"]
    reinvest = args["reinvest"]

    print(f"user stocks: {user_stocks} of type {type(user_stocks)}")
    print(f"user bonds: {user_bonds} of type {type(user_bonds)}")
    print(f"user cash: {user_cash} of type {type(user_cash)}")
    print(f"stock ret: {stock_ret} of type {type(stock_ret)}")
    print(f"stock std: {stock_std} of type {type(stock_std)}")
    print(f"stock div: {stock_div} of type {type(stock_div)}")
    print(f"bond ret: {bond_ret} of type {type(bond_ret)}")
    print(f"bond std: {bond_std} of type {type(bond_std)}")
    print(f"bond div: {bond_div} of type {type(bond_div)}")

    print(f"inflation rate: {inflation_rate} of type {type(inflation_rate)}")
    print(f"inflation std: {bond_std} of type {type(bond_std)}")
    print(f"horizon: {horizon} of type {type(horizon)}")
    print(f"num sims: {num_sims} of type {type(num_sims)}")
    print(f"principal: {principal} of type {type(principal)}")
    print(f"reinvest: {reinvest} of type {type(reinvest)}")




    stock_val_nominal_list = [ [] for _ in range(horizon)]
    stock_val_real_list = [ [] for _ in range(horizon)]
    bond_val_nominal_list = [ [] for _ in range(horizon)]
    bond_val_real_list = [ [] for _ in range(horizon)]
    cash_val_nominal_list = [ [] for _ in range(horizon)]
    cash_val_real_list = [ [] for _ in range(horizon)]
    inflation_list = [ [] for _ in range(horizon)]
    portfolio_nominal_list = [ [] for _ in range(horizon)] 
    portfolio_real_list =  [ [] for _ in range(horizon)]

    for sim in range(num_sims):

        stock_val_nominal = user_stocks * principal
        stock_val_real = user_stocks * principal
        bond_val_nominal = user_bonds * principal
        bond_val_real = user_bonds * principal
        cash_val_nominal = user_cash * principal
        cash_val_real = user_cash * principal

        portfolio_val_nominal = principal
        portfolio_val_real = principal

        start_cash = cash_val_nominal
               
        for x in range(horizon):
            
        
            inflation = random.gauss(inflation_rate, inflation_std)
            if inflation == -1:
                inflation = -.99999


            stock_return_rate = random.gauss(stock_ret, stock_std)
            stock_returns = stock_val_nominal * stock_return_rate
            stock_div_ret = stock_val_nominal * stock_div
            

            stock_val_nominal += stock_returns

            if reinvest == True:
                # print("reinvesting stocks")
                stock_val_nominal += stock_div_ret
            else:
                # print("not reinvesting stocks")
                cash_val_nominal += stock_div_ret
   
            real_stock_ret_rate = ((1 + stock_return_rate) / (1 + inflation)) - 1
            real_stock_returns = stock_val_nominal * real_stock_ret_rate

            stock_val_real += real_stock_returns
            
            # BONDS
            bond_return_rate = random.gauss(bond_ret, bond_std)
            bond_returns = bond_val_nominal * bond_return_rate
            bond_div_ret = bond_val_nominal * bond_div

            bond_val_nominal += bond_returns

            if reinvest == True:
                bond_val_nominal += bond_div_ret
            else:
                cash_val_nominal += bond_div_ret

            
            real_bond_ret_rate = ((1 + bond_return_rate) / (1 + inflation)) - 1
            real_bond_returns = bond_val_nominal * real_bond_ret_rate
            
            bond_val_real += real_bond_returns
 
            nominal_cash_returns = cash_val_nominal - start_cash

            if abs(nominal_cash_returns) == 0:
                real_cash_returns = (cash_val_nominal * (1 - inflation)) - start_cash
            else:
                if start_cash != 0:
                    nominal_cash_ret_rate = (cash_val_nominal / start_cash) - 1
                    real_cash_ret_rate = ((1 + nominal_cash_ret_rate) / (1 + inflation)) - 1
                    real_cash_returns = (start_cash * (1 + real_cash_ret_rate)) - start_cash
                else:
                    real_cash_returns = (nominal_cash_returns * (1 - inflation)) 

            
            cash_val_real += real_cash_returns

            portfolio_val_nominal = (cash_val_nominal + stock_val_nominal + bond_val_nominal)

            portfolio_val_real = (cash_val_real + stock_val_real + bond_val_real)

            start_cash = cash_val_nominal

            stock_val_nominal_list[x].append(stock_val_nominal)
            stock_val_real_list[x].append(stock_val_real)
            bond_val_nominal_list[x].append(bond_val_nominal)
            bond_val_real_list[x].append(bond_val_real)
            cash_val_nominal_list[x].append(cash_val_nominal)
            cash_val_real_list[x].append(cash_val_real)
            inflation_list[x].append(inflation)

            portfolio_nominal_list[x].append(portfolio_val_nominal)
            portfolio_real_list[x].append(portfolio_val_real)

    sim_results = {

    "stock_vals_nominal": stock_val_nominal_list,
    "stock_vals_real": stock_val_real_list,
    "bond_vals_nominal": bond_val_nominal_list,
    "bond_vals_real": bond_val_real_list,
    "cash_vals_nominal": cash_val_nominal_list,
    "cash_vals_real": cash_val_real_list,
    "Inflation": inflation_list,
    "portfolio_vals_nominal":  portfolio_nominal_list,
    "portfolio_vals_real":  portfolio_real_list,

    }
    
    dash_prep = analysis(sim_results)

    sim_results["yearly_avgs"] = dash_prep

    
    try:
        sims_col.update_one( {"username" : username, "APIkey": api_key, "portfolio_name" : portfolio_name }, 
                {"$set": sim_results}, upsert=True)
        results = {"success": 1}
    except:
        results = {"success": 0, "error_msg": "Something has gone wrong"}
    
    return results

def check_sim(username, portfolio_name, api_key):

    sim_run = sims_col.find_one({"username": username, "APIkey": api_key, "portfolio_name": portfolio_name})
    
    if not sim_run:
        error_msg = "No simulation has been run on this portfolio"
        results = {"success": 0, "error_msg": error_msg}
    else:
        del sim_run["_id"]
        del sim_run["APIkey"]
        results = {"success": 1, "results": sim_run}

    return results


