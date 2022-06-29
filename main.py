#L'EXPLICATION EN CLAIR VOUS EST PROPOSE DANS LE DOCUMENT WORD                          ////////////////////////////////////////////////////////////////


from bson import json_util           #BSON est l'abréviation de "Binary JSON" et est la sérialisation codée en binaire de documents de type JSON.

from flask import Flask              # Cette instruction permet d’importer la bibliothèque Flask, qui est disponible par défaut sous Anaconda,
from flask import request            # le request (Le package requests permet d’effectuer programmatiquement des requêtes HTTP)
from flask import jsonify            # jsonify permet de retourner des JSON data

from pymongo import MongoClient

import json                          #JSON permet de représenter des données structurées

import matplotlib.pyplot as plt

# JSON (JavaScript Objet Notation) est un langage léger d'échange de données textuelles. Pour les ordinateurs, ce format se génère et s'analyse facilement.
# Pour les humains, il est pratique à écrire et à lire grâce à une syntaxe simple et à une structure en arborescence.




# Creation de  l’objet application Flask, qui contient les données de l’application et les méthodes
# correspondant aux actions susceptibles d’être effectuées sur l’objet.

app = Flask(__name__)


cluster = MongoClient("mongodb+srv://Rene:Rene123456789@cluster0.m0c58.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


db = cluster["universities_db"]                                                  #link to the database
collection = db["universities_ranking"]                                          #connexion to the collection of the database



#############################      GET                 #####################

# L'instruction indique à Flask que la fonction home correspond au chemin /.
@app.route('/', methods=['GET'])
def home():
    return '''<p><h2 align = "center" color = "red" > <font color = "blue">BIENVENU SUR LA PLATEFORME DEVELOPPE PAR </font> </p></h2>
<p><h3 align = "center">Dinin René Lothaire BAZIE</h3></p>
'''



# L'instruction indique à Flask que la fonction getUniversitiesNumber correspond au chemin /GET/number_students.
@app.route('/GET/usa_universities', methods=['GET'])
def getUniversities():
    USA_universities = list(collection.find({ "location":"United States"}))
    return "LES UNIVERSITES AMERICAINES : \n \n "\
           + json.dumps(USA_universities, default=json_util.default)



# L'instruction indique à Flask que la fonction getUniversitiesNumberStudent correspond au chemin /GET/number_universities_students
@app.route('/GET/number_universities_students', methods=['GET'])
def getUniversitiesNumberStudent():
    USA_universities_Number = collection.count_documents({"number students":{"$gte" :"20,000"}})
    return "NOMBRE D'UNIVERSITES AVEC PLUS DE 20000 ETUDIANTS : \n \n "+\
           json.dumps(USA_universities_Number, default=json_util.default)



# L'instruction indique à Flask que la fonction universitiespercountries correspond au chemin /GET/universitiespercountries
#AGGREGATION -->le nombre d'universités par pays et par ordre decroissant
@app.route('/GET/universitiespercountries', methods=['GET'])
def universitiespercountries():
    u = list(collection.aggregate([
    {"$group":{"_id":"$location", "nombre" : { "$sum" : 1}}},
    {"$sort": {"nombre" : -1}}
    ]))

    # récupérer nos informations
    nb = []
    country = []
    for i in u:
        nb.append(i["nombre"])
        country.append(i["_id"])

    # Création du graphe
    plt.figure(figsize=(30, 10))
    plt.bar(country, nb, color='blue', width=0.4)
    plt.xlabel("location")
    plt.ylabel("nombre")
    plt.title("le nombre d'universités par pays et par ordre decroissant")
    plt.show()

    return "NOMBRE D'UNIVERSITES PAR PAYS ET PAR ODRE DECROISSANT : \n \n "+ json.dumps(u, default=json_util.default)




#Le nombre d'université dont la moitié des etudiants est composée d'etrangers
@app.route('/GET/number_strange_students', methods=['GET'])
def StrangeStudents():
    strange_students = collection.count_documents({"perc intl students":{"$gte" :"75%"}})
    return "NOMBRE D'UNIVERSITES OU LES 3/4 DES ETUDIANTS SONT DES ETRANGERS: \n \n "\
           + json.dumps(strange_students, default=json_util.default)




################################      POST                 #####################


# L'instruction indique à Flask que la fonction add_university correspond au chemin /add.
@app.route('/add', methods=['POST'])

def api_response():

    if request.method == 'POST':
        message = add_university()
        return message

def add_university():
    new = json.loads(request.data)
    ranking = new.get("ranking")
    title = new.get("title")
    location = new.get("location")
    number_students = new.get("number_students")
    students_staff_ratio = new.get("students_staff_ratio")
    perc_intl_students = new.get("perc_intl_students")
    gender_ratio = new.get("gender_ratio")

    condition = collection.find_one({"ranking" : ranking})

    if condition :
        return jsonify({"message" : "This university is already mentionned"})
    else :
        collection.insert_one({"ranking":ranking, "title" : title, "location":location,"number students":number_students,
                        "students staff ratio":students_staff_ratio,"perc intl students":perc_intl_students, "gender ratio":gender_ratio})
        return jsonify({'msg' : "university successfully ADDED !"})



##############################      DELETE                 #####################



# L'instruction indique à Flask que la fonction remove correspond au chemin /delete_universities.
@app.route('/delete_universities', methods=['DELETE'])

def api_delete():
    if request.method == 'DELETE':
        message = remove()
        return message

def remove():

   new = json.loads(request.data)
   ranking = new.get("ranking")
   title = new.get("title")
   location = new.get("location")
   number_students = new.get("number_students")
   students_staff_ratio = new.get("students_staff_ratio")
   perc_intl_students = new.get("perc_intl_students")
   gender_ratio = new.get("gender_ratio")

   condition = collection.find_one({"ranking": ranking})

   if condition:
       collection.delete_one(
           {"ranking": ranking, "title": title, "location": location, "number students": number_students,
            "students staff ratio": students_staff_ratio, "perc intl students": perc_intl_students,
            "gender ratio": gender_ratio})
       return jsonify({'msg': "university successfully REMOVED !"})
   else :
       return jsonify({"message" : "this ranking doesn't exist in the database"})




###############################      PUT                 #####################


# L'instruction indique à Flask que la fonction update correspond au chemin /delete_universities.
@app.route('/update_universities', methods=['PUT'])

def api_update():
    if request.method == 'PUT':
        message = update()
        return message

def update():

   new = json.loads(request.data)
   ranking = new.get("ranking")
   title = new.get("title")
   location = new.get("location")
   number_students = new.get("number_students")
   students_staff_ratio = new.get("students_staff_ratio")
   perc_intl_students = new.get("perc_intl_students")
   gender_ratio = new.get("gender_ratio")

   condition = collection.find_one({"ranking": ranking})

   if condition:
       collection.update_one(
           {"ranking": ranking}, {"$set": {"title": title, "location": location, "number students": number_students,
                                           "students staff ratio": students_staff_ratio,
                                           "perc intl students": perc_intl_students,
                                           "gender ratio": gender_ratio}}, upsert=False)
       return jsonify({'msg': "university successfully UPDATED !"})

   else :
       return jsonify({'msg' : "University does not exist !"})


#lance le débogueur, ce qui permet d’afficher un message autre que « Bad Gateway » s’il y a une erreur dans l’application.
app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run()                 #permet d’exécuter l’application.
