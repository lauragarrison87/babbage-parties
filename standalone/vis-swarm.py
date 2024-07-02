import pandas as pd
import altair as alt 

parties = pd.read_csv("parties.csv")

parties_ = parties['date'].str.split(
    '-', 
    expand=True
    ).rename(columns={
        0:'year', 
        1:'month', 
        2:'day'})

# dummy month-year: 01-01
parties_.fillna("01", inplace=True)

parties_["date-imputed"] = parties_["year"] + "-" + parties_["month"] + "-" + parties_["day"]

parties = parties.join(parties_["date-imputed"])

parties["date-imputed"] = pd.to_datetime(parties["date-imputed"], format="%Y-%m-%d")


search_input = alt.selection_point(
    fields=['guest'],
    empty=False,  # Start with no points selected
    bind=alt.binding(
        input='search',
        placeholder="Guest name",
        name='Search ',
    )
)

vis = alt.Chart(parties, title='Babbage Soiree Guests').mark_circle().encode(
    x="yearmonth(date-imputed):T",
    yOffset="jitter:Q",
    color=alt.condition(
        search_input, 
        alt.value("darkorange"),
        alt.value("lightgray")),
    size=alt.condition(
        search_input, 
        alt.value(80),
        alt.value(30)),
    tooltip=["guest", "date-imputed"]
).transform_calculate(
    # Generate Gaussian jitter with a Box-Muller transform
    jitter="sqrt(-2*log(random()))*cos(2*PI*random())"
).add_params(
    search_input
).properties(width=1200,height=300)

vis.save("vis-swarm.html")
