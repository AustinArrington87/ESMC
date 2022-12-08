# ESMC

API Steps
1: Obtain Client ID and Secret from ESMC / Heartland
2: Save environmental variables in .env file in working directory 
3: Add JSON with field boundaries and Producer Portal data
4: Run with examplePost.py iPython3 

Working with Data
Run Data/mrvQuery.py on a JSON file from MRVv1 / Producer Portal to explore the data being fed to models 

=====

Run mrvApi.py

$ python3
$ import mrvApi
$ c = mrvApi.configure(".env")
$ res = mrvApi.dndcGetProject("Missouri Partnership Pilot-11-22-22-17:22","MOCS.json")
