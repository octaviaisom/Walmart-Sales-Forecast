
import pandas as pd
import datetime

sales_csv = pd.read_csv("data\sales.csv")
sales = pd.DataFrame(sales_csv)
sales = sales.iloc[:500]
sales.Date = pd.to_datetime(sales.Date)

holiday_csv = pd.read_csv("data\holidays.csv")
holidays = pd.DataFrame(holiday_csv)
holidays.Date = pd.to_datetime(holidays.Date)

#holiday merge and loop
holidates = holidays.Date
total_rows = len(sales)
i=0
for index, row in sales.iterrows():
    wk_end = row['Date']
    six_days = datetime.timedelta(days = 6)
    wk_start = (wk_end - six_days)
    week = pd.date_range(start=wk_start,end=wk_end)

    for index, row in holidays.iterrows():
        holidate = row['Date']

        try:   
            sales.loc[index, "IsHoliday"] = wk_start <= holidate <= wk_end
            print(f"{i}")
            break

        except:
            print(f"Unable to assign value, skipping...")

    i = 1+i
sales.to_csv("data/sales_updated.csv")