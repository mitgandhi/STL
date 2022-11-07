
import adsk.core, adsk.fusion, adsk.cam, traceback
from adsk import core

ui = None
tbPanel = None
Button = None
handlers = []

def CommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:


        except:
            ui = adsk.core.Application.get().userInterface
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
    try:
        app = adsk.core.Application.get()
        global ui
        ui = app.userInterface

        workSpace = ui.workspaces.itemById('FusionSolidEnvironment')
        tbPanels = workSpace.toolbarPanels

        global tbPanel
        tbPanel = tbPanels.itemById('NewPanel')
        if tbPanel:
            tbPanel.deleteMe()
        tbPanel = tbPanels.add('NewPanel', 'Export', 'SelectPanel', False)

        # Empty panel can't be displayed. Add a command to the panel
        cmdDef = ui.commandDefinitions.itemById('STLExport')
        if cmdDef:
            cmdDef.deleteMe()
        cmdDef = ui.commandDefinitions.addButtonDefinition('STLExport', 'STL Export', 'STL Export Button')
        tbPanel.controls.addCommand(cmdDef)

        onCreated = CommandCreatedEventHandler()
        cmdDef.commandCreated.add(onCreated)
        handlers.append(onCreated)





        # try:
        #     onCreated_STL = CommandCreatedEventHandler2()
        #     cmdDef.commandCreated.add(onCreated_STL)
        #     ui.messageBox("Done")
        # except:
        #     ui.messageBox("Failed")
        #
        #
        # handlers.append(onCreated_STL)
        # ui.messageBox('Hello addin')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
