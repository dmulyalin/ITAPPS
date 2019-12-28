import dash
import dash_html_components as html

ttp_parser_dash_app = dash.Dash(
    __name__,
    routes_pathname_prefix='/tools/ttp_parser/'
)

ttp_parser_dash_app.layout = html.Div("My Dash app")