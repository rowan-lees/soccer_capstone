import streamlit as st
import pandas as pd
from pandas import Timestamp
import random

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit?usp=sharing", "/export?format=csv")
    return pd.read_csv(csv_url)

league_list = load_data(st.secrets["league_list_url"])

match_dict = {2766: {'date': Timestamp('2011-04-24 00:00:00'),
  'home_team_name': 'Bolton Wanderers',
  'away_team_name': 'Arsenal'},
 3442: {'date': Timestamp('2013-02-24 00:00:00'),
  'home_team_name': 'Manchester City',
  'away_team_name': 'Chelsea'},
 2768: {'date': Timestamp('2011-04-23 00:00:00'),
  'home_team_name': 'Chelsea',
  'away_team_name': 'West Ham United'},
 2862: {'date': Timestamp('2010-10-23 00:00:00'),
  'home_team_name': 'West Ham United',
  'away_team_name': 'Newcastle United'},
 2550: {'date': Timestamp('2010-11-28 00:00:00'),
  'home_team_name': 'Tottenham Hotspur',
  'away_team_name': 'Liverpool'},
 3738: {'date': Timestamp('2013-12-28 00:00:00'),
  'home_team_name': 'West Ham United',
  'away_team_name': 'West Bromwich Albion'},
 4652: {'date': Timestamp('2016-04-09 00:00:00'),
  'home_team_name': 'Manchester City',
  'away_team_name': 'West Bromwich Albion'},
 1746: {'date': Timestamp('2008-10-29 00:00:00'),
  'home_team_name': 'Aston Villa',
  'away_team_name': 'Blackburn Rovers'},
 2377: {'date': Timestamp('2010-04-04 00:00:00'),
  'home_team_name': 'Birmingham City',
  'away_team_name': 'Liverpool'},
 3648: {'date': Timestamp('2013-11-02 00:00:00'),
  'home_team_name': 'West Ham United',
  'away_team_name': 'Aston Villa'}}

# league_list = ['ALL',
#   'Belgium Pro League',
#  'England Premier League',
#  'France Ligue 1',
#  'Germany Bundesliga',
#  'Italy Serie A',
#  'Netherlands Eredivisie',
#  'Portugal Primeira Liga',
#  'Scotland Premier League',
#  'Spain LaLiga',
#  'Switzerland Super League']



season_list = ['ALL',
 '2008/2009',
 '2009/2010',
 '2010/2011',
 '2011/2012',
 '2012/2013',
 '2013/2014',
 '2014/2015',
 '2015/2016']

st.title("Applying Machine Learning for Soccer Betting Success")

league_selection = st.selectbox("Select League",league_list)
season_selection = st.selectbox("Select Season",season_list)


def generate_random_match():
    match_id = random.choice(list(match_dict.keys()))
    match_info = match_dict[match_id]
    match_df = pd.DataFrame.from_dict({match_id:match_info}, orient='index')
    return match_df

match_generated = False
sample_match = None

# Generate a new match
if st.button("Generate New Match"):
    sample_match = generate_random_match()
    match_generated = True

wager_str = st.text_input("Enter your $$ wager")

try:
    wager = float(wager_str)
except ValueError:
    st.warning("Please enter a valid wager (e.g. 100 or 55.55), please exclude the dollar sign")

st.write("Wager entered:", wager_str)

if match_generated:
    # Display the match information
    st.write(f"{sample_match['home_team_name'].values[0]} vs. {sample_match['away_team_name'].values[0]}")
    st.write(f"Date: {sample_match['date'].dt.strftime('%d-%m-%Y')}")

    # Get the user's bet
    home_w_button = st.button("Home Team Win")
    draw_button = st.button("Draw")
    away_w_button = st.button("Away Team Win")

    if home_w_button:
        st.write(f"You wagered ${wager} that {sample_match['home_team_name'].values[0]} will Win!")
    elif away_w_button:
        st.write(f"You wagered ${wager} that {sample_match['away_team_name'].values[0]} will Win!")
    elif draw_button:
        st.write(f"You wagered ${wager} that the match will end in a Draw!")
    else:
        st.write("Please make a selection.")
else:
    st.write("Please generate a match.") 

