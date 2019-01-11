from jira import JIRA

# instantiate jira
jira = JIRA(server='server', basic_auth=('username', 'password'))

# how big of a chunk to pull at a time
block_size = 1
# where to start
block_num = 0
# one list to drop the issues into
allissues = []

# loop through issues and append to list
while True:
    start_idx = block_num*block_size
    issues = jira.search_issues('project=RFC', start_idx, block_size,expand='renderedFields')
    if block_num ==1:
    #if len(issues) == 0:
        # Retrieve issues until there are no more to come
        break

    block_num += 1
    for issue in issues:
        allissues.append(issue)
        print(issue.fields.__dict__)

# create a dict to put the changelogs in
changelogs = {}

for issue in allissues:
    # get the issue dictionary
    issuedict = (issue.fields)
    # loop over the dict to do the needful
    for i in issuedict:
        # grab the key to get at the changelog
        if i == 'key':
            issue2 = jira.issue(issuedict[i], expand='changelog')
            changelog = issue2.changelog
            itemhistory = []
            # create ungodly strings to append to the item history because I only pretend to be a developer
            for history in changelog.histories:
                for item in history.items:
                    if item.field == 'status':
                        itemhistory.append(str('Date: ' + history.created + ' From:' + item.fromString + ' To:' + item.toString))
                        changelogs[issuedict[i]] = itemhistory

# need to put change logs into some sort of thing that I can then parse in python or in pilot
print(changelogs)