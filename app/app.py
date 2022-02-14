import dash
from dash import Dash, Input, Output, dcc, html
from flask import Flask

from delta_robot import DeltaRobot
from controller import DeltaController
from gcode_parser import GcodeParser

server = Flask(__name__)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(server=server, external_stylesheets=external_stylesheets)
app.title = "Delta-Robot"

# Robot setup
robot = DeltaRobot(base_radius=180, gripper_radius=100, active_arm=120, passive_arm=300)
start_pose = pose = [0, 0, -260]
controller = DeltaController(start_pose, speed=30)
gcode = GcodeParser('./gcode/D_leaf_test.gcode')
is_playing = False  # sets stopwatch on/off
duration = 100  # shouldn't change anything 

app.layout = html.Div(
    [
        dcc.Interval(id="stopper", interval=100, n_intervals=0, disabled=True),
        html.Div(
            [
                html.H2("A (wip) Delta Robot Simulator", style={"color": "#1b3147", "text-align": "left"}),
                html.H6(
                    "Use the buttons to move the robot, all dimensions are in mm, Press Play to run a gcode sample",
                    style={"color": "#1d2935", "text-align": "left"},
                ),
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
                        html.Button(
                            id="play",
                            n_clicks=0,
                            children="Play Gcode",
                            style={"background-color": "#41924B", "color": "#EFF3EF", "width": "120px"},
                        ),
                    ],
                    style={
                        "vertical-align": "top",
                        "margin-left": "16vw",
                        "margin-top": "2vw",
                        "margin-bottom": "2vw",
                    },
                ),
                html.Div(
                    [
                        html.H6("Top Triangle Radius", style={"color": "#b40000", "text-align": "left"}),
                        dcc.Input(id="base_radius", type="number", placeholder="180", value=None),
                        html.H6("Gripper Triangle Radius", style={"color": "#03396c", "text-align": "left"}),
                        dcc.Input(id="gripper_radius", type="number", placeholder="100", value=None),
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
                        dcc.Input(id="active_arm", type="number", placeholder="120", value=None),
                        html.H6("Passive Arms Length", style={"color": "#f5a335", "text-align": "left"}),
                        dcc.Input(id="passive_arm", type="number", placeholder="300", value=None),
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
            style={
                "width": "40%",
                "display": "inline-block",
                "horizontal-align": "right",
                "vertical-align": "top",
                "margin-left": "2vw",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="robot"),
                    ],
                    style={
                        "width": "100%",
                        # "display": "inline-block",
                        "vertical-align": "bottom",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                        "margin-bottom": "3vw",
                    },
                ),
                html.Div(
                    [
                        dcc.Textarea(
                            value=f"Current position is: X = {str(pose[0])} | Y = {str(pose[1])} | Z = {str(pose[2])}",
                            style={"width": "60%", "height": 20, "margin-left": "6vw", "color": "#617487"},
                            id="label",
                        )
                    ],
                    style={"color": "white"},
                ),
            ],
            style={"width": "50%", "display": "inline-block"},
        ),
    ]
)

@app.callback(
    Output("robot", "figure"),
    Output("label", "value"),
    Output("play", "children"),
    Output("stopper", "interval"),
    Output("stopper", "disabled"),
    Input("move_up", "n_clicks"),
    Input("move_down", "n_clicks"),
    Input("move_right", "n_clicks"),
    Input("move_left", "n_clicks"),
    Input("move_forward", "n_clicks"),
    Input("move_back", "n_clicks"),
    Input("reset", "n_clicks"),
    Input("play", "n_clicks"),
    Input("stopper", "n_intervals"),
)
def update_figure(b1, b2, b3, b4, b5, b6, b_reset, play, stopwatch):
    global pose, is_playing, duration
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "not pressed yet"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(button_id)
    inc = 4

    if button_id.endswith("up"):
        pose[2] += inc
    if button_id.endswith("down"):
        pose[2] -= inc
    if button_id.endswith("right"):
        pose[1] -= inc
    if button_id.endswith("left"):
        pose[1] += inc
    if button_id.endswith("forward"):
        pose[0] += inc
    if button_id.endswith("back"):
        pose[0] -= inc
    
    if button_id == "reset":
        pose = start_pose
        robot.reset_trace(pose)
    
    if button_id == "play":
        is_playing = not is_playing
        duration = 1

    if button_id == "stopper":
        if is_playing:
            command_dict = gcode.get.__next__()
            # print(f'Next command is {command_dict}')
            pose, duration = controller.next_action(command_dict)

    pose = robot.update_pose(pose)
    print(pose)
    plot = robot.draw()
    plot["layout"]["uirevision"] = "Do not change"
    return (
        plot,
        f"Current position is: X = {str(round(pose[0],3))} | Y = {str(round(pose[1],3))} | Z = {str(round(pose[2],3))}",
        "Pause" if is_playing else "Play",
        duration*1000,
        not is_playing  # disable interval if not playing
    )


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
