# Inkscape extension: Round Corners
Apply a radius to sharp corners of a path.
The extension is written for inkscape 1.0.1 (but also contains a backport for 0.92.4).

## Usage
The screenshot below demonstrates the usage.<br>
In the upper path, select the top left and bottom left corner (shown in blue).<br>
Run "Rounded Corners" from "Extensions" -> "Modify Path".<br>
The result is the path below. (Viewed here in edit mode to show the vertices.)

[![screenshot](doc/slanted_rect.png)](https://github.com/jnweiger/inkscape-round-corners/releases)


The top left corner is obtuse (inner angle is more than 90°). Therefore it is replaced with an spline path of only two vertices representing an arc of less than a quarter circle.<br>
The bottom left corner is acute ( < 90° ) and requires a spline of three vertices to nicely represent the desired arc.

Note how the bottom path segment is curved.<br>
In this case the direction of the spline handle is used to fit the arc. The direction and endpoint of the handle remain unchanged.
The curvature of the bottom path segment adjusts slightly to meet the new endpoint.

## Installation

Download and unpack a zip-archive from https://github.com/jnweiger/inkscape-round-corners/releases
The extension is installed by copying two files into your extensions folder (check Edit -> Settings -> System to find its location):

For inkscape 1.0.1 and later, copy
* `round_corners.py`
* `round_corners.inx`

For inkscape 0.92.4 and earler, copy
* `round_corners.py`
* `round_corners.092_inx` (renamed to end in `.inx`)

(All other files are not needed, but harmless if installed too.
With inkscape 1.0.1 you can e.g. unpack the entire zip as a subfolder into your extensions folder.
With inkscape 0.92.4 no subfolders are allowed.)

Then restart inkscape and look for Extensions -> Modify Path -> Round Corners

## Similar solutions

* Inkscape 1.0.1 has a path effect "Corners (Fillet/Chamfer)" - much more flexible, but makes simple cases quite hard.
* https://inkscape.org/~crowhoot/%E2%98%85rounded-corners - cannot select individual nodes, does not work on curved segments, 0.92 only.
