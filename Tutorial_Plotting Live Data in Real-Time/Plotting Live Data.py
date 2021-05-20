import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

frame_len = 10000

fig = plt.figure(figsize=(9, 6))

def animate(i):
    data = pd.read_csv('tweet data.csv')

    # data['Create_Time'] = pd.to_datetime(data['Create_Time']) # https://enjoyiot.tistory.com/entry/2-Time-Resampling
    # print(data.head())
    # print(data.info()) # 확인해보면, Create_Time의 data type이 datetime64로 변경됨.
    print(data)

    x = data['Create_Time']
    y1 = data['Bitcoin_Original']
    y2 = data['Bitcoin_RT']
    y3 = data['Total_Tweet']

    plt.cla()
    # 선 그래프
    plt.plot(x, y1, label='Bitcoin_Original')
    plt.plot(x, y2, label='Bitcoin_RT')
    plt.plot(x, y3, label='Total_Tweet')

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)  # gcf는 Get Current Figure

plt.tight_layout()
plt.xlabel("Time")
plt.ylabel("count")
plt.show()
