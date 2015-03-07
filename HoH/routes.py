# coding=utf-8
from HoH import app
from HoH import db
from HoH.models.Account import Account
from HoH.models.Hero import Hero
from HoH.models.AccountRegion import AccountRegion
from flask import render_template, abort, jsonify

# Accueil (sélection et import de compte)
@app.route('/')
def home():
    return render_template('home.html', accounts=Account.query.all(), regions=AccountRegion.query.all())

# Import de compte
@app.route('/account', methods=['POST'])
def import_account():
    return ''

# Détails d'un compte avec liste des héros
@app.route('/account/<int:account_id>')
def account_details(account_id):
    account = Account.query.get(account_id)

    if account is None:
        abort(404, {'message': 'Ce compte n\'existe pas.'})

    return render_template('account.html', account=account)

# Actualisation d'un compte
@app.route('/account/<int:account_id>', methods=['POST'])
def account_update(account_id):
    return ''

# Suppression d'un compte
@app.route('/account/<int:account_id>', methods=['DELETE'])
def account_delete(account_id):
    account = Account.query.get(account_id)

    if account is None:
        result = {'result': 'failure', 'data': {'message': 'Ce compte n\'existe pas.'}}
    else:
        try:
            db.session.delete(account)
            db.session.commit()

            result = {'result': 'success', 'data': {'message': 'Compte supprimé. Vous allez être redirigé(e) vers l\'accueil.'}}
        except:
            result = {'result': 'failure', 'data': {'message': 'Une erreur est survenue lors de la suppression du compte.'}}

    return jsonify(result)

# Détails d'un héros d'un compte
@app.route('/account/<int:account_id>/hero/<int:hero_id>')
def account_hero_details(account_id, hero_id):
    account = Account.query.get(account_id)

    if account is None:
        abort(404, {'message': 'Ce compte n\'existe pas.'})

    hero = Hero.query.get(hero_id)

    if hero is None:
        abort(404, {'message': 'Ce héro n\'existe pas.'})

    return render_template('hero.html', account=account, hero=hero)

# Actualisation d'un héros
@app.route('/account/<int:account_id>/hero/<int:hero_id>', methods=['POST'])
def account_hero_update(account_id, hero_id):
    return ''

# Récupération de données pour graphiques héros vue globale
@app.route('/account/<int:account_id>/hero/<int:hero_id>/datatype/<datatype>')
def account_hero_data(account_id, hero_id, datatype):
    return ''

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html', error=error)