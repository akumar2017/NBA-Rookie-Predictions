import requests
from bs4 import BeautifulSoup
import pandas as pd
from basketball_reference_web_scraper import client


def get_rookie_stats(year, rookie_names):
    season_totals = client.players_season_totals(season_end_year = year)
    stats_dict = {}
    for total in season_totals:
        if total['name'] in rookie_names and total['games_played'] >= 30:
            stats_dict[total['name']] = total
    return stats_dict

def get_rookie_advanced_stats(year, rookie_names):
    season_totals = client.players_advanced_season_totals(season_end_year=year)
    stats_dict = {}
    for total in season_totals:
        if total['name'] in rookie_names and total['games_played'] >= 30:
            stats_dict[total['name']] = total
    return stats_dict

df = pd.DataFrame(columns=['Rookie Year', 'Name', 'rpts', 'rrebs', 'rasts', 'rstls', 'rblks', 'rto', 'rfg%', 'rft%', 'r3fg%', 'rWS/48', 'rBPM', 'rPER', 'rTS%', 'rVORP', 'pts', 'rebs', 'asts', 'stls', 'blks', 'to', 'fg%', 'ft%', '3fg%', 'WS/48', 'BPM', 'PER', 'TS%', 'VORP'])

rookies = {} #dictionary, keys = year, value = list of rookie dictionaries (keys = columns, values = field)
for i in range(2010, 2017):
    rookies[i] = []
    url = 'https://www.basketball-reference.com/leagues/NBA_'+str(i)+'_rookies.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    players = soup.find_all('tr', class_='full_table')
    names = list(map(lambda x: x.find_all('a')[0].get_text(), players))#, x.find_all('a')[0]['href']), players))
    rookie_stats = get_rookie_stats(i, names)
    rookie_adv_stats = get_rookie_advanced_stats(i, names)
    later_stats = get_rookie_stats(i+3, names)
    later_adv_stats = get_rookie_advanced_stats(i+3, names)
    for rookie in names:
        if rookie not in rookie_stats or rookie not in later_stats:
            continue
        total = rookie_stats[rookie]
        stats = {}
        stats['Rookie Year'] = i
        stats['Name'] = rookie
        stats['rpts'] = (total['made_field_goals']*2 + total['made_free_throws'] + total['made_three_point_field_goals'])/total['minutes_played'] * 36
        stats['rrebs'] = (total['offensive_rebounds'] + total['defensive_rebounds'])/total['minutes_played'] * 36
        stats['rasts'] = total['assists']/total['minutes_played'] * 36
        stats['rstls'] = total['steals']/total['minutes_played'] * 36
        stats['rblks'] = total['blocks']/total['minutes_played'] * 36
        stats['rtos'] = total['turnovers']/total['minutes_played'] * 36
        stats['rfg%'] = total['made_field_goals']/total['attempted_field_goals']
        stats['r3fg%'] = 0
        if not total['attempted_three_point_field_goals'] == 0:
            stats['r3fg%'] = total['made_three_point_field_goals']/total['attempted_three_point_field_goals']
        stats['rft%'] = total['made_free_throws']/total['attempted_free_throws']
        total = rookie_adv_stats[rookie]
        stats['rWS/48'] = total['win_shares_per_48_minutes']
        stats['rBPM'] = total['box_plus_minus']
        stats['rPER'] = total['player_efficiency_rating']
        stats['rTS%'] = total['true_shooting_percentage']
        stats['rVORP'] = total['value_over_replacement_player']


        total = later_stats[rookie]
        stats['pts'] = (total['made_field_goals']*2 + total['made_free_throws'] + total['made_three_point_field_goals'])/total['minutes_played'] * 36
        stats['rebs'] = (total['offensive_rebounds'] + total['defensive_rebounds'])/total['minutes_played'] * 36
        stats['asts'] = total['assists']/total['minutes_played'] * 36
        stats['stls'] = total['steals']/total['minutes_played'] * 36
        stats['blks'] = total['blocks']/total['minutes_played'] * 36
        stats['tos'] = total['turnovers']/total['minutes_played'] * 36
        stats['fg%'] = total['made_field_goals']/total['attempted_field_goals']
        stats['3fg%'] = 0
        if not total['attempted_three_point_field_goals'] == 0:
            stats['3fg%'] = total['made_three_point_field_goals']/total['attempted_three_point_field_goals']
        stats['ft%'] = total['made_free_throws']/total['attempted_free_throws']
        total = later_adv_stats[rookie]
        stats['WS/48'] = total['win_shares_per_48_minutes']
        stats['BPM'] = total['box_plus_minus']
        stats['PER'] = total['player_efficiency_rating']
        stats['TS%'] = total['true_shooting_percentage']
        stats['VORP'] = total['value_over_replacement_player']
        df = df.append(stats, ignore_index = True)

df.to_csv('dataset.csv')




    
    