from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import pickle
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Try to import TensorFlow
try:
    import tensorflow as tf
    from tensorflow import keras
    MODEL_AVAILABLE = True
    print("[OK] TensorFlow loaded successfully")
except ImportError:
    MODEL_AVAILABLE = False
    print("[WARNING] TensorFlow not available - using enhanced color-based classification")

# Comprehensive Disease Classes (PlantVillage dataset - 38 classes)
DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# Detailed disease information database
DISEASE_INFO = {
    'healthy': {
        'severity': 'None',
        'treatment': 'No treatment needed. Plant appears healthy. Continue regular maintenance and monitoring.',
        'prevention': 'Maintain good agricultural practices, proper watering schedule, and regular inspection for early disease detection.'
    },
    'Apple_scab': {
        'severity': 'Moderate',
        'treatment': 'Remove infected leaves and fruit. Apply fungicides in early spring before symptoms appear.',
        'prevention': 'Plant resistant varieties, ensure good air circulation, and remove fallen leaves in autumn.'
    },
    'Black_rot': {
        'severity': 'High',
        'treatment': 'Prune infected branches at least 8-12 inches below visible cankers. Apply fungicides.',
        'prevention': 'Remove mummified fruit and infected wood. Maintain tree vigor through proper fertilization.'
    },
    'Cedar_apple_rust': {
        'severity': 'Moderate',
        'treatment': 'Apply fungicides from bud break through fruit development. Remove nearby cedar trees if possible.',
        'prevention': 'Plant resistant apple varieties and maintain distance from cedar trees.'
    },
    'Bacterial_spot': {
        'severity': 'Moderate',
        'treatment': 'Apply copper-based bactericides. Remove and destroy severely infected plant parts.',
        'prevention': 'Use disease-free seeds and transplants, avoid overhead irrigation, ensure good air circulation, and practice crop rotation.'
    },
    'Cercospora_leaf_spot': {
        'severity': 'Moderate',
        'treatment': 'Apply fungicides when symptoms first appear. Remove infected leaves from lower plant parts.',
        'prevention': 'Practice crop rotation (2-3 years), deep plow crop residue, and ensure adequate plant spacing.'
    },
    'Common_rust': {
        'severity': 'Moderate',
        'treatment': 'Apply fungicides at first sign of disease. Consider resistance rating when selecting varieties.',
        'prevention': 'Plant resistant hybrids, ensure adequate plant nutrition, and monitor fields regularly during humid weather.'
    },
    'Northern_Leaf_Blight': {
        'severity': 'High',
        'treatment': 'Apply foliar fungicides when disease first appears. Remove crop residue after harvest.',
        'prevention': 'Use resistant hybrids, practice minimum 2-year crop rotation, and tillage to bury crop debris.'
    },
    'Early_blight': {
        'severity': 'Moderate',
        'treatment': 'Apply fungicides containing chlorothalonil, mancozeb, or copper. Remove and destroy infected lower leaves.',
        'prevention': 'Use certified disease-free seeds, practice crop rotation (3-4 years), mulch to prevent soil splash, and avoid wetting foliage.'
    },
    'Late_blight': {
        'severity': 'High',
        'treatment': 'Apply fungicides immediately upon detection. In severe cases, destroy all infected plants to prevent spread.',
        'prevention': 'Plant resistant varieties, ensure good drainage and air circulation, avoid overhead irrigation, and monitor weather for blight-favorable conditions.'
    },
    'Leaf_blight': {
        'severity': 'Moderate',
        'treatment': 'Apply copper-based fungicide or chlorothalonil. Remove affected leaves and ensure proper plant spacing for air circulation.',
        'prevention': 'Maintain proper drainage, avoid overhead irrigation, apply preventive fungicides during humid seasons, and practice crop rotation.'
    },
    'Leaf_Mold': {
        'severity': 'Moderate',
        'treatment': 'Improve greenhouse ventilation and reduce humidity below 85%. Apply fungicides if infection is severe.',
        'prevention': 'Maintain good air circulation, avoid high humidity (keep below 85%), water at soil level, and remove infected leaves promptly.'
    },
    'Powdery_mildew': {
        'severity': 'Moderate',
        'treatment': 'Apply sulfur-based fungicides, potassium bicarbonate, or neem oil. Remove heavily infected plant parts.',
        'prevention': 'Ensure proper plant spacing for air flow, avoid excess nitrogen fertilizer, water early in day, and plant in sunny locations.'
    },
    'Septoria_leaf_spot': {
        'severity': 'Moderate',
        'treatment': 'Apply chlorothalonil or copper-based fungicides. Remove infected lower leaves and mulch around plants.',
        'prevention': 'Practice crop rotation (3 years minimum), avoid overhead watering, stake plants for airflow, and remove plant debris.'
    },
    'Spider_mites': {
        'severity': 'Moderate',
        'treatment': 'Spray with insecticidal soap, neem oil, or horticultural oil. Increase humidity around plants. Use miticides for severe infestations.',
        'prevention': 'Regular inspection of leaf undersides, maintain adequate moisture, introduce natural predators (ladybugs), and avoid dusty conditions.'
    },
    'Target_Spot': {
        'severity': 'Moderate',
        'treatment': 'Apply fungicides containing chlorothalonil or mancozeb. Remove and destroy infected leaves.',
        'prevention': 'Practice crop rotation, maintain proper plant spacing, avoid leaf wetness, and use disease-free transplants.'
    },
    'Yellow_Leaf_Curl_Virus': {
        'severity': 'High',
        'treatment': 'No cure available. Remove and destroy infected plants immediately to prevent virus spread to healthy plants.',
        'prevention': 'Control whitefly vectors with insecticides or yellow sticky traps, use virus-resistant varieties, employ reflective mulches, and use insect-proof nets.'
    },
    'Tomato_mosaic_virus': {
        'severity': 'High',
        'treatment': 'No cure exists. Remove infected plants immediately. Disinfect tools with 10% bleach solution.',
        'prevention': 'Use virus-free certified seeds, control aphid vectors, disinfect hands and tools, avoid tobacco use near plants, and practice strict sanitation.'
    },
    'Haunglongbing': {
        'severity': 'High',
        'treatment': 'No cure. Remove infected trees immediately. Control psyllid vectors with approved insecticides.',
        'prevention': 'Use certified disease-free nursery stock, control Asian citrus psyllid populations, and remove infected trees promptly.'
    },
    'Leaf_scorch': {
        'severity': 'Moderate',
        'treatment': 'Remove severely infected leaves. Improve watering practices and ensure consistent soil moisture.',
        'prevention': 'Maintain consistent moisture levels, mulch around plants, avoid water stress, and ensure proper drainage.'
    },
    'Esca': {
        'severity': 'High',
        'treatment': 'Prune infected vines during dormancy. There is no curative treatment once symptoms appear.',
        'prevention': 'Use proper pruning techniques, protect pruning wounds, and maintain vine vigor through proper nutrition.'
    }
}

