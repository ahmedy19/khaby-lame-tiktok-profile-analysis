# Import required packages 
import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff



# Load datasets
path = r'datasets/khaby_cleaned_dataset.csv'
df = pd.read_csv(path, low_memory=False)

st.set_page_config(
    page_title="Khaby TikTok Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# dashboard title
st.title("Khaby TikTok Dashboard")
st.markdown("---")


# top-level filters 
year_filter = st.selectbox("Year", pd.unique(df['created_year']))



# creating a single-element container.
placeholder = st.empty()

# dataframe filter 
df = df[df['created_year']==year_filter]


for seconds in range(200):

    # Group the data by duration and calculate the average views
    average_views = df.groupby('duration')['views'].mean().reset_index()
    
    # Sort the data in descending order by average price
    sorted_duration = average_views.sort_values('views', ascending=False)
    
    
    split_hash_df = df.explode('split_hashtags')
    hashtag_views = split_hash_df.groupby('split_hashtags')['views'].sum().reset_index()
    hashtag_views_sorted = hashtag_views.sort_values('views', ascending=False)

    # Select the top 10 most commonly used hashtags
    top_10_hashtags = hashtag_views_sorted.head(10)
    
    df_avg_likes = df.groupby('duration')['likes'].mean().reset_index()
    
    average_views_overtime = df.groupby('created_at')['views'].mean().reset_index()
    sorted_views = average_views_overtime.sort_values('views', ascending=False)

    
    with placeholder.container():
        
        # create two columns for charts 
        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            
            st.markdown("### Insight 1")
            
            fig = px.bar(sorted_duration, x='duration', y='views', color='duration',
                         labels={'duration': 'Video Duration', 'views': 'Average Views'},
                    title='<b>What is the video duration that tends to attract more views?</b>')
            fig.update_layout(xaxis_title='<b>Duration</b>', yaxis_title='<b>Average Views</b>', xaxis_tickangle=-45)
            
            st.write(fig)
            
        
        with fig_col2:
            st.markdown("### Insight 2")
            
            fig = px.bar(top_10_hashtags, x='split_hashtags', y='views', color='split_hashtags', 
             labels={'split_hashtags': 'Hashtag', 'views': 'Total Views'}, 
             title='<b>Which hashtags are most commonly used and do they have a correlation with views?</b>')
            fig.update_layout(xaxis_title='<b>Hashtags</b>', yaxis_title='<b>Total Views</b>')
            
            st.write(fig)
            
        
        with fig_col1:
            
            st.markdown("### Insight 3")
            
            fig = px.bar(df_avg_likes, x='duration', y='likes', color='likes', title='Average Likes by Duration')
            fig.update_layout(xaxis_title='<b>Duration</b>', yaxis_title='<b>Average Likes</b>', xaxis_tickangle=-45,
                              title='<b>What\'s the average likes over durations?</b>')
            
            st.write(fig)
            
        
        with fig_col2:
            st.markdown("### Insight 4")
            
            
            fig = px.line(sorted_views, x='created_at', y="views", color='views', 
             labels={'created_at': 'Posted At', 'views': 'Average Views'}, 
             title='<b>What\'s the average views over time?</b>')
            
            fig.update_layout(xaxis_title='<b>Posted At</b>', yaxis_title='<b>Average Views</b>')
                        
            st.write(fig)
            
            
            
        st.markdown("---")
            
        
        
        st.markdown("### Data")
        st.dataframe(df)
        time.sleep(1)
    