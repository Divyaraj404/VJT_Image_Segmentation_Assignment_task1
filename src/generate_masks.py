import os
import argparse
import numpy as np
from pycocotools.coco import COCO
from PIL import Image
from tqdm import tqdm

def update_mask(mask, ann_mask, category_id, strategy="last"):
    """
    Update the mask according to the overlap strategy.

    Parameters:
      mask (np.array): The current multi-class mask.
      ann_mask (np.array): Binary mask from the current annotation (1 inside object, 0 outside).
      category_id (int): The category id to assign (used as the pixel value).
      strategy (str): Overlap strategy. Options:
                      - "last": Overwrite existing pixels (last annotation wins).
                      - "first": Update only background pixels (first annotation wins).
                      - "skip": If an overlap is detected, skip this annotation.
                      
    Returns:
      The updated mask.
    """
    # Find the pixels where ann_mask is 1 (i.e. the region of the annotation).
    annotation_pixels = (ann_mask == 1)

    if strategy == "last":
        # Optionally, count and log how many pixels will overwrite previous values.
        overlap = ((mask != 0) & annotation_pixels).sum()
        if overlap > 0:
            print(f"[Info] Overwriting {overlap} overlapping pixels for category {category_id} (last-wins).")
        # Overwrite always.
        mask[annotation_pixels] = category_id

    elif strategy == "first":
        # Update only pixels that are currently background (i.e. value 0)
        mask[(annotation_pixels) & (mask == 0)] = category_id

    elif strategy == "skip":
        # Do not update if any overlapping pixel exists.
        if ((mask != 0) & annotation_pixels).any():
            print(f"[Info] Skipping annotation for category {category_id} due to overlapping pixels.")
        else:
            mask[annotation_pixels] = category_id

    else:
        raise ValueError("Invalid overlap strategy. Choose from 'last', 'first', or 'skip'.")
    
    return mask

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="Generate multi-class segmentation masks from COCO annotations")
    parser.add_argument('--ann_file', required=True, help='Path to COCO annotation JSON file')
    parser.add_argument('--img_dir', required=True, help='Path to directory containing COCO images')
    parser.add_argument('--output_dir', required=True, help='Path to directory to save generated masks')
    parser.add_argument('--max_images', type=int, default=None, help="Optional limit on number of images to process")
    args = parser.parse_args()
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Initialize COCO with the annotation file
    coco = COCO(args.ann_file)
    
    # Get list of image IDs from the dataset
    img_ids = coco.getImgIds()
    if args.max_images:
        img_ids = img_ids[:args.max_images]
    
    # Process each image (within your main() function)
    for img_id in tqdm(img_ids, desc="Processing images"):
        # Load image metadata (expects a list with one dictionary)
        img_info = coco.loadImgs(img_id)[0]
        file_name = img_info['file_name']
        width, height = img_info['width'], img_info['height']
        
        # Create an empty mask (all background, 0)
        mask = np.zeros((height, width), dtype=np.uint8)
        
        # Get all annotation IDs and then load those annotations for the current image
        ann_ids = coco.getAnnIds(imgIds=img_info['id'])
        anns = coco.loadAnns(ann_ids)
        
        # Process each annotation
        for ann in anns:
            # Edge Case 1: Skip annotations with missing segmentation or zero area.
            if not ann.get('segmentation') or ann.get('area', 0) == 0:
                print(f"[Warning] Skipping annotation {ann.get('id')} for image {file_name} (empty segmentation or zero area).")
                continue
            
            try:
                # Get the binary mask from the annotation.
                ann_mask = coco.annToMask(ann)
            except Exception as e:
                print(f"[Error] Failed to convert annotation {ann.get('id')} to mask for image {file_name}: {e}")
                continue
            
            # Retrieve the class label (category id).
            category_id = ann['category_id']
            
            # Update the mask with edge case handling for overlaps.
            # Change the 'strategy' parameter to "first" or "skip" as needed.
            mask = update_mask(mask, ann_mask, category_id, strategy="last")
        
        # Prepare output file name (replace image extension with .png)
        mask_file_name = os.path.splitext(file_name)[0] + ".png"
        out_path = os.path.join(args.output_dir, mask_file_name)
        
        # Convert the NumPy array to a PIL Image and save as a single-channel 8-bit PNG
        mask_img = Image.fromarray(mask, mode='L')
        mask_img.save(out_path, format='PNG')

    print("Mask generation completed!")

if __name__ == "__main__":
    main()