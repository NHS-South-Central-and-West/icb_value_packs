import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import streamlit as st
import altair as alt

path = './working_data'

# Import data allowing wildcard patterns

all_agg_traffic_pattern = f'{path}/all_agg_traffic_*.csv'
all_last90_pattern = f'{path}/all_last90_*.csv'
all_popular_content_pattern = f'{path}/all_popular_content_*.csv'

# not currently used
# all_usage_by_time_pattern = f'{path}/all_usage_by_time_*.csv'

all_agg_traffic_files = glob.glob(all_agg_traffic_pattern)
all_last90_files = glob.glob(all_last90_pattern)
all_popular_content_files = glob.glob(all_popular_content_pattern)

# not currently used
# all_usage_by_time_files = glob.glob(all_usage_by_time_pattern)

df_all_agg_traffic = pd.concat([pd.read_csv(file) for file in all_agg_traffic_files], ignore_index=True)
df_all_last90 = pd.concat([pd.read_csv(file) for file in all_last90_files], ignore_index=True)
df_all_popular_content = pd.concat([pd.read_csv(file) for file in all_popular_content_files], ignore_index=True)

# not currently used
# df_all_usage_by_time = pd.concat([pd.read_csv(file) for file in all_usage_by_time_files], ignore_index=True)

# ICB List

icbs = ['BOB',
        'Frimley',
        'HIOW',
        'Somerset',
        'Sussex'
        ]

###################### STREAMLIT APP ######################

st.set_page_config(
        page_title="Value Packs: Local Report Usage", page_icon=":chart_with_upwards_trend:",
        layout='wide'
    )

# this section contains HTML that fixes the sidebar width at 300px.
st.markdown(
    """
    <style>
    /* Adjust the sidebar width */
    [data-testid="stSidebar"] {
        min-width: 300px; /* Set your desired width */
        max-width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True # this is required to be able to use custom HTML and CSS in the app
)

def main():

    # title row
    t1,t2 = st.columns((0.07,1))

    t1.image('images/SCW-Logo-WHITE.png', width = 120)
    t2.title("Value Packs: Local Report Usage")

    # contact details
    c = st.columns(1)[0]
    c.markdown("**Product Owner:** Hazera Forth hazera.forth@nhs.net | **Technical Queries:** scwcsu.analytics.specialist@nhs.net")

        # create some space between the contact details and the first chart:

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("Select ICB")
        selected_icb = st.selectbox(
            options = icbs,
            label = 'ICB'
            
        )

    # filter the data based on the filter selections    

    df_all_agg_traffic_filtered = df_all_agg_traffic[df_all_agg_traffic['ICB'] == selected_icb]
    df_all_last90_filtered = df_all_last90[df_all_last90['ICB'] == selected_icb]
    df_all_popular_content_filtered = df_all_popular_content[df_all_popular_content['ICB'] == selected_icb]

    # not currently used
    # df_all_usage_by_time_filtered = df_all_usage_by_time[df_all_usage_by_time['ICB'] == selected_icb]

    chart_column = st.columns(1)[0]

    with chart_column:
  
        df_all_last90_filtered['Date'] = pd.to_datetime(df_all_last90_filtered['Date'])

        # Bar plot for Unique viewers (Top subplot)
        unique_viewers_chart = alt.Chart(df_all_last90_filtered).mark_bar(
            color='#1C355E',
            opacity=0.8
        ).encode(
            x=alt.X('Date:T', axis=alt.Axis(labelAngle=90, title=None, tickCount='day', format='%Y-%m-%d')),
            y=alt.Y('Unique viewers:Q', axis=alt.Axis(title='Unique viewers', titleColor='#1C355E')),
            tooltip=['Date:T', 'Unique viewers:Q']
        ).properties(
            title=f'Site visits and unique viewers for {selected_icb} ICB',
            width=1380,
            height=200
        )

        # Bar plot for Site visits (Bottom subplot)
        site_visits_chart = alt.Chart(df_all_last90_filtered).mark_bar(
            color='#AE2573',
            opacity=0.8
        ).encode(
            x=alt.X('Date:T', axis=alt.Axis(labelAngle=90, title=None, tickCount='day', format='%Y-%m-%d')),
            y=alt.Y('Site visits:Q', axis=alt.Axis(title='Site visits', titleColor='#AE2573')),
            tooltip=['Date:T', 'Site visits:Q']
        ).properties(
            width=1380,
            height=200
        )

        # Concatenate the two charts vertically
        last90_chart = alt.vconcat(
            unique_viewers_chart,
            site_visits_chart
        ).resolve_scale(
            x='shared'  # Share the x-axis between the two charts
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        )

        # display the chart
        st.altair_chart(last90_chart, use_container_width= False)

    tab1, tab2 = st.columns((0.5,1))

    with tab1:
        st.subheader("Activity Summary", divider="grey")
        st.write(df_all_agg_traffic_filtered.drop(columns=["ICB"]).reset_index(drop=True))
 
    with tab2:

        columns_to_format = ["Last 7 days unique viewers", "Last 7 days visits"]
        df_all_popular_content_display = df_all_popular_content_filtered.drop(columns=["ICB"])

        def pretty_table(styler):
            #styler.hide()                   # doesn't seem to work in Streamlit
            # styler.hide(subset=["ICB"], axis="columns")
            styler.background_gradient(axis=None, 
                                       vmin=df_all_popular_content_display[columns_to_format].min().min(), 
                                       vmax=df_all_popular_content_display[columns_to_format].max().max(),
                                       cmap="YlGnBu")
            return styler

        st.subheader("Popular content", divider="grey")
        st.write(df_all_popular_content_display.reset_index(drop=True).style.pipe(pretty_table))


if __name__ == "__main__":

    main()