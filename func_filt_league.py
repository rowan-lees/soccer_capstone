# this function takes in the season, league, and stage  
# and produces a league table for the current season going into the match

from func_master_league_table import f_league_table

def filtered_table(match_data, season, league, stage):
    
    assert isinstance(season, object), "sample Season must be a string"
    assert isinstance(league, object), "sample League must be a string"
    assert stage.dtype == 'int64', "sample Stage must be an integer"
    
    assert match_data["season"].dtype == 'object', "match Season must be a string"
    assert match_data["League"].dtype == 'object', "match League must be a string"
    assert match_data["stage"].dtype == 'int64', "match Stage must be an integer"

    filtered = match_data[(match_data["season"] == season) \
                & (match_data["League"] == league) \
                & (match_data["stage"] < stage)]

    filtered_league_table = f_league_table(filtered)
    filtered_league_table = filtered_league_table.set_index('rank')
    columns_to_drop = ['league_id', 'season', 'country']
    filtered_league_table = filtered_league_table.drop(columns = columns_to_drop)

    return filtered_league_table 
