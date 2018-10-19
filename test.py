import json

data = [{'id':123,'entities':{'url':'python.org','hashtags':['#python','#pythonjp']}}]
print(json.dumps(data,indent=2))