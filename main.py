import requests
import json
import torch
from rich.console import Console
from rich.tree import Tree
from query_list import *
from secure import *

def request_central_data(query, variables = None, save=False):
    if variables != None:
        payload = {
            "query": query,
            "variables": variables
        }
    else :
        payload = {
            "query": query
        }

    response = requests.post(url_central, headers=headers, json=payload)

    if response.status_code == 200:
        if save == True:
            with open('output.json', 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, indent=4, ensure_ascii=False)
        return response
    else:
        print("오류 발생:", response.status_code, response.text)

def request_live_data(query, variables = None, save=False):
    if variables != None:
        payload = {
            "query": query,
            "variables": variables
        }
    else :
        payload = {
            "query": query
        }

    response = requests.post(url_live, headers=headers, json=payload)

    if response.status_code == 200:
        if save == True:
            with open('output.json', 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, indent=4, ensure_ascii=False)
        return response
    else:
        print("오류 발생:", response.status_code, response.text)

def find_all_team_id():
    ## extract all of the teams id of the series.
    response = request_central_data(query5)
    data = response.json()

    # # Load the JSON data from the file
    # with open("output.json", 'r') as file:
    #     data = json.load(file)

    # Extracting all team IDs from each node in the JSON file
    team_ids = []
    for edge in data['data']['allSeries']['edges']:
        for team in edge['node']['teams']:
            team_ids.append(team['baseInfo']['id'])

    # Display the list of all team IDs
    print(team_ids)

def find_all_series_id():
    response = request_central_data(query6)
    data = response.json()
    series_ids = []
    for edge in data['data']['allSeries']['edges']:
        series_ids.append(edge['node']['id'])
    return series_ids
    
# find_all_series_id()
# find_all_team_id()

def find_game_state(variables):
    response = request_live_data(query7, variables)
    data = response.json()

    # with open("output.json", 'r') as file:
    #     data = json.load(file)

    edge = data['data']['seriesState']['teams']
    if edge[0]['won'] == True:
        feature = [edge[0]['kills'], edge[0]['deaths']]
        score = [edge[1]['score']]
    elif edge[1]['won'] == False:
        feature = [edge[1]['kills'], edge[1]['deaths']]
        score = [edge[0]['score']]
    return feature, score
    
# variables = {"series_id" : 2748095}
# feature, score = find_game_state(variables)
# print(feature, score)

def find_all_game_state():
    x_data = []
    y_data = []
    
    series_ids = find_all_series_id()
    # print(series_ids)
    num = 0
    for id in series_ids:
        print(num)
        num +=1
        id_variables = {"series_id" : int(id)}
        # print(id_variables)
        try :
            feature, score = find_game_state(id_variables)
            x_data.append(feature)
            y_data.append(score)
        except :
            pass

    x_data = torch.tensor(x_data)
    y_data = torch.tensor(y_data)

    return x_data, y_data

x_data, y_data = find_all_game_state()
print(x_data, y_data)