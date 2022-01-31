import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px

import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import praw
reddit = praw.Reddit(
    client_id="wBlYlJ7XtNtL0d1fEAj-vg",
    client_secret="muW07OSaCr5I4Dj23Sn7HeFeoifSLg",
    user_agent="a12487"
)
from wordcloud import WordCloud
import cv2 
# print(px.data.gapminder()[:15])

app = dash.Dash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([

     dcc.Graph(id='container-button-basic'),

    html.Div([
        dcc.Input(id='input_state', type='text'),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.Div(id='output_state'),
    ],style={'text-align': 'center'}),

])

#---------------------------------------------------------------
@app.callback(
    [Output('output_state', 'children'),
    Output(component_id='container-button-basic', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')]
)

def update_output(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        subreddit = reddit.subreddit(val_selected)
        sub_title = []
        for submission in subreddit.top('all',limit = 100):
            sub_title.append(submission.title)
        y = []
        for x in sub_title:
            x = x.lower()
            y.append(x)
        wordcloud = WordCloud(width = 1200, height = 600, max_font_size = 200,background_color = 'white', colormap = 'viridis')
        wordcloud = wordcloud.generate(' '.join(y))
        img = wordcloud.to_file('work.png')
        fimg = cv2.imread('work.png')
        fig = px.imshow(fimg)
        fig.update_layout(title_text='Commonly used words', title_x=0.5)
        
        

        return (fig)

if __name__ == '__main__':
    app.run_server(debug=True)