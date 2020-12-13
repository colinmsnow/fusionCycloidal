#Description-Create cycloidal

import adsk.core, adsk.fusion, traceback
import math

from . import fusionUtils


# to remove:

# from . import fusionUtils.CommandExecuteHandler
# from . import fusionUtils.CommandCreatedHandler
# from . import fusionUtils.CommandDestroyHandler

CommandExecuteHandler = fusionUtils.CommandExecuteHandler
CommandCreatedHandler = fusionUtils.CommandCreatedHandler
CommandDestroyHandler = fusionUtils.CommandDestroyHandler


# class CommandExecuteHandler(adsk.core.CommandEventHandler):
#     def __init__(self, app, ui, objectClass, inputParameters):
#         super().__init__()
#         self.objectClass = objectClass
#         self.app = app
#         self.parameters = inputParameters
#         self.ui = ui

#     def notify(self, args):
#         try:
#             unitsMgr = self.app.activeProduct.unitsManager
#             command = args.firingEvent.sender
#             inputs = command.commandInputs

#             # self.objectClass = CreatedObject()



#             for input in inputs:
#                 testParameter = self.parameters.parameterDict[input.id]
#                 self.objectClass.parameters[input.id] = unitsMgr.evaluateExpression(input.expression, testParameter.units)

#             self.objectClass.build()
#             args.isValidResult = True

#         except:
#             if self.ui:
#                 self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# class CommandDestroyHandler(adsk.core.CommandEventHandler):
#     def __init__(self, ui):
#         super().__init__()
#         self.ui = ui
#     def notify(self, args):
#         try:
#             # when the command is done, terminate the script
#             # this will release all globals which will remove all event handlers
#             adsk.terminate()
#         except:
#             if self.ui:
#                 self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):    
#     def __init__(self, app, ui, objectClass, inputParameters, handlers):
#         super().__init__()  
#         self.objectClass = objectClass
#         self.app = app    
#         self.parameters = inputParameters
#         self.ui = ui
#         self.handlers = handlers

#     def notify(self, args):
#         try:
#             cmd = args.command
#             cmd.isRepeatable = False
#             onExecute = CommandExecuteHandler(self.app, self.ui,  self.objectClass, self.parameters)
#             cmd.execute.add(onExecute)
#             onExecutePreview = CommandExecuteHandler(self.app, self.ui, self.objectClass, self.parameters)
#             cmd.executePreview.add(onExecutePreview)
#             onDestroy = CommandDestroyHandler(self.ui)
#             cmd.destroy.add(onDestroy)
#             # keep the handler referenced beyond this function
#             self.handlers.append(onExecute)
#             self.handlers.append(onExecutePreview)
#             self.handlers.append(onDestroy)

#             #define the inputs
#             inputs = cmd.commandInputs
#             # inputs.addStringValueInput('name', 'Name', defaultName)

#             for parameter in self.parameters.parameterList:
#                 initValue = adsk.core.ValueInput.createByReal(parameter.defaultValue)
#                 inputs.addValueInput(parameter.id, parameter.description, parameter.units, initValue)

#         except:
#             if self.ui:
#                 self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

























defaultName = 'Cycloidal'
defaultRotorThickness = .635
defaultHousingThickness = 2 * defaultRotorThickness
defaultR = 5
defaultN = 10
defaultBore = 1
defaultNumGears = 1
defaultNumHoles = 0
defaultHolePinDiameter = .25
defaultHoleCircleDiameter = 3
defaultEccentricityRatio = .5

class Parameter:
    def __init__(self, name, units, description, defaultValue):
        self.id = name
        self.units = units
        self.description = description
        self.defaultValue = defaultValue

class Parameters:

    def __init__(self):
        self.parameterList = []
        self.parameterDict = {}

    def addParameter(self, name, units, description, defaultValue):
        newParam = Parameter(name, units, description, defaultValue)
        self.parameterList.append(newParam)
        self.parameterDict[name] = newParam

