from npb.models import Team, Player, TeamYear, HitterStats, PitcherStats, MatchResult, MatchMember, Ranking, League
import sys
sys.path.append('/Users/shohei/Git/my_app/my_web_app/django/datascience/scripts/')
from tqdm import tqdm
import pandas as pd
import os
from util import *


def run():
    save_player_stats()
    print("all player stats saved.")


def save_player_stats():
    years = [str(idx + 2009) for idx in range(11)]
    teams = get_teams()
    for team in teams:
        for year in years:
            team_name = team.name
            pitchers, hitters = team_year_players(year, team_name)
            pitchers_stats, hitters_stats = team_year_players_stats(
                pitchers), team_year_players_stats(hitters)
            [make_csv(year, team_name, stats, idx+1)
             for idx, stats in enumerate([pitchers_stats, hitters_stats])]


def team_year_players(year, name):
    """ get players of a team in specific year """
    team = get_team(name)
    team_year = team.teamyear_set.all().filter(year=year)[0]
    pitchers = team_year.player_set.all().filter(category=1)
    hitters = team_year.player_set.all().filter(category=2)
    return pitchers, hitters


def team_year_players_stats(players):
    """ get players stats """
    return [player_stats(player) for player in players if player_stats(player) != None]


def player_stats(player):
    """ get one player stats """
    try:
        if player.category == 1:
            return player.pitcherstats_set.all()[0]
        else:
            return player.hitterstats_set.all()[0]
    except:
        print(f"{player.name} has no data.")


def make_csv(year, team_name, players_stats, category):
    player_type = 'pitcher' if category == 1 else 'hitter'
    team = get_team(team_name)
    league_name = 'central' if team.league.id == 1 else 'pacific'
    fields = [field.name for field in players_stats[0]._meta.fields][1:]
    fields.append('team')
    fields.append('year')
    all_values = []
    for player_stats in players_stats[1:]:
        values = []
        for field in fields:
            if field == 'player':
                values.append(getattr(player_stats.player, 'name'))
            elif field == 'team':
                values.append(team.name)
            elif field == 'year':
                values.append(year)
            else:
                values.append(getattr(player_stats, field))
        all_values.append(values)

    df = pd.DataFrame(all_values, columns=fields)
    df.to_csv(
        f'/Users/shohei/Git/my_app/my_web_app/django/datascience/data/{league_name}/{team.spell}/{year}/{player_type}.csv', header=True, index=False)
