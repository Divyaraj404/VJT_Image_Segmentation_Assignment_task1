import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def load_image(image_path):
    """Load an image from the given path."""
    return Image.open(image_path)

def display_image_and_mask(image_path, mask_path):
    """Display the original image and the corresponding mask side by side."""
    # Load the original image and mask
    orig_img = load_image(image_path)
    mask_img = load_image(mask_path)
    
    # Convert images to numpy arrays for shape inspection
    orig_arr = np.array(orig_img)
    mask_arr = np.array(mask_img)
    
    # Print out some basic information
    print(f"Image size: {orig_arr.shape}")
    print(f"Mask size: {mask_arr.shape}")
    print(f"Unique mask values: {np.unique(mask_arr)}")
    
    # Setup a figure for side-by-side display
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(orig_img)
    axes[0].set_title("Original Image")
    axes[0].axis("off")

    # Use a colormap (such as 'nipy_spectral') to visualize mask regions
    axes[1].imshow(mask_img, cmap='nipy_spectral')
    axes[1].set_title("Segmentation Mask")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()

def validate_mask(image_path, mask_path):
    """Performs automated validation on the dimensions and value ranges of a mask."""
    orig_img = load_image(image_path)
    mask_img = load_image(mask_path)
    
    orig_arr = np.array(orig_img)
    mask_arr = np.array(mask_img)
    
    # Check dimension match
    if orig_arr.shape[0:2] != mask_arr.shape[0:2]:
        print(f"Dimension mismatch: Image shape {orig_arr.shape[0:2]} vs. Mask shape {mask_arr.shape}")
    else:
        print("Dimensions match.")
    
    # Check pixel value range (should be within 0 to 255 for an 8-bit PNG)
    if mask_arr.min() < 0 or mask_arr.max() > 255:
        print("Error: Mask has pixel values outside the 0-255 range.")
    else:
        print(f"Mask pixel value range: {mask_arr.min()} to {mask_arr.max()}")
    
    # Optionally, report unique classes present in the mask.
    unique_values = np.unique(mask_arr)
    print(f"Unique values in the mask: {unique_values}")

if __name__ == "__main__":
    # For validation, choose one example.
    # Adjust these paths according to your local file structure.
    # Example: image '000000143975.jpg' and its mask '000000143975.png'.
    image_path = os.path.join("data", "images", "000000143975.jpg")
    mask_path = os.path.join("outputs", "masks", "000000143975.png")
    
    if not os.path.exists(image_path):
        print(f"Original image not found: {image_path}")
    elif not os.path.exists(mask_path):
        print(f"Mask not found: {mask_path}")
    else:
        display_image_and_mask(image_path, mask_path)
        
    validate_mask(image_path, mask_path)