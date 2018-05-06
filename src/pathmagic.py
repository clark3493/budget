import os
import sys

src_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.dirname(src_dir)
sys.path.insert(0, r'C:\Projects\_budget')
sys.path.insert(0, os.path.join(package_dir, 'src'))
