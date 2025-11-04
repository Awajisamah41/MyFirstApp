from PIL import Image
import os
import numpy as np

def save_uploaded_file(uploaded_file, dest_folder="uploads"):
    os.makedirs(dest_folder, exist_ok=True)
    file_path = os.path.join(dest_folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def classify_image(image_path):
    """Simple heuristic classifier (MVP) — replace with real ML model later.
       Computes proportion of green pixels to guess biodegradable vs non-biodegradable.
    """
    im = Image.open(image_path).convert("RGB")
    im = im.resize((200,200))
    arr = np.array(im).astype(int)
    r,g,b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    green_mask = (g > r) & (g > b) & (g > 90)
    green_prop = green_mask.sum() / (arr.shape[0]*arr.shape[1])
    # heuristic score
    score = float(green_prop)
    if green_prop > 0.10:
        label = "biodegradable (plant/organic likely)"
        action = "Compost or bury; consider composting facility."
    else:
        label = "non-biodegradable (plastic/metal/glass likely)"
        action = "Recycle where possible; if contaminated, safe disposal."
    return {"label": label, "score": score, "recommended_action": action}
