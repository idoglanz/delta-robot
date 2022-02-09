import plotly.graph_objects as go
import numpy as np

import logging

def rotM(theta_rad, axis:str='z'):
  if axis == 'z':
    return np.array([[np.cos(theta_rad),-np.sin(theta_rad),0],[np.sin(theta_rad),np.cos(theta_rad),0],[0,0,1]])
  if axis == 'x':
    return np.array([[1,0,0],[0, np.cos(theta_rad),-np.sin(theta_rad)],[0, np.sin(theta_rad),np.cos(theta_rad)]])
  if axis == 'y':
    return np.array([[np.cos(theta_rad),0, np.sin(theta_rad)],[0,1,0],[np.sin(theta_rad),0, -np.cos(theta_rad)]])


def triangle_from_r(fig, r,e,theta=[0,120,240],**kwargs):
  theta.append(theta[0])  # to get a "closed" triangle
  theta = np.array(theta)*np.pi/180
  triangle = np.vstack([r*(np.cos(theta)),r*(np.sin(theta)), np.zeros([4])]).T + e
  fig.add_trace(go.Scatter3d(x=triangle[:,0],y=triangle[:,1],z=triangle[:,2],mode="lines",line = {'width':2}))
  return triangle


def triangle_from_r_withM(fig, r,e,theta=[0,120,240],**kwargs):
  theta.append(theta[0])   # to get a "closed" triangle
  theta = np.array(theta)*np.pi/180
  r = np.expand_dims(np.array([r,0,0]), 1)
  triangle = np.hstack([np.matmul(rotM(angle,'z'),r) for angle in theta]).T + e
  fig.add_trace(go.Scatter3d(x=triangle[:,0],y=triangle[:,1],z=triangle[:,2],mode="lines",line = {'width':2}))
  return triangle
  

def draw_active_arms(fig, length, phi, triangle_r, theta, e, triangle):
  theta = np.array(theta)*np.pi/180
  vec = np.matmul(rotM(-phi*np.pi/180,'y'),np.expand_dims(np.array([length,0,0]), 1)) + np.expand_dims(np.array([triangle_r,0,0]), 1)
  arms = np.hstack([np.matmul(rotM(angle,'z'),vec) for angle in theta]).T + e
  for p1, p2 in zip(arms,triangle[:3,:]):
    fig.add_trace(go.Scatter3d(x=[p1[0],p2[0]],y=[p1[1],p2[1]],z=[p1[2],p2[2]],mode="lines",line = {'width':2}))
  return arms


def draw_passive_arms(fig, arms, triangle):
    for p1, p2 in zip(arms, triangle[:3,:]):
      fig.add_trace(go.Scatter3d(x=[p1[0],p2[0]],y=[p1[1],p2[1]],z=[p1[2],p2[2]],mode="lines",line = {'width':2}))


fig = go.Figure()

r = 10
e = [0,0,0]
R = 5
E = [0,0,-40]

t = [0,120,240]

phi = 40

triangle_from_r(fig,r,e,theta=[0,120,240])
triangle_from_r(fig,R,E,theta=[0,120,240])

top_triangle = triangle_from_r_withM(fig,r,e,theta=[0,120,240])
bottom_triangle = triangle_from_r_withM(fig,R,E,theta=[0,120,240])

arms = draw_active_arms(fig, 15,phi,r,[0,120,240],e,top_triangle)
draw_passive_arms(fig,arms, bottom_triangle)

fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=4, range=[-r*5,r*5],),
        yaxis = dict(nticks=4, range=[-r*5,r*5],),
        zaxis = dict(nticks=4, range=[-r*5,r*5],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))

fig.update_layout(scene_aspectmode='cube')

fig.show()