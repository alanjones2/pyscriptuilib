from uilib import Page, Container, TextInput, Button, Select, Alert

# Set up the page
page = Page(titletext="Demo App", width="narrow")

# Form container
form_container = Container()
page.add(form_container)

# Inputs
name_input = TextInput(caption="Your Name", placeholder="Enter your name")
color_select = Select(
    caption="Favorite Color",
    values=["red", "blue", "green"],
    labels=["Red", "Blue", "Green"]
)
submit_button = Button(caption="Submit")

# Result area
result_container = Container()
page.add(result_container)

# Callback function
def submit_form(component, event):
    name = name_input.get_value().strip()
    color = color_select.get_value()
    
    result_container.clear()
    if name:
        msg = f"**Hello {name}!** Your favorite color is **{color}**."
        alert = Alert(text=msg, category="success", dismissible=True)
        result_container.add(alert)
    else:
        alert = Alert(text="Please enter your name.", category="warning", dismissible=True)
        result_container.add(alert)

# Assign the callback
submit_button = Button(caption="Submit", callback=submit_form)

# Build the UI
form_container.add(name_input)
form_container.add(color_select)
form_container.add(submit_button)
