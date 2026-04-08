import numpy as np
import shap
from skimage.segmentation import slic
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def get_superpixels(image: np.ndarray, n_segments=50, compactness=10) -> np.ndarray:
    """Generates a superpixel mask array for a given 224x224x3 image."""
    return slic(image, n_segments=n_segments, compactness=compactness, start_label=1)

def generate_shap_heatmap(model_wrapper, input_tensor: np.ndarray) -> bytes:
    """
    Generates a SHAP KernelExplainer feature overlay using SLIC superpixels.
    This heavily boosts performance on TFLite black-box boundaries.
    """
    # 1. Extract the base image (224, 224, 3)
    img_3d = input_tensor[0]
    
    # 2. Get superpixels with lower density for speed
    segments = get_superpixels(img_3d, n_segments=8)
    
    # 3. Predict function that acts on purely binary masked versions of the superpixels
    def mask_predict(masks: np.ndarray) -> np.ndarray:
        # masks is shape (num_samples, num_superpixels)
        out = []
        for mask in masks:
            masked_img = np.copy(img_3d)
            for seg_id, is_active in enumerate(mask):
                if not is_active:
                    masked_img[segments == (seg_id + 1)] = 0.5 
            
            tensor = np.expand_dims(masked_img, axis=0)
            preds = model_wrapper.predict(tensor)
            out.append(preds[0])
        return np.array(out)
    
    # 4. Initialize KernelExplainer targeting all superpixels
    num_superpixels = len(np.unique(segments))
    background = np.zeros((1, num_superpixels))
    explainer = shap.KernelExplainer(mask_predict, background)
    
    active_mask = np.ones((1, num_superpixels))
    
    # 5. Calculate SHAP values (nsamples limits runtime drastically)
    # Must have nsamples > num_superpixels for LassoLars estimator to function mathematically
    shap_vals = explainer.shap_values(active_mask, nsamples=15)
    
    # Grab highest attribution index
    top_class_idx = np.argmax(model_wrapper.predict(input_tensor)[0])
    
    if isinstance(shap_vals, list):
        if len(shap_vals) > top_class_idx:
            class_shap = shap_vals[top_class_idx][0]
        else:
            class_shap = shap_vals[0][0] # Fallback for binary outputs
    else:
        # If output is 3D array (1, num_superpixels, num_classes)
        if len(shap_vals.shape) == 3:
            class_shap = shap_vals[0, :, top_class_idx]
        else:
            class_shap = shap_vals[0]

    # 6. Map the superpixel attributions back to pixel-level image structure
    heatmap = np.zeros_like(img_3d[:, :, 0])
    for seg_id in range(num_superpixels):
        heatmap[segments == (seg_id + 1)] = class_shap[seg_id]
        
    # 7. Normalize heatmap and use Matplotlib to overlay
    max_val = np.max(np.abs(heatmap))
    if max_val > 0:
        heatmap = heatmap / max_val
    
    plt.figure(figsize=(4, 4))
    plt.imshow(img_3d)
    # Red for positive SHAP values. We use 'jet' cmap
    # Mask out areas where attribution is near 0 so the original leaf shows
    alpha_mask = np.where(np.abs(heatmap) > 0.1, 0.6, 0.0) 
    plt.imshow(heatmap, cmap='jet', alpha=alpha_mask, vmin=-1, vmax=1)
    plt.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    
    return buf.read()
