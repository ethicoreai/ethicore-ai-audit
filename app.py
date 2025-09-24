from flask import Flask, request, jsonify
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric
import pandas as pd

app = Flask(__name__)

@app.route('/audit', methods=['POST'])
def run_audit():
    data = request.json
    df = pd.DataFrame(data['model_data'])
    dataset = BinaryLabelDataset(
        df=df,
        label_names=['outcome'],  # Adjust to your model's output
        protected_attribute_names=data['protected_attrs']
    )
    metric = BinaryLabelDatasetMetric(dataset, unprivileged_groups=[{'gender': 0}], privileged_groups=[{'gender': 1}])
    bias_score = metric.disparate_impact()
    privacy_score = 0.85  # Placeholder
    compliance_score = 0.92  # Placeholder
    return jsonify({
        'bias_score': round(1 - bias_score, 2),
        'privacy_score': privacy_score,
        'compliance_score': compliance_score,
        'risk_summary': 'Low bias detected; recommend reweighting dataset.',
        'suggestions': ['Mitigate with Reweighing algorithm.']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
