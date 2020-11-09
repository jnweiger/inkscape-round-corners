#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2020 Juergen Weigert, jnweiger@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# v0.1, 2020-11-08, jw	- initial draught, finding and printing selected nodes to the terminal...
#
"""
Rounded Corners

This extension finds selected pointy nodes and converts them to a radius. 
the radius is approximated by a bezier spline, as we are doing path operations here...

written according to https://gitlab.com/inkscape/extensions/-/wikis/home
started with https://gitlab.com/inkscape/extensions/-/wikis/uploads/25063b4ae6c3396fcda428105c5cff89/template_effect.zip


"""
# python2 compatibility:
from __future__ import print_function

import inkex

__version__ = '0.1'     # Keep in sync with round_corners.inx line 16

debug = True

class RoundedCorners(inkex.EffectExtension):

    def add_arguments(self, pars):              # __init__
      try:
        self.tty = open("/dev/tty", 'w')
      except:
        try:
          self.tty = open("CON:", 'w')        # windows. Does this work???
        except:
          self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
      if debug: print("RoundedCorners ...", file=self.tty)

      pars.add_argument("--radius", type=float, default=2.0, help="Radius [mm] to round selected vertices")


    def effect(self):
        paths = []
        for node in self.svg.selection.filter(inkex.PathElement).values():
            paths.append(node)
        if len(paths) < 1:
            raise inkex.AbortExtension("Need at least one selected path.")

        for path in paths:
            path.apply_transform()

        pts = [node.path.to_superpath() for node in paths]
        
        if debug:
          for i in range(0, len(pts)):
            print("RoundedCorners: pts[%d]: %s"   % (i, pts[i]), file=self.tty)
            print("RoundedCorners: paths[%d]: %s" % (i, paths[i].path), file=self.tty)
          print(self.svg_path(), file=self.tty)
          print(self.options.selected_nodes, file=self.tty)     # SvgInputMixin __init__: "id:subpath:position of selected nodes, if any"

        # documented in https://inkscape.gitlab.io/extensions/documentation/inkex.command.html
        # inkex.command.write_svg(self.svg, "/tmp/seen.svg")
        # - AttributeError: module 'inkex' has no attribute 'command


    def clean_up(self):         # __fini__
      if self.tty is not None:
        self.tty.close()
      super(RoundedCorners, self).clean_up()


if __name__ == '__main__':
    RoundedCorners().run()
