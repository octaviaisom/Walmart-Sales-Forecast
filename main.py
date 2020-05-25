from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

import pandas as pd
import numpy as np
import datetime

#---------------------------------------------------------------------------------------

#import data
csv1 = pd.read_csv("data/sales.csv")
sales = pd.DataFrame(csv1)
sales.Date = pd.to_datetime(sales.Date)

csv2 = pd.read_csv("data/holidays.csv")
holidays = pd.DataFrame(csv2)
holidays.Date = pd.to_datetime(holidays.Date)

holidates = holidays.Date
byDate_all = sales.groupby('Date').sum()

for index, row in byDate_all.iterrows():
    wk_end = index
    six_days = datetime.timedelta(days = 6)
    wk_start = (wk_end - six_days)
    week = pd.date_range(start=wk_start,end=wk_end)

    try:   
        byDate_all.loc[index, "IsHoliday"] = bool(set(week) & set(holidates))
        print(f"{index}: Holiday Check Complete")

    except:
        print(f"{index}: Unable to Complete Holiday Check, Skipping...")

byDate_all.IsHoliday = byDate_all.IsHoliday.astype('int')

csv3 = pd.read_csv("data/stores.csv")
stores = pd.DataFrame(csv3)

#---------------------------------------------------------------------------------------

#setting color palette for charts
pio.templates.default = "plotly_white"
walmart_palette = ['#004c91','#ffc220','#f47321','#007dc6','#78b9e7','#76c043']

#---------------------------------------------------------------------------------------

#Sales Analysis
def sales_plots():
    byDate = sales.groupby('Date',sort=False).sum()
    byDate.IsHoliday = byDate.IsHoliday.astype('bool').astype('int')
    byDate.index.freq = 'W-FRI'


    byDate_line = go.Figure(data=go.Scatter(x=byDate.index,y=byDate.Weekly_Sales, name='Weekly_Sales',marker_color=walmart_palette[0]))
    byDate_line.update_layout(title={
            'text': "Total Weekly Sales",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    byDate_line.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    byDate_line.update_layout(title={
            'text': "Total Weekly Sales",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    ymin=byDate.Weekly_Sales.min()
    ymax=byDate.Weekly_Sales.max()
    byDate_wm_markers = go.Figure(data=go.Scatter(x=byDate.index,y=byDate.Weekly_Sales, name='Weekly_Sales',marker_color=walmart_palette[0]))
    final_wk = max(byDate.index)
    for date in byDate.query("IsHoliday==1").index:
        byDate_wm_markers.add_shape(type="line",
                    x0=date,
                    y0=ymin,
                    x1=date,
                    y1=ymax,
                    opacity=0.2)
    byDate_wm_markers.update_layout(title={
            'text': "Total Weekly Sales with Walmart's Holiday Markers",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    byDate_all_markers = go.Figure(data=go.Scatter(x=byDate_all.index,y=byDate_all.Weekly_Sales, name='Weekly_Sales',marker_color=walmart_palette[0]))
    for date in byDate_all.query("IsHoliday==1").index:
        byDate_all_markers.add_shape(type="line",
                    x0=date,
                    y0=ymin,
                    x1=date,
                    y1=ymax,
                    opacity=0.2,)
    byDate_all_markers.update_layout(title={
            'text': "Total Weekly Sales with All Holiday Markers",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    return byDate_line, byDate_wm_markers, byDate_all_markers

#---------------------------------------------------------------------------------------

#Sales by Store
def store_plots():
    byStore = sales.reset_index().groupby('Store', as_index=False).sum()
    byStore = pd.merge(byStore, stores, on='Store', how='left')
    byStore = byStore[["Store", "Weekly_Sales", "Type", "Size"]]

    byStore_Bar = go.Figure(data=go.Bar(x=byStore.Store,y=byStore.Weekly_Sales,name='Weekly_Sales',marker_color=walmart_palette[0]))
    byStore_Bar.update_layout(title={
            'text': "Total Weekly Sales by Store",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    size_dist = px.histogram(byStore, x="Size", color='Type', color_discrete_sequence=walmart_palette)
    size_dist.update_layout(title={
            'text': "Size Distribution",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    store_sales_scatter = px.scatter(byStore, x="Size",y='Weekly_Sales',color='Type', color_discrete_sequence=walmart_palette)
    store_sales_scatter.update_traces(marker=dict(size=10, opacity=0.8))
    store_sales_scatter.update_layout(title={
            'text': "Size v. Sales",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    byStore['SalesPerSF'] = byStore.Weekly_Sales/byStore.Size
    store_scatter_sf = px.scatter(byStore, x="Size",y='SalesPerSF',color='Type',color_discrete_sequence=walmart_palette)
    store_scatter_sf.update_traces(marker=dict(size=10, opacity=0.8))
    store_scatter_sf.update_layout(title={
            'text': "Size v. Sales per Sq. Ft.",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    store_type_box = px.box(byStore, x="Type", y="Weekly_Sales", color='Type',color_discrete_sequence=walmart_palette)
    store_type_box.update_traces(width=0.7)
    store_type_box.update_layout(title={
            'text': "Weekly Sales by Store Type",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    store_size_box = px.box(byStore, x="Type", y="Size", color='Type',color_discrete_sequence=walmart_palette)
    store_size_box.update_traces(width=0.7)
    store_size_box.update_layout(title={
            'text': "Total Sq. Ft by Store Type",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    

    byStorex = byStore[['SalesPerSF','Weekly_Sales', 'Size']]


    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=6) 
    kmeans.fit(byStorex)
    byStorex['Cluster'] = kmeans.labels_
    byStorex = byStorex.sort_values('Cluster')
    byStorex.Cluster = byStorex.Cluster.astype('object')


    store_cluster_scatter = px.scatter(byStorex, x="Size",y='Weekly_Sales',color='Cluster', color_discrete_sequence=walmart_palette)
    store_cluster_scatter.update_traces(marker=dict(size=10, opacity=0.8))
    store_cluster_scatter.update_layout(title={
            'text': "Size v. Sales",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
   

    store_cluster_box = px.box(byStorex, x="Cluster", y="SalesPerSF", color="Cluster",color_discrete_sequence=walmart_palette)
    store_cluster_box.update_traces(width=.7)
    store_cluster_box.update_layout(title={
            'text': "Total Weekly Sales by Store",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    

    return store_cluster_scatter

