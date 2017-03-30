import httpcodes
import logging
import json
import os
import pickle
from flask import Flask, request, render_template, redirect, g, send_from_directory, url_for

# Create exportable app
app = Flask(__name__)
app.troops = {'Augment Gorilla': {'Move': 8, 'Fight': 3, 'Shoot': 0, 'Shield': 10, 'Morale': 2, 'Health': 8, 'Cost': 20,
                                  'Notes': 'Animal, Cannot carry treasure or items'},
              'Lackey': {'Move': 6, 'Fight': 2, 'Shoot': 0, 'Shield': 10, 'Morale': -1, 'Health': 10, 'Cost': 20,
                         'Notes': 'Melee Weapon'},
              'Security': {'Move': 6, 'Fight': 2, 'Shoot': 1, 'Shield': 12, 'Morale': 2, 'Health': 12, 'Cost': 80,
                           'Notes': 'Blaster, Blade'},
              'Engineer': {'Move': 4, 'Fight': 0, 'Shoot': 3, 'Shield': 12, 'Morale': 2, 'Health': 10, 'Cost': 60,
                           'Notes': 'Blaster, Repair Kit'},
              'Medic': {'Move': 5, 'Fight': 0, 'Shoot': 0, 'Shield': 12, 'Morale': 3, 'Health': 10, 'Cost': 50,
                        'Notes': 'Blade, Medkit'},
              'Commando': {'Move': 8, 'Fight': 4, 'Shoot': 0, 'Shield': 10, 'Morale': 4, 'Health': 12, 'Cost': 100,
                           'Notes': 'Stealth Suit, Blade, Needle Gun'},
              'Combat Droid': {'Move': 3, 'Fight': 2, 'Shoot': 4, 'Shield': 14, 'Morale': 0, 'Health': 14, 'Cost': 150,
                               'Notes': 'Mechanoid, Dual Blaster, Claws'},
              }
app.wizard = {
    'Captain': {'Move': 5, 'Fight': 2, 'Shoot': 2, 'Shield': 12, 'Morale': 4, 'Health': 12, 'Cost': 0, 'Skillset': [],
                'Specialism': None, 'Items': [], 'Experience': 0}}
app.apprentice = {'Ensign': {'Move': 7, 'Fight': 0, 'Shoot': -1, 'Shield': 10, 'Morale': 2, 'Health': 8, 'Skillset': [],
                             'Specialism': None, 'Cost': 250, 'Items': [], 'Experience': 0}}
app.specialisms = ['Engineering', 'Psychology', 'Marksman', 'Tactics', 'Melee', 'Defence']
app.skillsets = {'Engineering': ['Repair', 'Sabotage', 'Augment'], 'Psychology': ['Bolster', 'Terror', 'Counter'],
                 'Marksman': ['Aim', 'Pierce', 'Reload'], 'Tactics': ['Squad', 'Ambush', 'Surround'],
                 'Melee': ['Block', 'Risposte', 'Dual'], 'Defence': ['Shield', 'Sacrifice', 'Resolute']}
app.weapon = {'Blaster': 0, 'Needle Gun': 0, 'Blade': 0, 'Cannon': 0, 'Whip': 0}
app.cost = {'Blaster': 5, 'Needle Gun': 12, 'Blade': 3, 'Cannon': 15, 'Whip': 5}

app.login_name = ""


@app.route('/', methods=['GET', 'POST'])
def login():
    if not os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")):
        os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"))

    if not os.path.isfile(
            os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), "usersfile")):
        createduser = dict()
        createduser["inital_account"] = "123"
        pickle.dump(createduser,
                    open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), "usersfile"),
                         "wb"))

    loadedusers = pickle.load(
        open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), "usersfile"), "rb"))
    if request.method == 'GET':
        return render_template('login.html', users=loadedusers), httpcodes.OK
    if request.method == 'POST':
        name = request.form['username']
        app.login_name = name
        return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    loadedusers = pickle.load(
        open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), "usersfile"), "rb"))
    if request.method == 'GET':
        return render_template('register.html', users=loadedusers), httpcodes.OK
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        os.mkdir(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), username))
        loadedusers[username] = password
        pickle.dump(loadedusers,
                    open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), "usersfile"),
                         "wb"))
        return render_template('register.html', users=loadedusers), httpcodes.CREATED


