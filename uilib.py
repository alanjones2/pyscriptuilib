# uilib.py - A Pythonic UI library for PyScript
#
# This library provides a set of classes to build user interfaces
# in a more structured and object-oriented way than direct DOM manipulation.
# It is designed to work with Bootstrap 5 for styling.
#
# ---
#
# MIT License
#
# Copyright (c) 2025 Alan Jones
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT- LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



from pyscript import document
from pyscript import display
from typing import Any, Callable, List, Optional
import markdown as md

# The static ID for the main page container, used as the default parent for other containers.
PAGEID = "pui-id-page"

# Component Base Class (New)
class Component:
    """A base class for all UI components, providing common functionality."""
    def __init__(self, tag: str = "div"):
        self.id = f"pui-id-{id(self)}" # Use the object's unique memory id
        self.node = document.createElement(tag)
        self.node.setAttribute("id", self.id)

    def add_to(self, parent_node: Any) -> None:
        """Appends the component's node to a parent DOM node."""
        parent_node.append(self.node)

    def set_class(self, class_string: str) -> None:
        """Sets the CSS class attribute for the component's node."""
        self.node.setAttribute("class", class_string)

# UI Component Classes (New)
class Button(Component):
    """Creates an interactive button element."""
    def __init__(self, caption: str = "Button", callback: Optional[Callable] = None, value: str = "pressed", btnClass: str = "btn btn-primary"):
        """
        Args:
            caption (str, optional): The text displayed on the button. Defaults to "Button".
            callback (Callable, optional): The Python function to call when the button is clicked. Defaults to None.
            value (str, optional): The value attribute of the button. Defaults to "pressed".
            btnClass (str, optional): The CSS class(es) for styling. Defaults to "btn btn-primary".
        """
        super().__init__(tag="button")
        if callback:
            self.node.setAttribute("py-click", callback)
        self.set_class(btnClass)
        self.node.setAttribute("type", "button")
        self.node.setAttribute("value", value)
        self.node.append(document.createTextNode(caption))

class Select(Component):
    """Creates a dropdown selection menu."""
    def __init__(self, caption: str = "", callback: Optional[Callable] = None, values: List[Any] = [], labels: List[str] = []):
        """
        Args:
            caption (str, optional): A label displayed above the select menu. Defaults to "".
            callback (Callable, optional): The Python function to call when the selection changes. Defaults to None.
            values (List[Any], optional): The list of values for the options. Defaults to [].
            labels (List[str], optional): The list of display labels for the options. If empty, `values` will be used. Defaults to [].
        """
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
    """Creates a single-line text input field."""
    def __init__(self, caption: str = "", initial_value: str = "", placeholder: str = "", callback: Optional[Callable] = None):
        """
        Args:
            caption (str, optional): A label displayed above the input field. Defaults to "".
            initial_value (str, optional): The starting value in the input field. Defaults to "".
            placeholder (str, optional): Placeholder text to display when the field is empty. Defaults to "".
            callback (Callable, optional): The Python function to call on each keystroke (`input` event). Defaults to None.
        """
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
    """Creates a multi-line text input area."""
    def __init__(self, caption: str = "", initial_value: str = "", placeholder: str = "", rows: int = 3, callback: Optional[Callable] = None):
        """
        Args:
            caption (str, optional): A label displayed above the text area. Defaults to "".
            initial_value (str, optional): The starting text in the area. Defaults to "".
            placeholder (str, optional): Placeholder text to display when the area is empty. Defaults to "".
            rows (int, optional): The visible number of lines in the text area. Defaults to 3.
            callback (Callable, optional): The Python function to call on each keystroke (`input` event). Defaults to None.
        """
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
    """Creates a checkbox input with a label."""
    def __init__(self, label: str = "", callback: Optional[Callable] = None, value: Optional[Any] = None):
        """
        Args:
            label (str, optional): The text label displayed next to the checkbox. Defaults to "".
            callback (Callable, optional): The Python function to call when the checkbox state changes. Defaults to None.
            value (Any, optional): The value associated with the checkbox, accessible in the event. Defaults to None.
        """
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
    """Creates a slider (range input) control."""
    def __init__(self, caption: str = "", min_val: int = 0, max_val: int = 100, initial_val: Optional[int] = None, step: int = 1, callback: Optional[Callable] = None):
        """
        Args:
            caption (str, optional): A label displayed above the slider. Defaults to "".
            min_val (int, optional): The minimum value of the slider. Defaults to 0.
            max_val (int, optional): The maximum value of the slider. Defaults to 100.
            initial_val (Optional[int], optional): The starting value of the slider. Defaults to `min_val`.
            step (int, optional): The increment step of the slider. Defaults to 1.
            callback (Callable, optional): The Python function to call when the slider value changes. Defaults to None.
        """
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
    """Creates a group of radio buttons where only one can be selected."""
    def __init__(self, caption: str = "", callback: Optional[Callable] = None, values: List[Any] = [], labels: List[str] = [], initial_value: Optional[Any] = None):
        """
        Args:
            caption (str, optional): A label for the entire radio group. Defaults to "".
            callback (Callable, optional): The Python function to call when the selection changes. Defaults to None.
            values (List[Any], optional): The list of values for the radio options. Defaults to [].
            labels (List[str], optional): The list of display labels for the options. If empty, `values` will be used. Defaults to [].
            initial_value (Optional[Any], optional): The value of the radio button to be selected initially. Defaults to None.
        """
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
    """Creates a contextual feedback message box."""
    def __init__(self, text: str = "", category: str = "primary", dismissible: bool = False):
        """
        Args:
            text (str, optional): The message to display in the alert. Can contain markdown/HTML. Defaults to "".
            category (str, optional): The alert category, controlling the color (e.g., 'primary', 'success', 'danger'). Defaults to "primary".
            dismissible (bool, optional): If True, adds a close button to the alert. Defaults to False.
        """
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
    """Creates a large, prominent banner with a title and subtitle."""
    def __init__(self, title: str = "", subtitle: str = ""):
        """
        Args:
            title (str, optional): The main text of the banner. Defaults to "".
            subtitle (str, optional): The smaller text below the main title. Defaults to "".
        """
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
    """Creates a smaller, more compact banner."""
    def __init__(self, text: str = ""):
        """
        Args:
            text (str, optional): The text to display in the banner. Defaults to "".
        """
        super().__init__(tag="div")
        self.set_class("bg-primary text-center text-white p-2 my-1")

        title_elem = document.createElement("div")
        title_elem.setAttribute("class", "display-4")
        title_elem.append(document.createTextNode(text))
        self.node.append(title_elem)



