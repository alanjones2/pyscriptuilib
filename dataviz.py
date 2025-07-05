import uilib as ui
import plotly.express as px
import datetime

# --- 1. Create the main page ---
# This is the root container for all other components.
page = ui.Page(titletext="Data Visualization App")

# --- 2. Add a banner ---
# Use the Banner component for a prominent title.
page.add(ui.Banner("Simple Data Visualization", "A demonstration of Plotly and uilib"))

# --- 3. Create the main two-column layout ---
# Use a Row with a layout of 2 to create two equal-width columns.
main_row = ui.Row(layout=2)
page.add(main_row)

# Get a reference to the columns for easy access.
plot_col, text_col = main_row.columns

# --- 4. Populate the plot column ---
# Create some sample data and a Plotly figure.
df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip", color="sex", title="Restaurant Tips Analysis")

# Use the .disp() method to render the Plotly figure.
plot_col.disp(fig)

# --- 5. Populate the text column ---
# Add a header and some descriptive text.
text_col.header("About the Data")
text_col.write(
    "This chart displays the relationship between the total bill and the tip amount "
    "at a restaurant, colored by the gender of the person paying the bill."
)
text_col.writeHTML(
    "The data is from the <code>tips</code> dataset included with Plotly Express."
)

# --- 6. Add a footer ---
page.writeHTML("<hr>") # Use a horizontal rule for separation.
footer = ui.Container(class_name="text-center text-muted")
page.add(footer)
current_year = datetime.date.today().year
footer.writeHTML(f"<small>Created by Alan Jones &copy; {current_year}</small>")