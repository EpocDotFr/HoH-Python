from HoH import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    battlenet_id = db.Column(db.Integer)
    username = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, nullable=True)

    account_region_id = db.Column(db.Integer, db.ForeignKey('account_region.id'))
    region = db.relationship('AccountRegion')

    heros = db.relationship('Hero', backref='account', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, battlenet_id, username, region, last_updated=None):
        self.battlenet_id = battlenet_id
        self.username = username
        self.region = region
        self.last_updated = last_updated

    def __repr__(self):
        return '<Account> #{} : {}'.format(self.id, self.username)

def already_exists(battlenet_id, username, account_region_id):
    return Account.query.filter_by(battlenet_id = battlenet_id, username = username, account_region_id = account_region_id).count() > 0