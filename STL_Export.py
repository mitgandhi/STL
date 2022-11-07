
import adsk.core, adsk.fusion, adsk.cam, traceback
import os.path, sys 
ui = adsk.core.UserInterface.cast(None)
handlers = []
selectedEdges = []



def run(context):
    global ui
    ui = None
    try:
        global tbPanel
        app = adsk.core.Application.get()
        ui = app.userInterface

        workSpace = ui.workspaces.itemById('FusionSolidEnvironment')
        tbPanels = workSpace.toolbarPanels

        tbPanel = tbPanels.itemById('NewPanel')
        if tbPanel:
            tbPanel.deleteMe()
        tbPanel = tbPanels.add('NewPanel', 'Export', 'SelectPanel', False)

        # Create a command definition.
        cmdDef = ui.commandDefinitions.itemById('STLExport')
        if cmdDef:
            cmdDef.deleteMe()
        cmdDef = ui.commandDefinitions.addButtonDefinition('STLExport', 'STL Export', 'STL Export Button')
        tbPanel.controls.addCommand(cmdDef)
        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Execute the command.
        cmdDef.execute()

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            cmd.isExecutedWhenPreEmpted = False
            inputs = cmd.commandInputs

            app = adsk.core.Application.get()
            ui= app.userInterface 
            # selectInput = inputs.addSelectionInput('SelectionEventsSample', 'Edges', 'Please select edges')
            # selectInput.addSelectionFilter(adsk.core.Selections.E)
            # selectInput.setSelectionLimits(1)

            onUnSelect = MyUnSelectHandler()
            cmd.unselect.add(onUnSelect)
            handlers.append(onUnSelect)

            product = app.activeProduct
            design = adsk.fusion.Design.cast(product)

        # get root component in this design
            rootComp = design.rootComponent

        # create a single exportManager instance
            exportMgr = design.exportManager

        # # export the root component to printer utility
        # stlRootOptions = exportMgr.createSTLExportOptions(rootComp)
        #
        # # # get all available print utilities
        # printUtils = stlRootOptions.availablePrintUtilities
        # # #
        # # # # export the root component to the print utility, instead of a specified file
        # for printUtil in printUtils:
        #     stlRootOptions.sendToPrintUtility = True
        #     stlRootOptions.printUtility = printUtil
        # ui.messageBox(printUtils)
        # # exportMgr.execute(stlRootOptions)
        # # #
        # # get the script location
            scriptDir = os.path.dirname(os.path.realpath(__file__))
        #
        # # export the occurrence one by one in the root component to a specified file
            allOccu = rootComp.allOccurrences
            for occ in allOccu:
                fileName = scriptDir + "/" + occ.component.name

            # create stl exportOptions
                stlExportOptions = exportMgr.createSTLExportOptions(occ, fileName)
                stlExportOptions.sendToPrintUtility = False

                exportMgr.execute(stlExportOptions)

        # # export the body one by one in the design to a specified file
            allBodies = rootComp.bRepBodies
            for body in allBodies:
                fileName = scriptDir + "/" + body.parentComponent.name + '-' + body.name

            # create stl exportOptions
                stlExportOptions = exportMgr.createSTLExportOptions(body, fileName)
                stlExportOptions.sendToPrintUtility = False
        #
                exportMgr.execute(stlExportOptions)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



class MyUnSelectHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            selectedEdge = adsk.fusion.BRepEdge.cast(args.selection.entity)
            if selectedEdge:
                selectedEdges.remove(selectedEdge)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