parameters = Parameters()
parameters.addParameter('rotorThickness', "mm", 'Rotor Thickness', defaultRotorThickness)
parameters.addParameter('housingThickness', "mm", 'Housing Thickness', defaultHousingThickness)
parameters.addParameter('R', "mm", 'Radius', defaultR)
parameters.addParameter('N', "", 'Number of pins', defaultN)
parameters.addParameter('bore', "mm", 'Bore Diameter', defaultBore)
parameters.addParameter('numGears', "", 'Number of gears', defaultNumGears)
parameters.addParameter('numHoles', "", 'Number of drive holes', defaultNumHoles)
parameters.addParameter('holePinDiameter', "mm", 'Diameter of drive pins', defaultHolePinDiameter)
parameters.addParameter('holeCircleDiameter', "mm", 'Diameter of hole circle', defaultHoleCircleDiameter)
parameters.addParameter('eccentricityRatio', "", 'Eccentricity Ratio', defaultEccentricityRatio)


# global set of event handlers to keep them referenced for the duration of the command
handlers = []
app = adsk.core.Application.get()
if app:
    ui = app.userInterface

newComp = None

def createNewComponent():
    # Get the active design.
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component



class CreatedObject:

    def __init__(self):
        self.parameters = {}

    def build(self):
        global newComp
        newComp = createNewComponent()
        if newComp is None:
            ui.messageBox('New component failed to create', 'New Component Failed')
            return

        eccentricityRatio = self.parameters["eccentricityRatio"]
        rotorThickness = self.parameters["rotorThickness"]
        housingThickness = self.parameters["housingThickness"]
        R = self.parameters["R"]
        N = self.parameters["N"]
        bore = self.parameters["bore"]
        numGears = self.parameters["numGears"]
        numHoles = self.parameters["numHoles"]
        holePinDiameter = self.parameters["holePinDiameter"]
        holeCircleDiameter = self.parameters["holeCircleDiameter"]
        

        unitsMgr = app.activeProduct.unitsManager

        #other constants based on the original inputs
        housing_cir = 2 * R * math.pi
        Rr = housing_cir / (4 * N)#roller radius
        E = eccentricityRatio * Rr#eccentricity
        maxDist = 0.25 * Rr #maximum allowed distance between points
        minDist = 0.5 * maxDist #the minimum allowed distance between points
        
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        root = design.rootComponent

        rotorOcc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        rotor = rotorOcc.component
        rotor.name = 'rotor'

        sk = rotor.sketches.add(root.xYConstructionPlane)

        points = adsk.core.ObjectCollection.create()

        #ui.messageBox('Ratio will be ' + 1/N)

        (xs, ys) = getPoint(0, R, Rr, E, N)
        points.add(adsk.core.Point3D.create(xs,ys,0))

        et = 2 * math.pi / (N-1)
        (xe, ye) = getPoint(et, R, Rr, E, N)
        x = xs
        y = ys
        dist = 0
        ct = 0
        dt = math.pi / N
        numPoints = 0

        while ((math.sqrt((x-xe)**2 + (y-ye)**2) > maxDist or ct < et/2) and ct < et): #close enough to the end to call it, but over half way
        #while (ct < et/80): #close enough to the end to call it, but over half way
            (xt, yt) = getPoint(ct+dt, R, Rr, E, N)
            dist = getDist(x, y, xt, yt)

            ddt = dt/2
            lastTooBig = False
            lastTooSmall = False

            while (dist > maxDist or dist < minDist):
                if (dist > maxDist):
                    if (lastTooSmall):
                        ddt /= 2

                    lastTooSmall = False
                    lastTooBig = True

                    if (ddt > dt/2):
                        ddt = dt/2

                    dt -= ddt

                elif (dist < minDist):
                    if (lastTooBig):
                        ddt /= 2

                    lastTooSmall = True
                    lastTooBig = False
                    dt += ddt


                (xt, yt) = getPoint(ct+dt, R, Rr, E, N)
                dist = getDist(x, y, xt, yt)

            x = xt
            y = yt
            points.add(adsk.core.Point3D.create(x,y,0))
            numPoints += 1
            ct += dt

        points.add(adsk.core.Point3D.create(xe,ye,0))
        crv = sk.sketchCurves.sketchFittedSplines.add(points)

        lines = sk.sketchCurves.sketchLines
        line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), crv.startSketchPoint)
        line2 = lines.addByTwoPoints(line1.startSketchPoint, crv.endSketchPoint)

        prof = sk.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(rotorThickness)

        # Get extrude features
        extrudes = rotor.features.extrudeFeatures
        extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Get the extrusion body
        body1 = extrude1.bodies.item(0)
        body1.name = "rotor"

        inputEntites = adsk.core.ObjectCollection.create()
        inputEntites.add(body1)

        # Get Z axis for circular pattern
        zAxis = rotor.zConstructionAxis

        # Create the input for circular pattern
        circularFeats = rotor.features.circularPatternFeatures
        circularFeatInput = circularFeats.createInput(inputEntites, zAxis)

        # Set the quantity of the elements
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(N-1)

        # Set the angle of the circular pattern
        circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')

        # Set symmetry of the circular pattern
        circularFeatInput.isSymmetric = True

        # Create the circular pattern
        circularFeat = circularFeats.add(circularFeatInput)

        ToolBodies = adsk.core.ObjectCollection.create()
        for b in circularFeat.bodies:
            ToolBodies.add(b)

        combineInput = rotor.features.combineFeatures.createInput(body1, ToolBodies)
        combineInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
        combineInput.isNewComponent = False

        rotor.features.combineFeatures.add(combineInput)

        #Offset the rotor to make the shaft rotat concentric with origin
        transform = rotorOcc.transform
        transform.translation = adsk.core.Vector3D.create(E, 0, 0)
        rotorOcc.transform = transform
        design.snapshots.add()

        housingOcc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        housing = housingOcc.component
        housing.name = 'housing'

        #add a sketch so rotor clearance is obvious
        sketches = housing.sketches
        rotorClearanceSketch = sketches.add(root.xYConstructionPlane)
        sketchCircles = rotorClearanceSketch.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        sketchCircles.addByCenterRadius(centerPoint, R)

        #add rollers
        rollerSketch = sketches.add(root.xYConstructionPlane)
        sketchCircles = rollerSketch.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(R, 0, 0)
        sketchCircles.addByCenterRadius(centerPoint, Rr )

        rollerProfile = rollerSketch.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(housingThickness)
        rollerExtrudes = housing.features.extrudeFeatures.addSimple(rollerProfile, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        # Get the extrusion body
        roller = rollerExtrudes.bodies.item(0)
        roller.name = "roller"

        inputEntites = adsk.core.ObjectCollection.create()
        inputEntites.add(roller)

        # Create the input for circular pattern
        circularFeats = housing.features.circularPatternFeatures
        zAxis = housing.zConstructionAxis
        circularFeatInput = circularFeats.createInput(inputEntites, zAxis)

        # Set the quantity of the elements
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(N)

        # Set the angle of the circular pattern
        circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')

        # Set symmetry of the circular pattern
        circularFeatInput.isSymmetric = True

        # Create the circular pattern
        circularFeat = circularFeats.add(circularFeatInput)


        # create center hole
        centerHoleSketch = sketches.add(root.xYConstructionPlane)
        sketchCircles = centerHoleSketch.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(E, 0, 0)
        sketchCircles.addByCenterRadius(centerPoint, bore/2)

        centerHoleProfile = centerHoleSketch.profiles.item(0)

        distance = adsk.core.ValueInput.createByReal(rotorThickness)
        centerExtrudes = housing.features.extrudeFeatures.addSimple(centerHoleProfile, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)


        #Create holes for pins

        if numHoles != 0:
            pinHoleSketch = sketches.add(root.xYConstructionPlane)
            sketchCircles = pinHoleSketch.sketchCurves.sketchCircles
            centerPoint = adsk.core.Point3D.create(E, holeCircleDiameter/2, 0)
            sketchCircles.addByCenterRadius(centerPoint, holePinDiameter/2 + E)

            pinHoleProfile = pinHoleSketch.profiles.item(0)

            distance = adsk.core.ValueInput.createByReal(rotorThickness)
            pinExtrudes = housing.features.extrudeFeatures.addSimple(pinHoleProfile, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)

            inputEntites = adsk.core.ObjectCollection.create()
            inputEntites.add(pinExtrudes)

            # Get Z axis for circular pattern
            zAxis = rotor.zConstructionAxis

            # Create the input for circular pattern
            circularFeats = rotor.features.circularPatternFeatures
            circularFeatInput = circularFeats.createInput(inputEntites, zAxis)

            # Set the quantity of the elements
            circularFeatInput.quantity = adsk.core.ValueInput.createByReal(numHoles)

            # Set the angle of the circular pattern
            circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')

            # Set symmetry of the circular pattern
            circularFeatInput.isSymmetric = True

            # Create the circular pattern
            circularFeat = circularFeats.add(circularFeatInput)


        # Create multiple gears

        body = body1
        
        # Check to see if the body is in the root component or another one.
        target = None
        if body.assemblyContext:
            # It's in another component.
            target = body.assemblyContext
        else:
            # It's in the root component.
            target = root

        # Get the xSize.
        xSize = body.boundingBox.maxPoint.x - body.boundingBox.minPoint.x            

        # Create several copies of the body.
        currentZ = 0
        for i in range(0,int(numGears)-1):
            # Create the copy.
            newBody = body.copyToComponent(target)
            
            # Increment the position.            
            currentZ +=  rotorThickness

            trans = adsk.core.Matrix3D.create()
            trans.translation = adsk.core.Vector3D.create(0, 0, currentZ)
            

            # Move the body using a move feature.
            bodyColl = adsk.core.ObjectCollection.create()
            bodyColl.add(newBody)
            moveInput = root.features.moveFeatures.createInput(bodyColl, trans)
            moveFeat = root.features.moveFeatures.add(moveInput)
            
            if (i%2 == 0):
                rotation = adsk.core.Matrix3D.create()
                rotation.setToRotation(unitsMgr.convert(180, "deg", "rad"), root.yConstructionAxis.geometry.getData()[2], adsk.core.Point3D.create(0, 0, currentZ + rotorThickness/2))
                moveInput2 = root.features.moveFeatures.createInput(bodyColl, rotation)
                moveFeat = root.features.moveFeatures.add(moveInput2)

        return


def run(context):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('It is not supported in current workspace, please change to MODEL workspace and try again.')
            return
        commandDefinitions = ui.commandDefinitions
        #check the command exists or not
        cmdDef = commandDefinitions.itemById('Cycloidal')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition('Cycloidal',
                    'Create Cycloidal',
                    'Create a cycloidal.',
                    '') # Edit last parameter to provide resources

        createdObject = CreatedObject()

        onCommandCreated = CommandCreatedHandler(app, ui, createdObject, parameters, handlers)
        cmdDef.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def getPoint(t, R, Rr, E, N):
    psi = math.atan2(math.sin((1-N)*t), ((R/(E*N))-math.cos((1-N)*t)))
    x = (R*math.cos(t))    -(Rr*math.cos(t+psi))-(E*math.cos(N*t))
    y = (-R*math.sin(t))   +(Rr*math.sin(t+psi))+(E*math.sin(N*t))
    return (x,y)

def getDist(xa, ya, xb, yb):
    return math.sqrt((xa-xb)**2 + (ya-yb)**2)