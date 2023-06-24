import streamlit as st
import pandas as pd
from pandas import Timestamp
import random
from func_filt_league import filtered_table
import graph_funcs as gf
import numpy as np
from joblib import load
import requests
from io import BytesIO
from xgboost import XGBClassifier

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
# response_pca =requests.get(st.secrets["X_test_PCA_url"])
# response_xgb =requests.get(st.secrets['XGBOOST_grid_s_url'])
# joblib_file_pca = BytesIO(response_pca.content)
# joblib_file_xgb = BytesIO(response_xgb.content)
X_test_PCA = load("Models/X_test_PCA.joblib")
XGBOOST_grid_s = load("Models/XGBOOST_grid_s.joblib")
y_test  = load("Models/y_test.joblib") 

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
    samp_match_home_res = sample['home_result'].values[0]
    samp_h_bet_odds = sample['h_avg_odds'].values[0]
    samp_a_bet_odds = sample['a_avg_odds'].values[0]
    samp_d_bet_odds = sample['d_avg_odds'].values[0]
    home_team_short_name = sample['home_team_short_name'].values[0]
    away_team_short_name = sample['away_team_short_name'].values[0]
    home_team_goal = sample['home_team_goal'].values[0]
    away_team_goal = sample['away_team_goal'].values[0]
    match_api_id = sample['match_api_id'].values[0]

    # Check if any of the odds values are NaN, and if so, regenerate the sample match
    if pd.isna(samp_h_bet_odds) or pd.isna(samp_a_bet_odds) or pd.isna(samp_d_bet_odds):
        return generate_sample_match(test_matches, Country_league_flag)
    
    return samp_season, samp_league, samp_country, samp_stage, samp_h_team, samp_a_team, flag_url, samp_match_home_res, samp_h_bet_odds, samp_a_bet_odds, samp_d_bet_odds, \
        home_team_short_name, away_team_short_name, home_team_goal, away_team_goal, match_api_id


# Check if the match data is already stored in session state
if 'match_data' not in st.session_state or st.button("Next Match", key="next_match_button"):
    # Generate the sample match data and store it in session state
    (samp_season, samp_league, samp_country, samp_stage, samp_h_team, samp_a_team, flag_url, samp_match_home_res, samp_h_bet_odds, samp_a_bet_odds, \
     samp_d_bet_odds, home_team_short_name, away_team_short_name, home_team_goal, away_team_goal, match_api_id) = generate_sample_match(test_matches, Country_league_flag)
    st.session_state.match_data = {
                'season': samp_season,
                'league': samp_league,
                'country': samp_country,
                'stage': samp_stage,
                'home_team': samp_h_team,
                'away_team': samp_a_team,
                'flag_url': flag_url,
                'samp_match_home_res': samp_match_home_res,
                'samp_h_bet_odds': samp_h_bet_odds,
                "samp_a_bet_odds": samp_a_bet_odds,
                'samp_d_bet_odds':samp_d_bet_odds,
                'home_team_short_name':home_team_short_name,
                'away_team_short_name':away_team_short_name,
                'home_team_goal':home_team_goal,
                'away_team_goal':away_team_goal,
                'match_api_id': match_api_id
    }

