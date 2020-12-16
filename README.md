# inkscape-round-corners
An inkscape 1.0 extension to apply a radius to sharp corners of a path.


The screenshot below demonstrates the usage.<br>
In the upper path, select the top left and bottom left corner (shown in blue).<br>
Run "Rounded Corners" from "Extensions" -> "Modify Path".<br>
The result is the path below. (Also selected here in edit mode to show the vertices.)

[![screenshot](doc/slanted_rect.png)](https://github.com/jnweiger/inkscape-round-corners/releases)


The top left corner has a bit more than 90°, it is replaced with an spline path of two vertices representing an arc of a bit less than a quarter circle.<br>
The bottom left corner is acute ( < 90° ) and requires a spline of three vertices to nicely represent the desired arc.

Note how the bottom path segment is curved.<br>
In this case the direction of the spline handle is used to fit the arc. The direction and endpoint of the handle remain unchanged.
The curvature of the path segment adjusts slightly to fit the new endpoint.

## installation

Download and unpack a zip-archive from https://github.com/jnweiger/inkscape-round-corners/releases

For inkscape 1.0.1 and later, copy these two files into your extensions folder:
* `rounded_corners.py`
* `rounded_corners.inx`

For inkscape 0.92.4 and earler, copy these two files into your extensions folder:
* `rounded_corners.py`
* `rounded_corners.092_inx` (renamed to end in `.inx`)

All other files are not needed (but harmless). With inkscape 1.0.1 you can e.g. unpack the entire zip as a subfolder into your extensions folder.

Then restart inkscape, and look for Extensions -> Modify Path -> Rounded Corners
