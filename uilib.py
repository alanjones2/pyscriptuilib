# Towards a UI library for PyScript

"""NOTES to self: Containers, controls and content
the main page is a special container that attaches itself to the <body> tag
thus can inherit from the generic container
other containers like columns will be child containers too

Content like strings, headings or graphs can inherit from a generic content class 
Strings should probably implement markdown by default, and thus html, too

Let's automatically set the id and forget passing it. Create an id object that increments and id string
"""


from pyscript import document
from pyscript import display
import markdown as md

PAGEID = "pui-id-page"

# Component Base Class (New)
class Component:
    """A base class for all UI components."""
    def __init__(self, tag="div"):
        self.id = f"pui-id-{id(self)}" # Use the object's unique memory id
        self.node = document.createElement(tag)
        self.node.setAttribute("id", self.id)

    def add_to(self, parent_node):
        """Appends the component's node to a parent DOM node."""
        parent_node.append(self.node)

    def set_class(self, class_string):
        """Sets the CSS class attribute for the component's node."""
        self.node.setAttribute("class", class_string)

# UI Component Classes (New)
class Button(Component):
    """An object-oriented Button component."""
    def __init__(self, caption="Button", callback=None, value="pressed", btnClass="btn btn-primary"):
        super().__init__(tag="button")
        if callback:
            self.node.setAttribute("py-click", callback)
        self.set_class(btnClass)
        self.node.setAttribute("type", "button")
        self.node.setAttribute("value", value)
        self.node.append(document.createTextNode(caption))

class Select(Component):
    """An object-oriented Select (dropdown) component."""
    def __init__(self, caption="", callback=None, values=[], labels=[]):
        # The component's main node is a div wrapper for layout flexibility.
        super().__init__(tag="div")
        self.set_class("mb-3") # Good default styling for Bootstrap

        select_id = f"{self.id}-select" # Derive sub-element ID from component ID
        if not labels:
            labels = values

        if caption:
            label_elem = document.createElement("label")
            label_elem.setAttribute("for", select_id)
            label_elem.setAttribute("class", "form-label")
            label_elem.append(document.createTextNode(caption))
            self.node.append(label_elem)

        select_elem = document.createElement("select")
        if callback:
            select_elem.setAttribute("py-change", callback)
        select_elem.setAttribute("class", "form-select")
        select_elem.setAttribute("id", select_id)

        for l, v in zip(labels, values):
            option_elem = document.createElement("option")
            option_elem.setAttribute("value", str(v))
            option_elem.append(document.createTextNode(str(l)))
            select_elem.append(option_elem)

        self.node.append(select_elem)

class TextInput(Component):
    """An object-oriented Text Input component."""
    def __init__(self, caption="", initial_value="", placeholder="", callback=None):
        super().__init__(tag="div")
        self.set_class("mb-3") # Bootstrap margin-bottom

        input_id = f"{self.id}-input"

        if caption:
            label_elem = document.createElement("label")
            label_elem.setAttribute("for", input_id)
            label_elem.setAttribute("class", "form-label")
            label_elem.append(document.createTextNode(caption))
            self.node.append(label_elem)

        input_elem = document.createElement("input")
        input_elem.setAttribute("type", "text")
        input_elem.setAttribute("class", "form-control")
        input_elem.setAttribute("id", input_id)
        input_elem.setAttribute("value", initial_value)
        if placeholder: input_elem.setAttribute("placeholder", placeholder)
        if callback: input_elem.setAttribute("py-input", callback)
        self.node.append(input_elem)

class TextArea(Component):
    """An object-oriented TextArea component for multi-line text input."""
    def __init__(self, caption="", initial_value="", placeholder="", rows=3, callback=None):
        # Use a div wrapper for the label and textarea
        super().__init__(tag="div")
        self.set_class("mb-3") # Bootstrap margin-bottom

        textarea_id = f"{self.id}-textarea"

        if caption:
            label_elem = document.createElement("label")
            label_elem.setAttribute("for", textarea_id)
            label_elem.setAttribute("class", "form-label")
            label_elem.append(document.createTextNode(caption))
            self.node.append(label_elem)

        textarea_elem = document.createElement("textarea")
        textarea_elem.setAttribute("class", "form-control")
        textarea_elem.setAttribute("id", textarea_id)
        textarea_elem.setAttribute("rows", str(rows))
        if placeholder:
            textarea_elem.setAttribute("placeholder", placeholder)
        if callback:
            textarea_elem.setAttribute("py-input", callback)
        textarea_elem.append(document.createTextNode(initial_value))
        self.node.append(textarea_elem)

