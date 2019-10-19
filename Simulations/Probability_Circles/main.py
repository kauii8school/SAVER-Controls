#Simplified 2 dimensional simulation showing how SAVER will travel to probabilitiy distribution centers using travelling salesman and 
#Fluid mechanics calculations 

import numpy as np 
import matplotlib.pyplot as plt
import random
from functions import * 
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from TSP import tsp
from matplotlib.lines import Line2D

global side_length
side_length = 32/2 #km 

class SAVER:

    def __init__ (self, initial_position = None, initial_velocity = None, initial_acceleration = None, detection_radius = 17):

        """inital_position -  2D tuple of (x,y), where x and y are in km
            inital_velocity - 2D tuple of (x,y,s) where x,y are directional positions in km/s and s is total speed  """

        if initial_position == None:
            initial_position_x = random.uniform(-1*side_length, side_length)
            initial_position_y = random.uniform(-1*side_length, side_length)
            initial_position = (initial_position_x, initial_position_y)
        if initial_velocity == None:
            velocity_lower_bound, velocity_upper_bound = -.1, .1
            initial_velocity_x = random.uniform(velocity_lower_bound, velocity_upper_bound)
            initial_velocity_y = random.uniform(velocity_lower_bound, velocity_upper_bound)
            initial_velocity_s = np.sqrt((initial_velocity_x ** 2) + (initial_velocity_y ** 2))
            initial_velocity = (initial_velocity_x, initial_velocity_y, initial_velocity_s)
        else: 
            initial_velocity = (initial_velocity[0], initial_velocity[1], np.sqrt((initial_velocity[0] ** 2) + (initial_velocity[1] ** 2)))
        if initial_acceleration == None:
            acceleration_lower_bound, acceleration_upper_bound = -.1, .1
            initial_acceleration_x = random.uniform(acceleration_lower_bound, acceleration_upper_bound)
            initial_acceleration_y = random.uniform(acceleration_lower_bound, acceleration_upper_bound)
            initial_acceleration_s = np.sqrt((initial_acceleration_x ** 2) + (initial_acceleration_y ** 2))
            initial_acceleration = (initial_acceleration_x, initial_acceleration_y, initial_acceleration_s)
        else: 
            initial_acceleration = (initial_acceleration[0], initial_acceleration[1], np.sqrt((initial_acceleration[0] ** 2) + (initial_acceleration[1] ** 2)))
        
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration
        self.detection_radius = detection_radius
        self.get_detection_polygon()

    def update_velocity(self, delta_x, delta_y):
        x = self.velocity[0] + delta_x
        y = self.velocity[1] + delta_y
        s = np.sqrt((x**2) + (y**2))
        self.velocity = (x, y, s)

    def update_position(self, delta_x, delta_y):
        x = self.position[0] + delta_x
        y = self.position[1] + delta_y
        self.position = (x, y)

    def update_acceleration(self, delta_x, delta_y):
        x = self.acceleration[0] + delta_x
        y = self.acceleration[1] + delta_y
        s = np.sqrt((x**2) + (y**2))
        self.acceleration = (x, y, s)

    def print_properties(self):
        print("Position: {}".format(self.position))
        print("Velocity {}".format(self.velocity))
        print("Detection radius {}".format(self.detection_radius))

    def get_detection_polygon(self, num_pts=100):
        poly = Polygon([[self.detection_radius * np.cos(theta) + self.position[0], self.detection_radius * np.sin(theta) + self.position[1]]\
             for theta in np.linspace(0, 2*np.pi,num_pts)])
        self.polygon = poly
        return poly

    def plot_SAVER(self, ax):
        ax.scatter(self.position[0], self.position[1], marker="*", c='g', s=100, zorder=10, label='SAVER')
        ax.arrow(self.position[0], self.position[1], self.velocity[0], self.velocity[1], color='b', label='velocity', zorder=11)
        ax.arrow(self.position[0], self.position[1], self.acceleration[0], self.acceleration[1], color='r', label='acceleration', zorder=12)
        x,y = self.polygon.exterior.coords.xy
        ax.plot(x, y, color='g', alpha=0.3, linewidth=1, solid_capstyle='round', zorder=2)
        circle = plt.Circle((self.position[0], self.position[1]), self.detection_radius, color='g', alpha=.3)
        ax.add_artist(circle)

