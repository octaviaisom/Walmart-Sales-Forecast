'''THIS FILE WAS EXPORTED FROM JUPYTER NOTEBOOK THEN FORMATTED FOR USE IN DASH APP'''

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

    except:
        print(f"{index}: Unable to Complete Holiday Check, Skipping...")

byDate_all.IsHoliday = byDate_all.IsHoliday.astype('int')

csv3 = pd.read_csv("data/stores.csv")
stores = pd.DataFrame(csv3)

#---------------------------------------------------------------------------------------

#setting color palette for charts
pio.templates.default = "plotly_white"
walmart_palette = ['#004c91','#ffc220','#007dc6','#78b9e7','#76c043','#f47321']

#---------------------------------------------------------------------------------------

#Sales Analysis
def sales_plots():
    byDate = sales.groupby('Date',sort=False).sum()
    byDate.IsHoliday = byDate.IsHoliday.astype('bool').astype('int')
    byDate.index.freq = 'W-FRI'

    ymin=byDate.Weekly_Sales.min()
    ymax=byDate.Weekly_Sales.max()

    byDate_markers = go.Figure(data=go.Scatter(x=byDate_all.index,y=byDate_all.Weekly_Sales, name='Weekly_Sales',marker_color=walmart_palette[0]))
    for date in byDate_all.query("IsHoliday==1").index:
        byDate_markers.add_shape(type="line",
                    x0=date,
                    y0=ymin,
                    x1=date,
                    y1=ymax,
                    opacity=0.2,)
    byDate_markers.update_layout(title={
            'text': "Total Weekly Sales with All Holiday Markers",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    byDate_markers.update_xaxes(
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

    return byDate_markers

#---------------------------------------------------------------------------------------

#Sales by Store
def store_plots():
    byStore = sales.reset_index().groupby('Store', as_index=False).sum()
    byStore = pd.merge(byStore, stores, on='Store', how='left')
    byStore = byStore[["Store", "Weekly_Sales", "Type", "Size"]]

    size_dist = px.histogram(byStore, x="Size", color='Type', color_discrete_sequence=walmart_palette)
    size_dist.update_layout(title={
            'text': "Size Distribution",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    byStore['SalesPerSF'] = byStore.Weekly_Sales/byStore.Size
    store_scatter_sf = px.scatter(byStore, x="Size",y='SalesPerSF',color='Type',color_discrete_sequence=walmart_palette,width=400)
    store_scatter_sf.update_traces(marker=dict(size=10, opacity=0.8))
    store_scatter_sf.update_layout(title={
            'text': "Size v. Sales per Sq. Ft.",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    store_type_box = px.box(byStore, x="Type", y="Weekly_Sales", color='Type',color_discrete_sequence=walmart_palette,width=400)
    store_type_box.update_traces(width=0.7)
    store_type_box.update_layout(title={
            'text': "Store Type v. Sales",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


    store_size_box = px.box(byStore, x="Type", y="Size", color='Type',color_discrete_sequence=walmart_palette)
    store_size_box.update_traces(width=0.7)
    store_size_box.update_layout(title={
            'text': "Store Type v. Size",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    

    return store_size_box, store_type_box, size_dist, store_scatter_sf

#---------------------------------------------------------------------------------------

#Sales by Dept
def dept_plots():
    from statsmodels.tsa.stattools import adfuller

    #Dickey-Fuller Test
    dept_w_missing_wks = sales.groupby('Dept').nunique().sort_values('Date').query('Date<143')
    missing_wks = dept_w_missing_wks.index
    stat_list = []
    stat_bool_list = []
    dept_list = []
    depts = sales.Dept.unique()
    for dept in depts:
        if dept in missing_wks:
            continue
            
        byDeptx = sales.query(f"Dept=={dept}").groupby('Date').sum()
        dftest = adfuller(byDeptx['Weekly_Sales'], maxlag=55)
        p_value = dftest[1]
        lags = dftest[2]

        if p_value <= 0.05:
            stationarity = "Stationary"
            station_bool = 1
            
        else:
            stationarity = "Non-Stationary"
            station_bool = 0
        
        dept_list.append(dept)
        stat_list.append(stationarity)
        stat_bool_list.append(station_bool)

    stationarities = pd.DataFrame({'Dept': dept_list,
                                'Stationary': stat_list,
                                'Stationary_Bool': stat_bool_list})
    
    
    byStat = pd.merge(sales, stationarities, on='Dept', how='left')
    byStat = byStat.groupby(['Stationary','Date'], as_index=False).sum()

    byStat_line = px.line(byStat,x='Date', y='Weekly_Sales', color='Stationary',color_discrete_sequence=walmart_palette)
    byStat_line.update_layout(title={
            'text': "Department Stationarity",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    #byStat_line.update_layout(legend_orientation="h")

    byStat_pie = px.pie(byStat, values='Weekly_Sales', names='Stationary',color_discrete_sequence=walmart_palette)
    byStat_pie.update_yaxes(automargin=True)
    byStat_pie.update_layout(showlegend=False)
    
    return byStat_line, byStat_pie

#Create Models
def model_plots():
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from pmdarima import auto_arima    

    byDate = sales.groupby('Date',sort=False).sum()
    models = byDate[['Weekly_Sales', 'IsHoliday']]
    models.IsHoliday = byDate.IsHoliday.astype('bool').astype('int')
    models.index.freq = 'W-FRI'
 
    #Test/Train Split
    length = len(models)
    train_len = int(length*0.70)
    train = models.iloc[:train_len]
    test = models.iloc[train_len:]

    #Fit Model 1 (2,0,2)(1,0,0,52)
    model1 = SARIMAX(train['Weekly_Sales'],order=(2,0,2),seasonal_order=(1,0,0,52),enforce_invertibility=False)
    results1 = model1.fit()
    
    #Retrieve Predicted Values
    start=len(train)
    end=len(train)+len(test)-1
    predictions1 = results1.predict(start=start, end=end, dynamic=False)
    models['NoHolidays'] = predictions1

    #drop nan values from train set
    models.dropna(inplace=True)
   
    #Evaluate Model 1
    models_lines = go.Figure()
    models_lines.add_trace(
        go.Scatter(
            x=models.index,
            y=models.Weekly_Sales,
            name = "Weekly Sales - Actual",
            line=dict(color=walmart_palette[0],dash='dot'), 
        ))
    models_lines.add_trace(
        go.Scatter(
            x=models.index,
            y=models.NoHolidays,
            name = "Model 1 - No Holidays",
            line=dict(color=walmart_palette[1])
        ))
    models_lines.update_layout(
            title={
                'text': "Model Evaluation",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'}
    )

    #SARIMAX (Walmart's Holidays)
    model2 = SARIMAX(train['Weekly_Sales'],exog=train['IsHoliday'],order=(2,0,2),seasonal_order=(1,0,0,52),enforce_invertibility=False)
    results2 = model2.fit()
    
    #Retrieve Predicted Values
    start=len(train)
    end=len(train)+len(test)-1
    exog_forecast = test[['IsHoliday']]  # requires two brackets to yield a shape of (35,1)
    predictions2 = results2.predict(start=start, end=end, exog=exog_forecast)
    models['WalmartHolidays'] = predictions2
   
    #Evaluate Model 2
    models_lines.add_trace(
        go.Scatter(
            x=models.index,
            y=models.WalmartHolidays,
            name = "Model 2 - Walmart's Holidays",
            line=dict(color=walmart_palette[2])
        ))
    
    #SARIMAX (All Holidays)
    byDatex = byDate_all
    
    length = len(byDatex)
    train_len = int(length*0.70)
    train = byDatex.iloc[:train_len]
    test = byDatex.iloc[train_len:]

    model3 = SARIMAX(train['Weekly_Sales'],exog=train['IsHoliday'],order=(2,0,2),seasonal_order=(1,0,0,52),enforce_invertibility=False)
    results3 = model3.fit()

    start=len(train)
    end=len(train)+len(test)-1
    exog_forecast = test[['IsHoliday']]  # requires two brackets to yield a shape of (35,1)
    predictions3 = results3.predict(start=start, end=end, exog=exog_forecast)
    models['AllHolidays'] = predictions3
    
    #Evaluate Model 3
    models_lines.add_trace(
        go.Scatter(
            x=models.index,
            y=models.AllHolidays,
            name = "Model 3 - All Holidays",
            line=dict(color=walmart_palette[3])
        ))
   
    #Forecast the Future
    byDate = byDate[['Weekly_Sales','IsHoliday']]
    csv = pd.read_csv("data/fcast.csv")
    fcast_dates = pd.DataFrame(csv)
    fcast_dates.IsHoliday = fcast_dates.IsHoliday.astype('bool').astype('int')
    fcast_dates.Date = pd.to_datetime(fcast_dates.Date)
    
    fcast_dates.set_index('Date', inplace=True)
    fcast_dates.index.freq = 'W-FRI'
    
    model2x = SARIMAX(byDate['Weekly_Sales'],order=(2,0,2),seasonal_order=(1,0,0,52),enforce_invertibility=False)
    resultsx = model2x.fit()
    #Forcast Future Sales
    exog_forecast = fcast_dates[['IsHoliday']]
    fcast_predics = resultsx.predict(fcast_dates.index.min(),fcast_dates.index.max(),exog=exog_forecast)
    fcast_dates['Weekly_Sales'] = fcast_predics

    fcast_dates['SalesType'] = "Forecast (Model 1)"
    byDate['SalesType'] = "Actual"
    byDateFcast = pd.concat([byDate,fcast_dates])
    
    #Evaluate Forecast
    fcast_line = px.line(byDateFcast, x=byDateFcast.index,y='Weekly_Sales', color='SalesType',color_discrete_sequence=walmart_palette)
    fcast_line.update_layout(title={
            'text': "Weekly Sales Forecast (Model 1)",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return models_lines, fcast_line

