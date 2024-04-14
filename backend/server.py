from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app =  Flask(__name__)
CORS(app)

# Third party endpoints
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SEARCH_ENDPOINT = BASE_URL + "esearch.fcgi?db=pubmed&retmode=json"
DETAILS_ENDPOINT = BASE_URL + "esummary.fcgi?db=pubmed&retmode=json"

@app.route('/search', methods=["GET"])
def search():
    # Get the number of results to return
    num_results = request.args.get('num_results', default=10, type=int)
    # Create the URL for the search endpoint with term=cancer and number of results
    search_url = f"{SEARCH_ENDPOINT}&term=cancer&retmax={num_results}"
    response = requests.get(search_url)
    data = response.json()
    # Get the list of Ids from the response
    id_list = data['esearchresult']['idlist']
    return jsonify(id_list)

@app.route('/details', methods=['POST'])
def details():
    # Get target id and fields
    target_id = request.json['target_id']
    fields = request.json['fields']
    print("Fields:", fields)
    # Create the URL for the details endpoint with the target id
    details_url = f"{DETAILS_ENDPOINT}&id={target_id}"
    response = requests.get(details_url)
    data = response.json()
    # Get the details from the response
    result = {}
    for field in fields:
        if field == 'ID':
            result['ID'] = data['result'][target_id]['uid']
        elif field == 'Title':
            result['Title'] = data['result'][target_id]['title']
        elif field == 'Authors':
            result['Authors'] = data['result'][target_id]['authors']
        elif field == 'Publication Date':
            result['Publication Date'] = data['result'][target_id]['pubdate']
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)