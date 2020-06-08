import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,FFMpegWriter
import mpl_toolkits.mplot3d.axes3d as p3

import matplotlib as mpl 

mpl.rcParams['animation.ffmpeg_path'] = r'C:\\python\\ffmpeg\\bin\\ffmpeg.exe'

import pandas as pd 
import numpy as np


def animate(i):
    row = data.iloc[i]
    ax.clear()

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, 0])
    ax.set_zlim([0, z_max])

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    titolo = 'Misura del {0} angolo con il sole {1:.2f}°'.format(row['data'],row['angolo_sole'])
    fig.suptitle(titolo, fontsize=12, x=0.5, y=1)

    colors = '#00008B'
    if row['al_sole']:
        colors = '#FF8C00'

    ax.quiver(0, 0, 0, row['mag_x'], row['mag_y'], row['mag_z'],color=colors, arrow_length_ratio = 0.1)

data = pd.read_csv('test.csv')
data = data[20:]
data['data'] = pd.to_datetime(data.data, format="%Y-%m-%d %H:%M:%S")
data.set_index('misura')

fig = plt.figure()
ax = p3.Axes3D(fig)

x_min = data['mag_x'].min()
x_max = data['mag_x'].max()

y_min = data['mag_y'].min()
z_max = data['mag_z'].max()


ani = FuncAnimation(fig, animate, frames=len(data.index),interval=10, repeat=False)
writervideo = FFMpegWriter(fps=60) 

f = r"C://python/astropy_magneto/data/animation.mp4" 

ani.save(f, writer=writervideo)
#plt.show()