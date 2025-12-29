from flask import Flask, request, jsonify
import joblib
import pandas as pd
import HostBasedFeature
import LexicalFeature
import CleanData

app = Flask(__name__)

# Load the trained model
model = joblib.load("SimpleModel_final.sav")

def run_urlscan_api_withID(url):
    scan_id = HostBasedFeature.API_urlscan_post(url)
    final = {"status": 400,}
    result = None
    if scan_id:
        print("URLScan.io Scan ID:", scan_id)
        result = HostBasedFeature.API_urlscan_get(scan_id)
        if result is None:
            final = {"status": 400,}
        else:
            final = HostBasedFeature.print_scan_result(result)
    return final,scan_id, result


def preprocess_url(url):
    Features = {}
    try:
        Lexical = LexicalFeature.lexical_feature(url)
        Host, scanID , jsonOri = run_urlscan_api_withID(url)

        Features.update(Lexical)
        Features.update(Host)
        df = pd.DataFrame([Features])

        # returns the original DF, scanID and the json
        return df,scanID,jsonOri
    except Exception as e:
        print(f"Error occurred: {e}")

        raise


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data['url']

    # Preprocess the URL
    processed_data,scanID,jsonOri = preprocess_url(url)

    if not processed_data.empty:
        processed_data['status'] =  processed_data['status'].astype(int)
        if (processed_data['status'] == 200).any():
            # Clean the data
            cleaned_data = CleanData.clean_data_test(processed_data)
            # Make predictions
            predictions = model.predict(cleaned_data)
            prediction_results = ["Malicious" if prediction == 1 else "Benign" for prediction in predictions]
            response = {
                'url': url,
                'predictions': prediction_results
            }
        else:
            response = {
                'error': 'Failed to preprocess URL'
            }
    else:
        response = {
            'error': 'Failed to preprocess URL'
        }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)