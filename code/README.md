# Expert Modeling System (EMS)

This code takes input text documents and a configuration file to describe
a learned recomender system for identifying experts. The following `config`
represents a list of required fields associates with a document_type.

```yaml
document_types:
  # list allows you to have multiple configs in one document
  - PFR

PFR:
  # the source data directory, all files mentioned should exist here
  datadir: /Users/philipr/git/jpl-playground/code/data
  # document data as a csv
  filename: PFR.csv
  # what columns to be used by preprocessor and agglomerator
  free_text_labels:
    - CorrectiveAction
    - Description
    - ExecutiveSummary
    - Title
  # column housing document identification number
  key: Anomaly_ID
  # author / document lookup table, must use `key` to describe document
  attributions: PFR_experts.csv
  # column housing candidates for attrubutions file
  expert_key: Users_ID
  # expert lookup table contains metadata on authors
  experts: expert_map.csv
  # importance fields to extract from experts file
  expert_labels:
    - First_Name
    - Middle_Name
    - Last_Name
    - Organization_Number
  list_resources: # used by pre-processor
    rules: rules.txt # list of regular expressions to drop
    protected: protected.txt   # list of words to not stem
    stopwords: stopwords.txt   # list of words to drop
    truncable: words_alpha.txt # list of words that can be stemmed
  # number of learned topics
  topics: 25
  # number of learning steps
  iterations: 251
```

Examples of minimal data as described by the config file.

`PFR.csv`

```csv
Anomaly_ID,CorrectiveAction,Description,ExecutiveSummary,Title
1111,"We did lots of stuff","Things needed to be done...","seems to work!","their tasks"
2222,"didn't do much stuff","nothing needed to be done...","ain't broke don't fix!","our tasks"
```

`PFR_experts.csv`

```csv
Anomaly_ID,Users_ID
1111,70000
2222,98231
2222,70000
```

`expert_map.csv`

```csv
Users_ID,First_Name,Middle_Name,Last_Name,Organization_Number
70000,Isaday,,Celia,5082
98231,Wilhelm,Marshal,Zagava,7823
```

`rules.txt`

```txt
&euro;
&nbsp;
\d\d\d\d-\d\d-\d\d
[\(\),\'\"\.:]
```

`protected.txt`

```txt
command
commanding
system
telemetry
```

`stopwords.txt`

```txt
the
he
them
```

`words_alpha.txt`

```txt
forgetfulness
cheerly
platinammine
floppies
cursillo
```

# Setup Environment

There is a patch to `gensim` which doesn't yet exist in their public release.
You will need to install the patched version.

```bash
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ pip install git+git://github.com/probinso/gensim
(venv) $ deactivate
$
```

# Building Model

```bash
$ source venv/bin/activate
(venv) $ python preprocess.py /path/to/config.yaml /path/to/datastore
(venv) $ python builder.py /path/to/config.yaml /path/to/datastore
(venv) $ tree --charset=ascii /path/to/datastore
/path/to/datastore
`-- PFR-60eb901ef84342b53322721d9b9fcf7f8b1eb7e1-t25-i251
    |-- model.atm
    |-- model.atm.expElogbeta.npy
    |-- model.atm.id2word
    |-- model.atm.state
    |-- processed.csv
    |-- stemmer.pickle
    |-- test_attrs.csv
    |-- test_docs.csv
    |-- train_attrs.csv
    |-- train_docs.csv
    `-- vocab.gensim

1 directory, 11 files
```

# Start API

```bash
(venv) $ open site/index.html
(venv) $ FLASK_APP=./expertapi.py FLASK_ENV=development flask run
```