import numpy as np
import pandas as pd

# Load scraped game data for 2002-2017 seasons
df = pd.read_csv('nfl_scraped.csv')

# Remove all post-season games, format week and set a game id
df = df[df.week != 'Playoffs'].reset_index(drop=True)
df['week'] = df['week'].str.split(' ').str[-1].astype(int)
df = df.sort_values(by=['year', 'week', 'h_team']).reset_index(drop=True)
df['id'] = df.index + 1

# Update temperature and set indoor game temperature to 70
indoor = ['sportturf', 'fieldturf', 'astroturf', 'grass', 'matrixturf', 'a_turf', 'astroplay']
df['temp'] = df['temp'].str.strip()
df['temp'] = pd.to_numeric(np.array(np.where(df['temp'].isin(indoor), 70, df['temp'])))

# Convert time of possession to values in terms of minutes
df['h_poss'] = pd.to_datetime(df['h_poss'], format = '%M:%S')
df['a_poss'] = pd.to_datetime(df['a_poss'], format = '%M:%S')
df['h_poss'] = df['h_poss'].dt.minute + df['h_poss'].dt.second/60
df['a_poss'] = df['a_poss'].dt.minute + df['a_poss'].dt.second/60

# Split total passing stats into completions, pass attempts, passing yards, touchdowns and interceptions
h_ptot = pd.DataFrame(df['h_ptot'].str.split('-').tolist(), columns = 'comp patt pyds ptds ints'.split())
a_ptot = pd.DataFrame(df['a_ptot'].str.split('-').tolist(), columns = 'comp patt pyds ptds ints na'.split())

# Correct values for game with negative passing yards
neg = a_ptot.loc[a_ptot['na'] == '2']
a_ptot.loc[neg.index,:] = 2, 14, -7, 0, 2, 0
a_ptot = a_ptot.drop('na', axis=1)
h_ptot, a_ptot = h_ptot.astype(float), a_ptot.astype(float)

# Calculate pass yards per attempt, rush yards per carry, offensive TD, comp % and 3rd down conversion %
df['h_comp'], df['a_comp'] = h_ptot['comp'], a_ptot['comp']
df['h_patt'], df['a_patt'] = h_ptot['patt'], a_ptot['patt']
df['h_pyds'], df['a_pyds'] = h_ptot['pyds'], a_ptot['pyds']
df['h_ptds'], df['a_ptds'] = h_ptot['ptds'], a_ptot['ptds']
df['h_ints'], df['a_ints'] = h_ptot['ints'], a_ptot['ints']

df['h_pypa'], df['a_pypa'] = df['h_pyds']/df['h_patt'], df['a_pyds']/df['a_patt']
df['h_cpct'], df['a_cpct'] = df['h_comp']/df['h_patt'], df['a_comp']/df['a_patt']
df['h_rypc'], df['a_rypc'] = df['h_ryds']/df['h_ratt'], df['a_ryds']/df['a_ratt']
df['h_3pct'], df['a_3pct'] = df['h_3dcv']/df['h_3att'], df['a_3dcv']/df['a_3att']
df['h_otds'] = df['h_rtot'].str.split('-').str[-1].astype(float) + df['h_ptds']
df['a_otds'] = df['a_rtot'].str.split('-').str[-1].astype(float) + df['a_ptds']

df = df.drop(['a_ptot', 'h_ptot', 'a_rtot', 'h_rtot', 'a_ptds', 'h_ptds'], axis=1)

# Update team names to 2017 season names to account for name changes
df['h_team'] = np.array(np.where(df['h_team']=='St. Louis Rams', 'Los Angeles Rams', df['h_team']))
df['a_team'] = np.array(np.where(df['a_team']=='St. Louis Rams', 'Los Angeles Rams', df['a_team']))
df['h_team'] = np.array(np.where(df['h_team']=='San Diego Chargers', 'Los Angeles Chargers', df['h_team']))
df['a_team'] = np.array(np.where(df['a_team']=='San Diego Chargers', 'Los Angeles Chargers', df['a_team']))

# Convert line to value in terms of home team (>0 = underdog and <0 = favorite) 
fav = df['line'].str.rsplit(' ', expand=True, n=1)[0]
fav = np.array(np.where(fav == 'St. Louis Rams', 'Los Angeles Rams', fav))
fav = np.array(np.where(fav == 'San Diego Chargers', 'Los Angeles Chargers', fav))
fav_line = df['line'].str.split(' ').str[-1]
fav_line = pd.to_numeric(np.array(np.where(fav_line == 'Pick', 0.0, fav_line)))
df['line'] = np.array(np.where(df['h_team'] == fav, fav_line, abs(fav_line)))

