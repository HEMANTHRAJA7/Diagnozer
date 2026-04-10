import numpy as np
import shap
from skimage.segmentation import slic
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def get_superpixels(image: np.ndarray, n_segments=50, compactness=10) -> np.ndarray:
    """Generates a superpixel mask array for a given HxWx3 image."""
    return slic(image, n_segments=n_segments, compactness=compactness, start_label=1)

def generate_shap_heatmap(model_wrapper, input_tensor: np.ndarray, display_image: np.ndarray = None) -> bytes:
    """
    Generates a SHAP KernelExplainer feature overlay using SLIC superpixels.
    
    Args:
        model_wrapper: TFLite model wrapper with .predict() method.
        input_tensor: Preprocessed tensor of shape (1, H, W, 3) used for model inference.
        display_image: Optional clean [0,1] scaled image of shape (H, W, 3) for heatmap overlay.
                       If not provided, falls back to input_tensor[0] (which may look off
                       if the tensor was preprocessed with EfficientNet/ImageNet normalization).
    """
    # 1. Extract the preprocessed image for SHAP masking
    img_3d = input_tensor[0]
    
    # Use the clean display image for visualization if provided
    if display_image is not None:
        vis_image = display_image
    else:
        # Fallback: try to make the preprocessed tensor displayable
        vis_image = img_3d.copy()
        # If values are outside [0,1], rescale for display
        vmin, vmax = vis_image.min(), vis_image.max()
        if vmin < 0 or vmax > 1.0:
            vis_image = (vis_image - vmin) / (vmax - vmin + 1e-8)
    
    # 2. Get superpixels from the display image (cleaner segmentation on real pixels)
    segments = get_superpixels(vis_image, n_segments=15)
    
    # 3. Predict function that acts on binary masked versions of the superpixels
    def mask_predict(masks: np.ndarray) -> np.ndarray:
        # masks is shape (num_samples, num_superpixels)
        out = []
        for mask in masks:
            masked_img = np.copy(img_3d)
            for seg_id, is_active in enumerate(mask):
                if not is_active:
                    # Use 0.0 as baseline — proper neutral for normalized inputs
                    masked_img[segments == (seg_id + 1)] = 0.0
            
            tensor = np.expand_dims(masked_img, axis=0)
            preds = model_wrapper.predict(tensor)
            out.append(preds[0])
        return np.array(out)
    
    # 4. Initialize KernelExplainer targeting all superpixels
    num_superpixels = len(np.unique(segments))
    background = np.zeros((1, num_superpixels))
    explainer = shap.KernelExplainer(mask_predict, background)
    
    active_mask = np.ones((1, num_superpixels))
    
    # 5. Calculate SHAP values (nsamples should be > num_superpixels)
    shap_vals = explainer.shap_values(active_mask, nsamples=max(2 * num_superpixels + 1, 32))
    
    # Grab highest attribution index
    top_class_idx = np.argmax(model_wrapper.predict(input_tensor)[0])
    
    if isinstance(shap_vals, list):
        if len(shap_vals) > top_class_idx:
            class_shap = shap_vals[top_class_idx][0]
        else:
            class_shap = shap_vals[0][0]  # Fallback for binary outputs
    else:
        # If output is 3D array (1, num_superpixels, num_classes)
        if len(shap_vals.shape) == 3:
            class_shap = shap_vals[0, :, top_class_idx]
        else:
            class_shap = shap_vals[0]

    # 6. Map the superpixel attributions back to pixel-level image structure
    heatmap = np.zeros(vis_image.shape[:2], dtype=np.float64)
    for seg_id in range(num_superpixels):
        heatmap[segments == (seg_id + 1)] = class_shap[seg_id]
        
    # 7. Normalize heatmap and overlay on the DISPLAY image
    max_val = np.max(np.abs(heatmap))
    if max_val > 0:
        heatmap = heatmap / max_val
    
    fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
    ax.imshow(vis_image)
    # Overlay: highlight regions with significant attribution
    alpha_mask = np.where(np.abs(heatmap) > 0.05, 0.55, 0.0) 
    ax.imshow(heatmap, cmap='jet', alpha=alpha_mask, vmin=-1, vmax=1)
    ax.axis('off')
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    
    return buf.read()
