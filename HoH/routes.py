# coding=utf-8
from requests import HTTPError
from HoH import app
from HoH import db
from HoH.D3APIException import D3APIException
from HoH.models.Account import Account, already_exists as account_already_exists
from HoH.models.Hero import Hero
from HoH.models.AccountRegion import AccountRegion
from flask import render_template, abort, jsonify, request
from datetime import datetime
import time
from D3API import D3API

# Accueil (sélection et import de compte)
@app.route('/')
def home():
    return render_template('home.html', accounts=Account.query.all(), regions=AccountRegion.query.all())

# Import de compte
@app.route('/account', methods=['POST'])
def import_account():
    account_region_id = request.form['account_region_id']
    battlenet_id = request.form['battlenet_id']
    username = request.form['username']

    account_region = AccountRegion.query.get(account_region_id)

    if (account_already_exists(battlenet_id, username, account_region_id)):
        result = {'result': 'failure', 'data': {'message': 'Ce compte a déjà été importé.'}}
        return jsonify(result)

    try:
        d3api = D3API(account_region, username, battlenet_id)

        d3api.import_profile()

        result = {'result': 'success', 'data': {'message': 'Compte importé avec succès ! La page va maintenant s\'actualiser.'}}
    except HTTPError as httpe:
        result = {'result': 'failure', 'data': {'message': httpe.message}}
    except D3APIException as d3apie:
        result = {'result': 'failure', 'data': {'message': d3apie.message}}

    return jsonify(result)

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
    account = Account.query.get(account_id)

    if account is None:
        result = {'result': 'failure', 'data': {'message': 'Ce compte n\'existe pas.'}}
        return jsonify(result)

    hero = Hero.query.get(hero_id)

    if hero is None:
        result = {'result': 'failure', 'data': {'message': 'Ce Héro n\'existe pas.'}}
        return jsonify(result)

    if (hero.last_updated is not None and hero.last_updated.date() == datetime.today().date()):
        result = {'result': 'failure', 'data': {'message': 'Vous avez déjà actualisé ce Héros aujourd\'hui. Vous ne pouvez l\'actualiser qu\'une fois par jour.'}}
        return jsonify(result)

    try:
        d3api = D3API(account.region, account.username, account.battlenet_id)

        d3api.refresh_hero(hero)

        result = {'result': 'success', 'data': {'message': 'Héros actualisé. La page va maintenant s\'actualiser.'}}
    except HTTPError as httpe:
        result = {'result': 'failure', 'data': {'message': httpe.message}}
    except D3APIException as d3apie:
        result = {'result': 'failure', 'data': {'message': d3apie.message}}

    return jsonify(result)


# Récupération de données pour graphiques héros vue globale
@app.route('/account/<int:account_id>/hero/<int:hero_id>/datatype/<datatype>')
def account_hero_data(account_id, hero_id, datatype = None):
    account = Account.query.get(account_id)

    if account is None:
        result = {'result': 'failure', 'data': {'message': 'Ce compte n\'existe pas.'}}
        return jsonify(result)

    hero = Hero.query.get(hero_id)

    if hero is None:
        result = {'result': 'failure', 'data': {'message': 'Ce Héro n\'existe pas.'}}
        return jsonify(result)

    data = []

    if datatype == 'resists':
        data.append([])
        data.append([])
        data.append([])
        data.append([])
        data.append([])
        data.append([])

        for history in hero.history:
            timestamp = time.mktime(history.timestamp.timetuple()) * 1000

            data[0].append({'x': timestamp, 'y': history.physical_resist})
            data[1].append({'x': timestamp, 'y': history.fire_resist})
            data[2].append({'x': timestamp, 'y': history.cold_resist})
            data[3].append({'x': timestamp, 'y': history.lightning_resist})
            data[4].append({'x': timestamp, 'y': history.poison_resist})
            data[5].append({'x': timestamp, 'y': history.arcane_resist})
    elif datatype == 'life':
        data.append([])
        data.append([])
        data.append([])
        data.append([])

        for history in hero.history:
            timestamp = time.mktime(history.timestamp.timetuple()) * 1000

            data[0].append({'x': timestamp, 'y': history.life})
            data[1].append({'x': timestamp, 'y': history.life_per_kill})
            data[2].append({'x': timestamp, 'y': history.life_on_hit})
            data[3].append({'x': timestamp, 'y': history.healing})
    elif datatype == 'percentages':
        data.append([])
        data.append([])
        data.append([])
        data.append([])
        data.append([])
        data.append([])
        data.append([])

        for history in hero.history:
            timestamp = time.mktime(history.timestamp.timetuple()) * 1000

            data[0].append({'x': timestamp, 'y': history.crit_damage})
            data[1].append({'x': timestamp, 'y': history.block_chance})
            data[2].append({'x': timestamp, 'y': history.damage_increase})
            data[3].append({'x': timestamp, 'y': history.crit_chance})
            data[4].append({'x': timestamp, 'y': history.gold_find})
            data[5].append({'x': timestamp, 'y': history.lifes_steal})
            data[6].append({'x': timestamp, 'y': history.magic_find})

    result = {'result': 'success', 'data': data}
    return jsonify(result)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html', error=error)