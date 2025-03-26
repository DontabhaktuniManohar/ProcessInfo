from flask import Blueprint, jsonify, request
from data import data_list

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/deployment', methods=['GET'])
def get_deployment():
    bgflag = request.args.get('bgflag')
    environment = request.args.get('environment')

    filtered_list = [item for item in data_list if item.get("environment") == environment and item.get("bgflag") == bgflag]

    # Return only the FIRST match if it exists
    result = filtered_list[0] if filtered_list else {}

    return jsonify(result)
