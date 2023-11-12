import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import json
import time

x_data = []
y_datas = [[],[],[],[],[],[], []]
lines = []
f = open('data/Indoor/Participant_3/AFE_000_CONFIDENTIAL.json')
video_path = 'data/Indoor/Participant_3/Participant_3-Indoor-720p.mp4'  # Replace with your video file
data = json.load(f)
data_index = 0
start_time_data = data[0]['afe'][0]['i'][0]
start_time_video = time.time() * 1000
screen_number = 0

MAX_POINTS = 3000

# Function to update the graphs
def update_graphs(frame, axes):
    global data_index, lines, screen_number
    time_data = data[data_index]['afe'][0]['i'][0]
    time_video = screen_number * 17
    screen_number = screen_number + 1
    # time_video = time.time()
    
    
    while (time_data - start_time_data < time_video):
        print(time_video)
        data_index = data_index + 1
        time_data = data[data_index]['afe'][0]['i'][0]
    
    dists = data[data_index]['afe'][0]['m'][0]
    data_index = data_index + 1
    if len(x_data) > MAX_POINTS:
        x_data.pop(0)
    
    x_data.append((time_data - start_time_data) / 1000)
    for i in range(6):
        if len(y_datas[i]) > MAX_POINTS:
            y_datas[i].pop(0)
        y_datas[i].append(dists[i])
        lines[i].set_xdata(x_data)
        lines[i].set_ydata(y_datas[i])
        
    if len(y_datas[6]) > MAX_POINTS:
            y_datas[6].pop(0)
    
    if ('blinks' in data[data_index] and 'left' in data[data_index]['blinks']):
        print('left blink ' + time_data / 1000)
        y_datas[6].append(1)
    else:
        y_datas[6].append(0)
        
    lines[6].set_ydata(data[data_index]['afe'][0]['i'][0])
    
    axes[0, 0].relim()
    axes[0, 0].autoscale_view()
    axes[0, 1].relim()
    axes[0, 1].autoscale_view()
    axes[0, 2].relim()
    axes[0, 2].autoscale_view()
    axes[1, 0].relim()
    axes[1, 0].autoscale_view()
    axes[1, 1].relim()
    axes[1, 1].autoscale_view()
    axes[1, 2].relim()
    axes[1, 2].autoscale_view()
    axes[2, 0].relim()
    axes[2, 0].autoscale_view()

       
    return lines,

# Function to update the video frame
def update_video(frame, video_ax):
    video_ax.clear()
    video_ax.imshow(frame)
    video_ax.axis("off")

# Set up the video capture

cap = cv2.VideoCapture(video_path)

# Set up initial data for the graphs
x = []
y1, y2, y3, y4, y5, y6, y7 = [], [], [], [], [], [], []

# Create six subplots for graphs
fig, axs = plt.subplots(3, 3, figsize=(12, 8))
fig.suptitle('Real-time Graphs with Video')

# Create a subplot for the video
video_ax = fig.add_subplot(3, 3, 9)
video_ax.set_title('Video')
video_ax.axis("off")

for ax in axs.flat:
    # ax.set_xlim(0, 10)
    ax.set_ylim(0, 50000)
    
axs.flat[6].set_ylim(-1, 2)

# Set initial axis limits for video
# video_ax.set_xlim(0, cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# video_ax.set_ylim(0, cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# Plot initial graphs
line1, = axs[0, 0].plot(x, y1, label='sin(x)')
line2, = axs[0, 1].plot(x, y2, label='cos(x)')
line3, = axs[0, 2].plot(x, y3, label='tan(x)')
line4, = axs[1, 0].plot(x, y4, label='exp(x)')
line5, = axs[1, 1].plot(x, y5, label='log(x+1)')
line6, = axs[1, 2].plot(x, y6, label='x^2')
line7, = axs[2, 0].plot(x, y7, label='x^2')

line7.set_data([1, 2, 3],[1 , 2 ,3 ])

lines = [line1, line2, line3, line4, line5, line6, line7]

# Function to update the plots in each frame
def update(frame):
    # print('call update')
    ret, frame_image = cap.read()
    if not ret:
        ani.event_source.stop()
        cap.release()
        plt.close()
    else:
        update_video(frame_image, video_ax)
        update_graphs(frame_image, axs)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=10, interval=0, blit=False)

plt.show()
