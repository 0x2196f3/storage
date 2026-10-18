import FreeCAD, Part, Draft

# Create a new document
doc = FreeCAD.newDocument("Cylinders")

# Parameters for the smaller cylinder
small_radius = 15.0  # in cm
small_height = 150.0  # in cm

# Parameters for the larger cylinder
large_radius = 60.0  # in cm
large_height = 20.0  # in cm

# Create the larger cylinder
large_cylinder = Part.makeCylinder(large_radius, large_height)
large_cylinder.translate(FreeCAD.Vector(0, 0, 0))  # Position at the origin

# Create the smaller cylinder
small_cylinder = Part.makeCylinder(small_radius, small_height)
small_cylinder.translate(FreeCAD.Vector(0, 0, large_height))  # Position on top of the larger cylinder

# Add the shapes to the document
part_large = doc.addObject("Part::Feature", "LargeCylinder")
part_large.Shape = large_cylinder

part_small = doc.addObject("Part::Feature", "SmallCylinder")
part_small.Shape = small_cylinder

# Recompute the document to update the view
doc.recompute()

# Optionally, you can save the document
# doc.saveAs("Cylinders.FCStd")
