# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd

from PIL import Image
import io
import base64
import requests

from dash import Dash, dcc, html, Input, Output, no_update
import plotly.graph_objects as go
import plotly.express as px

option_list_time = ["256","1024"]
option_list_view = ["Definite Classes","All data","Intensity loss",
                    "HR1 loss", "HR2 loss"]

app = Dash(__name__)

app.layout = html.Div(
    className="container",
    children=[
        dcc.Dropdown(
            id = "dropdown_time",
            options = option_list_time,
            value = "256"
            ),
        dcc.Dropdown(
            id = "dropdown_view",
            options = option_list_view,
            value = "Definite Classes"
            ),
        dcc.Graph(id="graph-5", clear_on_unhover=True,
                  style={'width': '90vh', 'height': '90vh'}),
        dcc.Tooltip(id="graph-tooltip-5"),
    ],
)

@app.callback(
    Output("graph-tooltip-5", "show"),
    Output("graph-tooltip-5", "bbox"),
    Output("graph-tooltip-5", "children"),
    Input("graph-5", "hoverData"),
    Input("dropdown_time","value"),
    Input("dropdown_view","value"),
)
def display_hover(hoverData,time,view):
    if hoverData is None:
        return False, no_update, no_update

    if time == "256":
        file = "umap_codes"
    elif time == "1024":
        file = "umap_codes_1024"
    else:
        file = "umap_codes"
        
    df_final = pd.read_pickle("{}.pkl".format(file))
    
    hover_data = hoverData["points"][0] #remove [0] to get all hovered points
    bbox = hover_data["bbox"]
    num = hover_data["pointNumber"]
    cur = hover_data["curveNumber"]
    
    if view == "Definite Classes":
        filtered_list = ["alpha","beta","chi","delta","gamma","lambda","kappa","mu","nu",
                     "omega","phi","rho","theta"]
        ronclass = filtered_list[cur]
        point_arr = df_final[df_final["ronclass"] == ronclass].index[0]+num
    elif view == "All data":
        filtered_list = df_final["ronclass"].unique()
        ronclass = filtered_list[cur]
        point_arr = df_final[df_final["ronclass"] == ronclass].index[0]+num
    else:
        point_arr = num
    
    image_path = df_final["images"][point_arr]
    im = Image.open(requests.get(image_path, stream=True).raw).convert("RGB")

    # dump it to base64
    buffer = io.BytesIO()
    im.save(buffer, format="png")
    encoded_image = base64.b64encode(buffer.getvalue()).decode()
    im_url = "data:image/png;base64, " + encoded_image
    
    
    image_path_2 = df_final["ccs"][point_arr]
    im_2 = Image.open(requests.get(image_path_2, stream=True).raw).convert("RGB")

    # dump it to base64
    buffer_2 = io.BytesIO()
    im_2.save(buffer_2, format="png")
    encoded_image_2 = base64.b64encode(buffer_2.getvalue()).decode()
    im_url_2 = "data:image/png;base64, " + encoded_image_2
    children = [
        html.Div([
            html.Img(
                src=im_url,
                style={"height": "84px","width": "168px", 'display': 'block', 'margin': '0 auto'},
            ),
            html.Img(
                src=im_url_2,
                style={"height": "168px","width": "168px", 'display': 'block', 'margin': '0 auto'},
            ),
            html.P(str("Cluster Class:"+str(df_final["class"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("obs_ID:"+str(df_final["obsID"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("x:"+str(df_final["x"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("y:"+str(df_final["y"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("z:"+str(df_final["z"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("Intensity loss:"+str(df_final["intens_err"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("HR1 loss:"+str(df_final["HR1_err"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("HR2 loss:"+str(df_final["HR2_err"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("Ron's classification:"+str(df_final["ronclass"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("Physically motivated label:"+str(df_final["physical"][point_arr])), style={'font-weight': 'bold'}),
        ])
    ]

    return True, bbox, children

@app.callback(
    Output("graph-5", "figure"),
    Input("dropdown_time","value"),
    Input("dropdown_view","value"),
)
def update_figure(time,view):
    filtered_list = ["alpha","beta","chi","delta","gamma","lambda","kappa","mu","nu",
                     "omega","phi","rho","theta"]
    greek_list = ["α","β","χ","δ","γ","λ","κ","μ","ν","ω","φ","ρ","θ"]
    symbols = ["circle","cross","diamond","square","x","circle","cross","diamond",
               "square","x","circle","cross","diamond"]
    fig = go.Figure()
    
    if time == "256":
        file = "umap_codes"
    elif time == "1024":
        file = "umap_codes_1024"
    else:
        file = "umap_codes"
        
    df_final = pd.read_pickle("{}.pkl".format(file))
    
    if view == "Definite Classes":
        for i,item in enumerate(filtered_list):
            fig.add_trace(go.Scatter3d(
                x=df_final["x"][df_final["ronclass"] == item],
                y=df_final["y"][df_final["ronclass"] == item],
                z=df_final["z"][df_final["ronclass"] == item],
                mode='markers',
                name = greek_list[i],
                marker_symbol = symbols[i],
                marker=dict(
                    size=2,
                    color = px.colors.qualitative.Light24[i],)
                )
            )
        fig.update_traces(
            hoverinfo="none",
            hovertemplate=None,
        )
    elif view == "All data":
        for i,item in enumerate(df_final["ronclass"].unique()):
            fig.add_trace(go.Scatter3d(
                x=df_final["x"][df_final["ronclass"] == item],
                y=df_final["y"][df_final["ronclass"] == item],
                z=df_final["z"][df_final["ronclass"] == item],
                mode='markers',
                name = item,
                marker=dict(
                    size=2,
                    )
                )
            )
        fig.update_traces(
            hoverinfo="none",
            hovertemplate=None,
        )
    elif view == "Intensity loss":
        fig.add_trace(go.Scatter3d(
            x=df_final["x"],
            y=df_final["y"],
            z=df_final["z"],
            mode='markers',
            marker=dict(
                size=2,
                color = df_final["intens_err"],
                colorscale = "Viridis",
                cmax = 300,
                cmin = 0)
            )
        )
        fig.update_coloraxes()
        fig.update_traces(
            hoverinfo="none",
            hovertemplate=None,
            marker_showscale = True
        )
        
    elif view == "HR1 loss":
        fig.add_trace(go.Scatter3d(
            x=df_final["x"],
            y=df_final["y"],
            z=df_final["z"],
            mode='markers',
            marker=dict(
                size=2,
                color = df_final["HR1_err"],
                colorscale = "Viridis",
                cmax = 15,
                cmin = 0)
            )
        )
        fig.update_coloraxes()
        fig.update_traces(
            hoverinfo="none",
            hovertemplate=None,
            marker_showscale = True
        )
        
    elif view == "HR2 loss":
        fig.add_trace(go.Scatter3d(
            x=df_final["x"],
            y=df_final["y"],
            z=df_final["z"],
            mode='markers',
            marker=dict(
                size=2,
                color = df_final["HR2_err"],
                colorscale = "Viridis",
                cmax = 15,
                cmin = 0)
            )
        )
        fig.update_coloraxes()
        fig.update_traces(
            hoverinfo="none",
            hovertemplate=None,
            marker_showscale = True
        )
    
    
    
    fig.update_layout(
        legend= {'itemsizing': 'constant'},
        scene = dict(          
                        xaxis_title="UMAP axis 1",
                        yaxis_title="UMAP axis 2",
                        zaxis_title="UMAP axis 3",
                        aspectmode='cube',),
        legend_title_text="Manual Classifications",)
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
