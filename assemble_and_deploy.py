# -*- coding: utf-8 -*-
"""
Assembler and deployment script for Kingmakers of Indian Politics.
Combines all three modules and outputs index.html, docs/index.html, and WebPreview/index.html.
"""
import os
import shutil

print("Importing modules...")
from build_complete_game import part_css_html
from build_js_code import get_js_code
from build_engine_assets import get_engine_code

print("Concatenating HTML, CSS, JavaScript, 3D Engine, and Assets...")
full_html = part_css_html + "\n" + get_js_code() + "\n" + get_engine_code()

print(f"Total HTML character count: {len(full_html)}")
print(f"Total lines: {len(full_html.splitlines())}")

# Verify essential elements exist
assert "KINGMAKERS" in full_html
assert "DravidianTempleGopuram" in full_html
assert "RiponBuilding" in full_html
assert "isTricolorScarf" in full_html
assert "applyEmotePose" in full_html
assert "AmbassadorCar" in full_html
assert "WaterTanker" in full_html
assert "ChennaiMTCBus" in full_html
assert "screen-scenarios" in full_html
assert "screen-roster" in full_html

target_paths = [
    r"e:\kip android\index.html",
    r"e:\kip android\docs\index.html",
    r"e:\kip android\WebPreview\index.html"
]

for p in target_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Successfully generated: {p} ({os.path.getsize(p)} bytes)")

print("All game files generated and synchronized successfully!")