# Create team and a division dictionaries
teams = {'Arizona Cardinals':  'ARI', 'Atlanta Falcons':     'ATL', 'Baltimore Ravens':    'BAL', 'Buffalo Bills':       'BUF', 
        'Carolina Panthers':   'CAR', 'Chicago Bears':       'CHI', 'Cincinnati Bengals':  'CIN', 'Cleveland Browns':    'CLE', 
        'Dallas Cowboys':      'DAL', 'Denver Broncos':      'DEN', 'Detroit Lions':       'DET', 'Green Bay Packers':   'GB' , 
        'Houston Texans':      'HOU', 'Indianapolis Colts':  'IND', 'Jacksonville Jaguars':'JAX', 'Kansas City Chiefs':  'KC' , 
        'Los Angeles Chargers':'LAC', 'Los Angeles Rams':    'LAR', 'Miami Dolphins':      'MIA', 'Minnesota Vikings':   'MIN', 
        'New England Patriots':'NE' , 'New Orleans Saints':  'NO' , 'New York Giants':     'NYG', 'New York Jets':       'NYJ', 
        'Oakland Raiders':     'OAK', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 'Seattle Seahawks':    'SEA',
        'San Francisco 49ers': 'SF' , 'Tampa Bay Buccaneers':'TB' , 'Tennessee Titans':    'TEN', 'Washington Redskins': 'WAS'}

div = {'BUF':'AFC-E', 'MIA':'AFC-E', 'NE' :'AFC-E', 'NYJ':'AFC-E', 'BAL':'AFC-N', 'CIN':'AFC-N', 'CLE':'AFC-N', 'PIT':'AFC-N',
       'HOU':'AFC-S', 'IND':'AFC-S', 'JAX':'AFC-S', 'TEN':'AFC-S', 'DEN':'AFC-W', 'KC' :'AFC-W', 'LAC':'AFC-W', 'OAK':'AFC-W',
       'DAL':'NFC-E', 'NYG':'NFC-E', 'PHI':'NFC-E', 'WAS':'NFC-E', 'CHI':'NFC-N', 'DET':'NFC-N', 'GB' :'NFC-N', 'MIN':'NFC-N',
       'ATL':'NFC-S', 'CAR':'NFC-S', 'NO' :'NFC-S', 'TB' :'NFC-S', 'ARI':'NFC-W', 'LAR':'NFC-W', 'SF' :'NFC-W', 'SEA':'NFC-W'}

# Update team names with dictionary
df['h_team'], df['a_team'] = df['h_team'].replace(teams), df['a_team'].replace(teams)

# Create a divisional games column
h_div, a_div = df['h_team'].replace(div), df['a_team'].replace(div)
df['div_game'] = np.array(np.where(h_div == a_div , 1, 0))

# Create results columns (home win = 1 and loss/tie = 0)
df['h_wins'] = np.array(np.where(df['h_score'] > df['a_score'], 1, 0))
df['a_wins'] = np.array(np.where(df['h_score'] <= df['a_score'], 1, 0))
df['line_w'] = np.array(np.where((df['h_score'] + df['line']) > df['a_score'], 1, 0))
df['over_w'] = np.array(np.where(df['h_score'] + df['a_score'] > df['over'], 1, 0))

# Load Elo ratings (https://github.com/fivethirtyeight/nfl-elo-game)
elo = pd.read_csv('nfl_elo.csv')
elo = elo[elo.season > 2001]
elo_2017 = pd.read_csv('nfl_elo_2017.csv')
elo = elo.append(elo_2017)

# Merge Elo ratings with df
elo.date = pd.to_datetime(elo.date)
elo = elo[elo.playoff == 0]
elo.team1 = np.array(np.where(elo.team1 == 'WSH', 'WAS', elo.team1))
elo.team2 = np.array(np.where(elo.team2 == 'WSH', 'WAS', elo.team2))
elo = elo.sort_values(by=['season', 'date', 'team1']).reset_index(drop=True)
elo = elo.drop(['date', 'neutral', 'playoff', 'elo_prob1', 'result1'], axis=1)
elo_map = {'season': 'year', 'team1': 'h_team', 'team2': 'a_team', 'elo1': 'h_elo', 'elo2': 'a_elo', 'score1': 'h_score', 'score2': 'a_score'}
elo.rename(columns=elo_map,inplace=True)

