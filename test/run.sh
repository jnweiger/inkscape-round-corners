# new inkscape 1.0.1 API
env PYTHONPATH=/usr/share/inkscape/extensions python3 ./round_corners.py --selected-nodes path1684:0:2 test/zigzag.svg

# old inkscape 0.92.4 API
env PYTHONPATH=$(pwd)/test/inkex-0.92.4 python2 ./round_corners.py --selected-nodes path1684:0:2 test/zigzag.svg 