class Checkbox(Component):
    """An object-oriented Checkbox component."""
    def __init__(self, label="", callback=None, value=None):
        # The main node is a div wrapper for Bootstrap styling.
        super().__init__(tag="div")
        self.set_class("form-check")

        checkbox_id = f"{self.id}-checkbox"

        input_elem = document.createElement("input")
        input_elem.setAttribute("class", "form-check-input")
        input_elem.setAttribute("type", "checkbox")
        if value is not None:
            input_elem.setAttribute("value", str(value))
        input_elem.setAttribute("id", checkbox_id)
        if callback:
            input_elem.setAttribute("py-change", callback)

        label_elem = document.createElement("label")
        label_elem.setAttribute("class", "form-check-label")
        label_elem.setAttribute("for", checkbox_id)
        label_elem.append(document.createTextNode(label))

        self.node.append(input_elem)
        self.node.append(label_elem)

class Slider(Component):
    """An object-oriented Slider (range input) component."""
    def __init__(self, caption="", min_val=0, max_val=100, initial_val=None, step=1, callback=None):
        super().__init__(tag="div")
        self.set_class("mb-3")

        slider_id = f"{self.id}-slider"

        if caption:
            label_elem = document.createElement("label")
            label_elem.setAttribute("for", slider_id)
            label_elem.setAttribute("class", "form-label")
            label_elem.append(document.createTextNode(caption))
            self.node.append(label_elem)

        slider_elem = document.createElement("input")
        slider_elem.setAttribute("type", "range")
        slider_elem.setAttribute("class", "form-range")
        slider_elem.setAttribute("id", slider_id)
        slider_elem.setAttribute("min", str(min_val))
        slider_elem.setAttribute("max", str(max_val))
        slider_elem.setAttribute("step", str(step))
        slider_elem.setAttribute("value", str(initial_val if initial_val is not None else min_val))
        if callback: slider_elem.setAttribute("py-change", callback)
        self.node.append(slider_elem)

class RadioGroup(Component):
    """An object-oriented Radio Button Group component."""
    def __init__(self, caption="", callback=None, values=[], labels=[], initial_value=None):
        # The main node is a fieldset for semantic grouping of radio buttons.
        super().__init__(tag="fieldset")
        self.set_class("mb-3")

        # The 'name' attribute must be shared by all radio buttons in the group.
        group_name = f"{self.id}-radiogroup"

        if caption:
            legend_elem = document.createElement("legend")
            legend_elem.setAttribute("class", "col-form-label pt-0")
            legend_elem.append(document.createTextNode(caption))
            self.node.append(legend_elem)

        if not labels:
            labels = values

        for l, v in zip(labels, values):
            wrapper_div = document.createElement("div")
            wrapper_div.setAttribute("class", "form-check")

            radio_id = f"{self.id}-radio-{v}"
            input_elem = document.createElement("input")
            input_elem.setAttribute("class", "form-check-input")
            input_elem.setAttribute("type", "radio")
            input_elem.setAttribute("name", group_name)
            input_elem.setAttribute("id", radio_id)
            input_elem.setAttribute("value", str(v))
            if str(v) == str(initial_value):
                input_elem.setAttribute("checked", True)
            if callback:
                input_elem.setAttribute("py-change", callback)

            label_elem = document.createElement("label")
            label_elem.setAttribute("class", "form-check-label")
            label_elem.setAttribute("for", radio_id)
            label_elem.append(document.createTextNode(str(l)))

            wrapper_div.append(input_elem)
            wrapper_div.append(label_elem)
            self.node.append(wrapper_div)

class Alert(Component):
    """An object-oriented Alert component for displaying contextual messages."""
    def __init__(self, text="", category="primary", dismissible=False):
        # The main node is a div with alert roles.
        super().__init__(tag="div")

        class_list = f"alert alert-{category}"
        if dismissible:
            class_list += " alert-dismissible fade show"

        self.set_class(class_list)
        self.node.setAttribute("role", "alert")

        # Use a temporary node to parse potential markdown/html in the text
        content_node = document.createElement("span")
        content_node.innerHTML = md.markdown(text)
        for child in list(content_node.childNodes):
            self.node.append(child)

        if dismissible:
            button = document.createElement("button")
            button.setAttribute("type", "button")
            button.setAttribute("class", "btn-close")
            button.setAttribute("data-bs-dismiss", "alert")
            button.setAttribute("aria-label", "Close")
            self.node.append(button)

