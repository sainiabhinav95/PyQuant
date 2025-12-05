# PyQuant 

### A Quantitative Finance Library written in Python  
Created by Abhinav Saini  
Licensed under MIT License  

## PyPi Link:
https://pypi.org/project/python-quant/

## Installation:
#### Virtual Environment Method:  
Create a virtual environment anywhere: 

>python -m venv .venv

Activate it:  

>source .venv/bin/activate

Install the package:

>pip install python_quant    
>python_quant --help

Start the Web App:
>python_quant --web_app


Command Line Usage:

Download the input_data folder from the repo and place it anywhere. We need to pass it to the commandline tool:  

>python_quant --mode RISK --instrument input_data/eq_option/bsm_eq_option.json --input_data_path input_data/market_data --as_of_date 20251010 --verbose D

#### System-wide Installation:
Directly install using pip:
> pip install python_quant  




#### Sample Output (BSM Pricing):
<blockquote>  
RISK MODE OUTPUT  

price: 12.0  
delta: 0.3588137600913187  
gamma: 0.006817273571226615  
theta: -54.71301088919908  
rho: 16.650438655983557  
vega: 44.71555242847439

</blockquote>
