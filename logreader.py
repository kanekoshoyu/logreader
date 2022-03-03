import csv
import math
from bokeh.io import curdoc
from bokeh.models import CustomJS, Slider, ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.layouts import row, widgetbox

file = open('BTC-USD.csv')
csvreader = csv.reader(file)
# CSV Read
header = []
days = []
header = next(csvreader)
for day in csvreader:
    days.append(day)

# XY
x = list(range(0, len(days)))
y = []
ylog = []
for day in days:
    lin = float(day[4])
    y.append(lin)
    ylog.append(lin)

# Plots
print('preparing plotdata')
p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')
p.line(x, y, legend_label="Y", color="blue", line_width=2)
p.line(x, ylog, legend_label="YLog", color='red', line_width=2)

# Slider
source = ColumnDataSource(data=dict(x=x, y=y))
result = ColumnDataSource(data=dict(x=x, y=ylog))
slider_logbase = Slider(title="Log Base", value=1,
                        start=0.0, end=10.0, step=0.1)

# Slider
print('preparing slider')
slider_logbase.callback = CustomJS(
    args=dict(source=source, result=result), code="""
    var base = logbase.value;
    var sourcedata = source.data;
    var resultdata = result.data;
    for (let i = 0; i < x.length; i++) {
        var ys = sourcedata['y']
        var yr = resultdata['y']
        yr[i] = ys/Math.log(base);
    }
    resultdata.change.emit();
""")

layout = row(p,slider_logbase, width=800)
curdoc().add_root(layout)
curdoc().title = "Sliders"

show(layout)
# for i in range(len(days)-1):
#   print(x[i], y[i])

file.close()
