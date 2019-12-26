import os
from flask import Flask, Request, Response, jsonify, json, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug import secure_filename
#import unicodedata

app = Flask(__name__)
auth = HTTPBasicAuth()

cards = [
            {
                "id": 1,
                "title": u"Buy groceries",
                "description": u"Milk, Cheese, Pizza, Fruit, Tylenol",
                "done": False,
                "images_name": "image01.jpg"
            },
            {
                "id": 2,
                "title": u"Learn Python",
                "description": u"Need to find a good Python tutorial on the web",
                "done": False,
                "images_name": "image02.jpg"
            },
            {
                "id": 3,
                "title": u"Learn Office 365",
                "description": u"Office 365 in advance learning",
                "done": False,
                "images_name": "image03.jpg"
            }
        ]

class hawkeyes():   
    

    def __init__(self, app):
    

        #START GET METHOD

        @app.route("/hawkeyes/api/v0.0.1", methods=["GET"])
        def index():
            api_message = {
                "name": "HAWKEYES API",
                "version": "0.0.1",
                "description": "Hawkeyes is the web api for extract string from business card images",
                "released_date": "16 December, 2019"
            }

            data = {
                "success": "Request success",
                "api": api_message
            }

            resp = jsonify(data)
            resp.status_code = 200            

            return resp

        @app.route("/hawkeyes/api/v0.0.1/cards", methods=["GET"])
        @auth.login_required
        def get_cards():
            data = {
                "success": "Request success",
                "cards": [make_public_card(card) for card in cards]
            }

            resp = jsonify(data)
            resp.status_code = 200

            return resp

        @app.route("/hawkeyes/api/v0.0.1/cards/<int:card_id>", methods=["GET"])
        def get_card(card_id):
            card = [card for card in cards if card["id"] == card_id]

            if len(card) == 0:
                abort(404)

            data = {
                "success": "Request success",
                "card": card[0]
            }

            resp = jsonify(data)
            resp.status_code = 200

            return resp

        #END GET METHOD

        #START POST METHOD
        @app.route("/hawkeyes/api/v0.0.1/cards", methods=["POST"])
        def create_card():
            if not request.json or not "title" in request.json:
                abort(400)

            card = {
                "id": cards[-1]["id"] + 1,
                "title": request.json["title"],  
                "description": request.json.get("description", ""), #We tolerate a missing description field by set to "" (blank)
                "done": False   #we assume the done field will always start set to False
            }

            cards.append(card)

            data = {
                "success": "Successfully created",
                "card": card
            }

            resp = jsonify(data)
            resp.status_code = 201

            return resp  

        #END POST METHOD

        #START PUT METHOD 
        @app.route("/hawkeyes/api/v0.0.1/cards/<int:card_id>", methods=["PUT"])
        def update_card(card_id):
            card = [card for card in cards if card["id"]==card_id]

            if len(card) == 0:
                abort(404)

            if not request.json:
                abort(400)

            if "title" in request.json and type(request.json["title"]) != str:
                abort(400)

            if "description" in request.json and type(request.json["description"]) is not str:
                abort(400)

            if "done" in request.json and type(request.json["done"]) is not bool:
                abort(400)

            '''
            Update the new value from request to selected item
            '''
            card[0]["title"] =  request.json.get("title", card[0]["title"])
            card[0]["description"] = request.json.get("description", card[0]["description"])
            card[0]["done"] = request.json.get("done", card[0]["done"])   

            data = {
                "success": "Successfully updated",
                "card": card[0],
                "types_params": {
                    "title": str(type(request.json["title"])),
                    "description": str(type(request.json["description"])),
                    "done": str(type(request.json["done"]))
                }
            }


            resp = jsonify(data)
            resp.status_code = 200

            return resp

        #END PUT METHOD

        #START DELETE METHOD
        @app.route("/hawkeyes/api/v0.0.1/cards/<int:card_id>", methods=["DELETE"])
        def delete_card(card_id):
            card = [card for card in cards if card["id"]==card_id]

            if len(card)==0:
                abort(404)
            
            cards.remove(card[0])

            data = {
                "success": "Successfully deleted",
                "cards": cards
            }

            resp = jsonify(data)
            resp.status_code = 200

            return resp

        #END DELETE METHOD

        #START ERROR HANDLER AREA
        @app.errorhandler(404)
        def not_found(error):

            data = {
                "error": "404 error",
                "message": "Not found : " + request.url
            }

            resp = jsonify(data)
            resp.status_code = 404
            return resp
        #END ERROR HANDLER AREA
       


        #START AUTHENTICATION AND AUTHORIZATION AREA
        @app.route("/hawkeyes/api/v0.0.1/users/<string:user_id>", methods=["GET"])
        def api_users(user_id):
            users = {
                "1": "john",
                "2": "steve",
                "3": "bill",
                "4": "phillips",
                "5": "bushes"
            }

            user = None

            if user_id in users:
                user = users[user_id]


            if user == None:
                abort(404)

            data = {
                "success": "Request success",
                "user": users[user_id],
                "lenuser": len(user),
                "user": user,
                "typeuser": str(type(user))
            }

            resp = jsonify(data)
            resp.status_code = 200

            return resp

        @auth.get_password
        def get_password(username):
            users = [{

            }]

            if username == "tempo":
                return "test"

            return None

        #Send authentication error back to client 
        @auth.error_handler
        def unauthorized():
            data = {
                "error": "401 error",
                "message": "Unauthorized access"
            }

            resp = jsonify(data)
            resp.status_code = 401

            return resp

        #END AUTHENTICATION AND AUTHORIZATION AREA


        #START UTILITIES FUNCTION AREA
        def make_public_card(card):
            new_card = {}
            for field in card:
                if field=="id":
                    new_card["uri"] = url_for("get_cards", card_id=card["id"], _external=True)
                else:
                    new_card[field] = card[field]

            return new_card
        #END UTILITIES FUNCTION AREA


        #UPLOAD FILE AREA
        def allowed_file(filename):
            data = "." in filename and \
                filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

            return data

        @app.route("/hawkeyes/api/v0.0.1/uploads", methods=["POST"])
        def upload_file():
            
            file = request.files["file"]
            
            data = {                   
                "method": str(request.method) + " : " + str(request.url),
                "file": str(request.files),
                "filename": file.filename
            }

            if request.method == "POST":
                if "file" not in request.files:
                     data["error"]  = "The upload files not found"   
                

                if file.filename == "": 
                    data["error"]  = "The upload files not found" 

                if file and allowed_file(file.filename):
                    filename = file.filename

                    #filename = secure_filename(filename)                    

                    #file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    contents = ""
                    with open(filename,"rb") as f:
                        contents = f.read() 
                    
                    # with open(os.path.join(app.config["UPLOAD_FOLDER"], filename), "w", encoding="utf8") as f:
                    #     f.write(contents)                    

                    data["success"] = "Upload successfully " + str(app.config["UPLOAD_FOLDER"] + "\\" + filename)
                else:
                    data["error"] = "Files could not allowed"              

            
            resp = jsonify(data)
            resp.status_code = 200
                       
            return resp
                
        #UPLOAD FILE AREA

        #READ AND WRITE FILE AREA
        def read_file(file):
            with open(file, encoding="utf8") as f:
                contents = f.read()                

        def write_file(file):
            with open(filename, "w", encoding="utf8") as f:
                f.write()
        #READ AND WRITE FILE AREA

        

