"""
Live Preview Generator
Creates an HTML file you can open in your browser to see design changes instantly.

Usage:
    cd MLB_Matchup/image_generation
    python generate_live_preview.py

Then open: MLB_Matchup/image_generation/live_preview.html in your browser
Edit design_config.py, run this script again, and refresh your browser!
"""

import os
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from jinja2_image_generator import Jinja2ImageGenerator
from design_config import SAMPLE_DATA

def generate_preview():
    """Generate live preview HTML file"""
    print("Generating live preview...")

    # Initialize generator
    generator = Jinja2ImageGenerator()

    # Prepare template data
    template_data = generator.prepare_template_data(SAMPLE_DATA)

    # Render template  (swap v2 <-> v3 to preview either version)
    template_path = os.path.join(os.path.dirname(__file__), 'image_generator_v3.html')
    html_content = generator.render_template(template_path, template_data)

    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), 'live_preview.html')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Preview generated: {output_path}")
    print()
    print("How to use:")
    print("   1. Open live_preview.html in your browser")
    print("   2. Edit design_config.py to change sizes, colors, etc.")
    print("   3. Run this script again: python generate_live_preview.py")
    print("   4. Refresh your browser to see changes!")
    print()
    print("Tip: Keep the HTML file open and just refresh after changes")

    return output_path


if __name__ == "__main__":
    generate_preview()
