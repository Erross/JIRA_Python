from jira import JIRA

# instantiate jira
jira = JIRA(server='server', basic_auth=('userid', 'Password'))

issues = jira.fields()
jiracols = {}
#print(issues)
for i in issues:
    #print(i['name']+"_"+i['id'])
    jiracols[i['name']] = i['id']

print(jiracols)
for k,v in jiracols.items():
    print(k)
    print(v)
    print("NEXT!!")