df2 = pd.merge(df, elo, on=['year', 'h_team', 'a_team', 'h_score', 'a_score'], how='outer')
x = df2[df2.h_elo.isnull()].sort_values(by=['year', 'h_team']).reset_index(drop=True)
y = df2[df2.id.isnull()].sort_values(by=['year', 'a_team']).reset_index(drop=True)
x.h_elo = np.array(np.where(x.h_team == y.a_team, y.a_elo, 'na')).astype(float)
x.a_elo = np.array(np.where(x.a_team == y.h_team, y.h_elo, 'na')).astype(float)
df2 = df2[df2.h_elo.notnull()]
df2 = df2[df2.id.notnull()]
df = df2.append(x).sort_values(by='id').reset_index(drop=True)

# Clear unneeded objects from memory
del indoor, a_ptot, h_ptot, fav, fav_line, div, h_div, a_div, elo, elo_2017, elo_map, neg, df2, x, y

# Construct the dataframes needed for matchup predictions
info_col = ['temp', 'div_game', 'line', 'over', 'line_w', 'over_w', 'h_elo', 'a_elo']

games_col = ['id', 'year', 'week', 'team', 'score', 'wins', 'poss', 'otds', 'ryds', 'ratt', 'rypc', 'npyd', 
             'pyds', 'patt', 'comp', 'pypa', 'cpct', '1dcv', '3dcv', '3att', '3pct', 'sack', 'ints', 'turn', 'peny']

h_col = ['h_team', 'h_score', 'h_wins', 'h_poss', 'h_otds', 'h_npyd', 'h_pyds', 'h_patt', 'h_comp', 'h_cpct', 'h_pypa', 
         'h_ryds', 'h_ratt', 'h_rypc', 'h_1dcv', 'h_3dcv', 'h_3att', 'h_3pct', 'h_sack', 'h_ints', 'h_turn', 'h_peny'] 

a_col = ['a_team', 'a_score', 'a_wins', 'a_poss', 'a_otds', 'a_npyd', 'a_pyds', 'a_patt', 'a_comp', 'a_cpct', 'a_pypa',
         'a_ryds', 'a_ratt', 'a_rypc', 'a_1dcv', 'a_3dcv', 'a_3att', 'a_3pct', 'a_sack', 'a_ints', 'a_turn', 'a_peny'] 

h_map = {'id': 'id', 'year': 'year', 'week': 'week', 'h_team': 'team', 'h_score': 'score', 'h_wins': 'wins', 'h_poss': 'poss', 
         'h_otds': 'otds', 'h_npyd': 'npyd', 'h_pyds': 'pyds', 'h_patt': 'patt', 'h_comp': 'comp',  'h_cpct': 'cpct', 
         'h_pypa': 'pypa', 'h_ryds': 'ryds', 'h_ratt': 'ratt', 'h_rypc': 'rypc', 'h_1dcv': '1dcv', 'h_3dcv': '3dcv', 
         'h_3att': '3att', 'h_3pct': '3pct', 'h_sack': 'sack', 'h_ints': 'ints', 'h_turn': 'turn', 'h_peny': 'peny'}

a_map = {'id': 'id', 'year': 'year', 'week': 'week', 'a_team': 'team', 'a_score': 'score', 'a_wins': 'wins', 'a_poss': 'poss', 
         'a_otds': 'otds', 'a_npyd': 'npyd', 'a_pyds': 'pyds', 'a_patt': 'patt', 'a_comp': 'comp', 'a_cpct': 'cpct', 
         'a_pypa': 'pypa', 'a_ryds': 'ryds', 'a_ratt': 'ratt', 'a_rypc': 'rypc', 'a_1dcv': '1dcv', 'a_3dcv': '3dcv', 
         'a_3att': '3att', 'a_3pct': '3pct', 'a_sack': 'sack', 'a_ints': 'ints', 'a_turn': 'turn', 'a_peny': 'peny'}

home = df.drop(a_col + info_col, axis=1)
away = df.drop(h_col + info_col, axis=1)
home.rename(columns=h_map,inplace=True)
away.rename(columns=a_map,inplace=True)
home, away = home.reindex(columns=games_col), away.reindex(columns=games_col)
games = home.append(away).sort_values(['year', 'team', 'week'])
del h_col, a_col, h_map, a_map, home, away, info_col, games_col

# Create season average stats dataframe
years = games.drop(['id', 'week', 'pypa', 'rypc', 'cpct', '3pct'], axis=1)
years = years.groupby(['year', 'team']).mean().reset_index(drop=False)
years['pypa'] = years['pyds']/years['patt']
years['cpct'] = years['comp']/years['patt']
years['rypc'] = years['ryds']/years['ratt']
years['3pct'] = years['3dcv']/years['3att']
games = games.drop(['pyds', 'patt', 'comp', 'ratt', '3dcv', '3att'], axis=1) 
years = years.drop(['pyds', 'patt', 'comp', 'ratt', '3dcv', '3att'], axis=1)             
games_col = list(games.columns.values)
games_col.remove('week')
years = years.reindex(columns=games_col).sort_values(['year', 'team'])

