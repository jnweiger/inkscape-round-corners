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
# v0.2, 2020-11-08, jw	- duplicate the selected nodes in their superpaths, write them back.
# v0.3, 2020-11-21, jw	- find "meta-handles"
# v0.4, 2020-11-26, jw	- alpha and trim math added. trimming with a striaght line implemented, needs fixes.
#                         Option 'cut' added.
#
"""
Rounded Corners

This extension finds selected pointy nodes and converts them to a radius.
The radius is approximated by a bezier spline, as we are doing path operations here...

Written according to https://gitlab.com/inkscape/extensions/-/wikis/home

References:
 - https://gitlab.com/inkscape/extras/extensions-tutorials/-/blob/master/My-First-Effect-Extension.md
 - https://gitlab.com/inkscape/extensions/-/wikis/uploads/25063b4ae6c3396fcda428105c5cff89/template_effect.zip
 - https://inkscape-extensions-guide.readthedocs.io/en/latest/_modules/inkex/elements.html#ShapeElement.get_path
 - https://inkscape.gitlab.io/extensions/documentation/_modules/inkex/paths.html#CubicSuperPath.to_path

"""

# python2 compatibility:
from __future__ import print_function

import inkex
import sys, math, pprint

__version__ = '0.4'     # Keep in sync with round_corners.inx line 16

debug = True
max_trim_factor = 0.5   # 0.5: can cut half of a segment length or handle length away for rounding a corner

