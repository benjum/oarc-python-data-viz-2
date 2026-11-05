"""Exercise: a tips dashboard.  Run with:  streamlit run tips_app.py

Work through the TODOs. Save the file and the browser offers to rerun
(click "Always rerun" so it updates on every save).
"""
import plotly.express as px
import streamlit as st

st.title("Restaurant tips")

# TODO 1: wrap the data loading in a function decorated with @st.cache_data
tips = px.data.tips()
tips["tip_pct"] = tips.tip / tips.total_bill * 100

# TODO 2: in the sidebar, add
#   - a multiselect for `day` (default: all days)
#   - a radio button for `time` with options "Both", "Lunch", "Dinner"
#   - a slider for party size, as a range (hint: value=(1, 6) gives a range slider)
df = tips

# TODO 3: show three st.metric values in st.columns:
#   number of bills, mean tip %, mean bill

# TODO 4: a Plotly scatter of total_bill vs tip, colored by day
st.dataframe(df)

# TODO 5 (stretch): add a download button for the filtered data,
#   and a second tab with a box plot of tip_pct by day
