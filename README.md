# inkscape-round-corners
An inkscape 1.0 extension to apply a radius to sharp corners of a path.


The screenshot below demonstrates the usage.
We start with the upper path, select the top left and bottom left corner. 
Run "Rounded Corners" from "Extensions" -> "Modify Path".
The result is the path shown on the bottom.

![screenshot](doc/slanted_rect.png)


The top left corner has less than 90°, it is replaced with an spline path of two vertices representing an arc of a circle with radius 4.<br>
The bottom left corner is acute (>90°) and requires 3 vertices to nicely represent the desired arc as a spline.

Note how the bottom path segment is curved.<br>
In this case the direction of the spline handle is used to fit the arc. The direction and endpoint of the handle remain unchanged.
The curvature of the path segment adjusts slightly to fit the new endpoint.