class Banner(Component):
    """An object-oriented Banner component."""
    def __init__(self, title="", subtitle=""):
        super().__init__(tag="div")
        self.set_class("bg-primary text-center text-white p-2 my-2")

        title_elem = document.createElement("div")
        title_elem.setAttribute("class", "display-3")
        title_elem.append(document.createTextNode(title))
        self.node.append(title_elem)

        if subtitle:
            subtitle_elem = document.createElement("div")
            subtitle_elem.setAttribute("class", "lead")
            subtitle_elem.append(document.createTextNode(subtitle))
            self.node.append(subtitle_elem)

class SmallBanner(Component):
    """An object-oriented SmallBanner component."""
    def __init__(self, text=""):
        super().__init__(tag="div")
        self.set_class("bg-primary text-center text-white p-2 my-1")

        title_elem = document.createElement("div")
        title_elem.setAttribute("class", "display-4")
        title_elem.append(document.createTextNode(text))
        self.node.append(title_elem)



# Containers

class Container:
    def __init__(self, parent=PAGEID, class_name=None):
        """
        Initializes a generic container (a <div> element).

        Args:
            parent (str, optional): The ID of the parent element to append this container to.
                                    Defaults to the main page container.
            class_name (str, optional): The CSS class(es) to apply to the container. Defaults to None.
        """
        self.id = f"pui-id-{id(self)}"
        self.node = document.createElement("div")
        self.node.setAttribute("id", self.id)
        self.class_name = class_name
        if self.class_name:
            self.node.setAttribute("class", self.class_name)

        parentNode = document.getElementById(parent)
        parentNode.append(self.node)


    def add(self, component):
        """Adds a component object to this container."""
        component.add_to(self.node)
        return self # Return self to allow for method chaining
    
    # Content functions 

    def disp(self, content, append=True):
        display(content, target=self.id, append=append)
    def write(self, text, append = True):
        self.disp(text, append)
    def writeHTML(self, text, append = True):
        if append:
            # To avoid destroying existing elements (like plots or elements with listeners),
            # we create a temporary container, add the new HTML to it, and then
            # append its children to the actual node. This is non-destructive.
            temp_container = document.createElement("div")
            temp_container.innerHTML = md.markdown(text)
            # Use list() to create a static copy of childNodes, as it's a live NodeList
            for child in list(temp_container.childNodes):
                self.node.append(child)
        else:
            # This is destructive, which is the intended behavior for append=False
            self.node.innerHTML = md.markdown(text)
    def headertag(self,text,level):
        self.writeHTML(f"<h{level}>{text}</h{level}>")
    def title(self, text): self.headertag(text,1)
    def header(self, text): self.headertag(text,2)
    def subheader(self, text): self.headertag(text,3)

                                            
class Row(Container):
    """
    A specialized container that represents a Bootstrap row.
    It automatically creates a specified number of column containers within it.
    """
    def __init__(self, parent=PAGEID, num_cols=1):
        # A Row is a container with the "row" class.
        super().__init__(parent=parent, class_name="row")
        self.columns = []
        for _ in range(num_cols):
            # A Column is a simple container with the "col" class, and its parent is this row.
            col = Container(parent=self.id, class_name="col")
            self.columns.append(col)

class Page(Container):
    def __init__(self, titletext="", width="narrow"):
        # Page is a singleton container. Check if it already exists.
        page_node = document.getElementById(PAGEID)

        if page_node:
            # If it exists, just adopt the existing node.
            self.node = page_node
            self.id = PAGEID
        else:
            # If it doesn't exist, we can't use super().__init__() because
            # it appends to a parent. Page appends to the body.
            # We manually do the setup.
            self.id = PAGEID
            self.node = document.createElement("div")
            self.node.setAttribute("id", self.id)
            if width == "narrow":
                self.node.setAttribute("class", "container")
            # Append to the body, which is the special behavior of Page.
            bodyNode = document.getElementsByTagName("body")[0]
            bodyNode.append(self.node)

        # Set the document title. This is safe to run multiple times.
        headNode = document.getElementsByTagName("head")[0]
        titletag = headNode.querySelector("title")
        if not titletag:
            titletag = document.createElement("title")
            headNode.append(titletag)
        titletag.innerHTML = titletext