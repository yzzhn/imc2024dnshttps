# DNS HTTPS Resource Records: An End-to-End Perspective 

This repo contains artifact for our group's IMC 2024 publication: `Exploring the Ecosystem of DNS HTTPS Resource Records: An End-to-End Perspective.` 

---

## Table of Contents
1. [Dataset](#dataset)
1. [Installation](#installation)
2. [Folder Directory](#folder-directory)
3. [Usage](#usage)
5. [License](#license)
6. [Citation](#citation)
---
## Dataset

Our group plans to keep updating DNS HTTPS records for the Tranco 1 million domains on a monthly basis. For further information please vist our group's website: https://keyinfra.cs.virginia.edu/dns_http/

---
## Installation

To run this project, you need to install the required packages. We recommend setting up a virtual environment.

Step 1: Clone the Repository

```bash
git clone https://github.com/yzzhn/imc2024dnshttps.git
cd imc2024dnshttps
```

Step 2: Set up a Virtual Environment (Optional)
Create a virtual environment to keep dependencies isolated.

```bash
python3 -m venv env
source env/bin/activate
```

Step 3: Install Required Packages
Install the necessary packages listed below.

```
pip install jupyterlab matplotlib pandas numpy dnspython
```

This will install:
```
* JupyterLab - for interactive notebooks
* Matplotlib - for data visualization
* Pandas, Numpy - for data manipulation
* Dnspython - for dns records parsing
```

Step 4: Launch JupyterLab
```
jupyter lab
```
---

### Folder Directory

```
imc2024dnshttps/
│
├── notebooks/               # Jupyter notebooks for analysis
│   ├── *_adoption.ipynb     # DNS HTTPS RR adoption rate
│   ├── *_dnssec.ipynb       # signed and authenticated DNS HTTPS RR rate
│   └── *_ech.ipynb          # DNS HTTPS RR with ECH configuration
│
├── data/                    # Data files used in the project
│   ├── raw/                 # Raw data files
|   |  ├── 2023-05/*         # montly folders
|   |  ├── 2023-06/*
|   |  └── .../
│   └── processed/           # Processed data files
│
├── src/                     # Source code for the project
│   ├── scpt_*.py            # Script for data processing for dynamic trancon 1m list
│   └── scpt_*_overlap.py    # Script for data processing for overlapped domains
│
├── README.md                # Project description and instructions
├── requirements.txt         # List of dependencies
└── LICENSE                  # License for the project

```
---

### Usage

#### 1. Visualization
   
Data visualization does not require the download of data. Just launch JupyterLab and run notebooks in `notebook` directory.

#### 2. Download data and reprocess.

Please download data at https://keyinfra.cs.virginia.edu/ and save the data in `data/raw` directory.
Then run all scripts in `src/` to get new statistics. 

### Citation
If you are using our data or code, please cite us:

```
todo: update
```
