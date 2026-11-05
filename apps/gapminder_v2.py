import plotly.express as px
import streamlit as st

st.title("Wealth and health of nations")

gap = px.data.gapminder()

# --- Widgets: each returns its current value ---------------------------
with st.sidebar:
    st.header("Filters")
    year = st.slider("Year", min_value=1952, max_value=2007, value=2007, step=5)
    continents = st.multiselect("Continents", sorted(gap.continent.unique()),
                                default=sorted(gap.continent.unique()))
    log_x = st.checkbox("Log scale for GDP", value=True)

# --- Plain pandas filtering --------------------------------------------
df = gap[(gap.year == year) & (gap.continent.isin(continents))]

fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                 hover_name="country", log_x=log_x, size_max=55,
                 range_y=[25, 90])
st.plotly_chart(fig)

st.write(f"Showing {len(df)} countries in {year}.")