# Create a dataframe for week 1 matchup stats using last year's average stats for each team
# Shift season stats up 1 year and set values as stats for week 1 matchups
years['year'] = years['year'] + 1
years['week'] = 0

# Drop matchup stats not used for analysis
years = years[years.year != 2018].reset_index(drop=True)
df = df[df.year != 2002].reset_index(drop=True)
games = games[games.year != 2002].reset_index(drop=True)

# Assign ids for matchups (MIA and TB didn't play 2017 week 1, assign week 2 id)
week1 = games[(games.week == 1)]
mia = games[(games.week == 2) & (games.team == 'MIA') & (games.year == 2017)]['id'].values[0]
tb = games[(games.week == 2) & (games.team == 'TB') & (games.year == 2017)]['id'].values[0]
week1 = week1.append(games[(games.id == mia)]).sort_values(['year', 'team'])
week1 = week1.append(games[(games.id == tb)]).sort_values(['year', 'team'])
week1 = week1[~((week1.week == 2) & (week1.team == 'LAC') & (week1.year == 2017))]
week1 = week1[~((week1.week == 2) & (week1.team == 'CHI') & (week1.year == 2017))]
week1 = week1.sort_values(['year', 'team']).reset_index(drop=True)
years['id'] = week1['id']

# Merge week 1 matchup stats with games df
games = pd.concat([games, years]).sort_values(['year', 'team', 'week'])

games_col = list(games.columns.values)
games = games.reindex(columns=games_col)
games.week = games.week.astype(int)
games.id = games.id.astype(int)
del years, games_col, week1, mia, tb

# Define a progress bar function to monitor processing completion % 
def progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    '''
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    '''
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()

# Calculate moving average stats for each team during the year up until the game matchup
teams = list(teams.values())
for year in range(2003, 2018):
    for week in range (1, 18):
        week_stats = pd.DataFrame(columns=games.columns.values)
        for team in teams:
            sel_year = games[games['year'] == year]
            sel_team = sel_year[sel_year['team'] == team]
            sel_week = sel_team[sel_team['week'] < week]
            week_stats = week_stats.append(sel_week)
        
        # Last season stats will be averaged with each new game but will fall off after 7 games
        week_stats = week_stats.groupby('team').rolling(window=6, min_periods=1).mean()
        
        if week == 1 and year == 2003:
            tot_stats = week_stats
        else:
            tot_stats = tot_stats.append(week_stats)
    progress_bar(year - 2002, 15, prefix = 'Progress:', suffix = 'Complete', length = 50)

# Remove duplicate rows and assigning the appropriate game id for matchups
tot_stats = tot_stats.drop_duplicates(tot_stats.columns.difference(['week'])).sort_values(['year', 'team', 'week']).reset_index(drop=True)
tot_stats.id = tot_stats.id.shift(-1)
tot_stats.iloc[-1, tot_stats.columns.get_loc('id')] = 0
tot_stats.id = tot_stats.id.astype(int)

week17 = games[(games.week == 17)].sort_values(['year', 'team', 'week']).reset_index(drop=True)
week16 = tot_stats[(tot_stats.week == 16)].sort_values(['year', 'team', 'week']).reset_index(drop=True)
week16.id = week17[((week17.year == week16.year) & (week17.team == week16.team))].id
tot_stats = tot_stats[(tot_stats.week != 16)]
tot_stats = tot_stats.append(week16).sort_values(['id']).reset_index(drop=True)

# Create team differential matchup values using each team's average stats 
matchup_col = ['id', 'year', 'week', 'h_team','a_team', 'div_game', 'line', 'over', 'temp', 'elo_d', 'appg_d', 'wins_d', 'poss_d', 'otds_d', 'ryds_d', 
               'rypc_d', 'npyd_d', 'pypa_d', 'cpct_d', '1dcv_d', '3pct_d', 'sack_d', 'ints_d', 'turn_d', 'peny_d', 'h_wins', 'line_w', 'over_w']

matchup = pd.DataFrame(columns = matchup_col)
matchdf_col = ['id', 'year', 'week', 'h_team', 'a_team', 'div_game', 'line', 'over', 'temp', 'h_wins', 'line_w', 'over_w']
matchup[matchdf_col] = df[matchdf_col]
matchup['elo_d'] = df['h_elo'] - df['a_elo']

