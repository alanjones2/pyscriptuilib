import uilib as ui
import plotly.express as px

# --- 1. Create the main page ---
page = ui.Page(titletext="Interactive Dashboard")

# --- 2. Add a banner ---
page.add(ui.Banner("Interactive Dashboard", "Select a dataset to visualize"))

# --- 3. Create the main layout ---
# Use a custom layout for a sidebar (3/12) and a main content area (9/12).
main_row = ui.Row(layout=[3, 9])
page.add(main_row)

controls_col, plot_col = main_row.columns

# --- 4. Create the components ---
controls_col.header("Controls")

# The container that will hold the dynamically updated plot
plot_container = ui.Container()
plot_col.add(plot_container)

# --- 5. Define the callback function ---
# This function will be called whenever the dropdown selection changes.
def update_plot(select_component, event):
    """Clears the plot container and draws a new plot based on the selection."""
    dataset_name = select_component.get_value()

    if dataset_name == "iris":
        df = px.data.iris()
        fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="Iris Dataset")
    elif dataset_name == "gapminder":
        df = px.data.gapminder().query("continent=='Oceania'")
        fig = px.line(df, x="year", y="lifeExp", color="country", title="Gapminder (Oceania)")
    else: # Default to "tips"
        df = px.data.tips()
        fig = px.scatter(df, x="total_bill", y="tip", color="smoker", title="Tips Dataset")

    # Clear the old plot and display the new one
    plot_container.clear().disp(fig)

# --- 6. Create and configure the dropdown ---
dataset_select = ui.Select(
    caption="Choose a Dataset:",
    values=["tips", "iris", "gapminder"],
    labels=["Restaurant Tips", "Iris Flowers", "Gapminder"],
    callback=update_plot
)
controls_col.add(dataset_select)

# --- 7. Trigger the initial plot draw ---
update_plot(dataset_select, None)