import dash
import base64
import dash_html_components as html

app = dash.Dash(__name__)


test_png = 'wordcloud_output.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')


app.layout = html.Div([
        html.Img(src='data:image/png;base64,{}'.format(test_base64)),
        ])

if __name__ == '__main__':
        app.run_server(debug=True, use_reloader=False)