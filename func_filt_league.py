# this function takes in the season, league, and stage  
# and produces a league table for the current season going into the match

from func_master_league_table import f_league_table

def filtered_table(match_data, season, league, stage):
    filtered = match_data[(match_data["season"] == season) \
                & (match_data["league"] == league) \
                & (match_data["stage"] < stage)]

    filtered_league_table = f_league_table(filtered)

    return filtered_league_table
