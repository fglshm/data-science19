from npb.models import Team, Player, TeamYear, HitterStats, PitcherStats, MatchResult, MatchMember, Ranking, League
from bs4 import BeautifulSoup
import requests
from pprint import pprint
from tqdm import tqdm
from time import sleep
import re


def run():
    # scrape_ranking()
    print("hello")


def register_team_year():
    for team in get_teams():
        for idx in range(11):
            team_year = TeamYear(year=idx + 2009, team_id=team.id)
            team_year.save()


def init_request(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def scrape_team():
    """ プロ野球のチームをスグレイピングして保存 """
    soup = init_request(
        'https://baseball-data.com/stats/hitter-all/tpa-2.html'
    )
    submenus = soup.find('div', class_="sub-menu")
    pb_teams = submenus.find_all('a')[2:]
    for pb_team in pb_teams:
        team = Team(name=pb_team.text)
        team.save()


def scrape_players():
    for team in get_teams():
        urls = [f'https://baseball-data.com/player/{team.abb}/']
        years = ['2019']
        for idx in range(10):
            year = str(idx + 2009)
            years.append(year)
            urls.append(
                f'https://baseball-data.com/{year[2:]}/player/{team.abb}/'
            )

        for url, year in zip(urls, years):
            team_year = TeamYear.objects.filter(
                team_id=team.id, year=str(year))[0]
            sleep(2.5)
            soup = init_request(url)
            tbody = soup.find('tbody')
            trs = tbody.find_all('tr')
            for tr in tqdm(trs):
                no = tr.find('td').text
                field = tr.find_all('td')[2].text
                name = tr.a.text.replace('\u3000', '')
                player = Player(
                    no=no,
                    name=name,
                    team_year_id=team_year.id,
                    category=player_category(field),
                    position=player_position(field)
                )
                player.save()


def scrape_hitter_stats():
    count = 0

    for idx in range(10):
        y = str(idx + 2009)[2:]
        for team in tqdm(get_teams()):
            sleep(2)
            url1 = f'https://baseball-data.com/{y}/stats/hitter-{team.abb}/'
            url2 = f'https://baseball-data.com/{y}/stats/hitter2-{team.abb}/tpa-1.html'
            url3 = f'https://baseball-data.com/{y}/stats/hitter3-{team.abb}/tpa-1.html'
            url4 = f'https://baseball-data.com/{y}/stats/hitter4-{team.abb}/tpa-1.html'
            for url in tqdm([url1, url2, url3, url4]):
                for team_year in tqdm(team.teamyear_set.all().order_by('-year')):
                    soup = init_request(url)
                    tbody = soup.find('tbody')
                    thead = soup.find('thead')
                    thead_ths = [th.text for th in thead.find_all('th')]
                    for tr in tbody.find_all('tr'):
                        name = tr.a.text.replace('\u3000', '')
                        player = team_year.player_set.all().filter(name=name)
                        if not player:
                            continue
                        hitter_stats = player[0].hitterstats_set.all(
                        )[0] if player[0].hitterstats_set.all().count() > 0 else HitterStats()
                        if not player[0].hitterstats_set.all().count() > 0:
                            count += 1
                        hitter_stats.player_id = player[0].id
                        tds = [td.text.replace('\u3000', '')
                               for td in tr.find_all('td')]
                        if tds[2] == '-':
                            continue
                        for th, td in zip(thead_ths[2:], tds[2:]):
                            field = get_hitter_stats_field(th)
                            if field and re.search(r'\d', td):
                                bind_player_stats(
                                    hitter_stats, field, float(td))
                        hitter_stats.save()


def scrape_pitcher_stats():
    count = 0
    for idx in range(10):
        y = str(idx + 2009)[2:]
        for team in tqdm(get_teams()):
            print(team)
            sleep(2)
            url1 = f'https://baseball-data.com/{y}/stats/pitcher-{team.abb}/ip3-1.html'
            url2 = f'https://baseball-data.com/{y}/stats/pitcher2-{team.abb}/ip3-1.html'
            url3 = f'https://baseball-data.com/{y}/stats/pitcher3-{team.abb}/ip3-1.html'
            for url in tqdm([url2, url3, url1]):
                for team_year in tqdm(team.teamyear_set.all().order_by('-year')):
                    soup = init_request(url)
                    tbody = soup.find('tbody')
                    thead = soup.find('thead')
                    thead_ths = [th.text for th in thead.find_all('th')]
                    for tr in tbody.find_all('tr'):
                        name = tr.a.text.replace('\u3000', '')
                        player = team_year.player_set.all().filter(name=name)
                        if not player:
                            continue
                        pitcher_stats = player[0].pitcherstats_set.all(
                        )[0] if player[0].pitcherstats_set.all().count() > 0 else PitcherStats()
                        if not player[0].pitcherstats_set.all().count() > 0:
                            count += 1
                        pitcher_stats.player_id = player[0].id
                        tds = [td.text.replace('\u3000', '')
                               for td in tr.find_all('td')]
                        if tds[2] == '-':
                            continue
                        for th, td in zip(thead_ths[2:], tds[2:]):
                            field = get_pitcher_stats_field(th)
                            if field and re.search(r'\d', td):
                                bind_player_stats(
                                    pitcher_stats, field, float(td))
                        pitcher_stats.save()


def bind_player_stats(obj, field, val):
    setattr(obj, field, val)


def scrape_match_results():
    for team in tqdm(get_teams()):
        urls = [f'https://baseball-freak.com/game/{team.spell}.html']
        years = ['2019']
        for idx in range(10):
            year = str(idx + 2009)
            years.append(year)
            urls.append(
                f'https://baseball-freak.com/game/{year[2:]}/{team.spell}.html')

        for url, year in tqdm(zip(urls, years)):
            team_year = team.teamyear_set.all().filter(year=year)[0]
            soup = init_request(url)
            table = soup.find('table', class_='tschedule')
            trs = table.find_all('tr')
            tr_heads = [th.text for th in trs[0].find_all('th')]
            for tr in trs[1:]:
                row = [td.text for td in tr.find_all('td')]
                if row[2] == '中止':
                    continue
                match_result = MatchResult()
                match_result.date = row[0]
                match_result.result = 2 if row[1] == '●' else 1
                match_result.score = row[2].replace(' ', '')
                match_result.opponent = get_team(row[3])
                match_result.pitcher = get_starting_pitcher(
                    team, row[4], year)
                match_result.team_year = team_year
                match_result.year = year
                match_result.save()


def get_starting_pitcher(team, name, year):
    team_year = team.teamyear_set.all().filter(year=year)[0]
    player = team_year.player_set.all().filter(name__contains=name)
    if player.count() > 0:
        return player[0]
    elif '高' in name:
        new_name = '髙' + name[1:]
        player = team_year.player_set.all().filter(name__contains=new_name)[0]
        return player
    elif '髙' in name:
        new_name = '高' + name[1:]
        player = team_year.player_set.all().filter(name__contains=new_name)[0]
        return player
    elif '斉' in name:
        new_name = '齊' + name[1:]
        player = team_year.player_set.all().filter(name__contains=new_name)[0]
        return player
    else:
        return None


def get_teams():
    return Team.objects.all()


def get_team(name):
    if name == '横浜':
        name = 'DeNA'
    return Team.objects.filter(name=name)[0]


def player_position(filed):
    positions = {
        '投手': 1,
        '捕手': 2,
        '内野手': 3,
        '外野手': 4
    }
    return positions[filed]


def player_category(filed):
    return 1 if filed == '投手' else 2


def get_hitter_stats_field(name):
    fields = {
        "打率": "daritsu",
        "試合": "shiai",
        "打席数": "dasekisuu",
        "打数": "dasuu",
        "安打": "annda",
        "本塁打": "honnruida",
        "打点": "datenn",
        "盗塁": "tourui",
        "四球": "sikyuu",
        "死球": "deadball",
        "三振": "sannshinn",
        "犠打": "gida",
        "併殺打": "heisatsuda",
        "出塁率": "shutsuruiritsu",
        "長打率": "tyuodaritsu",
        "OPS": "ops",
        "RC27": "rc27",
        "XR27": "xr27",
        "得点": "tokutenn",
        "二塁打": "niruida",
        "三塁打": "sannruida",
        "塁打": "ruida",
        "盗塁刺": "tourui_fail",
        "NOI": "noi",
        "GPA": "gpa",
        "IsoD": "isod",
        "IsoP": "isop",
        "XR": "xr",
        "RC": "rc",
        "BABIP": "babip",
        "SecA": "seca",
        "TA": "ta",
        "PSN": "psn",
        "BB/K": "bbk",
    }
    try:
        return fields[name]
    except KeyError:
        pass


def get_pitcher_stats_field(name):
    fields = {
        "防御率": "bougyoritsu",
        "試合": "shiai",
        "勝利": "shouri",
        "敗北": "haiboku",
        "セlブ": "saves",
        "ホlルド": "hold",
        "HP": "hp",
        "完投": "kanntou",
        "勝率": "shouritsu",
        "打者": "dasha",
        "投球回": "toukyuukai",
        "被安打": "hiannda",
        "被本塁打": "hihonnruida",
        "与四球": "sikyuu",
        "与死球": "deadball",
        "奪三振": "datsusannshinn",
        "奪三振率": "datsusannshinnritsu",
        "失点": "shitten",
        "自責点": "jisekitenn",
        "完封勝": "kannpuu",
        "無四球": "mushikyuu",
        "WHIP": "whip",
        "DIPS": "dips",
        "K/BB": "kbb",
        "HldR": "hidr",
        "PFR": "pfr",
    }
    try:
        return fields[name]
    except KeyError:
        pass


def scrape_lineups():
    for team in tqdm(get_teams()):
        sleep(2)
        urls = [f'https://baseball-data.com/lineup/{team.abb}.html']
        years = ['2019']
        for idx1 in range(10):
            year = str(idx1 + 2009)
            years.append(year)
            urls.append(
                f'https://baseball-data.com/{year[2:]}/lineup/{team.abb}.html')
        for year2, url in tqdm(zip(years, urls)):
            soup = init_request(url)
            trs = soup.find_all('tr')[1:]
            for tr in trs:
                tds = [td.text for td in tr.find_all('td')]
                team_year = team.teamyear_set.all().filter(year=year2)[0]
                if len(tds) == 0:
                    continue
                match_result = team_year.matchresult_set.all().filter(date=tds[0])[
                    0]
                match_member = MatchMember()
                match_member.match_result = match_result
                match_member.first = get_lineup_player(team_year, tds[1])
                match_member.second = get_lineup_player(team_year, tds[2])
                match_member.third = get_lineup_player(team_year, tds[3])
                match_member.fourth = get_lineup_player(team_year, tds[4])
                match_member.fifth = get_lineup_player(team_year, tds[5])
                match_member.sixth = get_lineup_player(team_year, tds[6])
                match_member.seventh = get_lineup_player(team_year, tds[7])
                match_member.eighth = get_lineup_player(team_year, tds[8])
                match_member.nineth = get_lineup_player(team_year, tds[9])
                # print(match_member)
                match_member.save()


def get_lineup_player(team_year, name):
    player = team_year.player_set.all().filter(name=name.replace(' ', ''))
    if player.count() > 0:
        return player[0]
    else:
        return None


def scrape_ranking():

    dictionary = {
        "1": 'first',
        "2": 'second',
        "3": 'third',
        "4": 'fourth',
        "5": 'fifth',
        "6": 'sixth',
    }

    urls = ['https://baseball-data.com/']
    years = ['2019']

    for i in range(10):
        year = str(i + 2009)
        years.append(year)
        url = f'https://baseball-data.com/{year[2:]}/'
        urls.append(url)

    for idx, (year, url) in enumerate(zip(years, urls)):
        soup = init_request(url)
        table = soup.find_all('table')[1]
        trs = table.find_all('tr')
        ranking = Ranking()
        ranking.year = year
        ranking.league = League.objects.get(pk=2)
        for tr in trs[1:]:
            tds = [td.text for td in tr.find_all('td')]
            setattr(ranking, dictionary[tds[0]], get_team(tds[1]))
        ranking.save()
