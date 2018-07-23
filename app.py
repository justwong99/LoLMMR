#!flask/bin/python
from __future__ import print_function
import sys
import requests
import json
from flask import jsonify
from flask import jsonify,make_response
from flask import Flask
from flask import request
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)

rankdict = {
  "BRONZEV": 1,
  "BRONZEIV": 2,
  "BRONZEIII": 3,
  "BRONZEII": 4,
  "BRONZEI": 5,
  "SILVERV": 6,
  "SILVERIV": 7,
  "SILVERIII": 8,
  "SILVERII": 9,
  "SILVERI": 10,
  "GOLDV": 11,
  "GOLDIV": 12,
  "GOLDIII": 13,
  "GOLDII": 14,
  "GOLDI": 15,
  "PLATINUMV": 16,
  "PLATINUMIV": 17,
  "PLATINUMIII": 18,
  "PLATINUMII": 19,
  "PLATINUMI": 20,
  "DIAMONDV": 21,
  "DIAMONDIV": 22,
  "DIAMONDIII": 23,
  "DIAMONDII": 24,
  "DIAMONDI": 25,
  "MASTERI": 26,
  "CHALLENGERI": 27,
}
rankdictinv = {
  1: "BRONZE V",
  2: "BRONZE IV",
  3: "BRONZE III",
  4: "BRONZE II",
  5: "BRONZE I",
  6: "SILVER V",
  7: "SILVER IV",
  8: "SILVER III",
  9: "SILVER II",
  10: "SILVER I",
  11: "GOLD V",
  12: "GOLD IV",
  13: "GOLD III",
  14: "GOLD II",
  15: "GOLD I",
  16: "PLATINUM V",
  17: "PLATINUM IV",
  18: "PLATINUM III",
  19: "PLATINUM II",
  20: "PLATINUM I",
  21: "DIAMOND V",
  22: "DIAMOND IV",
  23: "DIAMOND III",
  24: "DIAMOND II",
  25: "DIAMOND I",
  26: "MASTER I",
  27: "CHALLENGER I",
}
@app.route("/info")
def info():
    ranks = []
    name = request.args.get('name')
    name.replace(" ", "")
    region = request.args.get('region')
    api_key = "RGAPI-1739cc49-69d4-4683-bc59-5fc0c6e19028"
    api_url = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + name + "?api_key=" + api_key
    response = requests.get(api_url)
    acc_id = json.dumps(response.json()['accountId'])

    api_url_2 = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + acc_id + "?api_key=" + api_key
    matches = requests.get(api_url_2).json()['matches']
    count = 0
    inc = 0
    while (count < 3 and inc < 100):
        if matches[inc]['queue'] == 420:
            game_id = matches[inc]['gameId']
            api_url_3 = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + str(game_id) + "?api_key=" + api_key
            players = requests.get(api_url_3).json()['participantIdentities']
            for i in range (10):
                if (str(players[i]['player']['accountId']) != str(acc_id)):
                    summ_id = players[i]['player']['summonerId']
                    api_url_4 = "https://" + region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(summ_id) + "?api_key=" + api_key
                    player = requests.get(api_url_4).json()
                    if (len(player) > 0):
                        for j in range (len(player)):
                            if player[j]['queueType'] == "RANKED_SOLO_5x5":
                                ranks.append(str(player[j]['tier'] + player[j]['rank']))
            
                        
            count += 1
        inc += 1
    if (len(ranks) > 0):
        total = 0
        for i in range (len(ranks)):
            total += rankdict[ranks[i]]
        average = total/len(ranks)
        average = int(round(average,0))
        print(rankdictinv[average], file=sys.stderr)
    return (json.dumps(rankdictinv[average]))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
