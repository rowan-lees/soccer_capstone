import streamlit as st
import pandas as pd
from pandas import Timestamp

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

match_df = pd.DataFrame.from_dict(match_dict, orient='index')

sample_match = match_df.sample(n=1)

st.title("Applying Machine Learning for Soccer Betting Success")

wager_str = st.text_input("Enter your $$ wager")

try:
    wager = float(wager_str)
except ValueError:
    st.error("Please enter a valid numeric wager, dollar sign should be excluded")

st.write("Wager entered:", wager)

st.write(f"{match_df['home_team_name'].values[0]} vs. {match_df['away_team_name'].values[0]}, {match_df['date'].values[0]}")

home_w_button = st.button("Home Team Win")
draw_button = st.button("Draw")
away_w_button = st.button("Away Team Win")

if home_w_button:
    st.write(f'You wagered ${wager} that {match_df['home_team_name'].values[0]} will Win!')
elif away_w_button:
    st.write(f'You wagered ${wager} that {match_df['away_team_name'].values[0]} will Win!')
elif draw_button:
    st.write(f'You wagered ${wager} that the match will end in a Draw!')
else:
    continue