# Global model variable
model = None
model_loaded = False

def load_trained_model():
    """Try to load a pre-trained model if available"""
    global model, model_loaded
    
    if not MODEL_AVAILABLE:
        return None
    
    try:
        model_path = 'models/plant_disease_model.h5'
        
        if os.path.exists(model_path):
            print(f"[INFO] Loading model from {model_path}...")
            model = keras.models.load_model(model_path, compile=False)
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            model_loaded = True
            print("[OK] Pre-trained model loaded successfully!")
            return model
        else:
            print("[WARNING] No pre-trained model found. Using fallback classification.")
            print(f"   To use ML model: place trained model at {model_path}")
            return None
            
    except Exception as e:
        print(f"[WARNING] Error loading model: {e}")
        return None

# Load Crop Recommendation Model
crop_model = None
crop_le = None

try:
    with open('models/crop_recommendation_model.pkl', 'rb') as f:
        crop_model = pickle.load(f)
    print(f"[OK] Crop Recommendation Model loaded successfully! Type: {type(crop_model)}")
    
    with open('models/label_encoder.pkl', 'rb') as f:
        crop_le = pickle.load(f)
    print(f"[OK] Label Encoder loaded successfully! Classes: {len(crop_le.classes_)}")
    
except Exception as e:
    print(f"[WARNING] Failed to load crop model: {e}")
    crop_model = None

