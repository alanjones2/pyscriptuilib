import uilib as ui

# The following code suppresses warnings from matplotlib.
# they are an unnecessary distraction for the user and anyway can be seen in the browser console 
import sys
import io

# Suppress the Matplotlib font cache build message by temporarily redirecting both stdout and stderr
_original_stdout = sys.stdout
_original_stderr = sys.stderr
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
try:
    import matplotlib.pyplot as plt
finally:
    # Restore stdout and stderr to their original states
    sys.stdout = _original_stdout
    sys.stderr = _original_stderr
# end of warning suppression code


# Make three figures

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



page.add(ui.Banner("Choose a graph","Select a graph and it will be drawn bigger, below"))


# Create a row with 3 columns directly inside the page container
row1 = ui.Row(layout=3)
page.add(row1)
cols = row1.columns

# button callback - the value of the button is the index of the fig
def cb(button, event):
    figcontainer.disp(getBigFig(button.node.value), append=False)

# This container will hold the large version of the selected figure
figcontainer = ui.Container()
page.add(figcontainer)

for i, x in enumerate(cols):
    x.disp(getFig(str(i)))
    x.add(ui.Button("Select fig", callback=cb, value=str(i)))

# A new container with content types

page.writeHTML("---")


# This row demonstrates having columns with just headers
row2 = ui.Row(layout=2)
page.add(row2)
my_new_cols = row2.columns
my_new_col_1 = my_new_cols[0]
my_new_col_2 = my_new_cols[1]
my_new_col_1.header("Left column")
my_new_col_2.header("Right column")

# This row demonstrates different header and text types
row3 = ui.Row(layout=3)
page.add(row3)
cols1 = row3.columns
c1 = cols1[0]
c2 = cols1[1]
c3 = cols1[2]


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

# This row demonstrates interactive controls in one column and their output in another.
row4 = ui.Row(layout=2)
page.add(row4)
con1col1, con1col2 = row4.columns
con1col1.header("Controls")
con1col2.header("Output")

def selectcb(select_component, event):
    con1col2.disp(f"Select: {select_component.select_elem.value}", append=False)
con1col1.add(ui.Select(caption="Select a number", values=[1,2,3], labels=["one","two","three"], callback=selectcb))

def checkcb(checkbox, event):
    con1col2.disp(f"Checkbox: {checkbox.input_elem.checked}, Value: {checkbox.input_elem.value}", append=False)
con1col1.add(ui.Checkbox(value=1, label="Select this for 1", callback=checkcb))
con1col1.add(ui.Checkbox(value=2, label="Select this for 2", callback=checkcb))

def radiocb(radio_group, event):
    con1col2.disp(f"Radio: {event.target.value}", append=False)
con1col1.add(ui.RadioGroup(caption="Choose one letter", values=['A', 'B', 'C'], initial_value='B', callback=radiocb))


def get_slider_value(slider, event):
    con1col2.disp(f"Slider: {slider.slider_elem.value}", append=False)
con1col1.add(ui.Slider(caption="slider", min_val=0, max_val=100, initial_val=50, step=1, callback=get_slider_value))

def get_input_value(text_input, event):
    # This will now update in real-time on every keystroke
    con1col2.disp(f"Input: {text_input.input_elem.value}", append=False)

con1col2.add(ui.TextInput(caption="Text Input", placeholder="Type here...", callback=get_input_value))

# Set the style on the output container once to handle newlines correctly
con1col2.node.style.whiteSpace = "pre-wrap"
def get_textarea_value(text_area, event):
    # This will now update in real-time on every keystroke
    con1col2.disp(f"Text Area content:\n{text_area.textarea_elem.value}", append=False)
con1col2.add(ui.TextArea(caption="Multi-line Input", placeholder="Enter a long text...", rows=4, callback=get_textarea_value))

page.writeHTML("---")
page.add(ui.SmallBanner("Alerts"))

alert_container = ui.Container()
page.add(alert_container)
alert_container.add(ui.Alert("This is a standard primary alert."))
alert_container.add(ui.Alert("This is a <strong>danger</strong> alert!", category="danger"))
alert_container.add(ui.Alert("This is a dismissible success alert. Click the 'x' to close it.", category="success", dismissible=True))

page.writeHTML("---")
page.add(ui.SmallBanner("Custom Width Rows"))

# This demonstrates a custom row with a 1/3 and 2/3 split (4 + 8 = 12)
custom_row = ui.Row(layout=[4, 8])
page.add(custom_row)

col_one_third, col_two_thirds = custom_row.columns

col_one_third.header("One Third")
col_one_third.write("This column takes up 4 of 12 units.")

col_two_thirds.header("Two Thirds")
col_two_thirds.write("This column takes up 8 of 12 units.")
col_two_thirds.add(ui.Alert("This is an alert in the wider column.", category="info"))
