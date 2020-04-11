## This repo contains python scripts to process charity commission data. 

#### Set Up

1) Download the charity commission data and convert to .csv using instructions in this repo - https://github.com/ncvo/charity-commission-extract
2) Git clone this repository 
3) Install requirements.txt. Can be done using virtual environment.
4) Move all .csv converted files from charity commission repo to `/extracts`directory contained in this repo. 
5) Run `python3 charity_data_processing.py` to process the data. 
    - The file will generate .csv files with 
    name, contact info, areas of operation
    - .csv files are saved in a new directory `/outputs`
    - A new file is created for each class of charity specified. These can be 
   defined in the list `control_group` in line 8 of `charity_data_processing.py`. Add more/less as you wish. 
   - I have cleaned this data a lot (removed subsidiares, only included current charities, cleaned text)
   - The data contains mixed data types in certain columns. This makes the script
   quite slow. I have provided a logging system to try and provide the user as much information as possible. I am getting in touch with the CC to try and sort this out. 

#### Other information

- All metadata of the charity commision  http://data.charitycommission.gov.uk/data-definition.aspx 