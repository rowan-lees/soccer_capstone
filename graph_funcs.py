# premier league 5, match form 2008/09
from statsmodels.nonparametric.smoothers_lowess import lowess
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt


def five_match_line_plt(match_data, league, season, stage, h_team, a_team):
    if stage < 5:
        return "No Data as less than 5 games played"
    else:
        current_season = match_data[(match_data['season']==season) & (match_data['League']==league)  & (match_data['stage'] > 5) & (match_data['stage'] < stage)][['stage', 'h_five_form_pts', 'a_five_form_pts','home_team_name','away_team_name']]
        teams = [h_team, a_team]

        home_form = current_season[['stage', 'h_five_form_pts', 'home_team_name']].rename(columns={'h_five_form_pts':'form_pts', 'home_team_name':'team_name'})
        away_form = current_season[['stage', 'a_five_form_pts', 'away_team_name']].rename(columns={'a_five_form_pts':'form_pts', 'away_team_name':'team_name'})

        form_melt = pd.concat([home_form,away_form]).sort_values(by=['team_name', 'stage'])
        form_melt = form_melt[form_melt['team_name'].isin(teams)]
        form_melt['form_avg_pts'] = form_melt['form_pts'] / 5

        plt.figure(figsize=(8,6))
        for team in teams:
            team_data = form_melt[form_melt['team_name'] == team]
            team_data_smooth = sm.nonparametric.lowess(team_data['form_avg_pts'], team_data['stage'],frac=0.2)
            plt.plot(team_data_smooth[:,0], team_data_smooth[:,1], label=team, alpha=0.7)

        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.title("5 Match Form for Home and Away team")
        plt.ylabel("Average Points Accumluted over Past 5 Games")
        plt.xlabel(f"Match Day of {season} Season")
        plt.show()