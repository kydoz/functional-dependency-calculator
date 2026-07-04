# Functional Dependency Calculator (work in progress)

A program which calculates the verified functional dependencies (**fd**s) in a given table. File types supported are: `.csv` and `.xlsx`.  

To note:  
Even though this script can give many useful insights concerning the fds that are verified, the results still require verification to be of any use.
Take a simple example, a table with cities and people living there. We are given this example table:  

```
city,name
Paris,John
New York,John
London,Jenny
```

It is easy to conclude from this table (and our program does too) that the single fd verified in this table is $\text{city} \ \rightarrow \ \text{name}$. However, it is up to us to verify if in the given context if it would really be possible retrieve someone's name by the city they are in.  

## Setup

For it's ease of use, it is recommended to run the script in a Python Virtual Environment. In this setup guide only the unix setup instructions will be detailled. For further details and Windows setup instructions check out [this guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for example.  

#### 1. Create (and enter) a python virtual environment with:

```bash
python3 -m venv .venv; source .venv/bin/activate
```

#### 2. Install requirements:

```bash
pip install -r requirements.txt
```

## Usage

The following instructions can also be found when executing the program without any arguments.

#### With .csv files

```
python3 fd_calc.py <file_name>.csv 
```

#### With .xlsx files

```
python3 fd_calc.py <file_name>.xlsx <sheet_name> (optional)
```

If the sheet name isn't given, the user is prompted with the list of available sheets.  
