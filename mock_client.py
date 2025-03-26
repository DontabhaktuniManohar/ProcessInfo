from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
data_list = [
    {
        "artifact": "microser",
        "commit": "23h4r4f",
        "bgflag": "Green",
        "deploymentstatus": "success",
        "deployby": "kiran",
        "environment" : "SIT4"
    },
    {
        "artifact": "microser",
        "commit": "23h4r4f",
        "bgflag": "Green",
        "deploymentstatus": "success",
        "deployby": "kiran3",
        "environment" : "SIT3"
    },
    {
        "artifact": "microser",
        "commit": "23h4r4f",
        "bgflag": "Green",
        "deploymentstatus": "success",
        "deployby": "kiran2",
        "environment" : "SIT2"
    },
    {
        "artifact": "microser",
        "commit": "23h4rdec4f",
        "bgflag": "Blue",
        "deploymentstatus": "success",
        "environment" : "SIT5",
        "deployby": "raj"
    },
    {
        "artifact": "weblic",
        "commit": "fr3afv",
        "bgflag": "Blue",
        "deploymentstatus": "success",
        "deployby": "raj",
        "environment" : "SIT5"
    },
    {
        "artifact": "weblic",
        "commit": "fr3afkiranv",
        "bgflag": "Blue",
        "deploymentstatus": "success",
        "deployby": "KIRAN4",
        "environment" : "SIT4"
    },
    {
        "artifact": "weblic",
        "commit": "fr3afkiranv",
        "bgflag": "NA",
        "deploymentstatus": "success",
        "deployby": "KIRAN4",
        "environment" : "PROD"
    },
    {
        "artifact": "weblic",
        "commit": "fr3afkiranv",
        "bgflag": "NA",
        "deploymentstatus": "success",
        "deployby": "KIRAN4",
        "environment" : "PROD"
    },
    {
        "artifact": "weblic",
        "commit": "fr3afkiranv",
        "bgflag": "NA",
        "deploymentstatus": "success",
        "deployby": "KIRAN4",
        "environment" : "CANARY"
    },
    {
        "artifact": "weblic",
        "commit": "fr3afkiranv",
        "bgflag": "NA",
        "deploymentstatus": "success",
        "deployby": "KIRAN4",
        "environment" : "PRODE"
    }
]

@app.route('/api/deployment', methods=['GET'])
def get_deployment():
    bgflag = request.args.get('bgflag')
    environment = request.args.get('environment')

    filtered_list = data_list

    # Apply filters if query params are present
    if bgflag:
        filtered_list = [item for item in filtered_list if item.get("bgflag") == bgflag]
    if environment:
        filtered_list = [item for item in filtered_list if item.get("environment") == environment]

    # Return only the FIRST match if it exists
    result = filtered_list[0] if filtered_list else {}

    print("Response:", result)
    print (type(result))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
