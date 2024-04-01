import streamlit as st
import snowflake.connector as snow
import pandas as pd
import matplotlib.pyplot as plt

from datetime import date
from pandas import DataFrame

# Custom
from shared.common import setTitle  

def main():
    setTitle()
    st.header("Exploratory Data Analysis")

    conn = snow.connect(
        user="ANALYTICS_USER_READER",
        password="***",
        account="***",
        warehouse="COMPUTE_WH",
        database="ADVENTUREWORKS_DEMO",
        schema="CONSUMPTION"
    )

    sql = """ 
        SELECT SUM(ORDER_QTY) AS ORDER_QTY,
                PRODUCT_NAME
        FROM ADVENTUREWORKS_DEMO.CONSUMPTION.FACT_SALES S
        INNER JOIN ADVENTUREWORKS_DEMO.CONSUMPTION.DIM_DATE D ON S.D_DIM_ID = D.D_DIM_ID
        WHERE D.ORDER_DATE >= '{}'
        GROUP BY PRODUCT_NAME
    """.format(date.today())
    df = pd.read_sql(sql, con=conn)
    conn.close()

    st.subheader("Today's Purchase")
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(df["ORDER_QTY"], explode=None, labels=df["PRODUCT_NAME"], autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)


if __name__ == "__main__":
    main()
