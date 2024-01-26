import math
from typing import Tuple, List
import json
import numpy as np



SIZE_X = SIZE_Y = 100
# 1000 frames in 40 seconds / 25 frames per seccond == 0.04 sec per frame
SEC_PER_FRAME = 0.04


def calculate_gravitational_force(x: float, y: float, mass: float, target_x: float, target_y: float) -> Tuple[float, float]:
    """
    Calculates the gravitational force between two points
    :param x: center of X point
    :param y: center of Y point
    :param mass: mass of the point
    :param target_x: influenced point's X
    :param target_y: influenced point's Y
    :return: difference of X-speed and Y-speed based on
    """
    gravity_strength = (mass * 10**-28)**0.5
    distance_x = target_x - x
    distance_y = target_y - y
    distance = (distance_x**2 + distance_y**2)**0.5
    force_x = (distance_x / distance) * gravity_strength / distance
    force_y = (distance_y / distance) * gravity_strength / distance
    return force_x, force_y


def calculate_gravity_affected_speed(x: float, y: float, mass: float, target_x: float, target_y: float, target_speed_x: float, target_speed_y: float) -> Tuple[float, float]:
    """
    Calculates new X-speed and Y-speed of a target point
    """
    force_x, force_y = calculate_gravitational_force(x, y, mass, target_x, target_y)
    return target_speed_x - force_x, target_speed_y - force_y


def direction_and_speed_to_x_speed_and_y_speed(direction: float, speed: float) -> Tuple[float, float]:
    """
    Converts direction and speed into a 2D vector representing the x speed and y speed.
    :param direction: direction in degrees (0-360)
    :param speed: speed in km/h
    :return: x-speed and y-speed in km/h
    """
    x_speed = speed * math.cos(math.radians(direction))
    y_speed = speed * math.sin(math.radians(direction))
    return x_speed, y_speed


def animation_update(_):
    # 1. vyresit zmenu rychlosti kvuli gravitaci
    pass
    # 2. vyresit posuny bodu
    pass

def get_position(data):
    xpos = []
    ypos = []
    for i in data:
        xpos.append(i['x'])
        ypos.append(i['y'])
    return xpos, ypos



def main():
    with open('asteroidy.json', 'r') as json_file:
        asteroids = json.load(json_file)
    import matplotlib.pyplot as plt
    
    # ... vykresleni histogramu
    
    from matplotlib.animation import FuncAnimation

    sizes = np.full(len(asteroids), 1)
    sizes[39] = 100
    colors = np.full(len(asteroids), 'black')
    colors[39] = 'blue'
    fig, ax = plt.subplots()
    ax.set_xlim(0, SIZE_X)
    ax.set_ylim(0, SIZE_Y)
    xs, ys = get_position(asteroids)
    ax.scatter(xs,ys, s=sizes, c=colors)

    collided: List[str] = []  # nazvy asteroidy ktere narazi do Zeme
    rocket_fuel = 0 # spotrebovane palivo rakety

    # ... nacteni objektu z datasetu & filtrace    

   # ani = FuncAnimation(fig, animation_update, frames=1000, blit=True)
    plt.show()
    print(collided)
    print(rocket_fuel)


if __name__ == '__main__':
    main()
