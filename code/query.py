from pathlib import Path
import sys
import json

from atmlibs.atm import ExpertTopicModel
from atmlibs.modelspec import ProgSpecification

def document_interface(specfile, dst, dtype, document, N=10):
    spec = ProgSpecification(specfile)
    dstpath = Path(dst)

    dt_spec = spec[dtype]
    model = ExpertTopicModel(dt_spec, dstpath)

    experts = model.get_experts(document)
    return dt_spec.get_expert_data(experts).head(N)

def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        specfile, dst, document = sys.argv[1:]
    except:
        print("usage: {}  <spec.yaml>  <dest> <query.doc>".format(sys.argv[0]))
        sys.exit(1)
    with open(document, 'r') as fd:
        print(document_interface(specfile, dst, 'ISA', json.load(fd)))


if __name__ == '__main__':
    cli_interface()
