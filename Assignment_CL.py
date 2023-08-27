import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import datetime

data = pd.read_csv('Assignment_Dataset.csv')
budget_start = 73.9
budget_decrease_rate = 0.008
data['Date'] = pd.to_datetime(data['Date'], format='mixed', dayfirst=True)
data['year'] = data['Date'].dt.year

data['30-day MA'] = data['PR'].rolling(window=30).mean()

budgets = []
for i in data['year']:
    start_year = 2019
    year_difference = i - start_year
    current_budget = budget_start - (budget_start * budget_decrease_rate * year_difference)
    budgets.append(current_budget)

def get_color(ghi):
    if ghi < 2:
        return 'navy'
    elif 2 <= ghi < 4:
        return 'lightblue'
    elif 4 <= ghi < 6:
        return 'orange'
    else:
        return 'brown'
data['color'] = data['GHI'].apply(get_color)
d_filtered = data[data['PR']>budgets]
fig, ax = plt.subplots()

size = 10
ax.scatter(data['Date'], data['PR'], c=data['color'], marker='D', s=size)

width = 3.0
ax.plot(data['Date'], data['30-day MA'], color='red', linewidth=width)

ax.plot(data['Date'], budgets, color='darkgreen')

ax.spines['top'].set_visible(False)  # Hide the top spine
ax.spines['right'].set_visible(False)
lower_limit = pd.Timestamp('Jul/2019')
higher_limit = pd.Timestamp('Mar/2022')
ax.set_xlim(lower_limit, higher_limit)
date_format = '%b/%y'
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

ax.set_ylim(0, 100)
ax.set_yticks(np.arange(0, 100+1, 10.0))
ax.set_ylabel('Performance Ratio [%]')

title = "Performance Ratio Evolution\n From 2019-07-01 to 2022-03-24"
ax.set_title(title, fontweight='bold')

legend_elements = [
    plt.Line2D([0], [0], color='w', label='Daily Irradiation [kWh/m2]'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='navy', markersize=5, label='< 2'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='lightblue', markersize=5, label='2 ~ 4'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='orange', markersize=5, label='4 ~ 6'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='brown', markersize=5, label='> 6')
]
legend_1 = ax.legend(handles=legend_elements, loc='upper left', ncol=5, frameon=False)

legend_elements_3 = [
    plt.Line2D([0], [0], color='g', label='Target Budget Yield Performance Ratio [1Y-73.9%,2Y-73.3%,3Y-72.7%]'),
    plt.Line2D([0], [0], color='r', label='30-d moving average of PR'),
    plt.Line2D([0], [0], color='w', label="Points above Target Budget PR = {}/{} = {}%".format(len(d_filtered), len(data), round((len(d_filtered)/len(data))*100, 1))),
]
legend_3 = ax.legend(handles=legend_elements_3, loc='center', frameon=False)

label_colors = ['green', 'red', 'black'] 
for text, color in zip(legend_3.get_texts(), label_colors):
    text.set_color(color)
    text.set_fontweight('bold')

legend_elements_2 = [
    plt.Line2D([0], [0], color='w', label="Average PR last 7-d: {} %".format(round(data['PR'].tail(7).mean(), 1))),
    plt.Line2D([0], [0], color='w', label="Average PR last 30-d: {} %".format(round(data['PR'].tail(30).mean(), 1))),
    plt.Line2D([0], [0], color='w', label="Average PR last 60-d: {} %".format(round(data['PR'].tail(60).mean(), 1))),
    plt.Line2D([0], [0], color='w', label="Average PR last 90-d: {} %".format(round(data['PR'].tail(90).mean(), 1))),
    plt.Line2D([0], [0], color='w', label="Average PR last 365-d: {} %".format(round(data['PR'].tail(365).mean(), 1))),
    plt.Line2D([0], [0], color='w', label="Average PR Lifetime: {} %".format(round(data['PR'].mean(), 1))),
]
legend_2 = ax.legend(handles=legend_elements_2, loc='lower right', frameon=False)
legend_2.get_texts()[5].set_fontweight('bold')

ax.add_artist(legend_1)
ax.add_artist(legend_2)
ax.add_artist(legend_3)

plt.grid(True, color='lightgray')
plt.show()