# Goodall: PPRL experiment management and analysis
This branch contains the code for the demonstration
_"SecUREmatch: Integrating Clerical Review in Privacy-Preserving Record Linkage"_ at the [SIGMOD 2025](https://2025.sigmod.org/index.shtml) conference.

[Demonstration video](https://cloud.scadsai.uni-leipzig.de/index.php/s/jin4W4JymPq58wt)

The demonstration is based on the protocol introduced in 
_"Multi-Layer Privacy-Preserving Record Linkage with Clerical Review based on gradual information disclosure"_
by Florens Rohde, Victor Christen, Martin Franke and Erhard Rahm ([Paper](https://doi.org/10.18420/BTW2025-18)).

## Getting started
### Prerequisites
- Python 3.12
- Poetry
- Running [PPRL Services](https://github.com/floroh/pprl-services/tree/sigmod-2025)
- CSV datasets in `datasets` directory in the repository base

Download datasets
```shell
cd data
./download_datasets.sh
```

### Installation
Install dependencies using [poetry](https://python-poetry.org/docs/)
```shell
cd scripts
poetry install
```

### Usage
Import plaintext datasets to the data owner service
```shell
poetry shell
python3 -m goodall.01_import_plaintext_datasets
```

Start Streamlit UI:
```shellr
poetry shell
python3 -m streamlit run goodall/ui/PPRL_Services_UI.py
```

## Development

### Update PPRL services API
Use the helper scripts to update the clients.
The scripts expect running PPRL Services on localhost on ports :8081 (do), :8082 (lu), :8085 (pm).

```shell
./api/update_client_do.sh
./api/update_client_lu.sh
./api/update_client_pm.sh
```
