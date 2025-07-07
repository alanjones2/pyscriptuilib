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

def show_matplotlib_integration():
    """Demonstrates displaying matplotlib figures and handling callbacks."""
    page.add(ui.Banner("Choose a graph", "Select a graph and it will be drawn bigger, below"))

    row1 = ui.Row(layout=3)
    page.add(row1)
    cols = row1.columns

    figcontainer = ui.Container()
    page.add(figcontainer)

    def cb(button, event):
        figcontainer.disp(getBigFig(button.node.value), append=False)

    for i, x in enumerate(cols):
        x.disp(getFig(str(i)))
        x.add(ui.Button("Select fig", callback=cb, value=str(i)))

def show_headers_and_text():
    """Demonstrates various header and text rendering components."""
    page.add(ui.SmallBanner("Headers and Text Content"))
    row = ui.Row(layout=3)
    page.add(row)
    c1, c2, c3 = row.columns

    c1.title("This is a Title")
    c1.header("This is a Header")
    c1.subheader("This is a Subheader")

    c2.headertag("header tag level 4", 4)
    c2.headertag("header tag level 5", 5)
    c2.headertag("header tag level 6", 6)

    c3.write("Write some plain text")
    c3.writeMarkdown("Write text with *markdown text* and <b>HTML text</b>")

def show_interactive_controls():
    """Demonstrates all interactive input components."""
    page.add(ui.SmallBanner("Interactive Controls"))
    row = ui.Row(layout=2)
    page.add(row)
    controls_col, output_col = row.columns
    controls_col.header("Controls")
    output_col.header("Output")
    output_col.node.style.whiteSpace = "pre-wrap"

    def selectcb(select_component, event):
        output_col.disp(f"Select: {select_component.get_value()}", append=False)
    controls_col.add(ui.Select(caption="Select a number", values=[1, 2, 3], labels=["one", "two", "three"], callback=selectcb))

    def checkcb(checkbox, event):
        output_col.disp(f"Checkbox: {checkbox.is_checked()}, Value: {checkbox.input_elem.value}", append=False)
    controls_col.add(ui.Checkbox(value=1, label="Select this for 1", callback=checkcb))
    controls_col.add(ui.Checkbox(value=2, label="Select this for 2", callback=checkcb))

    def radiocb(radio_group, event):
        output_col.disp(f"Radio: {radio_group.get_value()}", append=False)
    controls_col.add(ui.RadioGroup(caption="Choose one letter", values=['A', 'B', 'C'], initial_value='B', callback=radiocb))

    def get_slider_value(slider, event):
        output_col.disp(f"Slider: {slider.get_value()}", append=False)
    controls_col.add(ui.Slider(caption="slider", min_val=0, max_val=100, initial_val=50, step=1, callback=get_slider_value))

    def get_input_value(text_input, event):
        output_col.disp(f"Input: {text_input.get_value()}", append=False)
    controls_col.add(ui.TextInput(caption="Text Input", placeholder="Type here...", callback=get_input_value))

    text_area = ui.TextArea(caption="Multi-line Input", placeholder="Enter a long text...", rows=4)
    controls_col.add(text_area)
    def get_textarea_value(button, event):
        output_col.disp(f"Text Area content:\n{text_area.get_value()}", append=False)
    text_button = ui.Button("Get text area value", callback=get_textarea_value)
    controls_col.add(text_button)

def show_alerts():
    """Demonstrates different types of alerts."""
    page.add(ui.SmallBanner("Alerts"))
    alert_container = ui.Container()
    page.add(alert_container)
    alert_container.add(ui.Alert("This is a standard primary alert."))
    alert_container.add(ui.Alert("This is a <strong>danger</strong> alert!", category="danger"))
    alert_container.add(ui.Alert("This is a dismissible success alert. Click the 'x' to close it.", category="success", dismissible=True))

def show_custom_rows():
    """Demonstrates rows with custom-width columns."""
    page.add(ui.SmallBanner("Custom Width Rows"))
    custom_row = ui.Row(layout=[4, 8])
    page.add(custom_row)
    col_one_third, col_two_thirds = custom_row.columns
    col_one_third.header("One Third")
    col_one_third.write("This column takes up 4 of 12 units.")
    col_two_thirds.header("Two Thirds")
    col_two_thirds.write("This column takes up 8 of 12 units.")
    col_two_thirds.add(ui.Alert("This is an alert in the wider column.", category="info"))

def show_programmatic_access():
    """Demonstrates getting and setting component values programmatically."""
    page.add(ui.SmallBanner("Programmatic Get/Set Values"))
    programmatic_row = ui.Row(layout=2)
    page.add(programmatic_row)
    prog_col1, prog_col2 = programmatic_row.columns
    prog_col1.subheader("Control Panel")
    prog_col2.subheader("Status")

    my_input = ui.TextInput(caption="Enter a new status")
    status_alert = ui.Alert("No status set.", category="warning")
    prog_col1.add(my_input)
    prog_col2.add(status_alert)

    def update_status(button, event):
        status_alert.node.innerHTML = f"<strong>Status:</strong> {my_input.get_value()}"
        status_alert.set_class("alert alert-success")
        my_input.set_value("")
    update_button = ui.Button("Update Status", callback=update_status)
    prog_col1.add(update_button)

# --- Main Application Flow ---
show_matplotlib_integration()
page.writeMarkdown("---")
show_headers_and_text()
page.writeMarkdown("---")
show_interactive_controls()
page.writeMarkdown("---")
show_alerts()
page.writeMarkdown("---")
show_custom_rows()
page.writeMarkdown("---")
show_programmatic_access()