# Containers

class Container:
    """A generic container component that acts as a <div> element."""
    def __init__(self, parent: str = PAGEID, class_name: Optional[str] = None):
        """
        Initializes a generic container (a <div> element).

        Args:
            parent (str, optional): The ID of the parent element to append this container to. Defaults to the main page container.
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


    def add(self, component: 'Component') -> 'Container':
        """Adds a component object to this container and returns self for chaining."""
        component.add_to(self.node)
        return self # Return self to allow for method chaining
    
    # Content functions 

    def disp(self, content: Any, append: bool = True) -> None:
        """Displays content within this container using pyscript.display."""
        display(content, target=self.id, append=append)
    def write(self, text: str, append: bool = True) -> None:
        """Writes plain text to this container."""
        self.disp(text, append)
    def writeHTML(self, text: str, append: bool = True) -> None:
        """Writes a string of markdown/HTML to this container."""
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
    def headertag(self, text: str, level: int) -> None:
        """Creates a header tag of a specific level (1-6)."""
        self.writeHTML(f"<h{level}>{text}</h{level}>")
    def title(self, text: str) -> None:
        """Creates a main title (<h1>)."""
        self.headertag(text,1)
    def header(self, text: str) -> None:
        """Creates a secondary header (<h2>)."""
        self.headertag(text,2)
    def subheader(self, text: str) -> None:
        """Creates a subheader (<h3>)."""
        self.headertag(text,3)

                                            
class Row(Container):
    """A specialized container that represents a Bootstrap row, holding columns."""
    def __init__(self, parent: str = PAGEID, num_cols: int = 1):
        """
        Args:
            parent (str, optional): The ID of the parent element. Defaults to the main page container.
            num_cols (int, optional): The number of columns to create within this row. Defaults to 1.
        """
        super().__init__(parent=parent, class_name="row")
        self.columns: List['Container'] = []
        for _ in range(num_cols):
            # A Column is a simple container with the "col" class, and its parent is this row.
            col = Container(parent=self.id, class_name="col")
            self.columns.append(col)

class Page(Container):
    """A special singleton container that represents the main page content area."""
    def __init__(self, titletext: str = "", width: str = "narrow"):
        """
        Initializes the main page container. This class is a singleton; subsequent
        calls will adopt the existing page element.

        Args:
            titletext (str, optional): The text to set as the document's <title>. Defaults to "".
            width (str, optional): If "narrow", applies the Bootstrap 'container' class for a centered, max-width layout. Defaults to "narrow".
        """
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