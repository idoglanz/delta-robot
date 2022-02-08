import plotly.graph_objects as go

fig = go.Figure()

def triangle(fig:go.Figure,t1,t2,t3):
    points = [t1,t2,t3,t1]
    x = [p[0] for p in points]
    x = [p[0] for p in points]
    x = [p[0] for p in points]
    
    fig.add_trace(data=go.Scatter3d())