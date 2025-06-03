import dash  #brings the dash framework
from dash import html #to create html components
from dash import Input, Output #used for Dash callbacks which enables interactivity
from dash import dcc
import plotly.express as px

app = dash.Dash(__name__)  # initialize a Dash app, create a new instance of Dash app

fig = px.line(x=[1, 2, 3], y=[10, 20, 30])
x_values = [0]
y_values = [0]


#layout sets up the structure of your web page
app.layout = html.Div(children = [
    html.H1(id = "greeting", children="Hello, User!"),
    html.P("Welcome to your first Dash application."),
    dcc.Input(id= "user-input", type="text", placeholder = "Enter name to change the greeting", style={"width": "300px"}),
    html.Button("Submit", id="name_btn"),
    html.P(id="text"),
    html.Div(
        html.Button("Click Me", id="btn", n_clicks=0) 
        ),
    # dcc.Graph(id="graph", figure=fig, style={"margin-top":"10px"})
    dcc.Graph(id="graph", style={"margin-top":"10px"})
])



#connects UI components to Python functions
@app.callback(
    Output("greeting", "children"), #updates the greeting text
    Input("name_btn", "n_clicks"), #submit button to update greeting
    Input("user-input", "value") #capture user name

)

# Function to update the greeting when the "Submit" button is clicked
def update_greeting(n_clicks, name):
    if n_clicks and name:
        return f"Hello, {name}!"
    return "Hello, User!"  # Default greeting


def update_graph(n_clicks):
    if n_clicks > 0:  # Only add points after first click

        if n_clicks not in x_values:  # Prevent duplicates

            x_values.append(int(n_clicks))   # Add x as click count
            y_values.append(n_clicks * 10)  # Add y as 10 * clicks


    fig = px.line(x=x_values, y=y_values, title="Graph Growing with Clicks")

    # Add a footer annotation below the graph
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=-0.3,  # Positioning below the graph
        text="Y-axis represents the total value growing by multiples of 10",
        showarrow=False,
        font=dict(size=12, color="gray")
    )

    fig.update_layout(xaxis_title="Click Count", yaxis_title="Value",
                      xaxis=dict(tickmode="linear", tick0=0, dtick=1, range=[0, max(x_values) + 1]),  # Starts from 0, no negatives
                      yaxis=dict(range=[0, max(y_values) + 10])  # Ensures positive Y values

                      )
    
    return fig

#when button is clicked this function runs
# Function to update the text when the "Change Text" button is clicked
def update_text(n_clicks):
    if n_clicks == 0:
        return "Want to count how many times you click the below button?" #original text before the  click
    return f"Button clicked {n_clicks} times!" #updates when clicked

#connects UI components to Python functions
@app.callback(
    Output("text", "children"), #updates button click count text
    Output("graph", "figure"), #update the graph dynamically
    Input("btn", "n_clicks"), #change text button to track number of clicks

)

def update_content(n_clicks):

    text = update_text(n_clicks)
    #update graph
    fig = update_graph(n_clicks)

    return text, fig #return both updates




#this ensures the Dash server starts only when the script is run directly, not when it's imported into another module
#the app runs ons a local web server provided by Dash
if __name__ == '__main__':
    app.run(debug=True)