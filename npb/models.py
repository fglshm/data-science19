from django.db import models


def cls_str(cls):
    rep = f'#<{cls.__class__.__name__}: '
    for idx, field in enumerate(cls._meta.fields):
        val = getattr(cls, field.name)
        rep += f"{field.name}: {val}"
        if idx != len(cls._meta.fields) - 1:
            rep += ', '
    rep += '>'
    return rep


class League(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return cls_str(self)


class Team(models.Model):
    league = models.ForeignKey(
        to=League, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=30)
    abb = models.CharField(max_length=2, null=True)
    spell = models.CharField(max_length=30, null=True)

    def __str__(self):
        return cls_str(self)


class TeamYear(models.Model):
    year = models.CharField(max_length=4)
    team = models.ForeignKey(to=Team, on_delete=models.DO_NOTHING)

    def __str__(self):
        return cls_str(self)


class Player(models.Model):
    no = models.CharField(max_length=15, default='999')
    name = models.CharField(max_length=30)
    team_year = models.ForeignKey(
        to=TeamYear, on_delete=models.DO_NOTHING, null=True)
    category = models.IntegerField(default=0)  # 投手: 1 or 打者: 2
    position = models.IntegerField(default=0)  # 投手: 1, 捕手: 2, 内野手: 3, 外野手: 4

    def __str__(self):
        return cls_str(self)


class HitterStats(models.Model):
    player = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, null=True)
    daritsu = models.FloatField(default=0.0)
    shiai = models.FloatField(default=0.0)
    dasekisuu = models.FloatField(default=0.0)
    dasuu = models.FloatField(default=0.0)
    annda = models.FloatField(default=0.0)
    honnruida = models.FloatField(default=0.0)
    datenn = models.FloatField(default=0.0)
    tokutenn = models.FloatField(default=0.0)
    niruida = models.FloatField(default=0.0)
    sannruida = models.FloatField(default=0.0)
    ruida = models.FloatField(default=0.0)
    tourui_fail = models.FloatField(default=0.0)
    tourui = models.FloatField(default=0.0)
    sikyuu = models.FloatField(default=0.0)
    deadball = models.FloatField(default=0.0)
    sannshinn = models.FloatField(default=0.0)
    gida = models.FloatField(default=0.0)
    heisatsuda = models.FloatField(default=0.0)
    shutsuruiritsu = models.FloatField(default=0.0)
    tyuodaritsu = models.FloatField(default=0.0)
    ops = models.FloatField(default=0.0)
    rc = models.FloatField(default=0.0)
    noi = models.FloatField(default=0.0)
    gpa = models.FloatField(default=0.0)
    rc27 = models.FloatField(default=0.0)
    xr27 = models.FloatField(default=0.0)
    isop = models.FloatField(default=0.0)
    isod = models.FloatField(default=0.0)
    xr = models.FloatField(default=0.0)
    xr27 = models.FloatField(default=0.0)
    babip = models.FloatField(default=0.0)
    seca = models.FloatField(default=0.0)
    ta = models.FloatField(default=0.0)
    psn = models.FloatField(default=0.0)
    bbk = models.FloatField(default=0.0)

    def __str__(self):
        return cls_str(self)


class PitcherStats(models.Model):
    player = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, null=True)
    bougyoritsu = models.FloatField(default=0.0)
    shiai = models.FloatField(default=0.0)
    shouri = models.FloatField(default=0.0)
    haiboku = models.FloatField(default=0.0)
    saves = models.FloatField(default=0.0)
    hold = models.FloatField(default=0.0)
    hp = models.FloatField(default=0.0)
    kanntou = models.FloatField(default=0.0)
    shouritsu = models.FloatField(default=0.0)
    dasha = models.FloatField(default=0.0)
    toukyuukai = models.FloatField(default=0.0)
    hiannda = models.FloatField(default=0.0)
    hihonnruida = models.FloatField(default=0.0)
    sikyuu = models.FloatField(default=0.0)
    deadball = models.FloatField(default=0.0)
    datsusannshinn = models.FloatField(default=0.0)
    datsusannshinnritsu = models.FloatField(default=0.0)
    shitten = models.FloatField(default=0.0)
    jisekitenn = models.FloatField(default=0.0)
    kannpuu = models.FloatField(default=0.0)
    mushikyuu = models.FloatField(default=0.0)
    whip = models.FloatField(default=0.0)
    dips = models.FloatField(default=0.0)
    kbb = models.FloatField(default=0.0)
    pfr = models.FloatField(default=0.0)
    hidr = models.FloatField(default=0.0)

    def __str__(self):
        return cls_str(self)


class MatchResult(models.Model):
    date = models.CharField(max_length=10)
    result = models.IntegerField(default=0)  # 勝ち: 1, 負け: 2
    score = models.CharField(max_length=20)
    team_year = models.ForeignKey(to=TeamYear, on_delete=models.DO_NOTHING)
    opponent = models.ForeignKey(to=Team, on_delete=models.DO_NOTHING)
    pitcher = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, null=True)
    year = models.CharField(max_length=10, null=True)

    def __str__(self):
        return cls_str(self)


class MatchMember(models.Model):
    match_result = models.ForeignKey(
        to=MatchResult, on_delete=models.DO_NOTHING)
    first = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="first", null=True)
    second = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="second", null=True)
    third = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="third", null=True)
    fourth = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="fourth", null=True)
    fifth = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="fifth", null=True)
    sixth = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="sixth", null=True)
    seventh = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="seventh", null=True)
    eighth = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="eights", null=True)
    nineth = models.ForeignKey(
        to=Player, on_delete=models.DO_NOTHING, related_name="nineth", null=True)

    def __str__(self):
        return cls_str(self)


class Ranking(models.Model):
    year = models.CharField(max_length=4)
    league = models.ForeignKey(
        to=League, on_delete=models.DO_NOTHING, null=True)
    first = models.ForeignKey(
        to=Team, on_delete=models.DO_NOTHING, related_name="first")
    second = models.ForeignKey(
        to=Team, on_delete=models.DO_NOTHING, related_name="second")
    third = models.ForeignKey(
        to=Team, on_delete=models.DO_NOTHING, related_name="third")
    fourth = models.ForeignKey(
        to=Team, on_delete=models.DO_NOTHING, related_name="fourth")
    fifth = models.ForeignKey(
        to=Team, on_delete=models.DO_NOTHING, related_name="fifth")
    sixth = models.ForeignKey(
        to=Team, on_delete=models.DO_NOTHING, related_name="sixth")

    def __str__(self):
        return cls_str(self)
