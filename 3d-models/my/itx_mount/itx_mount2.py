import FreeCAD, Part, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("CombinedDocument")

# Parameters for the custom shape
thickness = 2.0  # Thickness of the shapes in mm

# Create the black square (150mm x 150mm) at (0, 200)
square = Part.makeBox(15, 15, thickness, FreeCAD.Vector(0, 20, 0))

# Create the big black circle (radius 75mm) at (75, 200)
big_circle = Part.makeCylinder(7.5, thickness, FreeCAD.Vector(7.5, 20, 0))

# Create the small white circle (radius 55mm) at (75, 200)
small_circle = Part.makeCylinder(5.5, thickness + 1, FreeCAD.Vector(7.5, 20, 0))  # Slightly thicker for cutting

# Combine the square and the big circle
black_shapes = square.fuse(big_circle)

# Cut the small circle from the combined shape
final_shape = black_shapes.cut(small_circle)

# Rotate the final shape by 90 degrees around the Z-axis
rotation_axis = FreeCAD.Vector(1, 0, 0)  # Z-axis
rotation_angle = 90  # Degrees
final_shape.rotate(FreeCAD.Vector(0, 0, 0), rotation_axis, rotation_angle)

rotation_axis = FreeCAD.Vector(0, 1, 0)  # Z-axis
rotation_angle = 180  # Degrees
final_shape.rotate(FreeCAD.Vector(0, 0, 0), rotation_axis, rotation_angle)

# Position the final shape at (90mm, 0mm, 3mm)
final_shape.Placement.Base = FreeCAD.Vector(145, 2, 36)

# Add the final shape to the document
Part.show(final_shape)

# Set the color of the final shape
final_shape.ViewObject.ShapeColor = (0.0, 0.0, 0.0)  # Black

# Create a 170x170x3 cube
cube = doc.addObject("Part::Box", "Cube")
cube.Length = 170
cube.Width = 170
cube.Height = 3
cube.Placement.Base = FreeCAD.Vector(0, 0, 0)

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

# Create holes in the cube
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

# Recompute the document to update the view
doc.recompute()
