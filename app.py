import json

from flask import Flask, render_template, jsonify, make_response

import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='templates')

urlArray = ["https://www.mohfw.gov.in/","https://www.worldometers.info/coronavirus/"]

def parse_data(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.content,'lxml')
	table = soup.find_all('table')[0] 
	df = pd.read_html(str(table))

	new_df = df[0]
	return new_df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/covid_india", methods=['GET'])
def in_live():
    url = urlArray[0]
    df = parse_data(url)
    new_df = df[:-2]
    labels = new_df["Name of State / UT"].to_list()
    confirmed_indian_case = new_df["Total Confirmed cases (Indian National)"].to_list()
    confirmed_foreig_case = new_df["Total Confirmed cases ( Foreign National )"].to_list()
    discharged = new_df["Cured/Discharged/Migrated"].to_list()
    death = new_df["Death"].to_list()
    
    data = {'labels': labels, 'confirmed_indian_case': confirmed_indian_case, 'confirmed_foreig_case': confirmed_foreig_case, 'discharged': discharged, 'death': death}
    return make_response(jsonify(data), 200)

@app.route("/covid_world", methods=['GET'])
def world_data():
    url = urlArray[1]
    df = parse_data(url)
    new_df = df[:-1].fillna(0)

    country_labels = new_df["Country,Other"].to_list()
    total_cases = new_df["TotalCases"].to_list()
    new_cases = new_df["NewCases"].to_list()
    total_deaths = new_df["TotalDeaths"].to_list()
    new_deaths = new_df["NewDeaths"].to_list()
    total_recovered = new_df["TotalRecovered"].to_list()
    active_cases = new_df["ActiveCases"].to_list()
    critical = new_df["Serious,Critical"].to_list()

    data =  {'country_labels': country_labels,'total_cases': total_cases,'new_cases': new_cases,'total_deaths': total_deaths,'new_deaths': new_deaths,'total_recovered': total_recovered,'active_cases': active_cases,'critical': critical}
    return make_response(jsonify(data), 200)


if __name__ == "__main__":
	app.run(threaded=True)