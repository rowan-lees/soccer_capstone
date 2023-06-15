import streamlit as st
import pandas as pd
from pandas import Timestamp
import random
from func_filt_league import filtered_table
import graph_funcs as gf
import numpy as np

st.set_page_config(page_title="Betting", page_icon="📈")

st.title("Applying Machine Learning for Soccer Betting Success")

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit?usp=sharing", "/export?format=csv")
    return pd.read_csv(csv_url)

Country_league_flag = load_data(st.secrets["Country_league_flag_url"])
league_table = load_data(st.secrets["league_table_url"])
test_matches = load_data(st.secrets["Test_matches_url"])
match_data = load_data(st.secrets["match_data_url"])

#variables
sample = test_matches.sample(1)
samp_season = sample['season'].values[0]
samp_league = sample['League'].values[0]
samp_stage = sample['stage'].values[0]
samp_country = sample['Country'].values[0]
samp_h_team = sample["home_team_name"].values[0]
samp_a_team = sample["away_team_name"].values[0]
flag_url = Country_league_flag[Country_league_flag['League'] == (samp_league)]['URL'].values[0]

# filt_leag_8_9_England = league_table[(league_table['country']=='England') & (league_table['season']=='2009/2010')]
# st.dataframe(filt_leag_8_9_England)\

# st.markdown(f'<h1 style="text-align: center; color: #2C74D3;">{samp_h_team}  vs  {samp_a_team}</h1>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center; color: #2C74D3;">{samp_h_team}</h1>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center; color: white;">vs</h1>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center; color: red;">{samp_a_team}</h1>', unsafe_allow_html=True)

st.image(flag_url, width=50)
st.write(f"League: {samp_league}")
st.write(f"Season: {samp_season}")
st.write(f"Match Day #{samp_stage}")


season_list = ['ALL',
 '2008/2009',
 '2009/2010',
 '2010/2011',
 '2011/2012',
 '2012/2013',
 '2013/2014',
 '2014/2015',
 '2015/2016']




current_table = filtered_table(match_data, samp_season, samp_league, samp_stage)

home_t = match_data[
    (match_data['season']==samp_season) & 
    (match_data['League']==samp_league) & 
    (match_data['stage'] < samp_stage) & 
    ((match_data['home_team_name']==samp_h_team) | (match_data['away_team_name']==samp_h_team))
    ][['League',
        'season',
       'stage',
       'date',
       'home_team_name',
       'away_team_name',
       'home_team_goal',
       'away_team_goal',
       'home_result',
       'h_five_form_pts',
       'a_five_form_pts']]

away_t = match_data[
    (match_data['season']==samp_season) & 
    (match_data['League']==samp_league) & 
    (match_data['stage'] < samp_stage) & 
    ((match_data['home_team_name']==samp_a_team) | (match_data['away_team_name']==samp_a_team))
    ][['stage',
       'home_team_name',
       'away_team_name',
       'home_result',
       'home_team_goal',
       'away_team_goal',
        'h_five_form_pts',
       'a_five_form_pts']]


#betting functionality

wager_str = st.text_input("Enter your $$ wager")

try:
    wager = float(wager_str)
except ValueError:
    st.warning("Please enter a valid wager (e.g. 100 or 55.55), please exclude the dollar sign")

st.write("Wager entered:", wager_str)

#Statistical Plots

st.dataframe(current_table)
st.write(f"{samp_h_team} Last 5 Matches this season")
st.dataframe(home_t.tail(5))
st.write(f"{samp_a_team} Last 5 Matches this season")
st.dataframe(away_t.tail(5))
st.set_option('deprecation.showPyplotGlobalUse', False)
fig = gf.five_match_line_plt(match_data,samp_league, samp_season, samp_stage,samp_h_team,samp_a_team)   #match_data, league, season, stage, h_team, a_team

st.pyplot(fig)

# league_selection = st.selectbox("Select League",league_list)
# season_selection = st.selectbox("Select Season",season_list)

# def generate_random_match():
#     match_id = random.choice(list(match_dict.keys()))
#     match_info = match_dict[match_id]
#     match_df = pd.DataFrame.from_dict({match_id:match_info}, orient='index')
#     return match_df

# match_generated = False
# sample_match = None

# # Generate a new match
# if st.button("Generate New Match"):
#     sample_match = generate_random_match()
#     match_generated = True


# if match_generated:
#     # Display the match information
#     st.write(f"{sample_match['home_team_name'].values[0]} vs. {sample_match['away_team_name'].values[0]}")
#     st.write(f"Date: {sample_match['date'].dt.strftime('%d-%m-%Y')}")

#     # Get the user's bet
#     home_w_button = st.button("Home Team Win")
#     draw_button = st.button("Draw")
#     away_w_button = st.button("Away Team Win")

#     if home_w_button:
#         st.write(f"You wagered ${wager} that {sample_match['home_team_name'].values[0]} will Win!")
#     elif away_w_button:
#         st.write(f"You wagered ${wager} that {sample_match['away_team_name'].values[0]} will Win!")
#     elif draw_button:
#         st.write(f"You wagered ${wager} that the match will end in a Draw!")
#     else:
#         st.write("Please make a selection.")
# else:
#     st.write("Please generate a match.") 

