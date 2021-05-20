from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# %matplotlib notebook #주피터에서 실행시

plt.style.use('fivethirtyeight')

frame_len = 10000

fig = plt.figure(figsize=(9, 6))


def animate(i):
    data = pd.read_csv('Total Tweets Modify.csv')
    print(data['Time'])

    data.set_index('Time', inplace=False)
    # x = data['Time']
    y1 = data['Bitcoin_Original']
    y2 = data['Bitcoin_RT']
    y3 = data['Total_Tweet']

    if len(y1) <= frame_len:
        plt.cla()
        # plt.plot(x, label='Time')
        plt.plot(y1, label='Bitcoin_Original')
        plt.plot(y2, label='Bitcoin_RT')
        plt.plot(y3, label='Total_Tweet')
    else:
        plt.cla()
        # plt.plot(x[-frame_len:], label='Time')
        plt.plot(y1[-frame_len:], label='Bitcoin_Original')
        plt.plot(y2[-frame_len:], label='Bitcoin_RT')
        plt.plot(y3[-frame_len:], label='Total_Tweet')

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1)
# 파이참에서 실행시 plt.show() 필요. http://blog.naver.com/PostView.nhn?blogId=mathesis_time&logNo=221988281625&categoryNo=0&parentCategoryNo=25&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView
plt.xlabel("Time")
plt.ylabel("count")
plt.show()
