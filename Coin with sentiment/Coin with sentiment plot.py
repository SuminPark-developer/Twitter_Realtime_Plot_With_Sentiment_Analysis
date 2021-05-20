import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
# %matplotlib notebook #주피터에서 실행시

plt.style.use('fivethirtyeight')

frame_len = 10000

fig = plt.figure(figsize=(9, 6))


def animate(i):
    data = pd.read_csv('Coin Sentiment.csv')
    y1 = data['Bitcoin']
    y2 = data['Ethereum']

    if len(y1) <= frame_len:
        plt.cla()
        plt.plot(y1, label='Bitcoin')
        plt.plot(y2, label='Ethereum')
    else:
        plt.cla()
        plt.plot(y1[-frame_len:], label='Bitcoin')
        plt.plot(y2[-frame_len:], label='Ethereum')

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1)
# 파이참에서 실행시 plt.show() 필요. http://blog.naver.com/PostView.nhn?blogId=mathesis_time&logNo=221988281625&categoryNo=0&parentCategoryNo=25&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView
plt.show()
