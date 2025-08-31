import FreeCAD
import Part

# Create a new document
doc = FreeCAD.newDocument()

# Create a 170x170x3 cube
cube = doc.addObject("Part::Box", "Cube")
cube.Length = 170
cube.Width = 170
cube.Height = 3

# Create 8 cylinders for the holes
holes_positions_1 = [
    (10.16, 6.35),
    (165.10, 6.35),
    (33.02, 163.83),
    (165.10, 163.83),

]

holes_positions_2 = [
    (23.5, 17.35),
    (81.5, 17.35),
    (23.5, 66.35),
    (81.5, 66.35),
]

i = 0
for pos in holes_positions_1:
    i += 1
    cylinder = doc.addObject("Part::Cylinder", "Cylinder" + str(i))
    cylinder.Radius = 1.5
    cylinder.Height = 3
    cylinder.Placement.Base = FreeCAD.Vector(pos[0], pos[1], 0)
    cube_cut = doc.addObject("Part::Cut", "Cut" + str(i))
    cube_cut.Base = cube
    cube_cut.Tool = cylinder
    cube = cube_cut

i = 0
for pos in holes_positions_2:
    i += 1
    cylinder = doc.addObject("Part::Cylinder", "Cylinder" + str(i))
    cylinder.Radius = 1.25
    cylinder.Height = 3
    cylinder.Placement.Base = FreeCAD.Vector(pos[0], pos[1], 0)
    cube_cut = doc.addObject("Part::Cut", "Cut" + str(i))
    cube_cut.Base = cube
    cube_cut.Tool = cylinder
    cube = cube_cut

# Show the result
FreeCADGui.ActiveDocument.ActiveView.viewIsometric()
FreeCADGui.SendMsgToActiveView("ViewFit")
FreeCADGui.showMainWindow()