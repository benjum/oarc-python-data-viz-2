"""Five million points with Panel + hvPlot + Datashader.  Run with:  panel serve panel_bigdata_app.py --show"""
import numpy as np
import pandas as pd
import panel as pn
import hvplot.pandas  # noqa: F401

pn.extension()


@pn.cache
def make_data(n=5_000_000, seed=0):
    rng = np.random.default_rng(seed)
    centers = {"A": (-2, -1, 0.6), "B": (1.5, 2, 0.4), "C": (2, -2, 0.9), "D": (0, 0, 2.5)}
    parts = []
    for name, (cx, cy, s) in centers.items():
        k = n // len(centers)
        parts.append(pd.DataFrame({"x": rng.normal(cx, s, k), "y": rng.normal(cy, s, k),
                                   "group": name}))
    df = pd.concat(parts, ignore_index=True)
    df["group"] = df["group"].astype("category")
    return df


df = make_data()

# import datashader as ds
# ds.Canvas(plot_width=650, plot_height=500).points(df, "x", "y")  # triggers the one-time JIT compile

groups = pn.widgets.MultiChoice(name="Groups", options=list("ABCD"), value=list("ABCD"))
norm = pn.widgets.RadioButtonGroup(name="Color scale", options=["eq_hist", "log", "linear"])


def plot(groups, norm):
    d = df[df.group.isin(groups)]
    return d.hvplot.points("x", "y", rasterize=True, cnorm=norm, cmap="viridis",
                           width=650, height=500, colorbar=True,
                           pixel_ratio=1,
                           title=f"{len(d):,} points")


pn.template.FastListTemplate(
    title="Datashader demo",
    sidebar=[groups, "Color normalization", norm],
    main=[pn.bind(plot, groups, norm)],
).servable()
