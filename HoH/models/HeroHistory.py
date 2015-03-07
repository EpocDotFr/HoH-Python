from HoH import db

class HeroHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    life = db.Column(db.Integer)
    damage = db.Column(db.Integer)
    toughness = db.Column(db.Integer)
    healing = db.Column(db.Float)
    attack_speed = db.Column(db.Float)
    armor = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    vitality = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    physical_resist = db.Column(db.Integer)
    fire_resist = db.Column(db.Integer)
    cold_resist = db.Column(db.Integer)
    lightning_resist = db.Column(db.Integer)
    poison_resist = db.Column(db.Integer)
    arcane_resist = db.Column(db.Integer)
    crit_damage = db.Column(db.Float)
    block_chance = db.Column(db.Float)
    block_amount_min = db.Column(db.Integer)
    block_amount_max = db.Column(db.Integer)
    damage_increase = db.Column(db.Float)
    crit_chance = db.Column(db.Float)
    damage_reduction = db.Column(db.Float)
    thorns = db.Column(db.Integer)
    lifes_steal = db.Column(db.Integer)
    life_per_kill = db.Column(db.Integer)
    gold_find = db.Column(db.Float)
    magic_find = db.Column(db.Float)
    life_on_hit = db.Column(db.Integer)
    primary_resource = db.Column(db.Integer)
    secondary_resource = db.Column(db.Integer)
    level = db.Column(db.Integer)
    kills_elites = db.Column(db.Integer)
    paragon_level = db.Column(db.Integer)

    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))

    def __init__(self, timestamp, life, damage, toughness, healing, attack_speed, armor, strength, dexterity, vitality,
                 intelligence, physical_resist, fire_resist, cold_resist, lightning_resist, poison_resist, arcane_resist,
                 crit_damage, damage_reduction, thorns, lifes_steal, life_per_kill, gold_find, magic_find, life_on_hit,
                 primary_resource, secondary_resource, level, kills_elites, paragon_level, hero):
        self.timestamp = timestamp
        self.life = life
        self.damage = damage
        self.toughness = toughness
        self.healing = healing
        self.attack_speed = attack_speed
        self.armor = armor
        self.strength = strength
        self.dexterity = dexterity
        self.vitality = vitality
        self.intelligence = intelligence
        self.physical_resist = physical_resist
        self.fire_resist = fire_resist
        self.cold_resist = cold_resist
        self.lightning_resist = lightning_resist
        self.poison_resist = poison_resist
        self.arcane_resist = arcane_resist
        self.crit_damage = crit_damage
        self.damage_reduction = damage_reduction
        self.thorns = thorns
        self.lifes_steal = lifes_steal
        self.life_per_kill = life_per_kill
        self.gold_find = gold_find
        self.magic_find = magic_find
        self.life_on_hit = life_on_hit
        self.primary_resource = primary_resource
        self.secondary_resource = secondary_resource
        self.level = level
        self.kills_elites = kills_elites
        self.paragon_level = paragon_level
        self.hero = hero

    def __repr__(self):
        return '<HeroHistory> #{} : {}'.format(self.id, self.hero)
