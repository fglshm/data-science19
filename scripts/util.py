from npb.models import Team, Player, TeamYear, HitterStats, PitcherStats, MatchResult, MatchMember, Ranking, League

def get_teams():
    return Team.objects.all()


def get_team(name):
    if name == '横浜':
        name = 'DeNA'
    return Team.objects.filter(name=name)[0]
