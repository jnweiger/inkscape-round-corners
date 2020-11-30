#! /usr/bin/python3
#
# compute the center of a circle given to tangent points and their vectors.
#
#

import math
from pprint import pprint

radius = 2

s = {'alpha': 28.663124735951218,
 'idx': 6,
 'next': {'dir': [22.611999999999995, -12.360799999999998],
          'handle': [22.611999999999995, -12.360799999999998],
          'hlen': 25.76998099805275,
          'idx': 7,
          'trim_pt': [139.25697508594644, 78.60588989729494]},
 'prev': {'dir': [30.0, 0.0],
          'handle': [30.0, 0.0],
          'hlen': 30.0,
          'idx': 5,
          'trim_pt': [140.21629282862804, 82.3608]},
 'trim': 7.828292828628044,
 'x': 132.388,
 'y': 82.3608}

pprint(s)

def find_arc_c_m(s, radius):
  ## given the supernode and the radius, we compute and return two point:
  # c, the center of the arc and m, the midpoint of the arc.
  # Method used:
  # - construct the ray c_m_vec that runs though the original point p=[x,y] through c and m.
  # - next.trim_pt, [x,y] and c form a rectangular triangle. Thus we can
  #   compute cdist as the length of the hypothenuses under trim and radius.
  # - c is then cdist away from [x,y] along the vector c_m_vec.
  # - m is closer to [x,y] than c by exactly radius.

  a = [ s['prev']['trim_pt'][0] - s['x'], s['prev']['trim_pt'][1] - s['y'] ]
  b = [ s['next']['trim_pt'][0] - s['x'], s['next']['trim_pt'][1] - s['y'] ]

  c_m_vec = [ a[0] + b[0],
              a[1] + b[1] ]
  l = math.sqrt( c_m_vec[0]*c_m_vec[0] + c_m_vec[1]*c_m_vec[1] )

  cdist = math.sqrt( radius*radius + s['trim']*s['trim'] )    # distance from original point xy to circle center.

  c = [ s['x'] + cdist * c_m_vec[0] / l,                      # circle center
        s['y'] + cdist * c_m_vec[1] / l ]

  m = [ s['x'] + (cdist-radius) * c_m_vec[0] / l,             # spline midpoint
        s['y'] + (cdist-radius) * c_m_vec[1] / l ]

  return (c, m)


arc_c, arc_m = find_arc_c_m(s, radius)

pprint(arc_c)
pprint(arc_m)


def arc_bezier_handles(p1, p4, c):
  """
  Compute the control points p2 and p3 between points p1 and p4, so that the cubic bezier spline
  defined by p1,p2,p3,p2 approximates an arc around center c

  https://stackoverflow.com/questions/734076/how-to-best-approximate-a-geometrical-arc-with-a-bezier-curve
  https://hansmuller-flex.blogspot.com/2011/10/more-about-approximating-circular-arcs.html
  """
  x1,y1 = p1
  x4,y4 = p4
  xc,yc = c

  ax = x1 - xc
  ay = y1 - yc
  bx = x4 - xc
  by = y4 - yc
  q1 = ax * ax + ay * ay
  q2 = q1 + ax * bx + ay * by
  k2 = 4./3. * (math.sqrt(2 * q1 * q2) - q2) / (ax * by - ay * bx)

  x2 = xc + ax - k2 * ay
  y2 = yc + ay + k2 * ax
  x3 = xc + bx + k2 * by
  y3 = yc + by - k2 * bx

  return ([x2, y2], [x3, y3])


p2, p3 = arc_bezier_handles(s['prev']['trim_pt'], arc_m, arc_c)
print("\narc_bezier_handles(s['prev']['trim_pt'], arc_m, arc_c)")
pprint([ s['prev']['trim_pt'], p2, p3, arc_m ])

p5, p6 = arc_bezier_handles(arc_m, s['next']['trim_pt'], arc_c)
print("\narc_bezier_handles(arc_m, s['next']['trim_pt'], arc_c)")
pprint([ arc_m, p5, p6, s['next']['trim_pt'] ])
