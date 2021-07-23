import numpy as np
from jpype import *
import orhelper
import random
import math
import os
import sys
import json
from datetime import datetime

from collections import OrderedDict
import matplotlib, urllib, base64
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# List of default data for simulation tracking.
DEFAULT_STATS = ['Lateral distance', 'Lateral direction', 'Time', 'Altitude']

def main():
    print("Start simulation")

    filename = 'rocket.ork'

    with orhelper.OpenRocketInstance('/app/share/OpenRocket.jar', log_level='DEBUG'):
        # Load the document and get simulation
        orh = orhelper.Helper()
        doc = orh.load_doc('/app/share/rockets/' + filename)
        sim = doc.getSimulation(0)

        opts = sim.getOptions()
        rocket = opts.getRocket()

        landings = []

        for j in range(3):
            opts.setLaunchRodAngle(math.radians(j*2 + 1))
            for i in range(18):
                opts.setLaunchRodDirection(math.radians(20 * i))

                orh.run_simulation(sim)
                data = orh.get_timeseries(sim, DEFAULT_STATS)
                events = orh.get_events(sim)

                landing = get_landing_point(data, events)

                landings.append(landing)

        print(landings)

        dist = 'Lateral distance'
        dirc = 'Lateral direction'

        xs = list(map(lambda l: l[dist] * math.cos(l[dirc]), landings))
        ys = list(map(lambda l: l[dist] * math.sin(l[dirc]), landings))
        plt.scatter(xs, ys)
        plt.savefig('/app/share/result/plot.png')

        # for landing in landings:


def get_landing_point(data, events):
    landed_at = 0
    while data['Time'][landed_at] < events['Ground hit']:
        landed_at += 1
        if landed_at >= len(data['Time']):
            landed_at -= 1
            break

    landed_point = {}
    for k, v in data.items():
        landed_point[k] = v[landed_at]

    return landed_point

if __name__ == "__main__":
    main()
