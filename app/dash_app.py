from tracemalloc import start
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from app.delta_robot import DeltaRobot

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

robot = DeltaRobot(base_radius=20, gripper_radius=12, active_arm=15, passive_arm=40)
start_pose = [0, 0, -40]

app = Dash(__name__, external_stylesheets=external_stylesheets)
# app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("A Delta Robot Simulator",style={'color':'#00361c','text-align':'left'
          }),
                html.Div(
                    [
                        html.Button(id="move_up", n_clicks=0, children="Move Up",style={'width':"15"}),
                        html.Button(id="move_down", n_clicks=0, children="Move Down",style={'width':"15"}),
                    ],
                    style={"vertical-align": "top", "margin-left": "10vw", "margin-top": "3vw", "margin-bottom": "2vw"},
                ),
                html.Div(
                    [
                        html.Button(id="move_forward", n_clicks=0, children="Move Forward",style={'width':"15"}),
                    ],
                    style={"vertical-align": "top", "margin-left": "13vw", "margin-top": "3vw", "margin-bottom": "2vw"},
                ),
                html.Div(
                    [
                        html.Button(id="move_right", n_clicks=0, children="Move Right",style={'width':"15"}),
                        html.Button(id="move_left", n_clicks=0, children="Move Left",style={'width':"15"}),
                    ],
                    style={"vertical-align": "top", "margin-left": "10vw", "margin-top": "3vw", "margin-bottom": "2vw"},
                ),
                html.Div(
                    [
                        html.Button(id="move_back", n_clicks=0, children="Move Back",style={'width':"15"}),
                    ],
                    style={"vertical-align": "top", "margin-left": "13vw", "margin-top": "3vw", "margin-bottom": "2vw"},
                ),
            ],
            style={"width": "30%", "display": "inline-block", "horizontal-align": "right", "vertical-align": "top"},
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
                            value=f"Current position is {str(start_pose)}",
                            style={"width": "90%", "height": 20, "margin-left": "3vw"},
                            id="label",
                        )
                    ]
                ),
            ],
            style={"width": "50%", "display": "inline-block"},
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
)
def update_figure(b1, b2, b3, b4, b5, b6):
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

    start_pose = robot.update_pose(start_pose)
    print(start_pose)
    plot = robot.draw()
    plot["layout"]["uirevision"] = "Do not change"
    return plot, f"Current position is {str(start_pose)}"


if __name__ == "__main__":
    app.run_server(debug=True)
