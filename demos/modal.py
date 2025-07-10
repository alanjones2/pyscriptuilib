from uilib import Page, Button, Modal

# Create page
page = Page("Modal Example")

# Create modal
my_modal = Modal(title="My Modal", body="This is the **modal body**.", footer="*This is the footer*")
my_modal.add_to(page.node)

# Button to trigger modal
def show_modal(component, event):
    my_modal.show()

btn = Button("Open Modal", callback=show_modal)
btn.add_to(page.node)
