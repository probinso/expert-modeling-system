#!/usr/bin/env python
from functools import partial, reduce
from operator import itemgetter, attrgetter
import pickle
from pathlib import Path
import sys

from atmlibs.modelspec import ProgSpecification
from atmlibs.utility import compose, TemporaryDirectory


def process_spec_and_build_stemmer(spec, keep=[], target='TARGET'):
    df = spec.raw_anomalies

    agglomerate = spec.AgglomerateProcessor()
    rule_filters = spec.RegexProcessor()
    stemmer = spec.FreshStemmer()

    process = compose(agglomerate, rule_filters, stemmer.stem_document)

    df[target] = df.apply(process, axis=1).apply(stemmer.unstem_document)

    return df[[spec.key, target] + keep], stemmer


def save(dst, doc, stemmer):
    doc.to_csv(dst / f'processed.csv', index=False)
    with open(dst / f'stemmer.pickle', 'wb') as fd:
        pickle.dump(stemmer, fd)


def interface(specfile, dst):
    spec = ProgSpecification(specfile)
    dstpath = Path(dst)

    for document_type in spec:
        dt_spec = spec[document_type]
        doc, stemmer = process_spec_and_build_stemmer(spec[document_type])
        dt_spec.save_processed(dstpath, doc)
        dt_spec.save_stemmer(dstpath, stemmer)


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
