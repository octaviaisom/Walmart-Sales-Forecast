
import pandas as pd
import datetime

sales_csv = pd.read_csv("data\sales.csv")
sales = pd.DataFrame(sales_csv)
sales.Date = pd.to_datetime(sales.Date)

holiday_csv = pd.read_csv("data\holidays.csv")
holidays = pd.DataFrame(holiday_csv)
holidays.Date = pd.to_datetime(holidays.Date)

#holiday merge and loop
holidates = holidays.Date
total_rows = len(sales)

for index, row in sales.iterrows():
    wk_end = row['Date']
    six_days = datetime.timedelta(days = 6)
    wk_start = (wk_end - six_days)
    week = pd.date_range(start=wk_start,end=wk_end)

    try:   
        sales.loc[index, "IsHoliday"] = f"{bool(set(week) & set(holidates))}"
        print(f"Row {index} of {total_rows}: value assigned")

    except:
        print(f"Row {index} of {total_rows}: unable to assign value, skipping...")

sales.to_csv("data/sales_updated.csv")