# Retrieve the match data from session state
samp_season = st.session_state.match_data['season']
samp_league = st.session_state.match_data['league']
samp_country = st.session_state.match_data['country']
samp_stage = st.session_state.match_data['stage']
samp_h_team = st.session_state.match_data['home_team']
samp_a_team = st.session_state.match_data['away_team']
flag_url = st.session_state.match_data['flag_url']
samp_match_home_res = st.session_state.match_data['samp_match_home_res']
samp_h_bet_odds = st.session_state.match_data['samp_h_bet_odds']
samp_a_bet_odds = st.session_state.match_data['samp_a_bet_odds']
samp_d_bet_odds = st.session_state.match_data['samp_d_bet_odds']
home_team_short_name = st.session_state.match_data['home_team_short_name']
away_team_short_name = st.session_state.match_data['away_team_short_name']
home_team_goal = st.session_state.match_data['home_team_goal']
away_team_goal = st.session_state.match_data['away_team_goal']
match_api_id = st.session_state.match_data['match_api_id']

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
    ][['stage',
       'home_team_name',
       'away_team_name',
       'home_result',
       'home_team_goal',
       'away_team_goal',
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
st.markdown(f'<h1 style="text-align: center; color: white; line-height: 1.5;"><u>Pre-Match Bookmaker Odds</u></h1>', unsafe_allow_html=True)

st.markdown(
    f'<h3 style="text-align: center; color: #2C74D3; line-height: 0.8;">{samp_h_team} WIN&nbsp;&nbsp;&nbsp; <u>{round(samp_h_bet_odds,1)} : 1</u></h3>', 
    unsafe_allow_html=True
)
st.markdown(
    f'<h3 style="text-align: center; color: yellow; line-height: 0.8;">DRAW&nbsp;&nbsp;&nbsp; <u>{round(samp_d_bet_odds,1)} : 1</u></h3>', 
    unsafe_allow_html=True
)
st.markdown(
    f'<h3 style="text-align: center; color: red; line-height: 0.8;">{samp_a_team} WIN&nbsp;&nbsp;&nbsp; <u>{round(samp_a_bet_odds,1)} : 1</u></h3>', 
    unsafe_allow_html=True
)



st.markdown(f'<h1 style="text-align: center; color: white; line-height: 1.5;"><u>ML Model Prediction</u></h1>', unsafe_allow_html=True)

def EV(prob, odds):
    '''
    Function that calculates the expected value of a bet, based on the outcome probability and the bookmaker odds for being correct
    probability should be a fraction
    '''
    if isinstance(odds, set):
        odds = list(odds)[0]

    if isinstance(prob, set):
        prob = list(prob)[0]

    ev = (prob * (odds - 1)) - (1 - prob)
    return ev


example_idx = y_test.index.get_loc(match_api_id)
   
example_x = X_test_PCA[example_idx]
example_y = y_test.iloc[example_idx]



prediction = XGBOOST_grid_s.predict([example_x])
prediction_prob = XGBOOST_grid_s.predict_proba([example_x])

# st.markdown(f"Probabilities: {prediction_prob}")
prediction_scalar = prediction.item()  # Convert prediction to a scalar value
prediction_labels = {0: "Away Win", 1: "Draw", 2: "Home Win"}
prediction_text = prediction_labels[prediction_scalar]
st.markdown(f"Model prediction: {prediction_text}")
# st.markdown(f"Model prediction: {prediction}")
# st.markdown(f"True label: {example_y}"a)

EV_h_win = round(EV(prediction_prob[0][2], {samp_h_bet_odds}),3)
EV_d_win =round(EV(prediction_prob[0][1], {samp_d_bet_odds}),3)
EV_a_win =round(EV(prediction_prob[0][0], {samp_a_bet_odds}),3)

# st.markdown(f'Expected Value of Home Win {round(EV(prediction_prob[0][2], {samp_h_bet_odds}),3)}')
# st.markdown(f'Expected Value of Draw {round(EV(prediction_prob[0][1], {samp_d_bet_odds}),3)}')
# st.markdown(f'Expected Value of Away Win {round(EV(prediction_prob[0][0], {samp_a_bet_odds}),3)}')

if EV_h_win > 0:
    st.write(f"Expected Value of Home Win: <span style='color:green'>{EV_h_win}</span>", unsafe_allow_html=True)
else:
    st.write(f"Expected Value of Home Win: <span style='color:red'>{EV_h_win}</span>", unsafe_allow_html=True)

if EV_d_win > 0:
    st.write(f"Expected Value of Draw: <span style='color:green'>{EV_d_win}</span>", unsafe_allow_html=True)
else:
    st.write(f"Expected Value of Draw: <span style='color:red'>{EV_d_win}</span>", unsafe_allow_html=True)

if EV_a_win > 0:
    st.write(f"Expected Value of Away Win: <span style='color:green'>{EV_a_win}</span>", unsafe_allow_html=True)
else:
    st.write(f"Expected Value of Away Win: <span style='color:red'>{EV_a_win}</span>", unsafe_allow_html=True)

#betting functionality

st.markdown(f'<br><h1 style="text-align: center; color: white; line-height: 0.8;"><u>Betting</u></h1>', unsafe_allow_html=True)

# Get the user's wager input
wager_str = st.text_input("Enter your wager:")



if wager_str:
    try:
        wager = float(wager_str)
        st.session_state.wager = wager

        # Perform the calculation on the betting outcome using the stored match data and the wager
        # Display the result to the user
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Choose Match Outcome:")
        # Code for calculating the betting outcome

        # Create buttons for the betting options
        result = None
        if st.button(f"Home Win (odds: {round(samp_h_bet_odds,1)} : 1)"):
            result = "home_win"
        if st.button(f"Draw (odds: {round(samp_d_bet_odds,1)} : 1)"):
            result = "draw"
        if st.button(f"Away Win (odds: {round(samp_a_bet_odds,1)} : 1)"):
            result = "away_win"

        st.markdown("<br>", unsafe_allow_html=True)

        if result:
            match_result = samp_match_home_res
            winnings = 0
            ev_winnings = 0
            pred_winnings = 0


            if match_result == "Win":
                if (EV_h_win > EV_d_win) & (EV_h_win > EV_a_win):
                    ev_winnings = (samp_h_bet_odds * wager) - wager
                else:
                    ev_winnings = -wager
            elif match_result == "Draw":
                if (EV_d_win > EV_a_win) & (EV_d_win > EV_h_win):
                    ev_winnings = (samp_d_bet_odds * wager) - wager
                else:
                    ev_winnings = -wager
            elif match_result == "Loss":
                if (EV_a_win > EV_d_win) & (EV_a_win > EV_h_win):
                    ev_winnings = (samp_a_bet_odds * wager) - wager
                else:
                    ev_winnings = -wager


            if match_result == "Win":
                if (prediction_prob[0][2] > prediction_prob[0][1]) & (prediction_prob[0][2] > prediction_prob[0][0]):
                    pred_winnings = (samp_h_bet_odds * wager) - wager
                else:
                    pred_winnings = -wager
            elif match_result == "Draw":
                if (prediction_prob[0][1] > prediction_prob[0][0]) & (prediction_prob[0][1] > prediction_prob[0][2]):
                    pred_winnings = (samp_d_bet_odds * wager) - wager
                else:
                    pred_winnings = -wager
            elif match_result == "Loss":
                if (prediction_prob[0][0] > prediction_prob[0][1]) & (prediction_prob[0][0] > prediction_prob[0][2]):
                    pred_winnings = (samp_a_bet_odds * wager) - wager
                else:
                    pred_winnings = -wager



            if result == "home_win":
                if match_result == "Win":
                    winnings = (samp_h_bet_odds * wager) - wager
                    st.write(f"Match Result:&nbsp; Home Win &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")
                elif match_result == "Draw":
                    winnings = -wager
                    st.write(f"Match Result:&nbsp; Draw &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")
                elif match_result == "Loss":
                    winnings = -wager
                    st.write(f"Match Result:&nbsp; Away Win &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")
            elif result == "draw":
                if match_result == "Draw":
                    winnings = (samp_d_bet_odds * wager) - wager
                    st.write(f"Match Result:&nbsp; Draw &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")
                elif match_result == "Win":
                    winnings = -wager
                    st.write(f"Match Result:&nbsp; Home Win &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")
                elif match_result == "Loss":
                    winnings = -wager
                    st.write(f"Match Result:&nbsp; Away Win &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")
            elif result == "away_win":
                if match_result == "Loss":
                    winnings = (samp_a_bet_odds * wager) - wager
                    st.write(f"Match Result:&nbsp; Away Win &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")
                elif match_result == "Win":
                    winnings = -wager
                    st.write(f"Match Result:&nbsp; Home Win &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")
                elif match_result == "Draw":
                    winnings = -wager
                    st.write(f"Match Result:&nbsp; Draw &nbsp;&nbsp;{home_team_short_name} {home_team_goal}:{away_team_goal} {away_team_short_name}")


            if winnings != 0:
                if winnings > 0:
                    st.write(f"Winnings: <span style='color:green'>${round(winnings,2)}</span>", unsafe_allow_html=True)
                else:
                    st.write(f"Winnings: <span style='color:red'>${round(winnings,2)}</span>", unsafe_allow_html=True)


                # Update the running total in session_state
                if 'running_total' not in st.session_state and 'EV_bet_running_total' not in st.session_state and 'model_pred_running_total' not in st.session_state:
                    st.session_state.running_total = 0
                    st.session_state.EV_bet_running_total = 0
                    st.session_state.model_pred_running_total = 0

                st.session_state.running_total += winnings
                if st.session_state.running_total > 0:
                    st.write(f"Running Total: <span style='color:green'>${round(st.session_state.running_total,2)}</span>", unsafe_allow_html=True)
                else:
                    st.write(f"Running Total: <span style='color:red'>${round(st.session_state.running_total,2)}</span>", unsafe_allow_html=True)

                st.session_state.EV_bet_running_total += ev_winnings
                if st.session_state.EV_bet_running_total > 0:
                    st.write(f"Expected Value Running Total: <span style='color:green'>${round(st.session_state.EV_bet_running_total,2)}</span>", unsafe_allow_html=True)
                else:
                    st.write(f"Expected Value Running Total: <span style='color:red'>${round(st.session_state.EV_bet_running_total,2)}</span>", unsafe_allow_html=True)


                # st.session_state.model_pred_running_total += pred_winnings
                # if st.session_state.model_pred_running_total > 0:
                #     st.write(f"Model Prediction Running Total: <span style='color:green'>${round(st.session_state.model_pred_running_total,2)}</span>", unsafe_allow_html=True)
                # else:
                #     st.write(f"Model Prediction Running Total: <span style='color:red'>${round(st.session_state.model_pred_running_total,2)}</span>", unsafe_allow_html=True)

                st.session_state.model_pred_running_total += pred_winnings
                if st.session_state.model_pred_running_total > 0:
                    st.write(f"Model Prediction Running Total: <span style='color:green; font-size: 18px'>${round(st.session_state.model_pred_running_total,2)}<span style='font-size: 12px'>({round(pred_winnings,2)})</span></span>", unsafe_allow_html=True)
                else:
                    st.write(f"Model Prediction Running Total: <span style='color:red; font-size: 18px'>${round(st.session_state.model_pred_running_total,2)}<span style='font-size: 12px'>({round(pred_winnings,2)})</span></span>", unsafe_allow_html=True)

    except ValueError:
        st.warning("Please enter a valid wager (e.g. 100 or 55.55), excluding the dollar sign.")


#markdown for league table
st.markdown(f'<br><h1 style="text-align: center; color: white; line-height: 0.8;"><u>Pre-Match Statistics</u></h1>', unsafe_allow_html=True)

#Statistical Plots
st.write(f"Current League Table")
st.dataframe(current_table)
st.write(f"{samp_h_team} Last 5 Matches")
st.dataframe(home_t.tail(5))
st.write(f"{samp_a_team} Last 5 Matches")
st.dataframe(away_t.tail(5))
st.set_option('deprecation.showPyplotGlobalUse', False)
fig = gf.five_match_line_plt(match_data,samp_league, samp_season, samp_stage,samp_h_team,samp_a_team)   #match_data, league, season, stage, h_team, a_team

st.pyplot(fig)


