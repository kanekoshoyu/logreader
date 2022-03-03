import csv
import math
import plotly
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from datetime import datetime


file = open('btcusd.csv')
csvreader = csv.reader(file)
# CSV Read
header = []
days = []
header = next(csvreader)
for day in csvreader:
    days.append(day)
print(days[0])
# XY
x = []
y = []
regx = []
regy = []
print(len(days))
for i in range(len(days)):
  regx.append(i+1)

for day in days:
    date_str = day[0]
    date_time_obj = datetime.strptime(date_str, '%Y-%m-%d')
    lin = float(day[4])
    y.append(lin)
    x.append(date_time_obj)

multiple, offset = np.polyfit(np.log(regx), y, 1)
print("Multiple: %f Offset: %f ", multiple, offset)
for idx, each in enumerate(regx):
  val  = offset+ multiple * each
  # print(val/math.log(math.e))
  regy.append(val/math.log(math.e))

# df = px.data.gapminder().query("year == 2007")
# fig = px.scatter(df, x="gdpPercap", y="lifeExp", hover_name="country", log_x=True)
fig = px.line(x=x, y=y)
fig.update_yaxes(type="log")

# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)


fig.show()

# trace0 = go.Scatter(
#     x=x,
#     y=y
# )
# trace1 = go.Scatter(
#     x=x,
#     y=regy
# )
# data = go.Data([trace0, trace1])
# plotly.offline.iplot(data, filename = 'basic-line')
