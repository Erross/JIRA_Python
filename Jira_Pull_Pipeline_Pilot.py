import swigpython3 as pilotbase  # for bare-metal stuff
import pilotpython  # nicer python classes
from jira import JIRA
import json


def onInitialize(ctxt):
    context = pilotpython.Context(ctxt)
    return pilotpython.READY_FOR_INPUT_OR_NEW_DATA


def onProcess(ctxt, dr):
    # First Bit here is pilot required, probably#
    context = pilotpython.Context(ctxt)
    data = pilotpython.DataRecord(dr)
    props = data.getProperties()
    # instatiate jira
    jira = JIRA(server='http://jira.monsanto.com', basic_auth=('$(username)', '$(password)'))

    # how big of a chunk to pull at a time
    block_size = 1000
    # where to start
    block_num = 0
    # one list to drop the issues into
    allissues = []
    alltickets = []
    addRecord = context.makeNewNode()
    addRecord.setName('record1')
    # loop through issues and append to list
    while True:
        start_idx = block_num * block_size
        issues = jira.search_issues('project=$(JiraBoard)', start_idx, block_size)
        if len(issues) == 0:
            # Retrieve issues until there are no more to come
            break

        block_num += 1
        for issue in issues:
            allissues.append(issue)
            x = issue.raw
            x = json.dumps(x)
            alltickets.append(x)
            addRecord.getProperties().defineStringProperty(issue.key, x)
            root = data.getRoot()
            root.appendChild(addRecord)

    # create a dict to put the changelogs in
    changelogs = {}

    for issue in allissues:
        # get the issue dictionary
        issuedict = (issue.__dict__)
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
                            itemhistory.append(
                                str('Date: ' + history.created + ' From:' + item.fromString + ' To:' + item.toString))
                            changelogs[issuedict[i]] = itemhistory

    # This bit pushes out the data on a single record as nodes - which seems the easiest option for getting out data from a single pull. Use detach nodes and process in pilot.
    addRecord = context.makeNewNode()
    addRecord.setName('record')
    for k, v in changelogs.items():
        # props.defineStringArrayProperty(k,v)
        addRecord.getProperties().defineStringArrayProperty(k, v)
        root = data.getRoot()
        root.appendChild(addRecord)

    return pilotpython.READY_FOR_INPUT_OR_NEW_DATA


def onFinalize(ctxt):
    context = pilotpython.Context(ctxt)
    None