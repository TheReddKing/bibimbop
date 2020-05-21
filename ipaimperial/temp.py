import sys
import os  # noqa
sys.path.append(os.path.join(os.path.dirname(__file__), 'englishipa'))  # noqa

import eng_to_ipa as ipa

print(ipa.convert("parallelogram"))