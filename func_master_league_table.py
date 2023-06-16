import pandas as pd 

def f_league_table(match_df):
    # create an empty dictionary to store the teams' stats
    team_stats = {}

    # create an empty DataFrame to initalize 
    league_table_df = pd.DataFrame()

    # loop through each match in the input DataFrame
    for i, row in match_df.iterrows():
        # get the home and away team names, and their scores
        home_team = row["home_team_name"]
        away_team = row["away_team_name"]
        home_team_score = row["home_team_goal"]
        away_team_score = row["away_team_goal"]
        season = row["season"]
        league_id = row["league_id"]
        country = row["Country"]

        # get the team indices in the dictionary
        if (home_team, season) not in team_stats:
            team_stats[(home_team, season)] = {"country":country, "league_id":league_id, "MP": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}
        if (away_team, season) not in team_stats:
            team_stats[(away_team, season)] = {"country":country, "league_id":league_id, "MP": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}

        # update the team stats based on the match outcome
        home_team_index = team_stats[(home_team, season)]
        away_team_index = team_stats[(away_team, season)]
        home_team_points = 0
        away_team_points = 0
        if home_team_score > away_team_score:
            home_team_index["W"] += 1
            away_team_index["L"] += 1
            home_team_points = 3
        elif home_team_score < away_team_score:
            home_team_index["L"] += 1
            away_team_index["W"] += 1
            away_team_points = 3
        else:
            home_team_index["D"] += 1
            away_team_index["D"] += 1
            home_team_points = 1
            away_team_points = 1
        home_team_index["MP"] += 1
        away_team_index["MP"] += 1
        home_team_index["GF"] += home_team_score
        away_team_index["GF"] += away_team_score
        home_team_index["GA"] += away_team_score
        away_team_index["GA"] += home_team_score
        home_team_index["GD"] += home_team_score - away_team_score
        away_team_index["GD"] += away_team_score - home_team_score
        home_team_index["Pts"] += home_team_points
        away_team_index["Pts"] += away_team_points

    # create a pandas DataFrame from the team_stats dictionary
        team_stats_list = []
        for key, value in team_stats.items():
            team_name, season = key
            value.update({"team_name": team_name, "season": season})
            team_stats_list.append(value)
        league_table_df = pd.DataFrame(team_stats_list)

        # reset the index and rename columns
        league_table_df = league_table_df.reset_index(drop=True)
        league_table_df = league_table_df.rename(columns={"team_name": "Team", "season": "season"})

    seas = league_table_df.pop('season')
    team = league_table_df.pop('Team')
    league_table_df.insert(0, 'season', seas)
    league_table_df.insert(0, 'Team', team)

    # sort the DataFrame by league_id, season, points, goal difference, and goals scored
    league_table_df = league_table_df.sort_values(["league_id", "season", "Pts", "GD", "GF"], ascending=[False, False, False, False, False])


    #team ranking per season

    #create new column called "rank"
    league_table_df["rank"] = 0

    #group for each league_id and for each season
    grouped = league_table_df.groupby(["league_id","season"])

    # for each league_id and for each season
    for name, group in grouped:
        # sort the group by points, then GD, then GF
        group = group.sort_values(["Pts", "GD", "GF"], ascending=[False, False, False])
        # then assign value to column depending on order
        group["rank"]=range(1,len(group)+1)
        #update master table
        league_table_df.loc[group.index, "rank"] = group["rank"]


    return league_table_df
