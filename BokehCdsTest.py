#from bokeh.models.sources import TableDataSource
from bokeh.io import output_file, show
from bokeh.layouts import gridplot, row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure

#import math
import sys

arg = '1'
if (len(sys.argv) > 1):
  arg = sys.argv[1]
print('arg ' + arg)
#exit()

axA = ['A', 'B', 'C', 'D']
axB = ['a', 'b', 'c', 'd']

colA = ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D']
colB = ['b', 'c', 'a', 'd', 'a', 'c', 'a', 'd', 'b', 'b', 'c', 'd']
#colC = [x/30 for x in [  1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12]]
colD = [abs(x)/10 + 0.1 for x in [  1,   2,   0,   2,  -1,   1,  -2,   1,  -1,  -2,  -1,   0]]

source = ColumnDataSource(data=dict(colA=colA, colB=colB, colD=colD))

axASumD = [0 for x in axA]
for i in range(len(axA)):
  for vi in range(len(colA)):
    if (colA[vi] == axA[i]):
       axASumD[i] += colD[vi]

print('source=\n', source)
print('source=\n', source.to_df())

dt = data=dict(colA=axA, colD=axASumD)
sourceAD = ColumnDataSource(dt)
#sourceT  = TableDataSource(dt)

TOOLS = "box_select,lasso_select,help"

fig = [None, None, None, None, None, None]

fn = 0
fig[fn] = figure(tools=TOOLS, x_range=axA, plot_width=400, plot_height=350, title="colA, colD") 
fig[fn].vbar(x='colA', top='colD', width=0.5, source=source)

fn += 1
fig[fn] = figure(tools=TOOLS, x_range=axA, plot_width=400, plot_height=350, title="colB, colD") 
fig[fn].vbar(x='colB', top='colD', width=.5, source=source)

fn += 1
fig[fn] = figure(tools=TOOLS, x_range=axA, plot_width=400, plot_height=350, title="colA, sumD") 
fig[fn].vbar(x='colA', top='colD', width=.5, source=sourceAD)

fn += 1
fig[fn] = figure(tools=TOOLS, x_range=axB, plot_width=400, plot_height=350, title="colB, colD") 
fig[fn].vbar(x='colB', top='colD', width=.5, source=source)

fn += 1
fig[fn] = figure(tools=TOOLS, x_range=axA, y_range=axB, plot_width=400, plot_height=350, title="colA, colB, colD") 
fig[fn].circle(x='colA', y='colB', radius="colD", source=source)

columns = [
        TableColumn(field="colA", title="Y"),
        TableColumn(field="colD", title="Text"),
    ]

fn += 1
fig[fn] = figure(tools=TOOLS, x_range=axA, plot_width=400, plot_height=350, title="Table")
#fig[fn] = DataTable(source=sourceT[sourceT['colA'] > 5], columns=columns, width=400, height=350)
fig[fn].circle(x='colA', y='colD', radius="colD", source=source)

#p = gridplot([[fig[0], fig[1], fig[2]], [fig[3], fig[4], fig[5]]])
p = Tabs(tabs=[Panel(child=row(fig[0], fig[1], fig[2]), title="Row 1"), 
               Panel(child=row(fig[3], fig[4], fig[5]), title="Row 2")])
show(p)