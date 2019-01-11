from jira import JIRA
import json
#instatiate jira
jira = JIRA(server='server', basic_auth=('username', 'password'))

#how big of a chunk to pull at a time
block_size = 1000
#where to start
block_num = 0
#one list to drop the issues into
allissues = []

#loop through issues and append to list
while True:
    start_idx = block_num*block_size
    issues = jira.search_issues('project=RFC', start_idx, block_size)
    if len(issues) == 0:
        # Retrieve issues until there are no more to come
        break

    block_num += 1
    for issue in issues:
        allissues.append(issue)

allraw = []
for issue in allissues:
    x = allissues[1].raw
    x = json.dumps(x)
    allraw.append(x)

print(len(allraw))
