# this function takes in the season, league, and stage  
# and produces a league table for the current season going into the match

from func_master_league_table import f_league_table

def filtered_table(match_data, season, league, stage):
    
    assert isinstance(season, object), "Season must be a string"
    assert isinstance(league, object), "League must be a string"
    assert stage.dtype == 'int64', "Stage must be an integer"
    
    print(match_data["season"].dtype)
    print(match_data["season"].shape)

    filtered = match_data[(match_data["season"] == season) \
                & (match_data["League"] == league) \
                & (match_data["stage"] < stage)]

    filtered_league_table = f_league_table(filtered)

    return filtered_league_table 
