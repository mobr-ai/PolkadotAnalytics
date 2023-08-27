# Polkadot Analytics Platform

Empowering the Polkadot community with a comprehensive analytics platform that provides natural language querying, supported by formal knowledge representations, and customizable dashboards for holistic data analyses.

<br>

# The concept

The Polkadot Analytics Platform aims at building a comprehensive data analysis and visualization tool for the Polkadot ecosystem. The platform will allow users to retrieve and analyze data from various Polkadot-related sources (e.g., different parachains and components such as browser wallets), aligned with the POnto ontology [1, 2, 3]. Users will be able to specify their queries using a controlled natural language (CNL), and the platform will provide a query engine to process these queries. Additionally, the platform will provide a UI to support constructing queries and visualizing informative artifacts that represent query results. As well as support for composing customizable dashboards using these artifacts.

[1] POnto source code: https://github.com/mobr-ai/POnto

[2] POnto documentation: https://www.mobr.ai/ponto

[3] POnto scientific paper: http://arxiv.org/abs/2308.00735

<br>

# How to run locally (see section a) or on docker (see section b)

## First of all, clone this repository: 
```
git clone https://github.com/mobr-ai/PolkadotAnalytics.git
```

<br>

## a. Run locally on your computer

<br>

## a.1) install dependencies

```bash
# python packages
pip install -r requirements.txt

# POnto flat file: 
wget https://raw.githubusercontent.com/mobr-ai/ponto/main/src/flat/POnto.ttl

# Fuseki and jena: 
# on mac
brew install fuseki jena

# or you can get the binaries on
https://jena.apache.org/download/ 
```

## a.2) fuseki and http servers

```bash
# run fuseki server
fuseki-server --update --tdb2

# run http flask server
python app.py
```

<br>

## b. Run on docker

```bash
# building our Jena-Fuseki image
# from the root of this repository go to the jena-fuseki subdir
cd jena-fuseki
docker build -t mobr/fuseki . --no-cache

# for Mac users: specify platform if you're using a mac with apple chip (M1 or M2)
cd jena-fuseki
docker build -t mobr/fuseki . --platform linux/x86_64/v2 --no-cache

# go back to the root dir to build and run the images
cd ..
docker compose build
docker compose up
```

# How to access the services

using your browser, you can access:
- the fuseki server frontend: http://127.0.0.1:3030
- the platform frontend: http://127.0.0.1:5000
- the platform swagger UI: http://127.0.0.1:5000/swagger

# How to test

```bash
# first make sure you have pytest
pip install pytest

# then make sure you have fuseki-server running
fuseki-server --update --tdb2

# now you can start testing...

# testing http endpoints
python -m pytest pap/tests/test_app.py

# testing kb crud operations
python -m pytest pap/tests/test_kb.py

# testing dataset crd operations
python -m pytest pap/tests/test_dataset.py

# runing all tests
python -m pytest pap/tests
```

# Python code documentation

Documentation of python source code available on ./docs/pap

The documentation was generated automatically using pdoc3

To regenerate it use the following command

```bash
# make sure you have pdoc3 installed
#     pip install pdoc3
pdoc --html -o docs pap
```
