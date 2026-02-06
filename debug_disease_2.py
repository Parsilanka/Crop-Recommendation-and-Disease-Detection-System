
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from PIL import Image
import numpy as np

try:
    from app import analyze_image_enhanced
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)

# Create a dummy image
dummy_path = "test_leaf.jpg"
img = Image.new('RGB', (500, 500), color = 'green')
img.save(dummy_path)

print("Running test on dummy image...")
result = analyze_image_enhanced(dummy_path)
print(f"Result: {result}")
