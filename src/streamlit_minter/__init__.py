import sys
from pathlib import Path

import os

# Necessary for Streamlit Cloud deployment
# sys.path.append(str(Path(__file__).parents[2]))

# sys.path.append(os.path.abspath('.'))

print(os.path.abspath('.'))
print(Path(__file__).parents[2])