from jira import JIRA

#instatiate jira
jira = JIRA(server='server', basic_auth=('username', 'password'))


# Returns a generator to yield issues
def issue_gen(project, block_size=100):

    # Get initial issues
    cur_index = 0
    issues = jira.search_issues("project={}".format(project), cur_index, block_size, expand='changelog')

    # Loop through until there are no issues
    while issues:
        cur_index += block_size
        for x in issues:
            yield x

        # Get next block of issues
        issues = jira.search_issues("project={}".format(project), cur_index, block_size, expand='changelog')

def format_item(item, created):
    return "Date: {created} From: {item.fromString} To: {item.toString}"

changelogs = {}
for issue in issue_gen("RFC", 1000):
    x = []
    for history in issue.changelog.histories:
        changelogs[issue.key] = [format_item(item, history.created) for item in history.items if item.field == "status"]

print(changelogs)