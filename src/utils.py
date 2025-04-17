import numpy as np

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