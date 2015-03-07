from HoH import db

class AccountRegion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    slug = db.Column(db.Text)

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

    def __repr__(self):
        return '<AccountRegion> #{} : {}'.format(self.id, self.name)
