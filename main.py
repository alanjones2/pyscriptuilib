#from uilib import *
import uilib as ui

# Make three figures
import matplotlib.pyplot as plt

fruits = ['apple', 'blueberry', 'cherry', 'orange']
counts = [40, 100, 30, 55]

def getFig(i,width=3, height=3):
    fig, ax = plt.subplots(figsize=(width, height))
    match i:
        case '0':    ax.bar(fruits, counts)
        case '1':    ax.plot(fruits, counts)
        case '2':    ax.scatter(fruits, counts)
    return fig

def getBigFig(i):
    return getFig(i,width=10, height=4)
#######################################

# Create page - you have to create a page
page = ui.Page(titletext="Kitchen sink")

# banner is a convenience function
page.banner("Choose a graph","Select a graph and it will be drawn bigger, below")

# makeCols returns a list of col containers inside a row container
cols = page.makeCols(3)

# button callback - the value of the button is the index of the fig
def cb(event):
    figcontainer.disp(getBigFig(event.target.value), append=False)

figcontainer = ui.Container()

for i, x in enumerate(cols):
    x.disp(getFig(str(i)))
    x.button("Select fig", callback = "cb", value=str(i))

# A new container with content types

page.writeHTML("---")

page.smallbanner("Content types")

c1, c2, c3 = page.makeCols(3)

c1.title("This is a Title")
c1.header("This is a Header")
c1.subheader("This is a Subheader")

c2.headertag("header tag level 1",1)
c2.headertag("header tag level 2",2)
c2.headertag("header tag level 3",3)
c2.headertag("header tag level 4",4)
c2.headertag("header tag level 5",5)
c2.headertag("header tag level 6",6)

c3.write("Write some plain text")
c3.writeHTML("Write text with *markdown text* and <b>HTML text</b>")

con1 = ui.Container()
con1col1, con1col2 = con1.makeCols(2)
con2 = ui.Container()

def selectcb(event):
    con2.disp(event.target.value)
con1col1.select(values=[1,2,3], labels=["one","two","three"], callback="selectcb")

def checkcb(event):
    con2.disp(f"{event.target.checked} {event.target.value}")
con1col1.check(value=1, label="Select this for 1", callback="checkcb")
con1col1.check(value=2, label="Select this for 2", callback="checkcb")


def get_slider_value(event):
    con2.disp(f"{event.target.value}")
con1col2.slider(caption="slider", min_val=0, max_val=100, initial_val=50, step=1, callback="get_slider_value")

def get_input_value(event):
    con2.disp(f"{event.target.value}")

con1col2.text_input(caption="text input", initial_value="", placeholder="", callback="get_input_value")
