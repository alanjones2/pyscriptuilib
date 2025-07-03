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
ID = 0
def newID():
    global ID 
    ID = ID + 1
    return f"pui-id-{ID}"

# Containers

class Container:
    node = None
    id = ""
    classAttributes = False
    def __init__(self, parent=PAGEID, classAttributes=False):
        self.id = newID()
        self.node = document.createElement("div")
        self.node.setAttribute("class", "container")
        self.node.setAttribute("id", self.id)
        if classAttributes: self.setClassAttributes(classAttributes)
        parentNode = document.getElementById(parent)
        parentNode.append(self.node)

    def setClassAttributes(self, classAttributes):
        self.classAttributes = classAttributes
        self.node.setAttribute("class", classAttributes)

    # Column functions
    def makeCols(self,number):
        # create a row of columns and display the figures in the columns
        row = Container(classAttributes="row")
        cols=[]
        for i in range(0,number):
            cols.append(Container(parent=row.id))
            cols[i].node.setAttribute("class","col") 
        return cols
    
    # Content functions 

    def disp(self, content, append=True):
        display(content, target=self.id, append=append)
    def write(self, text, append = True):
        self.disp(text, append)
    def writeHTML(self, text, append = True):
        if append:
            self.node.innerHTML = self.node.innerHTML + md.markdown(text)
        else:
            self.node.innerHTML = md.markdown(text)
    def headertag(self,text,level):
        self.writeHTML(md.markdown(f"<h{level}>{text}</h>"))         
    def title(self, text): self.headertag(text,1)
    def header(self, text): self.headertag(text,2)
    def subheader(self, text): self.headertag(text,3)

    def banner(self, title="", subtitle=""):
        headerField = Container(parent=self.id, classAttributes="bg-primary text-center text-white p-2 my-2")
        titleField = Container(parent=headerField.id, classAttributes="display-3")
        titleField.disp(title)
        subtitleField = Container(parent=headerField.id, classAttributes="lead")
        subtitleField.disp(subtitle)

    def smallbanner(self, text=""):
        headerField = Container(parent=self.id, classAttributes="bg-primary text-center text-white p-2 my-1")
        titleField = Container(parent=headerField.id, classAttributes="display-4")
        titleField.disp(text)

    # controls
    def button(self,caption="Button", callback=None, value="pressed", btnClass="btn btn-primary"):
        b = document.createElement("button")
        if callback: b.setAttribute("py-click",callback)
        b.setAttribute("class", btnClass)
        b.setAttribute("type","button")
        b.setAttribute("value",value)
        b.append(document.createTextNode(caption))
        self.node.append(b)

    def select(self,caption="", callback=None, values=[], labels=[]):
        select_id = newID() # Generate a unique ID for the select element
        if len(labels)==0: labels=values

        if caption:
            label_elem = document.createElement("label")
            label_elem.setAttribute("for", select_id)
            label_elem.append(document.createTextNode(caption))
            self.node.append(label_elem)

        s = document.createElement("select")
        if callback: s.setAttribute("py-change",callback)
        s.setAttribute("class", "form-select")
        s.setAttribute("id", select_id) # Set the ID for association with label

        for l, v in zip(labels, values):
            o = document.createElement("option")
            o.setAttribute("value",v)
            o.append(document.createTextNode(l))
            s.append(o)
        self.node.append(s)

    def check(self, caption="", callback=None, value=None, label=None): # 'label' here is the text for the checkbox
        checkbox_id = newID() # Generate a unique ID for the checkbox input
        s = document.createElement("div")
        s.setAttribute("class", "form-check")
        o = document.createElement("input")
        o.setAttribute("class", "form-check-input")
        o.setAttribute("type", "checkbox")
        o.setAttribute("value",value)
        o.setAttribute("id", checkbox_id) # Set the ID for association with label
        if callback: o.setAttribute("py-change",callback) # py-change should be on the input
        l = document.createElement("label")
        l.setAttribute("class", "form-check-label") # Bootstrap class for labels
        l.setAttribute("for", checkbox_id) # Associate label with input
        l.append(document.createTextNode(label if label else caption)) # Use 'label' text if provided, else 'caption'
        s.append(o)
        s.append(l)
        self.node.append(s)

    def text_input(self, caption="", initial_value="", placeholder="", callback=None):
        input_id = newID()

        # Create a div for the form group (optional, but good for styling)
        form_group_div = document.createElement("div")
        form_group_div.setAttribute("class", "mb-3") # Bootstrap margin-bottom

        # Create label
        if caption:
            label_elem = document.createElement("label")
            label_elem.setAttribute("for", input_id)
            label_elem.setAttribute("class", "form-label")
            label_elem.append(document.createTextNode(caption))
            form_group_div.append(label_elem)

        # Create input element
        input_elem = document.createElement("input")
        input_elem.setAttribute("type", "text")
        input_elem.setAttribute("class", "form-control")
        input_elem.setAttribute("id", input_id)
        input_elem.setAttribute("value", initial_value)
        if placeholder:
            input_elem.setAttribute("placeholder", placeholder)

        if callback:  
            #input_elem.setAttribute("py-enter", callback)
            # input_elem.setAttribute("onkeydown", f"if(event.key === 'Enter') {{ {callback}(event); }}")
            input_elem.setAttribute("py-change", callback)
            #input_elem.setAttribute("py-input", callback) # Use py-input for real-time updates

        form_group_div.append(input_elem)
        self.node.append(form_group_div)

    def slider(self, caption="", min_val=0, max_val=100, initial_val=None, step=1, callback=None):
        slider_id = newID()
        #output_id = newID() # ID for the element displaying the current value

        # Create a div for the form group
        form_group_div = document.createElement("div")
        form_group_div.setAttribute("class", "mb-3")

        # Create label
        label_elem = document.createElement("label")
        label_elem.setAttribute("for", slider_id)
        label_elem.setAttribute("class", "form-label")
        label_elem.append(document.createTextNode(caption))
        form_group_div.append(label_elem)

        # Create slider input
        slider_elem = document.createElement("input")
        slider_elem.setAttribute("type", "range")
        slider_elem.setAttribute("class", "form-range")
        slider_elem.setAttribute("id", slider_id)
        slider_elem.setAttribute("min", str(min_val))
        slider_elem.setAttribute("max", str(max_val))
        slider_elem.setAttribute("step", str(step))
        slider_elem.setAttribute("value", str(initial_val if initial_val is not None else min_val))
        if callback: slider_elem.setAttribute("py-change", callback) # Use py-input for real-time updates
        form_group_div.append(slider_elem)

        # Create an output element to display the current value
        #output_elem = document.createElement("output")
        #output_elem.setAttribute("for", slider_id) # Link to the slider
        #output_elem.setAttribute("id", output_id)
        #output_elem.append(document.createTextNode(str(initial_val if initial_val is not None else min_val)))
        #form_group_div.append(output_elem)

        self.node.append(form_group_div)

        # Return the output element's ID so the callback can update it
        #return output_id
                                            

class Page(Container):
    def __init__(self, titletext="", width="narrow"):
        self.id = PAGEID
        self.node = document.createElement("div")
        if width == "narrow":
            self.node.setAttribute("class", "container")
        self.node.setAttribute("id", self.id)

        bodyNode = document.getElementsByTagName("body")[0]
        bodyNode.append(self.node)

        titletag = document.createElement("title")
        titletag.innerHTML = titletext
        headNode = document.getElementsByTagName("head")[0]
        headNode.append(titletag)







    