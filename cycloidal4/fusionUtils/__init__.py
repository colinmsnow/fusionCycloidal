import adsk.core, adsk.fusion, traceback
import math

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, app, ui, objectClass, inputParameters):
        super().__init__()
        self.objectClass = objectClass
        self.app = app
        self.parameters = inputParameters
        self.ui = ui

    def notify(self, args):
        try:
            unitsMgr = self.app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs

            for input in inputs:
                testParameter = self.parameters.parameterDict[input.id]
                self.objectClass.parameters[input.id] = unitsMgr.evaluateExpression(input.expression, testParameter.units)

            self.objectClass.build()
            args.isValidResult = True

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class CommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):    
    def __init__(self, app, ui, objectClass, inputParameters, handlers):
        super().__init__()  
        self.objectClass = objectClass
        self.app = app    
        self.parameters = inputParameters
        self.ui = ui
        self.handlers = handlers

    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            onExecute = CommandExecuteHandler(self.app, self.ui,  self.objectClass, self.parameters)
            cmd.execute.add(onExecute)
            onExecutePreview = CommandExecuteHandler(self.app, self.ui, self.objectClass, self.parameters)
            cmd.executePreview.add(onExecutePreview)
            onDestroy = CommandDestroyHandler(self.ui)
            cmd.destroy.add(onDestroy)
            # keep the handler referenced beyond this function
            self.handlers.append(onExecute)
            self.handlers.append(onExecutePreview)
            self.handlers.append(onDestroy)

            #define the inputs
            inputs = cmd.commandInputs

            for parameter in self.parameters.parameterList:
                initValue = adsk.core.ValueInput.createByReal(parameter.defaultValue)
                inputs.addValueInput(parameter.id, parameter.description, parameter.units, initValue)

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class Parameter:
    """ A container for all parameters needed to create an input field """

    def __init__(self, name, units, description, defaultValue):
        self.id = name
        self.units = units
        self.description = description
        self.defaultValue = defaultValue


class Parameters:
    """ A container to hold parameters for input initialization """

    def __init__(self):
        self.parameterList = []
        self.parameterDict = {}

    def addParameter(self, name, units, description, defaultValue):
        newParam = Parameter(name, units, description, defaultValue)
        self.parameterList.append(newParam)
        self.parameterDict[name] = newParam


def createNewComponent(app):
    """ Create a new component in the active design """

    # Get the active design.
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component
