import json

# LOAD DATA 
file = open('Corteva4Fields.json')
data = json.load(file)

assets = []
projects = []
producers = []
prod_ids = []
fields = []
practices = []

for ass in data:
    assets.append(ass["assets"])

for proj in data:
    projects.append(proj["project"])

for prod in data:
    producers.append(prod["producers"])

print("PROJECT: ", projects[0])
print("ASSETS: ")
for ass in assets:
    print(ass)
print("============PRODUCERS==================")
for prod in producers[0]:
    print(prod["user_by_project_id"], "| Producer Agreement: ", prod["has_agreed_to_producer_agreement"])
    fields.append(prod['fields'])
    for field in fields:
        #print(field)
        for f in field:
            print(f['field_by_project_id'])
            practices.append(f["field_practice_changes"])
            for prac in practices:
                for p in prac:
                    print(p['name'])
            practices.clear()
            print("___________________________________")
    print("===================================")
    field.clear()
