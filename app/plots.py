from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Legend
from bokeh.palettes import Category20
import pandas as pd
import itertools

def createBokehPlot(df: pd.DataFrame, x: str, y: str, title: str, plotType="scatter", line=False):
    # Make sure df sorted by expiration date
    df = df.sort_values(by="expiration_date")
    palette = itertools.cycle(Category20[20])
    
    p = figure(title=title, x_axis_label=x, y_axis_label=y, sizing_mode="stretch_both", min_width=400, max_width=1200, min_height=800, max_height=1600)
    legendItems = []
    
    for (name, group) in df.groupby("expiration_date"):
        color = next(palette)
        group = group.sort_values(by=x)
        
        source = ColumnDataSource(group)
        
        if plotType == "scatter":
            renderer = p.scatter(x=x, y=y, source=source, size=10, color=color, alpha=0.5)
            
            if line:
                p.line(x=x, y=y, source=source, line_width=2, color=color, alpha=0.8)
                
        elif plotType == "bar":
            renderer = p.vbar(x=x, top=y, source=source, width=0.5, color=color, alpha=0.5)
            
        legendItems.append((str(name), [renderer]))
    
    legend = Legend(items=legendItems, location=(0, 0))
    p.add_layout(legend, "right")
    p.legend.title = "Expiration Date"
    p.legend.label_text_font_size = "8pt"
    p.legend.spacing = 1
    p.legend.click_policy="mute"
    
    script, div = components(p)
    return script, div