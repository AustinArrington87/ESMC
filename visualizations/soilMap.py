import pandas as pd
df = pd.read_csv('/Users/austinarrington/ESMC/visualizations/IL_SoilData.csv')

import plotly.express as px
fig = px.density_mapbox(df, lat='lat', lon='lon', z='soc (t/ha)', radius=10,
                        zoom=3,
                        mapbox_style="open-street-map")
fig.show()