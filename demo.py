import yaml
details = [{'name':'abc','age':'10'},{'name':'pqr','age':'20'}]
with open('config.yml','w') as file:
    yaml.dump(details,file)
print(open('config.yml').read())

"""details = [{'name':'abc','age':'10'},{'name':'pqr','age':'20'}]
print(yaml.dump(details))"""

#with open('config.yml', 'r') as file:
    #py_yml = yaml.safe_load(file)

#print(py_yml['prime_numbers'][3])
#print(py_yml['rest']['name'])
#print(py_yml['rest']['port'])
    