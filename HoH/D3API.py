import requests
from HoH import db
from HoH.D3APIException import D3APIException
from HoH.models.HeroClass import HeroClass
from HoH.models.Account import Account
from HoH.models.Hero import Hero
from datetime import datetime

class D3API:
    endpoint = None
    username = None
    id = None
    region_id = None

    api_key = 'ng2ssgrqdcesswztm75d3qaz2g8yrqdw'
    locale = 'fr_FR'

    def __init__(self, region, region_id, username, id):
        self.endpoint = 'https://{}.api.battle.net/d3/'.format(region)

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
            if response_json.code == 'NOTFOUND':
                message = 'Ce compte Battle.net n\'existe pas.'
            else:
                message = response_json.reason + ' (' + response_json.code + ')'

            raise D3APIException(message)

        return response_json

    def import_profile(self):
        endpoint = self.endpoint + 'profile/{}-{}/'.format(self.username, self.id)

        response = self._call(endpoint)

        classes = {}

        hero_classes = HeroClass.query.all()

        for hero_class in hero_classes:
            classes[hero_class.slug] = hero_class.id

        now = datetime.now()

        account = Account(
            self.id,
            self.username,
            self.region_id,
            now
        )

        db.session.add(account)
        db.session.commit()

        for hero in response:
            hero = Hero(
                hero.id,
                hero.name,
                hero.gender,
                True if response.lastHeroPlayed == hero.id else False,
                True if hero.seasonal == 1 else False,
                True if hero.hardcore == 1 else False,
                account,
                classes[hero.get('class')],
            )

            db.session.add(hero)

        db.session.commit()