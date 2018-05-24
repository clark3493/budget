import os
import sys

cli_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(cli_dir))
cfg_dir = r'C:\Projects\_budget'

if cli_dir not in sys.path:
    sys.path(cli_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)
if cfg_dir not in sys.path:
    sys.path.append(cfg_dir)
