import os
import sys

src_dir = os.path.dirname(os.path.abspath(__file__))
cfg_dir = r'C:\Projects\_budget'

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if cfg_dir not in sys.path:
    sys.path.append(cfg_dir)
