import FreeCAD as App
import Part

# -------- Case dimensions from the previous code (mm) --------
PCB_W = 29.10
PCB_L = 56.90
SIDE_CLEARANCE = 0.50
WALL = 1.60
CORNER_RADIUS = 2.00

# -------- Lid / fit settings (mm) --------
LID_THICKNESS = 2.00
SKIRT_DEPTH = 3.50
SKIRT_WALL = 1.20
FIT_CLEARANCE = 0.25
SKIRT_CORNER_RADIUS = 1.00

# Two friction bumps on opposite skirt sides
BUMP_RADIUS = 0.6
BUMP_INSET = 0.10       # bump center sits this far inside the skirt edge
BUMP_END_GAP = 0.70     # distance from the skirt's free end to bump center

# -------- Derived dimensions --------
OUT_W = PCB_W + 2.0 * (SIDE_CLEARANCE + WALL)
OUT_L = PCB_L + 2.0 * (SIDE_CLEARANCE + WALL)
IN_W = OUT_W - 2.0 * WALL
IN_L = OUT_L - 2.0 * WALL

SKIRT_OUT_W = IN_W - 2.0 * FIT_CLEARANCE
SKIRT_OUT_L = IN_L - 2.0 * FIT_CLEARANCE
SKIRT_IN_W = SKIRT_OUT_W - 2.0 * SKIRT_WALL
SKIRT_IN_L = SKIRT_OUT_L - 2.0 * SKIRT_WALL

# -------- Geometry helper --------
def rounded_box(x, y, z, dx, dy, dz, radius):
    """Create a box with rounded vertical corners."""
    shape = Part.makeBox(dx, dy, dz, App.Vector(x, y, z))
    r = min(radius, dx / 2.0 - 0.01, dy / 2.0 - 0.01)

    if r > 0:
        vertical_edges = []
        for edge in shape.Edges:
            vertices = edge.Vertexes
            if len(vertices) == 2:
                p1 = vertices[0].Point
                p2 = vertices[1].Point
                if abs(p1.x - p2.x) < 1e-7 and abs(p1.y - p2.y) < 1e-7:
                    vertical_edges.append(edge)

        if vertical_edges:
            shape = shape.makeFillet(r, vertical_edges)

    return shape

# -------- Create lid only --------
doc = App.newDocument("PCB_Case_Lid")

# Flat plate is at z=0 for printing with its broad face on the build plate.
plate = rounded_box(
    0, 0, 0,
    OUT_W, OUT_L, LID_THICKNESS,
    CORNER_RADIUS
)

# Skirt extends upward from the plate in print orientation.
skirt_x = (OUT_W - SKIRT_OUT_W) / 2.0
skirt_y = (OUT_L - SKIRT_OUT_L) / 2.0
skirt_z = LID_THICKNESS

skirt_outer = rounded_box(
    skirt_x, skirt_y, skirt_z,
    SKIRT_OUT_W, SKIRT_OUT_L, SKIRT_DEPTH,
    SKIRT_CORNER_RADIUS
)

skirt_inner = rounded_box(
    skirt_x + SKIRT_WALL,
    skirt_y + SKIRT_WALL,
    skirt_z - 0.05,
    SKIRT_IN_W,
    SKIRT_IN_L,
    SKIRT_DEPTH + 0.10,
    max(0.50, SKIRT_CORNER_RADIUS - SKIRT_WALL / 2.0)
)

skirt = skirt_outer.cut(skirt_inner)
lid_shape = plate.fuse(skirt)

# Add two rounded friction bumps on opposite long sides of the skirt.
bump_z = skirt_z + SKIRT_DEPTH - BUMP_END_GAP
bump_y = OUT_L / 2.0

left_bump = Part.makeSphere(
    BUMP_RADIUS,
    App.Vector(skirt_x + BUMP_INSET, bump_y, bump_z)
)

right_bump = Part.makeSphere(
    BUMP_RADIUS,
    App.Vector(skirt_x + SKIRT_OUT_W - BUMP_INSET, bump_y, bump_z)
)

lid_shape = lid_shape.fuse(left_bump).fuse(right_bump)

# -------- Add lid to document --------
lid_obj = doc.addObject("Part::Feature", "Lid")
lid_obj.Label = "PCB case lid with friction bumps"
lid_obj.Shape = lid_shape

doc.recompute()
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
