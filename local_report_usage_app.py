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
    t2.markdown("**e-mail:** scwcsu.analytics.specialist@nhs.net")

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
            width=1000,
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
            width=1000,
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

    tab1 = st.columns(1)[0]

    with tab1:
        data = df_all_agg_traffic_filtered.reset_index(drop=True).values
        columns = df_all_agg_traffic_filtered.reset_index(drop=True).columns

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.axis('off')

        table = ax.table(cellText=data,
                        colLabels=columns,
                        loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.auto_set_column_width(col=list(range(len(columns))))
        table.scale(1, 1)

        for (row, col), cell in table.get_celld().items():
            if row == 0:  # Header row
                cell.set_facecolor('#1C355E')  # SCW dark blue
                cell.set_text_props(color='#FFFFFF')  # White text

        #fig.tight_layout(rect=[0,0,1,0.75])
        fig.suptitle("Summary Actvivity Table", y=0.85, fontsize= 10)
        st.pyplot(fig, use_container_width= False)

    tab2 = st.columns(1)[0]
    with tab2:
        from matplotlib.cm import ScalarMappable
        from matplotlib.colors import Normalize, to_rgba

        def calculate_brightness(rgba_color):
            r, g, b, _ = rgba_color  # Extract RGB components
            brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
            return brightness
        
        df_all_popular_content_filtered.fillna('-', inplace=True)
        df_all_popular_content_filtered.rename(columns={'Type (Click to view)': 'Type'}, inplace=True)

        # Define columns for conditional formatting
        columns_to_format = ["Last 7 days unique viewers", "Last 7 days visits"]

        # Normalize values for color gradient
        norm = Normalize(vmin=df_all_popular_content_filtered[columns_to_format].min().min(), 
                         vmax=df_all_popular_content_filtered[columns_to_format].max().max())
        cmap = plt.cm.YlGnBu  # Choose a colormap

        # Calculate figure size based on DataFrame size
        num_rows, num_columns = df_all_popular_content_filtered.shape
        fig_width = max(8, num_columns * 1.2)  # Minimum width of 8, scale with columns
        fig_height = max(4, num_rows * 0.25)   # Minimum height of 4, scale with rows

        # Create figure and axis for table
        fig2, ax2 = plt.subplots(figsize=(fig_width, fig_height))
        ax2.axis('off')

        # Create the table
        table2 = ax2.table(cellText=df_all_popular_content_filtered.values, 
                          colLabels=df_all_popular_content_filtered.columns, 
                          loc='center', 
                          cellLoc='center'
                          )
        table2.auto_set_font_size(False)
        table2.set_fontsize(12)
        table2.auto_set_column_width(col=list(range(len(df_all_popular_content_filtered.columns))))
        table2.scale(1.2, 1.2)

        # Apply colour gradient to specific columns
        for (row, col), cell2 in table2.get_celld().items():
            if row > 0:  # Skip the header row
                column_name = df_all_popular_content_filtered.columns[col]
                if column_name in columns_to_format:
                    try:
                        # Get the value and map it to the coloyr range
                        value = df_all_popular_content_filtered.iloc[row - 1, col]
                        if isinstance(value, (int, float)):  # Ensure value is numeric
                            color = cmap(norm(value))  # Get RGBA colour
                            cell2.set_facecolor(color)

                            # Adjust text colour based on brightness
                            brightness = calculate_brightness(to_rgba(color))
                            text_color = '#FFFFFF' if brightness < 0.5 else '#000000'
                            cell2.set_text_props(color=text_color)
                    except Exception:
                        pass  # handle non-numeric cells

        # Customize header row
        for (row, col), cell2 in table2.get_celld().items():
            if row == 0:  # Header row
                cell2.set_facecolor('#1C355E')  # SCW dark blue
                cell2.set_text_props(color='#FFFFFF')  # White text

        fig2.suptitle('Popular Content')

        st.pyplot(fig2, use_container_width= False)


if __name__ == "__main__":

    main()