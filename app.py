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

print("This is the version of the plot which only includes definite definitions")

df_final = pd.read_pickle("umap_codes.pkl")

filtered_list = ["alpha","beta","chi","delta","gamma","lambda","kappa","mu","nu",
                 "omega","phi","rho","theta"]
greek_list = ["α","β","χ","δ","γ","λ","κ","μ","ν","ω","φ","ρ","θ"]

color_map = {
    -1: "#007fff",
    0: "#e52b50",
    1: "#9f2b68",
    2: "#3b7a57",
    3: "#3ddc84",
    4: "#ffbf00",
    5: "#915c83",
    6: "#008000",
    7: "#7fffc4",
    8: "#e9d66b",
}

symbols = ["circle","cross","diamond","square","x","circle","cross","diamond",
           "square","x","circle","cross","diamond"]

fig = go.Figure()
tot = 0
for i,item in enumerate(filtered_list):
    tot += df_final["x"][df_final["ronclass"] == item].size
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

fig.update_layout(
    legend= {'itemsizing': 'constant'},
    scene = dict(
                    xaxis = dict(range=[-4,11],),
                    yaxis = dict(range=[-5,3],),
                    zaxis = dict(range=[3,13],),
                    xaxis_title="UMAP axis 1",
                    yaxis_title="UMAP axis 2",
                    zaxis_title="UMAP axis 3",
                    aspectmode='cube',),
    legend_title_text="Manual Classifications",)

"""
fig.update_scenes(xaxis_title_font_size=28,
                  yaxis_title_font_size=28,
                  zaxis_title_font_size=28,
                  xaxis_tickfont_size=18,
                  yaxis_tickfont_size=18,
                  zaxis_tickfont_size=18) 
"""

app = Dash(__name__)

app.layout = html.Div(
    className="container",
    children=[
        dcc.Graph(id="graph-5", figure=fig, clear_on_unhover=True,
                  style={'width': '90vh', 'height': '90vh'}),
        dcc.Tooltip(id="graph-tooltip-5"),
    ],
)

@app.callback(
    Output("graph-tooltip-5", "show"),
    Output("graph-tooltip-5", "bbox"),
    Output("graph-tooltip-5", "children"),
    Input("graph-5", "hoverData"),
)

def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update
    
    hover_data = hoverData["points"][0] #remove [0] to get all hovered points
    bbox = hover_data["bbox"]
    num = hover_data["pointNumber"]
    cur = hover_data["curveNumber"]
    ronclass = filtered_list[cur]
    point_arr = df_final[df_final["ronclass"] == ronclass].index[0]+num
    

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
            html.P(str("Curve number:"+str(cur)), style={'font-weight': 'bold'}),
            html.P(str("Point number:"+str(num)), style={'font-weight': 'bold'}),
            html.P(str("Ron's classification:"+str(df_final["ronclass"][point_arr])), style={'font-weight': 'bold'}),
            html.P(str("Physically motivated label:"+str(df_final["physical"][point_arr])), style={'font-weight': 'bold'}),
        ])
    ]

    return True, bbox, children

if __name__ == "__main__":
    app.run_server(debug=True)
