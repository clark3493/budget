import os
import sys

pkg_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(pkg_dir)
cfg_dir = r'C:\Projects\_budget'

if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
if src_dir not in sys.path:
    sys.path.insert(1, src_dir)
if cfg_dir not in sys.path:
    sys.path.append(cfg_dir)