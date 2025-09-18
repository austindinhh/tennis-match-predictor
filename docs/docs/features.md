# Features

## Match Information
Basic information about each match. 

| Feature       | Included in Model | Description |
|:-------------:|:-----------------:|:-----------:|
| match_id      | No                | Unique match number
| year          | No                | int (ex. 2014)
| date          | No                | Date when match was played
| surfaace      | Yes               | Clay, grass, hard court
| series        | Yes               | Type of tournament (Grand slam, Masters 1000, etc)
| tournament    | No                | Tournament name
| round         | Yes               | Round of tournament (R128, QF, etc)
| draw_size     | No                | # of players in tournament
| best_of       | Yes               | Best of 3 or 5
| minutes       | Yes               | Match duration
| winner_sets   | No                | # sets winner won
| loser_sets    | No                | # sets loser won

## Player Information
Each player is randomly assigned player_a or player_b. The features are doubled (ex. there is a player_a_age and player_b_age) but only age would be displayed in the table.

| Feature       | Included in Model | Description |
|:-------------:|:-----------------:|:-----------:|
| name          | No                | Full name of player
| age           | Yes               | Age rounded to nearest decimal
| height        | Yes               | Height in centimeters (cm)
| rank          | Yes               | ATP ranking
| rank_points   | Yes               | ATP ranking points
| lefty         | Yes               | Left handed (1) or right handed (0)

## Match Statistics
Basic statistics calculated for each player in every match.

| Feature               | Included in Model | Description |
|:---------------------:|:-----------------:|:-----------:|
| aces                  | Yes               | # aces
| double_faults         | Yes               | # double  faults
| serve_points          | Yes               | # points on serve
| first_serves_in       | Yes               | # first serves in
| first_serves_won      | Yes               | # first serves won  
| first_serve_pct       | Yes               | first_serves_in / serve_points
| first_serve_won_pct   | Yes               | first_serves_won / first_serves_in
| second_serves_won     | Yes               | # second serves won
| second_serve_won_pct  | Yes               | second_serves_won / (serve_points - first_serves_in)
| serve_games           | Yes               | # games on serve
| bp_saved              | Yes               | # break points saved
| bp_faced              | Yes               | # break points faced
| bp_saved_pct          | Yes               | bp_saved / bp_faced

## Betting Odds
Betting odds calculated for each player in every match. 

| Feature               | Included in Model | Description |
|:---------------------:|:-----------------:|:-----------:|
| avg_odds              | Yes               | Average of odds from 5+ sites
| max_odds              | Yes               | Highest recorded odds
| implied_prob          | Yes               | 1 / avg_odds
| max_prob              | Yes               | 1 / max_odds
| market_confidence_avg | Yes               | a_implied_prob - b_implied_prob (absolute value)
| market_confidence_max | Yes               | a_max_prob - b_max_prob (absolute value)
| odds_movement         | Yes               | max_odds - avg_odds

## Player Statistics
Statistics aggregated through the last year, few matches, etc. X denotes (a,b) i.e either player a or player b. 

| Feature                       | Included in Model | Description |
|:-----------------------------:|:-----------------:|:-----------:|
| h2h_total_matches             | Yes               | # times 2 players have played each other
| h2h_player_x_wins             | Yes               | # wins each player has over each other
| h2h_player_x_win_rate         | Yes               | h2h_player_x_wins / h2h_total_matches
| h2h_5_player_x_win_rate       | Yes               | Calculated win rate for last 5 H2H matches
| h2h_surface_total_matches     | Yes               | Total matches played on the specifc surface
| h2h_surface_player_x_win_rate | Yes               | h2h_surface_player_x_wins / h2h_surface_total_matches
|h2h_surface_5_player_x_win_rate| Yes               | Calculated win rate for last 5 H2H matches on specific surface

## Player Statistics Differentials
The (non-absolute) differences between player stats are also calculated. These are often labeled with a "delta" suffix 