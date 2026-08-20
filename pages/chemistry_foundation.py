from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from foundation_content import CHEMISTRY_FOUNDATION
from foundation_renderer import render_foundation_course
render_foundation_course(CHEMISTRY_FOUNDATION)
