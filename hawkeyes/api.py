from flask import Flask, Request, Response, jsonify, json, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

class hawkeyes():
    def __init__(self, app):

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


    #START AUTHENTICATION AND AUTHORIZATION AREA
    @app.route("/hawkeyes/api/v0.0.1/users/<string:user_id>", methods=["GET"])
    #END AUTHENTICATION AND AUTHORIZATION AREA


        

