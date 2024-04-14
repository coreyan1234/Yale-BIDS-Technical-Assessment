from flask import Flask, request, jsonify
import requests

app =  Flask(__name__)

# Third party endpoints
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SEARCH_ENDPOINT = BASE_URL + "esearch.fcgi?db=pubmed&retmode=json"
DETAILS_ENDPOINT = BASE_URL + "esummary.fcgi?db=pubmed&retmode=json"

@app.route('/search', methods=["GET"])
def search():
    num_results = request.args.get('num_results', default=10, type=int)
    search_url = f"{SEARCH_ENDPOINT}&term=cancer&retmax={num_results}"
    response = requests.get(search_url)
    data = response.json()
    return jsonify(data['esearchresult']['idlist'])

@app.route('/details', methods=['POST'])
def details():
    target_id = request.json['target_id']
    fields = request.json['fields']
    details_url = f"{DETAILS_ENDPOINT}&id={target_id}"
    response = requests.get(details_url)
    data = response.json()
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