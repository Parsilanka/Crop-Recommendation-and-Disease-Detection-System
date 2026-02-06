
from PIL import Image
import numpy as np
import os

# Mock the function from app.py
def analyze_image_enhanced(image_path):
    print(f"Analyzing {image_path}")
    try:
        img = Image.open(image_path).convert('RGB')
        img_resized = img.resize((224, 224))
        img_array = np.array(img_resized)
        
        print(f"Image array shape: {img_array.shape}")
        
        # Calculate various color features
        r = img_array[:, :, 0]
        g = img_array[:, :, 1]
        b = img_array[:, :, 2]
        
        # Color statistics
        r_mean, g_mean, b_mean = r.mean(), g.mean(), b.mean()
        r_std, g_std, b_std = r.std(), g.std(), b.std()
        
        print(f"Stats: R={r_mean}, G={g_mean}, B={b_mean}")
        
        return "Success"
            
    except Exception as e:
        print(f"Error in enhanced analysis: {e}")
        import traceback
        traceback.print_exc()
        return 'Unknown Disease', 50

# Create a dummy image
dummy_path = "test_leaf.jpg"
img = Image.new('RGB', (500, 500), color = 'green')
img.save(dummy_path)

print("Running test...")
analyze_image_enhanced(dummy_path)
