import adsk.core, adsk.fusion, traceback
import math

def nothing():
    pass


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, app, objectClass, inputParameters):
        super().__init__()
        self.objectClass = objectClass
        self.app = app
        self.parameters = inputParameters

    def notify(self, args):
        try:
            unitsMgr = self.app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs

            # self.objectClass = CreatedObject()



            for input in inputs:
                testParameter = self.parameters.parameterDict[input.id]
                self.objectClass.parameters[input.id] = unitsMgr.evaluateExpression(input.expression, testParameter.units)

            self.objectClass.build()
            args.isValidResult = True

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class CommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):    
    def __init__(self, app, objectClass, inputParameters):
        super().__init__()  
        self.objectClass = objectClass
        self.app = app    
        self.parameters = inputParameters

    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            onExecute = CommandExecuteHandler(self.app, self.objectClass, self.parameters)
            cmd.execute.add(onExecute)
            onExecutePreview = CommandExecuteHandler(self.app, self.objectClass, self.parameters)
            cmd.executePreview.add(onExecutePreview)
            onDestroy = CommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            handlers.append(onExecutePreview)
            handlers.append(onDestroy)

            #define the inputs
            inputs = cmd.commandInputs
            # inputs.addStringValueInput('name', 'Name', defaultName)

            for parameter in self.parameters.parameterList:
                initValue = adsk.core.ValueInput.createByReal(parameter.defaultValue)
                inputs.addValueInput(parameter.id, parameter.description, parameter.units, initValue)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

