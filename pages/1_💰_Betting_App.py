import streamlit as st
import pandas as pd
from pandas import Timestamp
import random
from func_filt_league import filtered_table
import graph_funcs as gf
import numpy as np

st.set_page_config(page_title="Betting", page_icon="📈")


# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit?usp=sharing", "/export?format=csv")
    return pd.read_csv(csv_url)

#load data
Country_league_flag = load_data(st.secrets["Country_league_flag_url"])
league_table = load_data(st.secrets["league_table_url"])
test_matches = load_data(st.secrets["Test_matches_url"])
match_data = load_data(st.secrets["match_data_url"])

# Define the match data generation function
def generate_sample_match(test_matches, Country_league_flag):
    sample = test_matches.sample(1)
    samp_season = sample['season'].values[0]
    samp_league = sample['League'].values[0]
    samp_stage = sample['stage'].values[0]
    samp_country = sample['Country'].values[0]
    samp_h_team = sample["home_team_name"].values[0]
    samp_a_team = sample["away_team_name"].values[0]
    flag_url = Country_league_flag[Country_league_flag['League'] == (samp_league)]['URL'].values[0]
    
    return samp_season, samp_league, samp_country, samp_stage, samp_h_team, samp_a_team, flag_url


# Check if the match data is already stored in session state
if 'match_data' not in st.session_state:
    # Generate the sample match data and store it in session state
    (samp_season, samp_league, samp_country, samp_stage, samp_h_team, samp_a_team, flag_url) = generate_sample_match(test_matches, Country_league_flag)
    st.session_state.match_data = {
                'season': samp_season,
                'league': samp_league,
                'country': samp_country,
                'stage': samp_stage,
                'home_team': samp_h_team,
                'away_team': samp_a_team,
                'flag_url': flag_url
    }

# Retrieve the match data from session state
samp_season = st.session_state.match_data['season']
samp_league = st.session_state.match_data['league']
samp_country = st.session_state.match_data['country']
samp_stage = st.session_state.match_data['stage']
samp_h_team = st.session_state.match_data['home_team']
samp_a_team = st.session_state.match_data['away_team']
flag_url = st.session_state.match_data['flag_url']


st.markdown(
    f'<div style="display: flex; justify-content: center;">'
    f'<img src="{flag_url}" width="125" />'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<h1 style="text-align: center; color: #2C74D3; line-height: 0.8;">{samp_h_team}</h1>', 
    unsafe_allow_html=True
)
st.markdown(
    f'<h1 style="text-align: center; color: white; line-height: 0.8;">vs</h1>', 
    unsafe_allow_html=True
)
st.markdown(
    f'<h1 style="text-align: center; color: red; line-height: 0.8;">{samp_a_team}</h1>', 
    unsafe_allow_html=True
)

sample_match_data = {
    "League": [samp_league],
    "Season": [samp_season],
    "Match Day": [samp_stage]}

sample_match_data_df = pd.DataFrame(sample_match_data)
sample_match_data_df = sample_match_data_df.rename_axis(index=None)  # Remove the index label
st.table(sample_match_data_df)


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

#odds both model and bookie

#markdown
st.markdown(f'<h3 style="text-align: center; color: white; line-height: 0.8;">Match Odds</h3>', unsafe_allow_html=True)

h_win_odds = 2
h_loss_odds = 1.5
draw_odds = 4

st.markdown(
    f'<h3 style="text-align: center; color: #2C74D3; line-height: 0.8;">{samp_h_team} WIN {h_win_odds}:1</h3>', 
    unsafe_allow_html=True
)
st.markdown(
    f'<h3 style="text-align: center; color: yellow; line-height: 0.8;">DRAW {draw_odds}:1</h3>', 
    unsafe_allow_html=True
)
st.markdown(
    f'<h3 style="text-align: center; color: red; line-height: 0.8;">{samp_a_team} WIN {h_loss_odds}:1</h3>', 
    unsafe_allow_html=True
)


#betting functionality

#markdown
st.markdown(f'<h3 style="text-align: center; color: white; line-height: 0.8;">Betting</h3>', unsafe_allow_html=True)

# Get the user's wager input
wager_str = st.text_input("Enter your wager:")

if wager_str:
    try:
        wager = float(wager_str)
        # Perform the calculation on the betting outcome using the stored match data and the wager
        # Display the result to the user
        st.write("Betting Outcome Calculation:")
        # Code for calculating the betting outcome
        h_winnings = h_win_odds * wager
        d_winnings = draw_odds * wager
        a_winnings = a_win_odds * wager

        st.write(f"Home Win Winnings: ${h_winnings}")
        st.write(f"Draw Winnings: ${d_winnings}")
        st.write(f"Away Win Winnings: ${a_winnings}")

    except ValueError:
        st.warning("Please enter a valid wager (e.g. 100 or 55.55), excluding the dollar sign.")


# with st.form("wager_form"):
#     wager_str = st.text_input("Enter your $$ wager")
#     wager_submit = st.form_submit_button("Submit")

# if wager_submit:
#     try:
#         wager = float(wager_str)
#         st.write("Wager entered:", wager_str)
#         # Perform calculations using the wager amount
#     except ValueError:
#         st.warning("Please enter a valid wager (e.g. 100 or 55.55), please exclude the dollar sign")



#markdown for league table
st.markdown(f'<h3 style="text-align: center; color: white; line-height: 0.8;">Current League Table</h3>', unsafe_allow_html=True)

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

