# COCO Segmentation Task – Multi‑Class Mask Generation 🌟✨🚀

Generate single‑channel 8‑bit PNG masks from COCO instance‑segmentation annotations. Each pixel’s value equals its object class ID (0 = background, 1‑80 = COCO categories). 🌟✨🚀

---

## Repository Structure 🌟✨🚀

```
coco_segmentation_task/
├── src/                      # Python source
│   ├── generate_masks.py
│   └── utils.py
├── data/                     # ⬇️ download from Google Drive
│   ├── images/               # COCO jpgs
│   └── annotations/          # COCO JSON
├── outputs/                  # ⬇️ download from Google Drive
│   └── masks/                # generated 8‑bit PNGs
├── figures/                  # tiny example PNGs for report
├── report/                   # LaTeX / PDF
├── pyproject.toml            # uv deps
├── uv.lock                   # locked versions
└── README.md
```

*Large files (raw COCO images, JSON, generated masks) are **not** tracked.*  
👉 **Download ready‑made `data/` and `outputs/` folders from Google Drive and place them in the project root before running any code:**  
<https://drive.google.com/drive/folders/1P41Eq1sV4aYf9GOJ7g_jOXYWOtsOvHdi?usp=sharing>  
After extracting, the directory tree should match the structure above. 🌟✨🚀 🌟✨🚀

---

## 1. Prerequisites 🌟✨🚀

| Requirement | Tested Version / Notes |
|-------------|------------------------|
| Linux (Ubuntu 20.04 LTS or later) | Any modern distro works |
| Python ≥ 3.10 | Managed by **uv** |
| Build tools  | `build-essential`, `python3-dev` |
| Git          | For cloning this repo |
| (~1 GB disk) | COCO annotations + sample images |

Install build tools (Debian/Ubuntu): 🌟✨🚀

```bash
sudo apt update && sudo apt install -y build-essential python3-dev
```

---

## 2. Clone and set up the environment 🌟✨🚀

```bash
git clone https://github.com/Divyaraj404/VJT_Image_Segmentation_Assignment.git
cd VJT_Image_Segmentation_Assignment

# Install uv (one‑time)
pip install uv

# Create the environment and install locked deps
uv sync
```

Activate the virtual environment: 🌟✨🚀

```bash
uv venv            # prints activation command
source .venv/bin/activate
```

---

## 3. Download COCO 2017 data (minimal subset) 🌟✨🚀

```bash
# Annotations (~240 MB)
mkdir -p data/annotations && cd data/annotations
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip annotations_trainval2017.zip
cd ../../

# Validation images (~1 GB)
mkdir -p data/images && cd data/images
wget http://images.cocodataset.org/zips/val2017.zip
unzip val2017.zip
cd ../../
```

---

## 4. Run the mask‑generation script 🌟✨🚀

```bash
uv run python src/generate_masks.py \
  --ann_file  data/annotations/instances_val2017.json \
  --img_dir   data/images/val2017 \
  --output_dir outputs/masks \
  --max_images 8000   # optional cap
```

Arguments: 🌟✨🚀

| Flag | Description |
|------|-------------|
| `--ann_file` | COCO JSON annotations |
| `--img_dir`  | Folder containing images |
| `--output_dir` | Destination for PNG masks |
| `--max_images N` | (Optional) limit for quick tests |

---

## 5. Edge‑Case Handling (≤ 10 lines) 🌟✨🚀

* Overlapping objects → later annotations overwrite earlier (last‑wins).
* Invalid / zero‑area annotations are skipped (logged).
* Images with no annotations produce an all‑background mask.
* Handles polygon and RLE masks via `pycocotools`.
* 8‑bit output (0‑255) covers all 80 COCO classes.

---

## 6. Quick Visualization 🌟✨🚀

```bash
python - <<'PY'
import matplotlib.pyplot as plt
from PIL import Image
img  = Image.open('data/images/val2017/000000000139.jpg')
mask = Image.open('outputs/masks/000000000139.png')
plt.subplot(1,2,1); plt.imshow(img); plt.axis('off'); plt.title('Original')
plt.subplot(1,2,2); plt.imshow(mask, cmap='nipy_spectral'); plt.axis('off'); plt.title('Mask')
plt.show()
PY
```

---

## 7. Troubleshooting 🌟✨🚀

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: pycocotools` | Ensure `uv sync` succeeded; compiler may be needed |
| Script slow on 8k images | Use `--max_images` for debug; consider multiprocessing |
| Mask looks all‑black | Remember masks are grayscale IDs; view with a colormap |

---

## 8. License / Citation 🌟✨🚀

COCO dataset © 2014 COCO Consortium, CC BY 4.0. Code in this repo released under MIT License. 🌟✨🚀

---

### Contact 🌟✨🚀

Divyaraj Singh Chundawat  
Indian Institute of Science  
<divyarajs@iisc.ac.in> 🌟✨🚀

