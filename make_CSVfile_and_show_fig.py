#https://mtkbirdman.com/fusion360-serializedcsv-python-script

#Author-Autodesk Inc.
#Description-Import spline from serialized csv file

import adsk.core, adsk.fusion, traceback
import io

def run(context):
    ui = None
    try:
        # Black magic for Fusion360 launching
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # Get all components in the active design.
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # Launch a browser for csv file selection
        # Choose the largest number in the serialized csv files
        title = 'Import Serialized csv'
        if not design:
            ui.messageBox('No active Fusion design', title)
            return
        dlg = ui.createFileDialog()
        dlg.title = 'Open CSV File'
        dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'
        if dlg.showOpen() != adsk.core.DialogResults.DialogOK :
            return
        filename = dlg.filename

        # Create the list of serialized csv files
        basename=filename[:-8]
        index_max=filename[-8:-4]
        filetype=filename[-4:]


        #↓エラーの原因
        #filenames=[basename+'{:0=4}'.format(index)+filetype for index in range(0,int(index_max)+1,1)]
        #↓とりあえず動くようにした
        filenames = [f"{dlg.filename}"]

        # Get the root component of the active design
        rootComp = design.rootComponent
        # Create sketch
        sketches = rootComp.sketches
        sketch = sketches.add(rootComp.xYConstructionPlane)
        for filename in filenames:
            with io.open(filename, 'r', encoding='utf-8-sig') as f:
                points = adsk.core.ObjectCollection.create()
                line = f.readline()
                data = []
                TE=True
                # Read airfoil points data from csv file
                while line:
                    pntStrArr = line.split(',')
                    data=[]
                    for pntStr in pntStrArr:
                        try:
                            data.append(float(pntStr))
                        except:
                            break
                    if len(data) >= 3 :
                        if TE:
                            point_TE = adsk.core.Point3D.create(data[0], data[1], data[2])
                            points.add(point_TE)
                            TE=False
                        else:
                            point = adsk.core.Point3D.create(data[0], data[1], data[2])
                            points.add(point)
                    line = f.readline()
                
                # Add the trailing edge point into "points"
                points.add(point_TE)
            
            if points.count:
                # Add spline of airfoil
                sketch.sketchCurves.sketchFittedSplines.add(points)
            else:
                ui.messageBox('No valid points', title)
            
    except:
        
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))    
