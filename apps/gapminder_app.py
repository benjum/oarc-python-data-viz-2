"""Gapminder explorer: a complete Streamlit example.

Run with:  streamlit run gapminder_app.py
"""
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Gapminder explorer", layout="wide")


@st.cache_data
def load_data():
    return px.data.gapminder()


gap = load_data()

with st.sidebar:
    st.header("Filters")
    year = st.slider("Year", 1952, 2007, 2007, step=5)
    continents = st.multiselect("Continents", sorted(gap.continent.unique()),
                                default=sorted(gap.continent.unique()))

df = gap[(gap.year == year) & (gap.continent.isin(continents))]

st.title("Gapminder explorer")
st.caption("Select countries on the scatter plot (click, or box/lasso select) "
           "to see their history on the right.")

c1, c2, c3 = st.columns(3)
c1.metric("Countries", len(df))
c2.metric("Median life expectancy", f"{df.lifeExp.median():.1f} yrs" if len(df) else "–")
c3.metric("Total population", f"{df['pop'].sum() / 1e9:.2f} bn")

left, right = st.columns([3, 2])

with left:
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                     hover_name="country", custom_data=["country"],
                     log_x=True, size_max=55, range_y=[25, 90],
                     labels={"gdpPercap": "GDP per capita", "lifeExp": "Life expectancy"})
    # on_select="rerun": selecting points reruns the script and returns the selection
    event = st.plotly_chart(fig, width="stretch", key="scatter",
                            on_select="rerun", selection_mode=("points", "box", "lasso"))

selected = [p["customdata"][0] for p in event.selection.points]

with right:
    if selected:
        hist = gap[gap.country.isin(selected)]
        st.plotly_chart(px.line(hist, x="year", y="lifeExp", color="country",
                                markers=True, range_y=[25, 90],
                                title="Life expectancy over time"),
                        width="stretch")
    else:
        st.info("Nothing selected yet: click or lasso some countries.")

with st.expander("Show data"):
    shown = df[df.country.isin(selected)] if selected else df
    st.dataframe(shown, hide_index=True, width="stretch")
    st.download_button("Download CSV", shown.to_csv(index=False),
                       file_name=f"gapminder_{year}.csv", mime="text/csv")