@app.route('/new', methods=['GET', 'POST'])
def new_warband():
    if request.method == 'GET':
        if app.login_name == "":
            return redirect(url_for('login'))
        else:
            bands = os.listdir(
                os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), app.login_name))
            return render_template('blankband.html', bands=bands, people=app.troops, wizard=app.wizard,
                                   apprentice=app.apprentice,
                                   specs=app.specialisms, skills=app.skillsets, weaps=app.weapon,
                                   costs=app.cost), httpcodes.OK
    if request.method == 'POST':
        bands = os.listdir(
            os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), app.login_name))
        bandname = request.form['bandname']
        treasury = request.form['treasury']
        ispublic = request.form['isPublic']
        mbnumber = request.form['mbNumber']
        capspec = request.form['capspec']
        capskill = request.form['capskill']
        capweap1 = request.form['capweap1']
        capweap2 = request.form['capweap2']
        troops = json.loads(request.form['troops'])
        createdband = dict()
        createdband['Name'] = bandname
        createdband['isPublic'] = ispublic
        createdband['mbNumber'] = mbnumber
        createdband['Captain'] = dict(app.wizard['Captain'])
        createdband['Captain']['Specialism'] = capspec
        createdband['Captain']['Skillset'] = []
        createdband['Captain']['Skillset'].append(capskill)
        createdband['Captain']['Items'] = []
        createdband['Captain']['Items'].append(capweap1)
        createdband['Captain']['Items'].append(capweap2)
        if 'hasensign' in request.form.keys():
            ensspec = request.form['ensspec']
            ensskill = request.form['ensskill']
            ensweap = request.form['ensweap']
            createdband['Ensign'] = dict(app.apprentice['Ensign'])
            createdband['Ensign']['Specialism'] = ensspec
            createdband['Ensign']['Skillset'] = []
            createdband['Ensign']['Skillset'].append(ensskill)
            createdband['Ensign']['Items'] = []
            createdband['Ensign']['Items'].append(ensweap)
        createdband['Troops'] = []
        for item in troops:
            if item != "Empty":
                createdband['Troops'].append(item)
        createdband['Treasury'] = treasury
        pickle.dump(createdband,
                    open(os.path.join(
                        os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"),
                                     app.login_name),
                        bandname), "wb"))
        return render_template('blankband.html', bands=bands, people=app.troops, wizard=app.wizard,
                               apprentice=app.apprentice,
                               specs=app.specialisms, skills=app.skillsets, weaps=app.weapon,
                               costs=app.cost), httpcodes.CREATED


@app.route('/index', methods=['GET'])
def home():
    if request.method == 'GET':
        if app.login_name == "":
            return redirect(url_for('login'))
        else:
            return render_template('index.html', users=app.login_name), httpcodes.OK


@app.route('/edit', methods=['GET'])
def edit_warband():
    if request.method == 'GET':
        if app.login_name == "":
            return redirect(url_for('login'))
        else:
            bands = os.listdir(
                os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), app.login_name))
            return render_template('bandlist.html', bands=bands), httpcodes.OK


def check_public(rootDir):
    if not os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands")):
        os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands"))
    else:
        for file in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands")):
            if file == "puclicbands":
                os.remove(
                    os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands"), "publicbands"))

    public_bands = dict()
    flag = 0
    for users in os.listdir(rootDir):
        if users != app.login_name:
            path = os.path.join(rootDir, users)
            if os.path.isdir(path):
                bands_list = []
                for bands in os.listdir(path):
                    loadedpublicbands = pickle.load(
                        open(os.path.join(
                            os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), users),
                            bands), "rb"))
                    if loadedpublicbands['isPublic'] == "public":
                        bands_list.append(bands)
                if len(bands_list) > 0:
                    flag = 1
                    public_bands[users] = bands_list
    if flag == 0:
        public_bands['0'] = '0'

    pickle.dump(public_bands,
                open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands"), "publicbands"),
                     "wb"))


@app.route('/view', methods=['GET'])
def view_warband():
    if request.method == 'GET':
        if app.login_name == "":
            return redirect(url_for('login'))
        else:
            check_public(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"))
            bands = pickle.load(
                open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands"), "publicbands"),
                     "rb"))
            return render_template('viewlist.html', bands=bands), httpcodes.OK


@app.route('/view/<user>/<band>', methods=['GET'])
def view_given_warband(user, band):
    if request.method == 'GET':
        if app.login_name == "":
            return redirect(url_for('login'))
        else:
            loadedband = pickle.load(
                open(
                    os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), user),
                                 band),
                    "rb"))
            return render_template('viewband.html', owner=user, band=loadedband, people=app.troops, wizard=app.wizard,
                                   apprentice=app.apprentice, specs=app.specialisms, skills=app.skillsets,
                                   weaps=app.weapon), httpcodes.OK


