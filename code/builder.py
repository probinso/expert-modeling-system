from pathlib import Path
import sys

from atmlibs.atm import ATMBuildHandler
from atmlibs.modelspec import ProgSpecification

def interface(specfile, dst):
    spec = ProgSpecification(specfile)
    dstpath = Path(dst)

    for document_type in spec:
        dt_spec = spec[document_type]

        handler = ATMBuildHandler(
            dt_spec.load_processed(dstpath),
            dt_spec.attributions_table,
            dt_spec.topics, dt_spec.iterations,
            dt_spec.key, dt_spec.expert_key,
        )

        handler.save(dt_spec, dst)
        #dt_spec.save_atm(dstpath, handler.model)
        #dt_spec.save_vocab(dstpath, handler.vocab)


def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        specfile, dst = sys.argv[1:]
    except:
        print("usage: {}  <spec.yaml>  <dest>".format(sys.argv[0]))
        sys.exit(1)
    interface(specfile, dst)


if __name__ == '__main__':
    cli_interface()
