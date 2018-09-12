# Subject Matter Expert - Topic Modeling

A description of this project proposal can be found [here](./proposal/report.tex). To build
this as a `pdf`, run `make` from the `./proposal/` directory.

# Loading Data

In order to insure that there aren't data leaks, we have added a `./data/` directory and a
coorepsonding `.gitignore`. All contibutors should request required data over a more secure
channel. Required data files must be located in the `./data/` directory in order to have
consistant directory tree.

If you plan to load data into this directory, please add its description to this listed
summary.

**If you do not update this list, then contributors will not know what to request.**

- `ldap.json` employee ldap metadata
- `prs.csv` problem reporting system documents
- `prs_signatures.csv` signers for each `anomoly_id`
- `html_escape_characters.csv` list of escaped html characters



- `PRS_M2020_Tier_Structure_160609.csv`
- `PRS_MSL_Tier_Structure_160609.csv`
