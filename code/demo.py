from pathlib import Path
import sys
import json

from atmlibs.atm import ExpertTopicModel
from atmlibs.modelspec import ProgSpecification

def interface(specfile, dst, dtype, N):
    spec = ProgSpecification(specfile)[dtype]
    documents, attributions = spec.load_train(dst)
    targets = documents.sample(N).Anomaly_ID.tolist()
    print(attributions)
    experts = attributions[attributions.Anomaly_ID.isin(targets)]
    print(experts)

    anomalies = spec.raw_anomalies
    raw = anomalies[anomalies.Anomaly_ID.isin(targets)]
    return raw, experts, spec


def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        specfile, dst = sys.argv[1:]
    except:
        print("usage: {}  <spec.yaml>  <dest> <query.doc>".format(sys.argv[0]))
        sys.exit(1)

    raw, candidates, spec = interface(specfile, dst, 'ISA', 5)

    for _, row in raw.iterrows():
        row.to_json(f'{row.Anomaly_ID}.json')
        experts = candidates[candidates.Anomaly_ID == row.Anomaly_ID].Users_ID
        print(spec.get_expert_data(experts))
        input()

    print('*')


if __name__ == '__main__':
    cli_interface()
