# coding=utf-8
import requests
from HoH import db
from HoH.D3APIException import D3APIException
from HoH.models.HeroClass import HeroClass
from HoH.models.Account import Account
from HoH.models.Hero import Hero
from HoH.models.HeroHistory import HeroHistory
from datetime import datetime

class D3API:
    endpoint = None
    username = None
    id = None
    region_id = None
    region = None

    api_key = 'uevsvyrvw5qw6tksskk8r7em73ghbjck'
    locale = 'fr_FR'

    def __init__(self, region, region_id, username, id):
        self.endpoint = 'https://{}.api.battle.net/d3/'.format(region)

        self.region = region
        self.username = username
        self.id = id
        self.region_id = region_id

    def _call(self, endpoint):
        endpoint = endpoint + '?locale={}&apikey={}'.format(self.locale, self.api_key)

        headers = {
            'Accept': 'application/json',
            'User-Agent': 'History of Heroes Python Requests/'+requests.__version__
        }

        response = requests.get(endpoint, headers=headers)

        response.raise_for_status()

        response_json = response.json()

        if 'code' in response_json:
            if response_json['code'] == 'NOTFOUND':
                message = 'Ce compte Battle.net n\'existe pas.'
            else:
                message = response_json['reason'] + ' (' + response_json['code'] + ')'

            raise D3APIException(message)

        return response_json

    def import_profile(self):
        endpoint = self.endpoint + 'profile/{}-{}/'.format(self.username, self.id)

        response = self._call(endpoint)

        now = datetime.now()

        account = Account(
            self.id,
            self.username,
            self.region,
            now
        )

        db.session.add(account)

        for hero in response:
            hero_class = Hero.query.filter(slug=hero.get('class')).first()

            hero = Hero(
                hero.id,
                hero.name,
                hero.gender,
                True if response.lastHeroPlayed == hero.id else False,
                True if hero.seasonal == 1 else False,
                True if hero.hardcore == 1 else False,
                account,
                hero_class
            )

            db.session.add(hero)

        db.session.commit()

    def refresh_account(self):
        pass # TODO

    def refresh_hero(self, hero):
        endpoint = self.endpoint + 'profile/{}-{}/hero/{}'.format(self.username, self.id, hero.battlenet_id)

        response = self._call(endpoint)

        bnet_last_updated = datetime.fromtimestamp(response.get('last-updated'))
        hoh_last_updated = hero.last_updated

        if hero.last_updated and bnet_last_updated <= hoh_last_updated:
            raise D3APIException('Aucune actualisation n\'est nécéssaire, vous n\'avez pas joué avec ce Héros depuis la dernière actualisation.')

        hero_history = HeroHistory(
            datetime.now(),
            response.stats.life,
            response.stats.damage,
            response.stats.toughness,
            response.stats.healing,
            response.stats.attackSpeed,
            response.stats.armor,
            response.stats.strength,
            response.stats.dexterity,
            response.stats.vitality,
            response.stats.intelligence,
            response.stats.physicalResist,
            response.stats.fireResist,
            response.stats.coldResist,
            response.stats.lightningResist,
            response.stats.poisonResist,
            response.stats.arcaneResist,
            response.stats.critDamage,
            response.stats.blockChance,
            response.stats.blockAmountMin,
            response.stats.blockAmountMax,
            response.stats.damageIncrease,
            response.stats.critChance,
            response.stats.damageReduction,
            response.stats.thorns,
            response.stats.lifeSteal,
            response.stats.lifePerKill,
            response.stats.goldFind,
            response.stats.magicFind,
            response.stats.lifeOnHit,
            response.stats.primaryResource,
            response.stats.secondaryResource,
            response.level,
            response.kills.elites,
            response.paragonLevel,
            hero
        )

        hero.last_updated = datetime.now()

        db.session.add(hero_history)
        db.session.add(hero)
        db.session.commit()