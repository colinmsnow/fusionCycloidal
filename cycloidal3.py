#Description-Create cycloidal

import adsk.core, adsk.fusion, traceback
import math

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

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            unitsMgr = app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs

            cycloidal = Cycloidal()
            for input in inputs:
                if input.id == 'name':
                    cycloidal.name = input.value
                elif input.id == 'rotorThickness':
                    cycloidal.rotorThickness = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'housingThickness':
                    cycloidal.housingThickness = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'R':
                    cycloidal.R = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'N':
                    cycloidal.N = unitsMgr.evaluateExpression(input.expression, "")
                elif input.id == 'bore':
                    cycloidal.bore = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'numGears':
                    cycloidal.numGears = unitsMgr.evaluateExpression(input.expression, "")
                elif input.id == 'numHoles':
                    cycloidal.numHoles = unitsMgr.evaluateExpression(input.expression, "")
                elif input.id == 'holePinDiameter':
                    cycloidal.holePinDiameter = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'holeCircleDiameter':
                    cycloidal.holeCircleDiameter = unitsMgr.evaluateExpression(input.expression, "mm")
                # elif input.id == 'cutAngle':
                #     bolt.cutAngle = unitsMgr.evaluateExpression(input.expression, "deg") 
                # elif input.id == 'chamferDistance':
                #     bolt.chamferDistance = adsk.core.ValueInput.createByString(input.expression)
                # elif input.id == 'filletRadius':
                #     bolt.filletRadius = adsk.core.ValueInput.createByString(input.expression)

            cycloidal.build()
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
    def __init__(self):
        super().__init__()        
    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            onExecute = CommandExecuteHandler()
            cmd.execute.add(onExecute)
            onExecutePreview = CommandExecuteHandler()
            cmd.executePreview.add(onExecutePreview)
            onDestroy = CommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            handlers.append(onExecutePreview)
            handlers.append(onDestroy)

            #define the inputs
            inputs = cmd.commandInputs
            inputs.addStringValueInput('name', 'Name', defaultName)

            initRotorThickness = adsk.core.ValueInput.createByReal(defaultRotorThickness)
            inputs.addValueInput('rotorThickness', 'Rotor Thickness','mm',initRotorThickness)

            initHousingThickness = adsk.core.ValueInput.createByReal(defaultHousingThickness)
            inputs.addValueInput('housingThickness', 'Housing Thickness', 'mm', initHousingThickness)

            initR = adsk.core.ValueInput.createByReal(defaultR)
            inputs.addValueInput('R', 'Radius', 'mm', initR)

            initN = adsk.core.ValueInput.createByReal(defaultN)
            inputs.addValueInput('N', 'Number', '', initN)

            initBore = adsk.core.ValueInput.createByReal(defaultBore)
            inputs.addValueInput('bore', 'Bore Diameter', 'mm', initBore)

            initNumGears = adsk.core.ValueInput.createByReal(defaultNumGears)
            inputs.addValueInput('numGears', 'Number of gears', '', initNumGears)

            # initNumGears = adsk.core.ValueInput.createByReal(defaultNumGears)
            # inputs.addValueInput('numGears', 'Number of gears', '', initNumGears)

            initNumHoles = adsk.core.ValueInput.createByReal(defaultNumHoles)
            inputs.addValueInput('numHoles', 'Number of drive holes', '', initNumHoles)

            initHolePinDiameter = adsk.core.ValueInput.createByReal(defaultHolePinDiameter)
            inputs.addValueInput('holePinDiameter', 'Diameter of drive pins', 'mm', initHolePinDiameter)

            initHoleCircleDiameter = adsk.core.ValueInput.createByReal(defaultHoleCircleDiameter)
            inputs.addValueInput('holeCircleDiameter', 'Diameter of drive pin circle', 'mm', initHoleCircleDiameter)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class Cycloidal:
    def __init__(self):
        self.cycloidalname_ = defaultName
        self.rotorThickness_ = defaultRotorThickness
        self.housingThickness_ = defaultHousingThickness
        self.R_ = defaultR
        self.N_ = defaultN
        self.bore_ = defaultBore
        self.numGears_ = defaultNumGears
        self.numHoles_ = defaultNumHoles
        self.holePinDiameter_ = defaultHolePinDiameter
        self.holeCircleDiameter_ = defaultHoleCircleDiameter

    #properties
    @property
    def name(self):
        return self.cycloidalname_
    @name.setter
    def name(self, value):
        self.cycloidalname_ = value

    @property
    def rotorThickness(self):
        return self.rotorThickness_
    @rotorThickness.setter
    def rotorThickness(self, value):
        self.rotorThickness_ = value

    @property
    def housingThickness(self):
        return self.housingThickness_
    @housingThickness.setter
    def housingThickness(self, value):
        self.housingThickness_ = value 

    @property
    def R(self):
        return self.R_
    @R.setter
    def R(self, value):
        self.R_ = value 

    @property
    def N(self):
        return self.N_
    @N.setter
    def N(self, value):
        self.N_ = value   

    @property
    def bore(self):
        return self.bore_
    @bore.setter
    def bore(self, value):
        self.bore_ = value

    @property
    def numGears(self):
        return self.numGears_
    @numGears.setter
    def numGears(self, value):
        self.numGears_ = value  

    @property
    def numHoles(self):
        return self.numHoles_
    @numHoles.setter
    def numHoles(self, value):
        self.numHoles_ = value  

    @property
    def holePinDiameter(self):
        return self.holePinDiameter_
    @holePinDiameter.setter
    def holePinDiameter(self, value):
        self.holePinDiameter_ = value  

    @property
    def holeCircleDiameter(self):
        return self.holeCircleDiameter_
    @holeCircleDiameter.setter
    def holeCircleDiameter(self, value):
        self.holeCircleDiameter_ = value  



    def build(self):
        global newComp
        newComp = createNewComponent()
        if newComp is None:
            ui.messageBox('New component failed to create', 'New Component Failed')
            return


        rotorThickness = self.rotorThickness_
        housingThickness = self.housingThickness_
        R = self.R_
        N = self.N_
        bore = self.bore_
        numGears = self.numGears_
        numHoles = self.numHoles_
        holePinDiameter = self.holePinDiameter_
        holeCircleDiameter = self.holeCircleDiameter_

        unitsMgr = app.activeProduct.unitsManager

        #other constants based on the original inputs
        housing_cir = 2 * R * math.pi
        Rr = housing_cir / (4 * N) #roller radius
        E = 0.5 * Rr #eccentricity
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
        sketchCircles.addByCenterRadius(centerPoint, Rr)

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
            centerPoint = adsk.core.Point3D.create(E + holeCircleDiameter/2, 0, 0)
            sketchCircles.addByCenterRadius(centerPoint, holePinDiameter + E)

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
        """ -----------------------Create multiple gears-----------------------"""

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
                    '') # relative resource file path is specified

        onCommandCreated = CommandCreatedHandler()
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
    #psi = -math.atan(math.sin((1 - N) * theta) / ((R / (E * N)) - math.cos((1 - N) * theta)))
    #x = R * math.cos(theta) - Rr * math.cos(theta - psi) - E * math.cos(N * theta)
    #y =  - R * math.sin(theta) + Rr * math.sin(theta - psi) + E * math.cos(N * theta)
    psi = math.atan2(math.sin((1-N)*t), ((R/(E*N))-math.cos((1-N)*t)))

    x = (R*math.cos(t))-(Rr*math.cos(t+psi))-(E*math.cos(N*t))
    y = (-R*math.sin(t))+(Rr*math.sin(t+psi))+(E*math.sin(N*t))
    #x = (10*math.cos(t))-(1.5*math.cos(t+math.atan(math.sin(-9*t)/((4/3)-math.cos(-9*t)))))-(0.75*math.cos(10*t))
    #y = (-10*math.sin(t))+(1.5*math.sin(t+math.atan(math.sin(-9*t)/((4/3)-math.cos(-9*t)))))+(0.75*math.sin(10*t))
    return (x,y)

def getDist(xa, ya, xb, yb):
    return math.sqrt((xa-xb)**2 + (ya-yb)**2)