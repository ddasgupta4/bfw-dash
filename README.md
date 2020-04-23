# bfw-dash

[! https://img.shields.io/github/license/ddasgupta4/bfw-dash] [! https://img.shields.io/badge/Made%20at-Starschema-red]
A short description of the project.


## Running locally

To run a development instance locally, create a virtualenv, install the 
requirements from `requirements.txt` and launch `app.py` using the 
Python executable from the virtualenv.


## TODO

- [x] Fix layout to emphasize graphs
- [x] Move data table section to take up less space
- [x] Fix callback error
- [x] Configure global filters for data
    - Add more filters (age, subgroup, etc.)
    - Fix filter style
- [ ] Create more visualizations
    - ROC Curve
    - Summary table
    - Confusion Matrix
    - DET Curves 
    - SDM
- [ ] Make all tabs/callbacks trigger after upload data
    - Right now uploading new data works, but the datatable/graphs don't update unless they're clicked
- [x] Add instructions, github, report to "more" in header
- [ ] Add warning/error message when data is invalid
- [ ] Add more styling to CSS to avoid inline styling in app.py
    - Reduce clutter and increase readability