@app.route('/edit/<band>', methods=['GET', 'POST'])
def edit_given_warband(band):
    if request.method == 'GET':
        if app.login_name == "":
            return redirect(url_for('login'))
        else:
            loadedband = pickle.load(
                open(os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), app.login_name),
                    band),
                    "rb"))
            bandlist = os.listdir(
                os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), app.login_name))
            return render_template('editband.html', bandlist=bandlist, band=loadedband, people=app.troops,
                                   wizard=app.wizard,
                                   apprentice=app.apprentice, specs=app.specialisms, skills=app.skillsets,
                                   weaps=app.weapon, costs=app.cost), httpcodes.OK
    if request.method == 'POST':
        loadedband = pickle.load(
            open(os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"), app.login_name),
                band),
                "rb"))
        bandname = request.form['bandname']
        treasury = request.form['treasury']
        ispublic = request.form['isPublic']
        mbnumber = request.form['mbNumber']
        capspec = request.form['capspec']
        skills = json.loads(request.form['capskill'])
        capweap1 = request.form['capweap1']
        capweap2 = request.form['capweap2']
        troops = json.loads(request.form['troops'])
        capmov = request.form['capmove']
        capfig = request.form['capfight']
        capsho = request.form['capshoot']
        capshi = request.form['capshield']
        capmor = request.form['capmorale']
        caphea = request.form['caphealth']
        capexp = request.form['capexperience']
        createdband = dict()
        createdband['Name'] = bandname
        createdband['isPublic'] = ispublic
        createdband['mbNumber'] = mbnumber
        createdband['Captain'] = dict(app.wizard['Captain'])
        createdband['Captain']['Specialism'] = capspec
        createdband['Captain']['Skillset'].extend(skills)
        createdband['Captain']['Items'] = []
        createdband['Captain']['Items'].append(capweap1)
        createdband['Captain']['Items'].append(capweap2)
        createdband['Captain']['Move'] = capmov
        createdband['Captain']['Fight'] = capfig
        createdband['Captain']['Shoot'] = capsho
        createdband['Captain']['Shield'] = capshi
        createdband['Captain']['Morale'] = capmor
        createdband['Captain']['Health'] = caphea
        createdband['Captain']['Experience'] = capexp
        if 'hasensign' in request.form.keys():
            createdband['Ensign'] = dict(app.apprentice['Ensign'])
            if 'fireensign' in request.form.keys():
                ensspec = loadedband['Ensign']['Specialism']
                eskills = json.loads(request.form['ensskill'])
                createdband['Ensign']['Skillset'].extend(eskills)
            else:
                ensspec = request.form['ensspec']
                eskills = request.form['ensskill']
                createdband['Ensign']['Skillset'] = []
                createdband['Ensign']['Skillset'].append(eskills)
            ensmov = request.form['ensmove']
            ensfig = request.form['ensfight']
            enssho = request.form['ensshoot']
            ensshi = request.form['ensshield']
            ensmor = request.form['ensmorale']
            enshea = request.form['enshealth']
            ensexp = request.form['ensexperience']
            ensweap = request.form['ensweap']
            createdband['Ensign']['Specialism'] = ensspec
            createdband['Ensign']['Items'] = []
            createdband['Ensign']['Items'].append(ensweap)
            createdband['Ensign']['Move'] = ensmov
            createdband['Ensign']['Fight'] = ensfig
            createdband['Ensign']['Shoot'] = enssho
            createdband['Ensign']['Shield'] = ensshi
            createdband['Ensign']['Morale'] = ensmor
            createdband['Ensign']['Health'] = enshea
            createdband['Ensign']['Experience'] = ensexp
        createdband['Troops'] = []
        for item in troops:
            if item != "Empty":
                createdband['Troops'].append(item)

        createdband['Treasury'] = treasury
        pickle.dump(createdband,
                    open(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users"),
                                                   app.login_name), bandname),
                         "wb"))
        return redirect(url_for("edit_warband"))


@app.route('/delete/<band>', methods=['GET'])
def delete_given_warband(band):
    if request.method == 'GET':
        if app.login_name == "":
            return redirect(url_for('login'))
        else:
            os.remove(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "users", ), app.login_name,
                                   band))
            return redirect(url_for('edit_warband'))


@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        app.login_name = ""
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
