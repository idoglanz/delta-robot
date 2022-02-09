from tracemalloc import start

import dash
from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
from flask import Flask

from delta_robot import DeltaRobot

server = Flask(__name__)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(server=server, external_stylesheets=external_stylesheets)
# app = Dash(server=server)
app.title = "Delta-Robot"

robot = DeltaRobot(base_radius=20, gripper_radius=12, active_arm=15, passive_arm=40)
start_pose = [0, 0, -40]

app.layout = html.Div(
    [
        html.Div(
            [
                html.H2("A (wip) Delta Robot Simulator", style={"color": "#1b3147", "text-align": "left"}),
                html.H6("By Matan Weksler and Ido Glanz", style={"color": "#1d2935", "text-align": "left"}),
                html.Div(
                    [
                        html.Button(
                            id="move_up",
                            n_clicks=0,
                            children="Move Up",
                            style={"background-color": "#1b3147", "color": "#cedae9", "width": "150px"},
                        ),
                        html.Button(
                            id="move_down",
                            n_clicks=0,
                            children="Move Down",
                            style={"background-color": "#1b3147", "color": "#cedae9", "width": "150px"},
                        ),
                    ],
                    style={
                        "vertical-align": "top",
                        "margin-left": "10vw",
                        "margin-top": "3vw",
                        "margin-bottom": "2vw",
                    },
                ),
                html.Div(
                    [
                        html.Button(
                            id="move_forward",
                            n_clicks=0,
                            children="Move Forward",
                            style={"background-color": "#617487", "color": "#cedae9", "width": "200px"},
                        ),
                    ],
                    style={
                        "vertical-align": "top",
                        "margin-left": "13vw",
                        "margin-top": "2vw",
                        "margin-bottom": "2vw",
                    },
                ),
                html.Div(
                    [
                        html.Button(
                            id="move_right",
                            n_clicks=0,
                            children="Move Right",
                            style={"background-color": "#99b2d1", "color": "#0c2032", "width": "150px"},
                        ),
                        html.Button(
                            id="move_left",
                            n_clicks=0,
                            children="Move Left",
                            style={"background-color": "#99b2d1", "color": "#0c2032", "width": "150px"},
                        ),
                    ],
                    style={
                        "vertical-align": "top",
                        "margin-left": "10vw",
                        "margin-top": "2vw",
                        "margin-bottom": "2vw",
                    },
                ),
                html.Div(
                    [
                        html.Button(
                            id="move_back",
                            n_clicks=0,
                            children="Move Back",
                            style={"background-color": "#617487", "color": "#cedae9", "width": "200px"},
                        ),
                    ],
                    style={
                        "vertical-align": "top",
                        "margin-left": "13vw",
                        "margin-top": "2vw",
                        "margin-bottom": "2vw",
                    },
                ),
                html.Div(
                    [
                        html.Button(
                            id="reset",
                            n_clicks=0,
                            children="Reset",
                            style={"background-color": "#cedae9", "color": "#1b3147", "width": "120px"},
                        ),
                    ],
                    style={
                        "vertical-align": "top",
                        "margin-left": "16vw",
                        "margin-top": "5vw",
                        "margin-bottom": "2vw",
                    },
                ),
                html.Div(
                    [
                        html.H6("Top Triangle Radius", style={"color": "#b40000", "text-align": "left"}),
                        dcc.Input(id="base_radius", type="number", placeholder="20", value=None),
                        html.H6("Gripper Triangle Radius", style={"color": "#03396c", "text-align": "left"}),
                        dcc.Input(id="gripper_radius", type="number", placeholder="12", value=None),
                    ],
                    style={
                        "width": "35%",
                        "display": "inline-block",
                        "horizontal-align": "right",
                        "vertical-align": "top",
                        "margin-left": "4vw",
                    },
                ),
                html.Div(
                    [
                        html.H6("Active Arms Length", style={"color": "#2f5233", "text-align": "left"}),
                        dcc.Input(id="active_arm", type="number", placeholder="15", value=None),
                        html.H6("Passive Arms Length", style={"color": "#f5a335", "text-align": "left"}),
                        dcc.Input(id="passive_arm", type="number", placeholder="40", value=None),
                    ],
                    style={
                        "width": "35%",
                        "display": "inline-block",
                        "horizontal-align": "right",
                        "vertical-align": "top",
                        "margin-left": "4vw",
                    },
                ),
            ],
            style={"width": "40%", "display": "inline-block", "horizontal-align": "right", "vertical-align": "top", "margin-left": "2vw"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="robot"),
                    ],
                    style={
                        "width": "80%",
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                        "margin-bottom": "3vw",
                    },
                ),
                html.Div(
                    [
                        dcc.Textarea(
                            value=f"Current position is: X = {str(start_pose[0])} | Y = {str(start_pose[1])} | Z = {str(start_pose[2])}",
                            style={"width": "60%", "height": 20, "margin-left": "3vw",'color':'#617487',"outline-color":'white'},
                            id="label",
                        )
                    ],style={'color':'white'}
                ),
            ],
            style={"width": "50%", "display": "inline-block", "margin-left": "2vw"},
        ),
    ]
)


@app.callback(
    Output("robot", "figure"),
    Output("label", "value"),
    Input("move_up", "n_clicks"),
    Input("move_down", "n_clicks"),
    Input("move_right", "n_clicks"),
    Input("move_left", "n_clicks"),
    Input("move_forward", "n_clicks"),
    Input("move_back", "n_clicks"),
    Input("reset", "n_clicks"),
)
def update_figure(b1, b2, b3, b4, b5, b6, b_reset):
    global start_pose
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = "not pressed yet"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(button_id)
    inc = 4
    if button_id.endswith("up"):
        start_pose[2] += inc
    if button_id.endswith("down"):
        start_pose[2] -= inc
    if button_id.endswith("right"):
        start_pose[1] -= inc
    if button_id.endswith("left"):
        start_pose[1] += inc
    if button_id.endswith("forward"):
        start_pose[0] += inc
    if button_id.endswith("back"):
        start_pose[0] -= inc
    if button_id == "reset":
        start_pose = [0, 0, -40]
    start_pose = robot.update_pose(start_pose)
    print(start_pose)
    plot = robot.draw()
    plot["layout"]["uirevision"] = "Do not change"
    return plot, f"Current position is: X = {str(start_pose[0])} | Y = {str(start_pose[1])} | Z = {str(start_pose[2])}"


@app.callback(
    Output("base_radius", "type"),
    Input("base_radius", "value"),
    Input("gripper_radius", "value"),
    Input("active_arm", "value"),
    Input("passive_arm", "value"),
)
def set_robot_params(top_r, grip_r, active, passive):
    input_dict = {"base_radius": top_r, "gripper_radius": grip_r, "active_arm": active, "passive_arm": passive}
    print(input_dict)
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if isinstance(input_dict.get(input_id), int):
        print({input_id: input_dict[input_id]})
        robot.update_structure({input_id: input_dict[input_id]})
    return "number"


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
