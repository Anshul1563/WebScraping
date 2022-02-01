import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from selenium import webdriver
import time
import sys
import re
from bs4 import BeautifulSoup
import bs4
import requests
import pandas as pd
import numpy as np
#------------------------------------------------------------------------------
d = {'name':['a','b','c','d','e'],'views':[0,0,0,0,0],'year':[0,1,2,3,4],'tick':[1,2,3,4,5]}
df=pd.DataFrame(d)
d1 = {'tv':[0,0,0,0,0],'tick':[1,2,3,4,5]}
df1=pd.DataFrame(d)



def scraper(url):
    chrome_path = "C:/Users/bhara/py/ct/ch/chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)

    #url = 'https://www.youtube.com/c/veritasium/videos'
    driver.get(url)
    time.sleep(3)


    i = 0

    while True:
        i=i+1 
        html_from_page1 = driver.page_source
        cmd='window.scrollTo('+str(i*100000)+','+str((i+1)*100000)+');'
        driver.execute_script(cmd)
        html_from_page2 = driver.page_source
        if html_from_page2 == html_from_page1:
            time.sleep(2)
            driver.close()
            driver.quit()
            break
        html_from_page2 = html_from_page1



    html_text = html_from_page2
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    soup = BeautifulSoup(html_text, 'html.parser')

    title=soup.find_all('a',class_="yt-simple-endpoint style-scope ytd-grid-video-renderer")




    for i in range(len(title)):
        title[i]=str(title[i]).replace(',','')

    cmd1 = '(.*)(\s)(\d+)(\s)(.*)ago(\s)(\d+)(\s)(\w+)(\s)(\d*)(\s*)(.*)(\s*)(\d*)(\s*)(.*)(\s)(.*)'
    cmd2 = '(.*)aria-label=\"(.*)(\s)by(\s)(.*)ago(.*)(\s)(\d+)(\s)views'


    ago = []
    for i in title:
        m1 = re.match(cmd1,i,re.M)
        if m1:
            if (m1.group(5)).find('year') != -1:
                ago.append(int(m1.group(3)))
            else:
                ago.append(0)
        
    

    vid=[]
    viw=[]
    tick=[]
    n=1
    for i in title:
        m2 = re.match(cmd2,i,re.M)
        if m2:
            vid.append(m2.group(2))
            viw.append(int(m2.group(8)))
            tick.append(n)
            n=n+1

    global df
    d = {'name':vid,'views':viw,'year':ago,'tick':tick}
    df=pd.DataFrame(d)
    return df

def hist_plot():
    #min1=df['ago'].min()
    #max1=df['ago'].max()
    nov=[]
    b = df.year[0]
    s=0
    for i in range(len(df['name'])):
        a = df.year[i]
        if a==b:
            s=s+df.views[i]
        else:
            nov.append(s)
            s=0
        b = a
    d1={'tv':nov,'tick':[i for i in range(len(nov))]}
    df1=pd.DataFrame(d1)
    return df1


#df=scraper()
#print(df)



app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', type='text', placeholder='URL')
    ]),
    html.Button(id='sub',n_clicks=0,children=['submit']),
    html.Div(id='my-output'),
    html.Br(),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): '{} years'.format(str(year)) for year in df['year'].unique()},
        step=None
    ),
    html.Br(),
    dcc.Graph(id='complete_plot'),
    dcc.Graph(id='hist')
])


@app.callback(
    dash.dependencies.Output('year-slider', 'min'),
    dash.dependencies.Output('year-slider', 'max'),
    dash.dependencies.Output('year-slider', 'marks'),
    Output(component_id='my-output', component_property='children'),
    Input('sub','n_clicks'),
    State(component_id='my-input', component_property='value'))
def slider_setting(clicks,input_url):
    cmd='https://www.youtube.com/(.*)/videos'
    m3 = re.match(cmd,input_url,re.M)
    if m3:
        df=scraper(input_url)
        #df1=hist_plot()
        min1=df['year'].min()
        max1=df['year'].max()
        mar1={str(year): '{} years'.format(str(year)) for year in df['year'].unique()}
        return min1,max1,mar1,'success'
    else:
        min1=df['year'].min()
        max1=df['year'].max()
        mar1={str(year): '{} years'.format(str(year)) for year in df['year'].unique()}
        return min1,max1,mar1,'invalid url'



@app.callback(
    Output('graph-with-slider', 'figure'),
    Output('hist', 'figure'),
    Output('complete_plot', 'figure'),
    Input('year-slider', 'value'))
def graph_gen(slider_val):
    filtered_df = df[df.year == slider_val]
    fig = px.line(filtered_df, x='tick',y="views",markers=True,hover_data={"name":True,"views":True,"tick":False})
    fig.update_layout(transition_duration=500)
    df1=hist_plot()
    fig1=px.bar(df1,x='tick',y='tv',text_auto=True)
    fig1.update_layout(transition_duration=500)
    fig2=px.line(df,x='tick',y='views',markers=True,hover_data={"name":True,"views":True,"tick":False})
    fig2.update_layout(transition_duration=500)
    return fig,fig1,fig2



if __name__ == '__main__':
    app.run_server(debug=True)