del teams, year, week, team, sel_year, sel_team, sel_week, week_stats, games, week16, week17, matchup_col, matchdf_col

for row in range(len(matchup)):
    try:
        gameid = matchup.iloc[row]['id']
        h_team = matchup.iloc[row]['h_team']
        a_team = matchup.iloc[row]['a_team']        
        
        h_appg = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['score'].values[0]
        h_wins = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['wins'].values[0]
        h_poss = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['poss'].values[0]
        h_otds = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['otds'].values[0]
        h_ryds = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['ryds'].values[0]
        h_rypc = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['rypc'].values[0]
        h_npyd = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['npyd'].values[0]
        h_pypa = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['pypa'].values[0]
        h_cpct = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['cpct'].values[0]
        h_1dcv = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['1dcv'].values[0]
        h_3pct = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['3pct'].values[0]
        h_sack = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['sack'].values[0]
        h_ints = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['ints'].values[0]
        h_turn = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['turn'].values[0]
        h_peny = tot_stats[((tot_stats.team == h_team) & (tot_stats.id == gameid))]['peny'].values[0]
       
        a_appg = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['score'].values[0]
        a_wins = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['wins'].values[0]
        a_poss = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['poss'].values[0]
        a_otds = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['otds'].values[0]    
        a_ryds = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['ryds'].values[0]
        a_rypc = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['rypc'].values[0]
        a_npyd = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['npyd'].values[0]
        a_pypa = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['pypa'].values[0]
        a_cpct = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['cpct'].values[0]
        a_1dcv = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['1dcv'].values[0]
        a_3pct = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['3pct'].values[0]
        a_sack = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['sack'].values[0]
        a_ints = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['ints'].values[0]        
        a_turn = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['turn'].values[0]
        a_peny = tot_stats[((tot_stats.team == a_team) & (tot_stats.id == gameid))]['peny'].values[0]
        
        matchup.ix[row, 'appg_d'] = h_appg - a_appg
        matchup.ix[row, 'wins_d'] = h_wins - a_wins
        matchup.ix[row, 'poss_d'] = h_poss - a_poss
        matchup.ix[row, 'otds_d'] = h_otds - a_otds
        matchup.ix[row, 'ryds_d'] = h_ryds - a_ryds
        matchup.ix[row, 'rypc_d'] = h_rypc - a_rypc
        matchup.ix[row, 'npyd_d'] = h_npyd - a_npyd
        matchup.ix[row, 'pypa_d'] = h_pypa - a_pypa
        matchup.ix[row, 'cpct_d'] = h_cpct - a_cpct   
        matchup.ix[row, '1dcv_d'] = h_1dcv - a_1dcv 
        matchup.ix[row, '3pct_d'] = h_3pct - a_3pct
        matchup.ix[row, 'sack_d'] = h_sack - a_sack
        matchup.ix[row, 'ints_d'] = h_ints - a_ints
        matchup.ix[row, 'turn_d'] = h_turn - a_turn
        matchup.ix[row, 'peny_d'] = h_peny - a_peny
    
    except:
        pass
    progress_bar(row + 1, len(matchup), prefix = 'Progress:', suffix = 'Complete', length = 50)

# Reindex columns and export matchup dataframe
matchup = matchup.drop(['id'], axis=1).sort_values(['year', 'week', 'h_team'])
matchup.to_csv('nfl_cleaned.csv', index=False)

'''
Data Dictionary:   
01. year      # Beginning year of the NFL season
02. week      # Week game was played
03. div_game  # Indicates if matchup is a divisional game
04. line      # Vegas point spread with respect to the home team
05. over      # Vegas over/under line
06. temp      # Temperature of the stadium
07. elo_d     # Matchup differential of FiveThirtyEight's Elo ratings
08. appg_d    # Points per game differential
09. wins_d    # Winning percentage differential
10. poss_d    # Time of possesion differential
11. otds_d    # Offensive touchdowns differential
12. ryds_d    # Rushing yards differential
13. rypc_d    # Rushing yards per carry differential
14. npyd_d    # Net passing yards differential
15. pypa_d    # Passing yards per attempt differential
16. cpct_d    # Completion percentage differential
17. 1dcv_d    # 1st down conversion differential
18. 3pct_d    # 3rd down conversion percentage differential
19. sack_d    # QB sacks taken differential
20. ints_d    # Interception differential
21. turn_d    # Turnover differential
22. peny_d    # Penalty yards differential
23. h_wins    # Dummy variable indicating if home team won
24. line_w    # Dummy variable indicating if home covered spread
25. over_w    # Dummy variable indicating if over line was covered
'''