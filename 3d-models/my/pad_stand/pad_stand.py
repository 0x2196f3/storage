import FreeCAD as App
import Part

# ---------------------------------------------------------------
# 0) New document
# ---------------------------------------------------------------
doc = App.newDocument('J_with_L_and_halfCylinder')

# ---------------------------------------------------------------
# 1) First rectangular prism   ( 5 × 100 × 100 )  ── along +Y
# ---------------------------------------------------------------
prism1 = Part.makeBox(5, 100, 100)         # (dx, dy, dz)
prism1_obj = doc.addObject('Part::Feature', 'Prism1')
prism1_obj.Shape = prism1                  

# ---------------------------------------------------------------
# 2) Hollow semicircular shell  ( Ri = 10, Ro = 15,  H = 100 )
# ---------------------------------------------------------------
outer_half = Part.makeCylinder(13, 100, App.Vector(0, 0, 0),
                               App.Vector(0, 0, -1), 150)
inner_half = Part.makeCylinder(8, 100, App.Vector(0, 0, 0),
                               App.Vector(0, 0, -1), 150)
shell = outer_half.cut(inner_half)

# Flat face must sit on X = 5 → rotate 180 ° about Z, then shift −10 mm in X
shell.Placement = App.Placement(App.Vector(0, 0, 0),
                                App.Rotation(App.Vector(0, 0, 1), 180))
shell.translate(App.Vector(-8, 0, 100))

shell_obj = doc.addObject('Part::Feature', 'SemiShell')
shell_obj.Shape = shell

# ---------------------------------------------------------------
# 3) Second rectangular prism   (100 × 5 × 100)  ── rotated 90°
#     Bonded to prism1 at Y = 10 … 15 mm                [1]
# ---------------------------------------------------------------
prism2 = Part.makeBox(80, 5, 100)
prism2.translate(App.Vector(5, 12.5, 0))      # puts its 5 mm face on prism1[1]
prism2_obj = doc.addObject('Part::Feature', 'Prism2')
prism2_obj.Shape = prism2

# ---------------------------------------------------------------
# 4) Solid half-cylinder  r = 5 mm, h = 100 mm
#     Axis along +Z, centre at intersection (0, 10, 0) [2]
# ---------------------------------------------------------------
radius  = 10
height  = 100
centre  = App.Vector(5, 15, 0)              # bottom-centre of the new solid[2]

full_cyl  = Part.makeCylinder(radius, height, centre, App.Vector(0, 0, 1))
# remove the part where X < 0 to obtain a semicircle lying on X ≥ 0
cut_box   = Part.makeBox(radius, radius*2, height,
                         centre - App.Vector(radius, radius, 0))
half_cyl  = full_cyl.cut(cut_box)           # solid semicircular cylinder[3]

half_obj  = doc.addObject('Part::Feature', 'HalfCylinder')
half_obj.Shape = half_cyl

# ---------------------------------------------------------------
# 5) Fuse everything into one solid
# ---------------------------------------------------------------
j_column = prism1.fuse(shell).fuse(prism2).fuse(half_cyl)
j_obj    = doc.addObject('Part::Feature', 'J_Column_Final')
j_obj.Shape = j_column

doc.recompute()

# (optional) hide building blocks
for obj in (prism1_obj, shell_obj, prism2_obj, half_obj):
    obj.ViewObject.Visibility = False
    
