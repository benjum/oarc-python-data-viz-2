import plotly.express as px
import streamlit as st

st.title("Wealth and health of nations")

gap = px.data.gapminder()
g07 = gap.query("year == 2007")

fig = px.scatter(g07, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=55)
st.plotly_chart(fig)

st.dataframe(g07)
