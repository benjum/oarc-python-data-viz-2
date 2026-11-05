import time

import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Gapminder explorer", layout="wide")


@st.cache_data  # runs once; later reruns reuse the result
def load_data():
    time.sleep(2)  # pretend this is a slow database query
    return px.data.gapminder()


gap = load_data()

with st.sidebar:
    st.header("Filters")
    year = st.slider("Year", 1952, 2007, 2007, step=5)
    continents = st.multiselect("Continents", sorted(gap.continent.unique()),
                                default=sorted(gap.continent.unique()))

df = gap[(gap.year == year) & (gap.continent.isin(continents))]
prev = gap[(gap.year == year - 5) & (gap.continent.isin(continents))]

st.title("Gapminder explorer")

# --- A row of headline numbers ------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Countries", len(df))
c2.metric("Median life expectancy", f"{df.lifeExp.median():.1f} yrs",
          delta=f"{df.lifeExp.median() - prev.lifeExp.median():+.1f} vs 5 yrs earlier"
          if len(prev) else None)
c3.metric("Total population", f"{df['pop'].sum() / 1e9:.2f} bn")

# --- Tabs keep the page tidy --------------------------------------------
tab_chart, tab_table = st.tabs(["Chart", "Data"])
with tab_chart:
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                     hover_name="country", log_x=True, size_max=55, range_y=[25, 90])
    st.plotly_chart(fig, width="stretch")
with tab_table:
    st.dataframe(df, hide_index=True, width="stretch")
    st.download_button("Download CSV", df.to_csv(index=False),
                       file_name=f"gapminder_{year}.csv", mime="text/csv")
