import pandas as pd
import datetime
from datetime import datetime, date, timedelta
import time
import numpy as np
import plotly
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import psycopg2  # required to connect to the PostgreSQL databases

# Establish a connection to the PostgreSQL database
# Replace 'YourNetID' with your actual NetID (inside double quotes)
db_connection = psycopg2.connect(
    host='129.105.248.26',   # IP address of the Postgres database server
    dbname="onmart",         # Name of the database to connect to
    user="esn2981"         # NetID for authentication
)

# Create a cursor object using the established connection
# The cursor is used to execute queries and fetch data from the database
cursor = db_connection.cursor()

pd.set_option('display.max_rows', None)
cursor.execute("SELECT deliveryzipcode, category, SUM(sales) AS total_sales FROM transactions_log GROUP BY category, deliveryzipcode ORDER BY deliveryzipcode DESC")
# cursor.execute("SELECT DISTINCT(deliveryzipcode) FROM transactions_log")
# cursor.execute("SELECT DISTINCT(category) FROM transactions_log")
# Fetch all the rows returned by the executed query.
rows=cursor.fetchall()
columns = [column[0] for column in cursor.description]
results = pd.DataFrame(rows, columns=columns)
results["deliveryzipcode"] = results["deliveryzipcode"].astype(int)

sns.boxplot(
  data=results,
  x="category",
  y="deliveryzipcode",
  hue="total_sales"
)

