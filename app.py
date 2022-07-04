from os import system
system('chmod 600 /Users/srinivasansrinivasan/.kaggle/kaggle.json')
import kaggle
system("kaggle d download -d robikscube/zillow-home-value-index")

import zipfile

zip_ref = zipfile.ZipFile("./zillow-home-value-index.zip", 'r')
zip_ref.extractall("./")
zip_ref.close()

import pandas as pd
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

ZHVI = pd.read_csv('./ZHVI.csv')

ZHVI.columns = ['Date', 'California', 'Florida', 'New York', 'Arizona',
           'Massachusetts', 'Texas', 'Colorado', 'New Jersey', 'Georgia', 'Nevada',
           'North Carolina', 'Montana', 'Tennessee', 'Illinois', 'Oregon',
           'Minnesota', 'the District of Columbia', 'New Hampshire', 'Washington',
           'Michigan', 'Connecticut', 'Missouri', 'Hawaii', 'Ohio', 'Utah',
           'Virginia', 'Idaho', 'Vermont', 'Alabama', 'Rhode Island', 'Kansas',
           'South Carolina', 'Maryland', 'New Mexico', 'Wisconsin', 'Pennsylvania',
           'Nebraska', 'Arkansas', 'Alaska', 'Kentucky', 'West Virginia',
           'South Dakota', 'Indiana', 'Maine', 'Wyoming', 'Mississippi',
           'Delaware', 'Iowa', 'Oklahoma', 'Louisiana', 'North Dakota']

import plotly
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

def makePlotandSaveToHTML(dataset, x='Date', title='Title'):
      fig1 = px.line(title=title)
      df_sample = dataset - dataset[x]
      for i in dataset.columns[1:]:
          fig1.add_scatter(x=dataset[x], y=dataset[i], name=i)
      fig = go.Figure(data=fig1)
      plotly.offline.plot(fig,filename=f'templates/{title.replace(" ", "_")}.html',config={'displayModeBar': False})
      return fig
def normalize_data(df):
      x = df.copy()
      for i in x.columns[1:]:
        x[i] = x[i]/x[i][0]
      return x
def get_daily_return_percent(df, indStocks):
      new_df = pd.DataFrame()
      new_df[indStocks[0]] = df[indStocks[0]]
      for stock in indStocks[1:]:
        a = df[stock]
        b = a.copy()
        for i in range(1, len(a)):
          b[i] = ((a[i] - a[i-1])/a[i-1])*100
        b[0] = 0
        new_df[stock] = b
      return new_df
def get_daily_return_real(df, indStocks):
      new_df = pd.DataFrame()
      new_df[indStocks[0]] = df[indStocks[0]]
      for stock in indStocks[1:]:
        a = df[stock]
        b = a.copy()
        for i in range(1, len(a)):
          b[i] = a[i] - a[i-1]
        b[0] = 0
        new_df[stock] = b
      return new_df
def total_return(df, indStocks):
      new_df = pd.DataFrame()
      new_df[indStocks[0]] = df[indStocks[0]]
      for stock in indStocks[1:]:
        a = df[stock]
        b = a.copy()
        for i in range(1, len(a)):
          b[i] = a[i] - a[0]
        b[0] = 0
        new_df[stock] = b
      return new_df

main = makePlotandSaveToHTML(ZHVI, 'Date', 'House Prices In Dollars')
normalized = makePlotandSaveToHTML(normalize_data(ZHVI), 'Date', 'Overall Change As A Percent')
daily_percent = makePlotandSaveToHTML(get_daily_return_percent(ZHVI, ZHVI.columns), 'Date', 'Monthly Change As A Percent')
daily_numchange = makePlotandSaveToHTML(get_daily_return_real(ZHVI, ZHVI.columns), 'Date', 'Monthly Change In Dollars')
overall_numchange = makePlotandSaveToHTML(total_return(ZHVI, ZHVI.columns), 'Date', 'Overall Change In Dollars')

from flask import Flask, render_template, request, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img
logo = img(src="./static/img/logo.png" , height="50", width="50", style="margin-top:-15px")
topbar = Navbar(logo,
                View('Homepage', 'homePage'),
                View('House Prices In Dollars', 'housePricesInDollars'),
                View('Monthly Change In Dollars', 'monthlyChangeInDollars'),
                View('Monthly Change As A Percent', 'monthlyChangeAsAPercent'),
                View('Overall Change In Dollars', 'overallChangeInDollars'),
                View('Overall Change As A Percent', 'overallChangeAsAPercent'),
                View('Credits', 'creditsTo'))
nav = Nav()
nav.register_element('top', topbar)
app = Flask(__name__)
app.config['SECRET_KEY'] = '17bb05ad20765f49322692652f2bf6d761bf9wn29dm39aso'
Bootstrap(app)


@app.route('/', methods=["Get"])
def homePage():
    return render_template('homePage.html')

@app.route('/credits', methods=["Get"])
def creditsTo():
    return render_template('Credits.html')


@app.route('/housePricesInDollars', methods=["Get"])
def housePricesInDollars():
    return render_template('UniversalDataShower.html', data=['House_Prices_In_Dollars.html'])

@app.route('/monthlyChangeInDollars', methods=["Get"])
def monthlyChangeInDollars():
    return render_template('UniversalDataShower.html', data=['Monthly_Change_In_Dollars.html'])

@app.route('/monthlyChangeAsAPercent', methods=["Get"])
def monthlyChangeAsAPercent():
    return render_template('UniversalDataShower.html', data=['Monthly_Change_As_A_Percent.html'])

@app.route('/overallChangeInDollars', methods=["Get"])
def overallChangeInDollars():
    return render_template('UniversalDataShower.html', data=['Overall_Change_In_Dollars.html'])

@app.route('/overallChangeAsAPercent', methods=["Get"])
def overallChangeAsAPercent():
    return render_template('UniversalDataShower.html', data=['Overall_Change_As_A_Percent.html'])

nav.init_app(app)
app.run()