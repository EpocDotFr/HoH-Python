from HoH import db

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    battlenet_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.Integer)
    lastly_played = db.Column(db.Boolean)
    seasonal = db.Column(db.Boolean)
    hardcore = db.Column(db.Boolean)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    hero_class_id = db.Column(db.Integer, db.ForeignKey('hero_class.id'))
    hero_class = db.relationship('HeroClass')

    history = db.relationship('HeroHistory', backref='hero', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, battlenet_id, name, gender, lastly_played, seasonal, hardcore, account, hero_class, last_updated=None):
        self.battlenet_id = battlenet_id
        self.name = name
        self.gender = gender
        self.lastly_played = lastly_played
        self.seasonal = seasonal
        self.hardcore = hardcore
        self.account = account
        self.hero_class = hero_class
        self.last_updated = last_updated

    def __repr__(self):
        return '<Hero> #{} : {}'.format(self.id, self.name)
