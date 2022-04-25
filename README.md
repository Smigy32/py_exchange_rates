It uses the following libraries:  
- [Requests](https://pypi.org/project/requests/) for requests to exchange rates;  
- [Matplotlib](https://pypi.org/project/matplotlib/) for building graphs.

# Quick Install / Usage
- --
`pip install git+https://github.com/Smigy32/py_exchange_rates`  

To get the NBU exchange rates of needed currency use the function
`get_nbu_exchange_rates(valcode, start_date: date, end_date: date = None, to_csv=False, to_json=False)`,  

To get PrivatBank exchange rates of needed currency use the function
`get_pb_exchange_rates(valcode: str, start_date: date, end_date: date = None, to_csv=False, to_json=False)`

#### Both functions take next parameters:
- **_valcode_**: Currency code  
- **_start_date_**: Start date of needed date range  
- **_end_date_**: End date of needed date range  
- **_to_csv_**: If this param's True the result will be written into a csv file  
- **_to_json_**: If this param's True the result will be written into a json file  

To build a graph that'll show the NBU and PrivatBank exchange rates for some date range use  
`graph_of_exchange_rates(valcode: str, start_date: date, end_date: date)`