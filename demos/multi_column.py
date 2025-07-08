from uilib import Page, Banner, Row, Container, TextInput, Select, Button, Alert, SmallBanner
import plotly.express as px
from pyscript import display

# --- Page and Banner ---
page = Page(titletext="Sales Dashboard", width="narrow")
page.add(Banner(title="Sales Dashboard", subtitle="Real-time Metrics & Insights"))

# --- Summary Row ---
summary_row = Row(layout=[4, 4, 4])
summary_row.columns[0].add(SmallBanner("📈 Revenue: $12,450"))
summary_row.columns[1].add(SmallBanner("🛒 Orders: 235"))
summary_row.columns[2].add(SmallBanner("👥 Customers: 89"))
page.add(summary_row)

# --- Data Storage ---
sales_data = {
    "North": 1000,
    "South": 1500,
    "East": 800,
    "West": 1200
}

# --- Form Row ---
form_row = Row(layout=[6, 6])
form_container = form_row.columns[0]
result_container = form_row.columns[1]
page.add(form_row)

product_input = TextInput(caption="Product Name", placeholder="e.g., Widget X")
region_select = Select(caption="Region", values=list(sales_data.keys()))
sales_input = TextInput(caption="Sales Amount", placeholder="e.g., 1000")

form_container.add(product_input)
form_container.add(region_select)
form_container.add(sales_input)

# --- Chart Container ---
chart_container = Container()
page.add(chart_container)

# --- Chart Drawing Function ---
def draw_chart():
    chart_container.clear()
    regions = list(sales_data.keys())
    values = list(sales_data.values())
    
    fig = px.bar(
        x=regions,
        y=values,
        labels={'x': 'Region', 'y': 'Sales ($)'},
        title="Sales by Region",
        text=values
    )
    fig.update_traces(marker_color=['#007bff', '#28a745', '#ffc107', '#dc3545'])
    fig.update_layout(yaxis_title="Sales Amount ($)", xaxis_title="Region")
    
    chart_container.disp(fig, append=False)

# --- Initial Chart ---
draw_chart()

# --- Submit Callback ---
def submit_data(component, event):
    product = product_input.get_value().strip()
    region = region_select.get_value()
    sales = sales_input.get_value().strip()

    result_container.clear()
    if product and region and sales.isdigit():
        sale_value = int(sales)
        sales_data[region] = sales_data.get(region, 0) + sale_value
        
        msg = f"**Product:** {product}<br>**Region:** {region}<br>**Sales Added:** ${sale_value}"
        alert = Alert(text=msg, category="success", dismissible=True)
        result_container.add(alert)

        draw_chart()
    else:
        alert = Alert(text="Please complete all fields correctly.", category="danger", dismissible=True)
        result_container.add(alert)

submit_button = Button(caption="Add Record", callback=submit_data)
form_container.add(submit_button)