# Comprehensive Fertilizer Recommendations Database
FERTILIZER_INFO = {
    'rice': {
        'primary_fertilizer': 'NPK 20-10-10',
        'npk_ratio': '20-10-10',
        'application_rate': '120-150 kg/hectare',
        'timing': 'Apply at planting (30%), tillering stage (30%), and panicle initiation (40%)',
        'organic_alternative': 'Compost (5-7 tons/hectare) + Green manure',
        'micronutrients': 'Zinc sulfate (25 kg/ha) for better yield',
        'notes': 'Rice requires high nitrogen. Split application is crucial for optimal growth.'
    },
    'maize': {
        'primary_fertilizer': 'NPK 15-15-15',
        'npk_ratio': '15-15-15',
        'application_rate': '100-120 kg/hectare',
        'timing': 'Apply at sowing (50%) and knee-high stage (50%)',
        'organic_alternative': 'Farm yard manure (10 tons/hectare) + Vermicompost',
        'micronutrients': 'Zinc (5 kg/ha) and Boron (1 kg/ha)',
        'notes': 'Balanced NPK is essential. Side-dress nitrogen at V6 stage for best results.'
    },
    'chickpea': {
        'primary_fertilizer': 'DAP (Diammonium Phosphate)',
        'npk_ratio': '18-46-0',
        'application_rate': '60-80 kg/hectare',
        'timing': 'Apply full dose at sowing as basal application',
        'organic_alternative': 'Rhizobium culture + Rock phosphate (200 kg/ha)',
        'micronutrients': 'Sulfur (20 kg/ha) for better nodulation',
        'notes': 'Being a legume, chickpea fixes nitrogen. Focus on phosphorus for root development.'
    },
    'kidneybeans': {
        'primary_fertilizer': 'NPK 10-26-26',
        'npk_ratio': '10-26-26',
        'application_rate': '50-70 kg/hectare',
        'timing': 'Apply at planting with additional side-dressing at flowering',
        'organic_alternative': 'Compost (3-4 tons/hectare) + Rhizobium inoculation',
        'micronutrients': 'Molybdenum for nitrogen fixation',
        'notes': 'Low nitrogen requirement due to nitrogen fixation. Emphasize phosphorus and potassium.'
    },
    'pigeonpeas': {
        'primary_fertilizer': 'SSP (Single Super Phosphate)',
        'npk_ratio': '0-16-0',
        'application_rate': '40-50 kg/hectare',
        'timing': 'Apply at sowing time',
        'organic_alternative': 'Farmyard manure (5 tons/hectare) + Rhizobium culture',
        'micronutrients': 'Sulfur (15 kg/ha)',
        'notes': 'Minimal fertilizer needed. Pigeon pea is drought-resistant and fixes nitrogen efficiently.'
    },
    'mothbeans': {
        'primary_fertilizer': 'NPK 12-32-16',
        'npk_ratio': '12-32-16',
        'application_rate': '40-50 kg/hectare',
        'timing': 'Apply full dose at sowing',
        'organic_alternative': 'Vermicompost (2 tons/hectare)',
        'micronutrients': 'Zinc and Iron for arid conditions',
        'notes': 'Drought-tolerant crop. Minimal fertilizer requirement with focus on phosphorus.'
    },
    'mungbean': {
        'primary_fertilizer': 'NPK 10-20-20',
        'npk_ratio': '10-20-20',
        'application_rate': '50-60 kg/hectare',
        'timing': 'Apply at sowing with light top-dressing at flowering',
        'organic_alternative': 'Compost (3 tons/hectare) + Rhizobium inoculation',
        'micronutrients': 'Molybdenum and Boron',
        'notes': 'Short-duration crop. Moderate fertilizer needs with emphasis on phosphorus.'
    },
    'blackgram': {
        'primary_fertilizer': 'NPK 10-26-26',
        'npk_ratio': '10-26-26',
        'application_rate': '50-60 kg/hectare',
        'timing': 'Apply at sowing time',
        'organic_alternative': 'Farmyard manure (4 tons/hectare) + Biofertilizers',
        'micronutrients': 'Sulfur (20 kg/ha) and Zinc (5 kg/ha)',
        'notes': 'Leguminous crop with good nitrogen fixation. Focus on P and K for better yields.'
    },
    'lentil': {
        'primary_fertilizer': 'DAP (Diammonium Phosphate)',
        'npk_ratio': '18-46-0',
        'application_rate': '50-60 kg/hectare',
        'timing': 'Apply full dose at sowing',
        'organic_alternative': 'Compost (3-4 tons/hectare) + Rhizobium culture',
        'micronutrients': 'Sulfur (15 kg/ha) and Boron (1 kg/ha)',
        'notes': 'Cool-season legume. Phosphorus is critical for root development and nodulation.'
    },
    'pomegranate': {
        'primary_fertilizer': 'NPK 19-19-19',
        'npk_ratio': '19-19-19',
        'application_rate': '500-600 grams/plant/year',
        'timing': 'Split into 4 doses: Feb, May, Aug, Nov',
        'organic_alternative': 'Farmyard manure (20-25 kg/plant) + Neem cake',
        'micronutrients': 'Zinc, Iron, and Boron sprays during flowering',
        'notes': 'Fruit crop requiring balanced nutrition. Increase K during fruit development.'
    },
    'banana': {
        'primary_fertilizer': 'NPK 10-6-40',
        'npk_ratio': '10-6-40',
        'application_rate': '200-300 grams/plant/month',
        'timing': 'Monthly application for 9-10 months',
        'organic_alternative': 'Farmyard manure (25 kg/plant) + Vermicompost',
        'micronutrients': 'Magnesium and Calcium for quality fruits',
        'notes': 'Heavy feeder requiring high potassium. Regular feeding essential for bunch development.'
    },
    'mango': {
        'primary_fertilizer': 'NPK 10-10-20',
        'npk_ratio': '10-10-20',
        'application_rate': '1-1.5 kg/tree/year (mature trees)',
        'timing': 'Apply in 2 splits: May-June and Sept-Oct',
        'organic_alternative': 'Farmyard manure (50 kg/tree) + Bone meal',
        'micronutrients': 'Zinc, Boron, and Iron sprays',
        'notes': 'Increase potassium during fruit setting. Reduce nitrogen to avoid excessive vegetative growth.'
    },
    'grapes': {
        'primary_fertilizer': 'NPK 19-19-19',
        'npk_ratio': '19-19-19',
        'application_rate': '400-500 grams/vine/year',
        'timing': 'Apply in 3-4 splits during growing season',
        'organic_alternative': 'Compost (10-15 kg/vine) + Seaweed extract',
        'micronutrients': 'Zinc, Boron, and Magnesium',
        'notes': 'Balanced nutrition critical. Adjust K during berry development for sweetness.'
    },
    'watermelon': {
        'primary_fertilizer': 'NPK 12-12-17',
        'npk_ratio': '12-12-17',
        'application_rate': '80-100 kg/hectare',
        'timing': 'Apply at planting (40%), vine growth (30%), and flowering (30%)',
        'organic_alternative': 'Compost (8-10 tons/hectare) + Bone meal',
        'micronutrients': 'Boron and Calcium for fruit quality',
        'notes': 'High potassium needed for fruit sweetness. Avoid excess nitrogen to prevent vine growth.'
    },
    'muskmelon': {
        'primary_fertilizer': 'NPK 13-13-21',
        'npk_ratio': '13-13-21',
        'application_rate': '80-100 kg/hectare',
        'timing': 'Apply at planting, vine growth, and fruit development stages',
        'organic_alternative': 'Farmyard manure (10 tons/hectare) + Vermicompost',
        'micronutrients': 'Boron, Calcium, and Magnesium',
        'notes': 'Similar to watermelon. High K for sweetness and shelf life.'
    },
    'apple': {
        'primary_fertilizer': 'NPK 10-10-10',
        'npk_ratio': '10-10-10',
        'application_rate': '1-2 kg/tree/year (bearing trees)',
        'timing': 'Apply in early spring and after fruit set',
        'organic_alternative': 'Compost (30-40 kg/tree) + Bone meal',
        'micronutrients': 'Calcium, Boron, and Zinc',
        'notes': 'Balanced fertilization. Calcium critical for preventing bitter pit.'
    },
    'orange': {
        'primary_fertilizer': 'NPK 8-3-9',
        'npk_ratio': '8-3-9',
        'application_rate': '1.5-2 kg/tree/year',
        'timing': 'Apply in 3 splits: Feb, June, and Sept',
        'organic_alternative': 'Farmyard manure (40-50 kg/tree) + Neem cake',
        'micronutrients': 'Zinc, Iron, and Manganese sprays',
        'notes': 'Citrus-specific fertilizer recommended. Regular micronutrient sprays prevent deficiencies.'
    },
    'papaya': {
        'primary_fertilizer': 'NPK 12-12-12',
        'npk_ratio': '12-12-12',
        'application_rate': '200-250 grams/plant/month',
        'timing': 'Monthly application starting 2 months after planting',
        'organic_alternative': 'Vermicompost (5 kg/plant/month) + Neem cake',
        'micronutrients': 'Boron and Zinc for fruit quality',
        'notes': 'Fast-growing crop. Regular balanced feeding essential for continuous fruiting.'
    },
    'coconut': {
        'primary_fertilizer': 'NPK 16-16-16',
        'npk_ratio': '16-16-16',
        'application_rate': '1.3 kg/palm/year (adult palms)',
        'timing': 'Apply in 2 splits: May-June and Sept-Oct',
        'organic_alternative': 'Farmyard manure (50 kg/palm) + Green manure',
        'micronutrients': 'Boron (50g/palm) and Magnesium',
        'notes': 'Add common salt (1 kg/palm) for coastal areas. Chloride improves nut quality.'
    },
    'cotton': {
        'primary_fertilizer': 'NPK 17-17-17',
        'npk_ratio': '17-17-17',
        'application_rate': '100-125 kg/hectare',
        'timing': 'Apply at sowing (50%) and square formation (50%)',
        'organic_alternative': 'Farmyard manure (10 tons/hectare) + Neem cake',
        'micronutrients': 'Zinc (25 kg/ha) and Boron (10 kg/ha)',
        'notes': 'High nutrient demanding crop. Potassium critical for fiber quality and boll development.'
    },
    'jute': {
        'primary_fertilizer': 'NPK 20-10-5',
        'npk_ratio': '20-10-5',
        'application_rate': '80-100 kg/hectare',
        'timing': 'Apply at sowing (60%) and 30 days after sowing (40%)',
        'organic_alternative': 'Compost (5 tons/hectare) + Green manure',
        'micronutrients': 'Sulfur (20 kg/ha) for fiber quality',
        'notes': 'High nitrogen requirement for fiber production. Adequate moisture essential.'
    },
    'coffee': {
        'primary_fertilizer': 'NPK 10-10-20',
        'npk_ratio': '10-10-20',
        'application_rate': '300-400 grams/plant/year',
        'timing': 'Apply in 3 splits: April, June, and September',
        'organic_alternative': 'Compost (10-15 kg/plant) + Coffee pulp',
        'micronutrients': 'Zinc, Boron, and Magnesium',
        'notes': 'Shade-grown crop. Organic matter critical. High K for bean quality.'
    }
}

