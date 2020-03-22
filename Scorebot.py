from flask import Flask
from flask import render_template
from flask import request
import sys
import threading

app = Flask(__name__, template_folder="Template", static_folder="Static")

from Classes.Team import Team
from Classes.Service import Service
from Classes.Game import Game

@app.route("/")
def renderIndex():
	return render_template("index.html", teamList = teamList, teamListStatus = teamListStatus)

@app.route("/sendFlag")
def renderSendFlag():
	return render_template("sendFlag.html", teamList = teamList, serviceList = serviceList)

@app.route("/getFlagID")
def renderGetFlagID():
	return render_template("getFlagID.html", teamList = teamList, serviceList = serviceList)

@app.route('/submit', methods=['POST'])
def submitFlag():
	flag = request.form.get('flag', None)
	team_name = request.form.get('team', None)
	service_name = request.form.get('service', None)
	status = game.submitFlags(team_name, service_name, flag)
	return status

@app.route('/flagid', methods=['GET'])
def getFlagID():
	username = request.args.get('enemy_name')
	service_name = request.args.get('service')
	flagid = game.getFlagID(service_name, username)
	return str(flagid)

def routine():
	game.setFlags(teamListStatus)
	game.getFlags()
	game.updateLog()
	threading.Timer(300, routine).start()

if __name__ == "__main__":

	teamList = { 
		"CrunchyFan": Team("CrunchyFan", "10.7.40.100", "Mario.png"),
		"UmamiPad": Team("UmamiPad", "10.7.40.200", "Luigi.png")
	}
	
	serviceList = {}

	teamListStatus = { }
	for teamName, team in teamList.iteritems():
		serviceListStatus = { }
		for serviceName, service in serviceList.iteritems():
			serviceListStatus[serviceName] = "Down"
		teamListStatus[teamName] = serviceListStatus

	honeypotList = {}

	game = Game(teamList, serviceList, honeypotList)
	
	newGame = 0
	for arg in sys.argv:
		if arg == "-n":
			newGame = 1
	if newGame:
		game.resetLog()
	else:
		game.restoreLog()
	
	threading.Timer(2, routine).start()
	app.run(host = "0.0.0.0")