class RoundedCorners(inkex.EffectExtension):

    def add_arguments(self, pars):              # an __init__ in disguise ...
      try:
        self.tty = open("/dev/tty", 'w')
      except:
        try:
          self.tty = open("CON:", 'w')        # windows. Does this work???
        except:
          self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
      if debug: print("RoundedCorners ...", file=self.tty)
      self.nodes_inserted = {}
      self.eps = 0.00001                # avoid division by zero
      self.radius = None

      pars.add_argument("--radius", type=float, default=2.0, help="Radius [mm] to round selected vertices")
      pars.add_argument("--cut", type=str, default="false", help="cut corners with straight lines (instead of fitting an arc)")


    def effect(self):
        if debug: print(self.options.selected_nodes, file=self.tty)     # SvgInputMixin __init__: "id:subpath:position of selected nodes, if any"

        self.radius = math.fabs(self.options.radius)
        self.cut = False
        if self.options.cut in ('True', 'TRUE', 'true', '1', 'Yes', 'YES', 'yes'):
          self.cut = True
        if len(self.options.selected_nodes) < 1:
          raise inkex.AbortExtension("Need at least one selected node in the path. Go to edit path, click a corner, then try again.")
        for node in sorted(self.options.selected_nodes):
          ## we walk through the list sorted, so that node indices are processed within a subpath in ascending numeric order.
          ## that makes adjusting index offsets after node inserts easier.
          ss = self.round_corner(node)


    def round_corner(self, node_id):
      """ round the corner at (adjusted) node_idx of subpath
          Side_effect: store (or increment) in self.inserted["pathname:subpath"] how many points were inserted in that subpath.
          the adjusted node_idx is computed by adding that number (if exists) to the value of the node_id before doing any manipulation
      """
      s = node_id.split(":")
      path_id = s[0]
      subpath_idx = int(s[1])
      subpath_id = s[0] + ':' + s[1]
      idx_adjust = self.nodes_inserted.get(subpath_id, 0)
      node_idx = int(s[2]) + idx_adjust

      elem = self.svg.getElementById(path_id)
      elem.apply_transform()       # modifies path inplace? -- We save later save back to the same element. Maybe we should not?
      path = elem.path
      s = path.to_superpath()
      sp = s[subpath_idx]

      ## call the actual path manipulator, record how many nodes were inserted.
      orig_len = len(sp)
      sp = self.subpath_round_corner(sp, node_idx)
      idx_adjust += len(sp) - orig_len

      # convert the superpath back to a normal path
      s[subpath_idx] = sp
      elem.set_path(s.to_path(curves_only=False))
      self.nodes_inserted[subpath_id] = idx_adjust

      # documented in https://inkscape.gitlab.io/extensions/documentation/inkex.command.html
      # inkex.command.write_svg(self.svg, "/tmp/seen.svg")
      # - AttributeError: module 'inkex' has no attribute 'command


    def super_node(self, sp, node_idx):
      """ In case of node_idx 0, we need to use either the last, or the second-last node as a previous node.
          For a closed subpath, the last an the first node are identical, then we use the second-last.
          In case of the node_idx being the last node, we already know that the subpath is not closed,
          we use 0 as the next node.
      """
      prev_idx = node_idx - 1
      if node_idx == 0:
        prev_idx = len(sp) - 1
        # deep compare. all elements in sub arrays are compared for numerical equality
        if sp[node_idx] == sp[prev_idx]: prev_idx = prev_idx - 1
      next_idx = node_idx + 1
      if next_idx >= len(sp): next_idx = 0
      t = sp[node_idx]
      p = sp[prev_idx]
      n = sp[next_idx]
      dir1 = [ p[1][0] - t[1][0], p[1][1] - t[1][1] ]           # direction to the previous node (rel coords)
      dir2 = [ n[1][0] - t[1][0], n[1][1] - t[1][1] ]           # direction to the next node (rel coords)
      dist1 = math.sqrt(dir1[0]*dir1[0] + dir1[1]*dir1[1])      # distance to the previous node
      dist2 = math.sqrt(dir2[0]*dir2[0] + dir2[1]*dir2[1])      # distance to the next node
      handle1 = [ t[0][0] - t[1][0], t[0][1] - t[1][1] ]        # handle towards previous node (rel coords)
      handle2 = [ t[2][0] - t[1][0], t[2][1] - t[1][1] ]        # handle towards next node (rel coords)
      if handle1 == [ 0, 0 ]: handle1 = dir1
      if handle2 == [ 0, 0 ]: handle2 = dir2

      prev = { 'idx': prev_idx, 'dir':dir1, 'handle':handle1 }
      next = { 'idx': next_idx, 'dir':dir2, 'handle':handle2 }
      sn = { 'idx': node_idx, 'prev': prev, 'next': next, 'x': t[1][0], 'y': t[1][1] }

      if dist1 < self.radius:
        print("subpath node_idx=%d, dist to prev(%d) is smaller than radius: %g < %g" %
              (node_idx, prev_idx, dist1, self.radius), file=sys.stderr)
        pprint.pprint(sn, stream=sys.stderr)
        return None
      if dist2 < self.radius:
        print("subpath node_idx=%d, dist to next(%d) is smaller than radius: %g < %g" %
              (node_idx, next_idx, dist2, self.radius), file=sys.stderr)
        pprint.pprint(sn, stream=sys.stderr)
        return None

      len_h1 = math.sqrt(handle1[0]*handle1[0] + handle1[1]*handle1[1])
      len_h2 = math.sqrt(handle2[0]*handle2[0] + handle2[1]*handle2[1])
      prev['hlen'] = len_h1
      next['hlen'] = len_h2

      if len_h1 < self.radius:
        print("subpath node_idx=%d, handle to prev(%d) is shorter than radius: %g < %g" %
              (node_idx, prev_idx, len_h1, self.radius), file=sys.stderr)
        pprint.pprint(sn, stream=sys.stderr)
        return None
      if len_h2 < self.radius:
        print("subpath node_idx=%d, handle to next(%d) is shorter than radius: %g < %g" %
              (node_idx, next_idx, len_h2, self.radius), file=sys.stderr)
        pprint.pprint(sn, stream=sys.stderr)
        return None

      if len_h1 > dist1: # shorten that handle to dist1, avoid overshooting the point
        handle1[0] = handle1[0] * dist1 / len_h1
        handle1[1] = handle1[1] * dist1 / len_h1
        prev['hlen'] = dist1
      if len_h2 > dist2: # shorten that handle to dist2, avoid overshooting the point
        handle2[0] = handle2[0] * dist2 / len_h2
        handle2[1] = handle2[1] * dist2 / len_h2
        next['hlen'] = dist2

      return sn


    def subpath_round_corner(self, sp, node_idx):
      sn = self.super_node(sp, node_idx)
      if sn is None: return sp          # do nothing. stderr messages are already printed.

      # from https://de.wikipedia.org/wiki/Schnittwinkel_(Geometrie)
      # wikipedia has an abs() in the formula, which extracts the smaller of the two angles.
      # we don't want that. We need to distinguish betwenn spitzwingklig and stumpfwinklig.
      #
      # The angle to be rounded is now between the vectors a and b
      #
      a = sn['prev']['handle']
      b = sn['next']['handle']
      a_len = sn['prev']['hlen']
      b_len = sn['next']['hlen']
      alpha = math.acos( (a[0]*b[0]+a[1]*b[1]) / ( math.sqrt(a[0]*a[0]+a[1]*a[1]) * math.sqrt(b[0]*b[0]+b[1]*b[1]) ) )
      sn['alpha'] = math.degrees(alpha)

      # find the amount to trim back both sides so that a circle of radius self.radius would perfectly fit.
      if alpha < self.eps: return sp    # path folds back on itself here. No use to apply a radius.
      if abs(alpha - math.pi/2) < self.eps: return sp   # stretched. radius won't be visible.
      trim = self.radius / math.tan(0.5 * alpha)
      sn['trim'] = trim
      if trim < 0.0:
        print("Error: at node_idx=%d: angle=%g°, trim is negative: %g" % (node_idx, math.degrees(alpha), trim), file=sys.stderr)
        return sp
      if trim > max_trim_factor*min(a_len, b_len):
        if self.debug:
          print("Skipping where trim > %g * hlen" % max_trim_factor, file=self.tty)
          pprint.pprint(sn, stream=self.tty)
        return sp
      trim_pt_p = [ sn['x'] + a[0] * trim / a_len, sn['y'] + a[1] * trim / a_len ]
      trim_pt_n = [ sn['x'] + b[0] * trim / b_len, sn['y'] + b[1] * trim / b_len ]
      sn['prev']['trim_pt'] = trim_pt_p
      sn['next']['trim_pt'] = trim_pt_n

      pprint.pprint(sn, stream=self.tty)
      pprint.pprint(self.cut, stream=self.tty)
      # we replace the node_idx node by two points pt_a, pt_b.
      # FIXME: do we need an extra middle point if alpha > 90° ?
      # dummy variant: a stright line instead of an arc:
      pt_a = [ sp[node_idx][0][:], trim_pt_p[:], trim_pt_p[:]       ]
      pt_b = [ trim_pt_n[:],       trim_pt_n[:], sp[node_idx][2][:] ]
      sp = sp[:node_idx] + [pt_a] + [pt_b] + sp[node_idx+1:]

      # FIXME: Move out the outer handles pt_a[0] and pt_b[2], so that they are never inside.
      # FIXME: adjust the inner handles pt_a[2] and pt_b[0] so that they shape a nice arc

      return sp


    def clean_up(self):         # __fini__
      if self.tty is not None:
        self.tty.close()
      super(RoundedCorners, self).clean_up()


if __name__ == '__main__':
    RoundedCorners().run()
