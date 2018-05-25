import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.dirname(test_dir)
cfg_dir = r'C:\Projects\_budget'
sys.path.append(cfg_dir)
sys.path.insert(0, os.path.join(package_dir, 'src'))
