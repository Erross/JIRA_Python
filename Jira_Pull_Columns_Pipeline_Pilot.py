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
    jira = JIRA(server='server', basic_auth=('$(username)', '$(password)'))
    issues = jira.fields()
    jiracols = {}
    for i in issues:
        # print(i['name']+"_"+i['id'])
        jiracols[i['name']] = i['id']

    # This bit pushes out the data on a single record as nodes - which seems the easiest option for getting out data from a single pull. Use detach nodes and process in pilot.
    addRecord = context.makeNewNode()
    addRecord.setName('record')
    for k, v in jiracols.items():
        # props.defineStringArrayProperty(k,v)
        addRecord.getProperties().defineStringProperty(k, v)
        root = data.getRoot()
        root.appendChild(addRecord)

    return pilotpython.READY_FOR_INPUT_OR_NEW_DATA


def onFinalize(ctxt):
    context = pilotpython.Context(ctxt)
    None