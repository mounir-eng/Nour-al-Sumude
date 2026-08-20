from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from review_content import PHYSICS_REVIEW
from review_renderer import render_review_course

render_review_course(PHYSICS_REVIEW)
