import math
from typing import Tuple, List
import json
import numpy as np
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


"""
ZDROJE:
https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
https://www.tutorialspoint.com/how-to-animate-a-scatter-plot-in-matplotlib
https://widdowquinn.github.io/Teaching-Data-Visualisation/exercises/making_movies/making_movies.html
https://stackoverflow.com/questions/69798653/how-to-speed-up-an-animation-in-matplotlib
https://www.geeksforgeeks.org/matplotlib-button-widget/
"""

SIZE_X = SIZE_Y = 100
# 1000 frames in 40 seconds / 25 frames per seccond == 0.04 sec per frame
SEC_PER_FRAME = 0.04

# ENABLE ROCKET
ROCKET = False

# for a quicker render
SHOW_TEXT = False


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

def x_speed_and_y_speed_to_direction_and_speed(x_speed: float, y_speed: float) -> Tuple[float, float]:
    """
    Converts x-speed and y-speed into direction and speed.
    :param x_speed: speed in the x direction in km/h
    :param y_speed: speed in the y direction in km/h
    :return: direction in degrees (0-360) and speed in km/h
    """
    direction = math.degrees(math.atan2(y_speed, x_speed)) % 360  # Convert radians to degrees and normalize to 0-360
    speed = math.sqrt(x_speed**2 + y_speed**2)  # Pythagorean theorem to find the magnitude of the vector
    return direction, speed

def collision_detection(x1, y1, x2, y2, hitbox=0.5):
    distance_x = x1 - x2
    distance_y = y1 - y2
    distance = math.sqrt((distance_x**2)+(distance_y**2))
    if distance <= hitbox and distance != 0:
        print(distance)
        return True
    else:
        return False

"""nevědel jsem jak bych zobrazil explozi země, tak jsem jí rozdělil na tři části"""
def earth_explosion(data, texts, colors):
    earth = data[39]
    
    earth1 = {'x': earth['x'], 'y': earth['y']+1, 'mass': earth['mass']/3, 'name': 'ZEME1', 'direction': 120, 'speed': 0.3, 'type': 'rock', 'acceleration': -0.005}
    earth2 = {'x': earth['x'], 'y': earth['y']-1, 'mass': earth['mass']/3, 'name': 'ZEME2', 'direction': 240, 'speed': 0.3, 'type': 'rock', 'acceleration': -0.005}
    earth3 = {'x': earth['x']+1, 'y': earth['y'], 'mass': earth['mass']/3, 'name': 'ZEME3', 'direction': 0, 'speed': 0.2, 'type': 'rock', 'acceleration': 0.1}

    if SHOW_TEXT:
        t1 = plt.text(earth1['x'], earth1['y'], earth1['name'], fontsize=10, ha='left', va='bottom', c="deepskyblue")
        t2 = plt.text(earth2['x'], earth2['y'], earth2['name'], fontsize=10, ha='left', va='bottom', c="deepskyblue")
        t3 = plt.text(earth3['x'], earth3['y'], earth3['name'], fontsize=10, ha='left', va='bottom', c="deepskyblue")
        texts += [t1, t2, t3]
    data += [earth1, earth2, earth3]
    earth['x'] = 1000
    earth['y'] = 1000
    earth['mass'] = 0
    colors += ["deepskyblue", "deepskyblue", "deepskyblue"]

def animation_update(frame, data, scatter, texts, collided, colors):
    # 1. vyresit zmenu rychlosti kvuli gravitaci
    offsets = []
    print(frame)
    for i, d in enumerate(data):
        
        final_force_x = 0
        final_force_y = 0
        for k, obj in enumerate(data):
            if k == i:
                continue
            force_x, force_y = calculate_gravitational_force(obj['x'], obj['y'], obj['mass'], d['x'], d['y'])
            final_force_x += force_x
            final_force_y += force_y

        sx, sy = direction_and_speed_to_x_speed_and_y_speed(d['direction'], d['speed'])
        x_offset = (sx - final_force_x)
        y_offset = (sy - final_force_y)
        
        d['x'] += x_offset
        d['y'] += y_offset
        direction, speed = x_speed_and_y_speed_to_direction_and_speed(x_offset, y_offset)
        d['direction'] = direction
        d['speed'] = speed
        if collision_detection(d['x'], d['y'], data[39]['x'], data[39]['y']) and len(collided)==0:
            print("COLLISION DETECTED", d['name'])
            collided.append(d)
            earth_explosion(data, texts, colors)
            
        offsets.append([d['x'], d['y']])
        if SHOW_TEXT:
            texts[i].set_position((d['x'], d['y']))
    # 2. vyresit posuny bodu
    scatter.set_offsets(offsets)
    scatter.set_color(colors)
    
    # if blit is True, update func needs to return iterable
    return [scatter, *texts]


def get_data(data):
    """
    getting data from the data dictionary to initialize the plot
    """
    xpos = []
    ypos = []
    names = []
    for i in data:
        xpos.append(i['x'])
        ypos.append(i['y'])
        names.append(i['name'])
    return xpos, ypos, names


def main():
    with open('asteroidy.json', 'r') as json_file:
        dataset = json.load(json_file)
   
    # ... vykresleni histogramu
    asteroids = [asteroid for asteroid in dataset if asteroid['name'] != 'Zeme' and asteroid['mass'] > 500]
    print()
    
    # setting up parameters for the scatter plot, custom parameters for the earth and the target asteroid
    sizes = np.full(len(dataset), 1)
    sizes[39] = 7
    colors = np.full(len(dataset), 'white', dtype='<U14')
    colors[39] = 'deepskyblue' # earth
    colors[277] = 'red' # asteroid that will hit the earth
    colors = colors.tolist() # converting to list so i will be able to add elements after earth explosion

    fig, ax = plt.subplots()
    ax.set_xlim(0, SIZE_X)
    ax.set_ylim(0, SIZE_Y)
    xs, ys, names = get_data(dataset)
    sc = ax.scatter(xs,ys, s=sizes, c=colors, marker="o")

    ax.set_facecolor('black')

    # initializing TEXT OBJECTS
    texts = [] # text object list
    if SHOW_TEXT:
        for i, name in enumerate(names):
            if name == 'Zeme':
                text = plt.text(xs[i], ys[i], name, fontsize=10, ha='left', va='bottom', c="deepskyblue")
            elif name == 'A-D81HE':
                text = plt.text(xs[i], ys[i], name, fontsize=7, ha='left', va='bottom', c="red")
            else:
                text = plt.text(xs[i], ys[i], name, fontsize=5, ha='left', va='bottom', c="white")
            texts.append(text)
      
        

    collided: List[str] = []  # nazvy asteroidy ktere narazi do Zeme
    rocket_fuel = 0 # spotrebovane palivo rakety

    # ... nacteni objektu z datasetu & filtrace    

    ani = FuncAnimation(fig, animation_update, frames=1000, interval=4, blit=False, fargs=(dataset, sc, texts, collided, colors), repeat=False)
    plt.show()
    print(collided)
    print(rocket_fuel)

    # to save the animation
    #ani.save("asteroids.gif", writer='Pillow', fps=30)


if __name__ == '__main__':
    main()
