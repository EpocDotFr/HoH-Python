from HoH import db

class HeroClass(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slug = db.Column(db.Text)
    name_female = db.Column(db.Text)
    name_male = db.Column(db.Text)

    def __init__(self, slug, name_female, name_male):
        self.slug = slug
        self.name_female = name_female
        self.name_male = name_male

    def __repr__(self):
        return '<HeroClass> #{} : {}'.format(self.id, self.slug)
