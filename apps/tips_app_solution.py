"""Solution: a tips dashboard.  Run with:  streamlit run tips_app_solution.py"""
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Restaurant tips", layout="wide")
st.title("Restaurant tips")


@st.cache_data
def load_tips():
    tips = px.data.tips()
    tips["tip_pct"] = tips.tip / tips.total_bill * 100
    return tips


tips = load_tips()
days = ["Thur", "Fri", "Sat", "Sun"]

with st.sidebar:
    sel_days = st.multiselect("Day", days, default=days)
    meal = st.radio("Meal", ["Both", "Lunch", "Dinner"], horizontal=True)
    size_lo, size_hi = st.slider("Party size", 1, 6, value=(1, 6))

df = tips[tips.day.isin(sel_days) & tips["size"].between(size_lo, size_hi)]
if meal != "Both":
    df = df[df.time == meal]

c1, c2, c3 = st.columns(3)
c1.metric("Bills", len(df))
c2.metric("Mean tip", f"{df.tip_pct.mean():.1f}%" if len(df) else "–")
c3.metric("Mean bill", f"${df.total_bill.mean():.2f}" if len(df) else "–")

tab1, tab2 = st.tabs(["Tips vs bill", "Tip % by day"])
with tab1:
    st.plotly_chart(px.scatter(df, x="total_bill", y="tip", color="day",
                               category_orders={"day": days},
                               hover_data=["size", "time"]), width="stretch")
with tab2:
    st.plotly_chart(px.box(df, x="day", y="tip_pct", points="all",
                           category_orders={"day": days}), width="stretch")

st.dataframe(df, hide_index=True, width="stretch")
st.download_button("Download CSV", df.to_csv(index=False), "tips_filtered.csv", "text/csv")
