# blurred.py

A lightweight Python utility for converting photographs into cinematic 9:16 reel-ready images using blurred background fills, adaptive borders, and Instagram-optimized processing.

blurred.py automatically creates vertical showcase compositions for:
- Instagram Reels
- TikTok
- YouTube Shorts
- Stories
- Vertical slideshows
- Film photography showcases

The tool preserves the original image composition while generating a soft blurred background derived from the image itself.

---

# Features

## Cinematic Blurred Backgrounds

- Automatically generates a 9:16 vertical background
- Uses the original image as the backdrop
- Applies configurable Gaussian blur
- Optional darkening and desaturation
- Preserves color harmony and scene continuity

---

## Smart Foreground Placement

- Maintains original image aspect ratio
- Never clips left/right edges
- Supports portrait, landscape, square, and panoramic images
- Configurable foreground scaling

---

## Adaptive Border System

blurred.py supports four border modes:

### 0 — No Border

Clean floating image presentation.

---

### 1 — White Border

Thin minimalist white keyline.

---

### 2 — Black + White Concentric Border

Gallery-style editorial framing:
- thin black inner border
- thin white outer border

---

### 3 — Dynamic Automatic Bordering

Automatically selects border style based on image highlight density:

| Image Characteristics | Border Style |
|---|---|
| dark / low highlights | none |
| moderate highlights | white border |
| highlight-heavy / high-key | black + white border |

This helps preserve visual edge separation automatically.

---

## Sharpening

Optional post-resize sharpening using Unsharp Mask:
- compensates for Instagram compression
- improves detail retention
- especially useful for film scans

---

## EXIF-Aware Processing

Automatically corrects orientation metadata using:

```python
ImageOps.exif_transpose()
```

Ensures proper handling of:
- phone photos
- Lightroom exports
- mirrorless cameras
- TIFF scans

---

## TIFF Support

Supports:
- JPG
- JPEG
- PNG
- TIF
- TIFF

Exports:
- high-quality JPEG

---

## Recursive Folder Processing

Supports nested input folders.

Example:

```text
input/
    Iceland/
    Japan/
    Portraits/
```

Automatically creates:

```text
output_Iceland/
output_Japan/
output_Portraits/
```

---

# Installation

## 1. Install Python

Download Python:

https://www.python.org/downloads/

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

Place folders/images into:

```text
input/
```

Run:

```bash
python blurred.py.py
```

Processed reel-ready images will automatically appear in generated output folders.

---

# Example Workflow

Input:

```text
input/
    Iceland/
        aurora.tif

    Portraits/
        scan001.jpg
```

Output:

```text
output_Iceland/
    aurora_reel.jpg

output_Portraits/
    scan001_reel.jpg
```

---

# Configuration

Inside `blurred.py.py`:

```python
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920

FOREGROUND_SCALE = 0.92

BLUR_RADIUS = 40

BACKGROUND_BRIGHTNESS = 0.75

BACKGROUND_SATURATION = 0.80
```

---

# Border Configuration

```python
BORDER_MODE = 3
```

Options:

```python
0 = none
1 = white border
2 = black + white concentric border
3 = dynamic automatic mode
```

---

# Sharpening Configuration

```python
ENABLE_SHARPENING = True

SHARPEN_RADIUS = 1.2
SHARPEN_PERCENT = 140
SHARPEN_THRESHOLD = 2
```

---

# Why blurred.py?

Traditional reel formatting often:
- crops compositions
- adds black bars
- destroys framing intent

blurred.py preserves the original photograph while adapting it elegantly to vertical social media formats.

Designed especially for:
- film photographers
- fine-art presentation
- editorial layouts
- cinematic photography showcases

---

# Future Plans

- GUI application
- drag-and-drop support
- animated Ken Burns motion
- video export
- adaptive edge-aware border analysis
- shadow generation
- Lightroom integration
- reel slideshow generation
- music synchronization
- export presets

---

# License

MIT License

See `LICENSE` for details.