class Astronaut:

    def __init__ (self, initial_position = None, initial_velocity = None, initial_acceleration = None):

        """inital_position -  2D tuple of (x,y), where x and y are in km
            inital_velocity - 2D tuple of (x,y,s) where x,y are directional positions in km/s and s is total speed  """

        if initial_position == None:
            initial_position_x = random.uniform(-1*side_length, side_length)
            initial_position_y = random.uniform(-1*side_length, side_length)
            initial_position = (initial_position_x, initial_position_y)
        if initial_velocity == None:
            velocity_lower_bound, velocity_upper_bound = -.1, .1
            initial_velocity_x = random.uniform(velocity_lower_bound, velocity_upper_bound)
            initial_velocity_y = random.uniform(velocity_lower_bound, velocity_upper_bound)
            initial_velocity_s = np.sqrt((initial_velocity_x ** 2) + (initial_velocity_y ** 2))
            initial_velocity = (initial_velocity_x, initial_velocity_y, initial_velocity_s)
        else: 
            initial_velocity = (initial_velocity[0], initial_velocity[1], np.sqrt((initial_velocity[0] ** 2) + (initial_velocity[1] ** 2)))
        if initial_acceleration == None:
            acceleration_lower_bound, acceleration_upper_bound = -.1, .1
            initial_acceleration_x = random.uniform(acceleration_lower_bound, acceleration_upper_bound)
            initial_acceleration_y = random.uniform(acceleration_lower_bound, acceleration_upper_bound)
            initial_acceleration_s = np.sqrt((initial_acceleration_x ** 2) + (initial_acceleration_y ** 2))
            initial_acceleration = (initial_acceleration_x, initial_acceleration_y, initial_acceleration_s)
        else: 
            initial_acceleration = (initial_acceleration[0], initial_acceleration[1], np.sqrt((initial_acceleration[0] ** 2) + (initial_acceleration[1] ** 2)))
        
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration

    def update_velocity(self, delta_x, delta_y):
        x = self.velocity[0] + delta_x
        y = self.velocity[1] + delta_y
        s = np.sqrt((x**2) + (y**2))
        self.velocity = (x, y, s)

    def update_position(self, delta_x, delta_y):
        x = self.position[0] + delta_x
        y = self.position[1] + delta_y
        self.position = (x, y)

    def update_acceleration(self, delta_x, delta_y):
        x = self.acceleration[0] + delta_x
        y = self.acceleration[1] + delta_y
        s = np.sqrt((x**2) + (y**2))
        self.acceleration = (x, y, s)

    def in_polygon(self, polygon):
        return polygon.contains(Point([self.position[0], self.position[1]]))

    def print_properties(self):
        print("Position: {}".format(self.position))
        print("Velocity {}".format(self.velocity))

    def plot_astronaut(self, ax, saver):
        if self.in_polygon(saver.get_detection_polygon()) == True:
            color_astro = 'g'
        else: 
            color_astro = 'k'
        ax.scatter(self.position[0], self.position[1], marker="^", c=color_astro, s=20, zorder=7, label='Astonaut')
        ax.arrow(self.position[0], self.position[1], self.velocity[0], self.velocity[1], color='b', label='velocity', zorder=8)
        ax.arrow(self.position[0], self.position[1], self.acceleration[0], self.acceleration[1], color='r', label='acceleration', zorder=9)


svr = SAVER(initial_velocity = (11, -1.2), initial_acceleration=(1,5))
num_astronauts = 4
lst_astronauts = [Astronaut() for i in range(0, num_astronauts)]
svr.print_properties()

svr.update_velocity(-1, 1)
svr.update_position(-1, 1)
fig, ax = plt.subplots()
for astronaut in lst_astronauts:
    astronaut.print_properties()
    astronaut.plot_astronaut(ax, svr)

#Beginning of travelling salesman
node_list = [astronaut.position for astronaut in lst_astronauts]
node_list.insert(0, svr.position)
print(node_list)
tsp_idx, distance = tsp(node_list)
tsp_idx.pop(-1)

node_list_x, node_list_y = zip(*node_list)
ax.set_xlabel('km')
ax.set_ylabel('km')
ax.plot(node_list_x, node_list_y, linestyle="--", linewidth=3, color='m')
ax.set_xlim([-1*side_length, side_length])
ax.set_ylim([-1*side_length, side_length])
ax.grid()
svr.plot_SAVER(ax)

custom_lbls = [Line2D([0], [0], color='r', lw=4, alpha=1),
                Line2D([0], [0], color='b', lw=4, alpha=1),
               Line2D([], [], color='m', lw=3, linestyle='--'),
              Line2D([], [], color='g', linestyle="None", marker="*", lw=3),
              Line2D([], [], color='k', linestyle="None", marker="^", lw=3),
              Line2D([], [], color='g', linestyle="None", marker="^", lw=3)]

ax.legend(custom_lbls, ['Acceleration', 'Velocity', 'Path', 'SAVER', 'Astronaut out of FOV', 'Astronaut in FOV' ], loc='upper left')

plt.show()