def get_fertilizer_recommendation(crop_name):
    """Get fertilizer recommendation for a specific crop"""
    crop_key = crop_name.lower().strip()
    
    # Handle variations in crop names
    crop_mapping = {
        'kidney beans': 'kidneybeans',
        'pigeon peas': 'pigeonpeas',
        'moth beans': 'mothbeans',
        'mung bean': 'mungbean',
        'black gram': 'blackgram'
    }
    
    crop_key = crop_mapping.get(crop_key, crop_key)
    
    return FERTILIZER_INFO.get(crop_key, {
        'primary_fertilizer': 'NPK 10-10-10',
        'npk_ratio': '10-10-10',
        'application_rate': 'Consult local agricultural expert',
        'timing': 'Apply based on crop growth stages',
        'organic_alternative': 'Compost and farmyard manure',
        'micronutrients': 'Based on soil test',
        'notes': 'For specific recommendations, consult your local agricultural extension office.'
    })


def preprocess_image_for_ml(image_path):
    """Preprocess image for ML model prediction"""
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def analyze_image_enhanced(image_path):
    """
    Enhanced color and pattern-based disease detection
    More sophisticated with plant type identification
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_resized = img.resize((224, 224))
        img_array = np.array(img_resized)
        
        # Calculate various color features
        r = img_array[:, :, 0]
        g = img_array[:, :, 1]
        b = img_array[:, :, 2]
        
        # Color statistics
        r_mean, g_mean, b_mean = r.mean(), g.mean(), b.mean()
        r_std, g_std, b_std = r.std(), g.std(), b.std()
        
        # Color ratios
        rg_ratio = r_mean / (g_mean + 1)
        rb_ratio = r_mean / (b_mean + 1)
        gb_ratio = g_mean / (b_mean + 1)
        
        # Overall variability
        total_std = (r_std + g_std + b_std) / 3
        
        # Detect bright spots (potential diseases)
        bright_spots = np.sum((r > 200) & (g > 200) & (b > 200))
        total_pixels = r.size
        bright_ratio = bright_spots / total_pixels
        
        # Detect dark spots (diseases)
        dark_spots = np.sum((r < 60) & (g < 60) & (b < 60))
        dark_ratio = dark_spots / total_pixels
        
        # Detect red/ripe fruit (tomatoes, apples)
        red_fruit = np.sum((r > 140) & (r > g * 1.3) & (r > b * 1.3))
        red_ratio = red_fruit / total_pixels
        
        # Detect orange colors (tomatoes, rust diseases)
        orange_pixels = np.sum((r > 150) & (g > 80) & (g < 150) & (b < 100))
        orange_ratio = orange_pixels / total_pixels
        
        # Yellow/pale colors (rust, yellowing diseases)
        yellow_pixels = np.sum((r > 150) & (g > 130) & (b < 120))
        yellow_ratio = yellow_pixels / total_pixels
        
        # Green vegetation
        green_pixels = np.sum((g > r) & (g > b) & (g > 60))
        green_ratio = green_pixels / total_pixels
        
        # Brown/tan (dead tissue, blight)
        brown_pixels = np.sum((r > 80) & (r < 160) & (g > 60) & (g < 140) & (b < 100))
        brown_ratio = brown_pixels / total_pixels
        
        print(f"\nDetailed Image Analysis:")
        print(f"  RGB Means: R={r_mean:.1f}, G={g_mean:.1f}, B={b_mean:.1f}")
        print(f"  Red fruit: {red_ratio:.3f}, Orange: {orange_ratio:.3f}")
        print(f"  Yellow: {yellow_ratio:.3f}, Green: {green_ratio:.3f}, Brown: {brown_ratio:.3f}")
        print(f"  Dark spots: {dark_ratio:.3f}, Variability: {total_std:.1f}")
        
        # ========== STEP 1: IDENTIFY PLANT TYPE ==========
        
        plant_type = "unknown"
        
        # Check for tomato fruit (red/orange round fruit)
        if red_ratio > 0.15 or (orange_ratio > 0.2 and r_mean > 140):
            plant_type = "tomato"
            print(f"  -> Detected: TOMATO plant (red/orange fruit present)")
        
        # Check for corn/maize (elongated leaves, yellow-green, vertical patterns)
        elif green_ratio > 0.4 and yellow_ratio > 0.1 and r_mean < 140 and total_std < 60:
            plant_type = "corn"
            print(f"  -> Detected: CORN/MAIZE plant")
        
        # Check for potato (broader leaves, darker green)
        elif green_ratio > 0.5 and r_mean < 100 and brown_ratio > 0.1:
            plant_type = "potato"
            print(f"  -> Detected: POTATO plant")
        
        # Check for apple/fruit trees (woody stems, round fruits)
        elif red_ratio > 0.1 and green_ratio > 0.3:
            plant_type = "apple"
            print(f"  -> Detected: APPLE/FRUIT tree")
        
        # Default to tomato if red/orange dominant
        elif r_mean > 120 and r_mean > g_mean:
            plant_type = "tomato"
            print(f"  -> Detected: Likely TOMATO (red tones)")
        else:
            plant_type = "general"
            print(f"  -> Could not determine specific plant type")
        
        # ========== STEP 2: IDENTIFY DISEASE BASED ON PLANT TYPE ==========
        
        # TOMATO DISEASES
        if plant_type == "tomato":
            # Late blight - dark brown/black lesions
            if dark_ratio > 0.05 and brown_ratio > 0.1 and total_std > 45:
                return 'Tomato___Late_blight', 82
            
            # Bacterial spot - dark spots on fruit/leaves
            elif dark_ratio > 0.03 and total_std > 50:
                return 'Tomato___Bacterial_spot', 78
            
            # Early blight - brown concentric rings
            elif brown_ratio > 0.15 and total_std > 40:
                return 'Tomato___Early_blight', 75
            
            # Target spot
            elif brown_ratio > 0.1 and dark_ratio > 0.02:
                return 'Tomato___Target_Spot', 72
            
            # Septoria leaf spot
            elif dark_ratio > 0.02 and yellow_ratio > 0.05:
                return 'Tomato___Septoria_leaf_spot', 70
            
            # Yellow leaf curl virus
            elif yellow_ratio > 0.3 and green_ratio < 0.3:
                return 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 80
            
            # Leaf mold
            elif yellow_ratio > 0.2 and brown_ratio > 0.05:
                return 'Tomato___Leaf_Mold', 68
            
            # Healthy tomato
            elif red_ratio > 0.2 and dark_ratio < 0.02:
                return 'Tomato___healthy', 85
            
            # Default tomato disease
            else:
                return 'Tomato___Bacterial_spot', 65
        
        # CORN DISEASES
        elif plant_type == "corn":
            # Common rust - orange/yellow pustules
            if yellow_ratio > 0.15 and orange_ratio > 0.1:
                return 'Corn_(maize)___Common_rust_', 78
            
            # Northern Leaf Blight - tan elongated lesions
            elif brown_ratio > 0.15 and total_std > 45:
                return 'Corn_(maize)___Northern_Leaf_Blight', 75
            
            # Gray leaf spot
            elif brown_ratio > 0.1 and dark_ratio > 0.05:
                return 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 72
            
            # Healthy corn
            elif green_ratio > 0.5 and dark_ratio < 0.02:
                return 'Corn_(maize)___healthy', 85
            
            else:
                return 'Corn_(maize)___Common_rust_', 68
        
        # POTATO DISEASES
        elif plant_type == "potato":
            # Late blight
            if dark_ratio > 0.1 and brown_ratio > 0.15:
                return 'Potato___Late_blight', 82
            
            # Early blight
            elif brown_ratio > 0.15 and total_std > 40:
                return 'Potato___Early_blight', 76
            
            # Healthy
            elif green_ratio > 0.6:
                return 'Potato___healthy', 85
            
            else:
                return 'Potato___Early_blight', 70
        
        # APPLE DISEASES
        elif plant_type == "apple":
            # Apple scab
            if dark_ratio > 0.05 and brown_ratio > 0.1:
                return 'Apple___Apple_scab', 75
            
            # Black rot
            elif dark_ratio > 0.1:
                return 'Apple___Black_rot', 78
            
            # Cedar apple rust
            elif orange_ratio > 0.05 and yellow_ratio > 0.1:
                return 'Apple___Cedar_apple_rust', 72
            
            # Healthy
            elif red_ratio > 0.3 or green_ratio > 0.5:
                return 'Apple___healthy', 85
            
            else:
                return 'Apple___Apple_scab', 68
        
        # GENERAL CLASSIFICATION (when plant type unknown)
        else:
            # Powdery mildew (white powdery appearance)
            if bright_ratio > 0.3 and r_mean > 180:
                return 'Squash___Powdery_mildew', 73
            
            # Late blight (dark lesions)
            elif dark_ratio > 0.15 and brown_ratio > 0.1:
                return 'Tomato___Late_blight', 75
            
            # Healthy green
            elif green_ratio > 0.6 and dark_ratio < 0.02:
                return 'Tomato___healthy', 80
            
            # Default
            else:
                return 'Tomato___Bacterial_spot', 65
            
    except Exception as e:
        print(f"Error in enhanced analysis: {e}")
        return 'Unknown Disease', 50

def analyze_image(image_path):
    """Main analysis function - tries ML model first, then fallback"""
    global model, model_loaded
    
    # Try ML model if available
    if MODEL_AVAILABLE and model_loaded and model is not None:
        try:
            img_array = preprocess_image_for_ml(image_path)
            predictions = model.predict(img_array, verbose=0)
            
            top_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][top_idx] * 100)
            
            predicted_class = DISEASE_CLASSES[top_idx]
            
            print(f"[OK] ML Prediction: {predicted_class} ({confidence:.2f}%)")
            
            return predicted_class, confidence
            
        except Exception as e:
            print(f"[WARNING] ML prediction failed: {e}")
            print("  Falling back to enhanced analysis...")
    
    # Fallback to enhanced color-based analysis
    return analyze_image_enhanced(image_path)

def format_disease_name(class_name):
    """Convert class name to readable format"""
    if '___' in class_name:
        plant, disease = class_name.split('___')
        plant = plant.replace('_', ' ').replace(',', '')
        disease = disease.replace('_', ' ')
        return f"{plant} - {disease}"
    return class_name.replace('_', ' ')

def get_disease_info(disease_name):
    """Get disease information from database"""
    # Normalize disease name for lookup
    disease_key = disease_name.lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace(',', '')
    
    # Try to find matching disease info
    for key, info in DISEASE_INFO.items():
        if key.lower() in disease_key or disease_key in key.lower():
            return info
    
    # Try partial matching
    for key, info in DISEASE_INFO.items():
        key_parts = key.lower().split('_')
        disease_parts = disease_key.split('_')
        if any(part in disease_parts for part in key_parts if len(part) > 3):
            return info
    
    # Default info
    return {
        'severity': 'Moderate',
        'treatment': 'Consult with an agricultural expert or extension service for proper identification and treatment plan for this specific condition.',
        'prevention': 'Maintain good agricultural practices including proper spacing, adequate nutrition, appropriate watering, and regular monitoring for early detection.'
    }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Crop recommendation prediction endpoint"""
    try:
        data = request.json
        nitrogen = float(data.get('nitrogen', 0))
        phosphorus = float(data.get('phosphorus', 0))
        potassium = float(data.get('potassium', 0))
        temperature = float(data.get('temperature', 0))
        humidity = float(data.get('humidity', 0))
        ph = float(data.get('pH', 0))
        rainfall = float(data.get('rainfall', 0))
        
        if crop_model and crop_le:
            # Prepare input array
            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
            
            # Get probabilities
            probs = crop_model.predict_proba(input_data)[0]
            
            # Get top 3 predictions
            top_3_idx = np.argsort(probs)[-3:][::-1]
            top_3_crops = crop_le.inverse_transform(top_3_idx)
            top_3_probs = probs[top_3_idx]
            
            # Main prediction
            crop = top_3_crops[0]
            confidence = round(top_3_probs[0] * 100, 2)
            
            # Create reason string
            reason = f"Based on your conditions (N:{nitrogen}, P:{phosphorus}, K:{potassium}, Temp:{temperature}°C, Rain:{rainfall}mm), " \
                     f"the model is {confidence}% confident that {crop} is the best choice."
            
            # Additional details for response
            recommendations = []
            for c, p in zip(top_3_crops, top_3_probs):
                recommendations.append({
                    'crop': c,
                    'confidence': round(p * 100, 1)
                })
            
            # Get fertilizer recommendation for the top crop
            fertilizer = get_fertilizer_recommendation(crop)
            
            return jsonify({
                'crop': crop.title(),
                'confidence': confidence,
                'reason': reason,
                'recommendations': recommendations,
                'fertilizer': fertilizer
            })
            
        else:
            # Fallback to rule-based if model fails
            print("[WARNING] Using fallback rule-based system")
            if rainfall > 150 and humidity > 70 and temperature > 20:
                crop, confidence, reason = 'Rice', 88, 'High rainfall and humidity with warm temperatures are ideal for rice cultivation.'
            elif temperature < 25 and rainfall < 100 and ph > 6:
                crop, confidence, reason = 'Wheat', 85, 'Cool temperatures with moderate rainfall are suitable for wheat cultivation.'
            elif temperature > 25 and rainfall > 100 and potassium > 40:
                crop, confidence, reason = 'Cotton', 82, 'Warm climate with adequate rainfall and potassium levels favor cotton growth.'
            elif temperature > 25 and rainfall > 150 and humidity > 70:
                crop, confidence, reason = 'Coconut', 92, 'Based on your soil nutrient levels and climate conditions, coconut cultivation is highly suitable for this region.'
            elif nitrogen > 80 and temperature > 20 and rainfall > 80:
                crop, confidence, reason = 'Maize', 86, 'Good nitrogen levels with favorable temperature and rainfall support maize cultivation.'
            else:
                crop, confidence, reason = 'Mixed Vegetables', 70, 'Your conditions are suitable for mixed vegetable cultivation with proper management.'
            
            # Get fertilizer recommendation
            fertilizer = get_fertilizer_recommendation(crop)
            
            return jsonify({
                'crop': crop, 
                'confidence': confidence, 
                'reason': reason,
                'recommendations': [{'crop': crop, 'confidence': confidence}],
                'fertilizer': fertilizer
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/classify_disease', methods=['POST'])
def classify_disease():
    """Disease classification endpoint"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            print(f"\n{'='*60}")
            print(f"Analyzing: {filename}")
            print(f"{'='*60}")
            
            # Analyze image
            predicted_class, confidence = analyze_image(filepath)
            
            # Format disease name
            disease_name = format_disease_name(predicted_class)
            
            # Get disease information
            disease_data = get_disease_info(predicted_class)
            
            result = {
                'disease': disease_name,
                'confidence': round(confidence, 2),
                'severity': disease_data['severity'],
                'treatment': disease_data['treatment'],
                'prevention': disease_data['prevention']
            }
            
            print(f"\nResult: {disease_name} ({confidence:.2f}%)")
            print(f"{'='*60}\n")
            
            return jsonify(result)
        
        return jsonify({'error': 'Invalid file type. Please upload JPG, JPEG, or PNG'}), 400
    
    except Exception as e:
        print(f"Error in classify_disease: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CROP RECOMMENDATION & DISEASE DETECTION SYSTEM")
    print("="*60)
    
    # Try to load ML model
    if MODEL_AVAILABLE:
        print("\n[INFO] TensorFlow available")
        load_trained_model()
    else:
        print("\n[WARNING] TensorFlow not available")
        print("  Using enhanced color-based disease detection")
    
    print("\n" + "="*60)
    print("Starting Flask server...")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)