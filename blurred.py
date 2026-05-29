from PIL import (
    Image,
    ImageFilter,
    ImageEnhance,
    ImageOps
)

from pathlib import Path

# ============================================
# INPUT / OUTPUT
# ============================================

INPUT_DIR = "input"
OUTPUT_DIR = "output"

# ============================================
# OUTPUT SETTINGS
# ============================================

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920

JPEG_QUALITY = 95

# ============================================
# FOREGROUND SETTINGS
# ============================================

FOREGROUND_SCALE = 0.92

# ============================================
# BACKGROUND SETTINGS
# ============================================

BLUR_RADIUS = 40

BACKGROUND_BRIGHTNESS = 0.75

# Optional desaturation
BACKGROUND_SATURATION = 0.80

# ============================================
# SHARPENING SETTINGS
# ============================================

ENABLE_SHARPENING = True

SHARPEN_RADIUS = 1.2
SHARPEN_PERCENT = 140
SHARPEN_THRESHOLD = 2

# ============================================
# BORDER SETTINGS
# ============================================

BORDER_MODE = 3

# 0 = none
# 1 = white border
# 2 = black + white concentric border
# 3 = dynamic automatic mode

# --------------------------------------------
# White Border
# --------------------------------------------

WHITE_BORDER_SIZE = 8

# --------------------------------------------
# Black + White Border
# --------------------------------------------

BLACK_BORDER_SIZE = 4
OUTER_WHITE_BORDER_SIZE = 8

# ============================================
# DYNAMIC BORDER THRESHOLDS
# ============================================

WHITE_THRESHOLD = 200
VERY_BRIGHT_THRESHOLD = 240

# % of bright pixels required
NO_BORDER_MAX_RATIO = 0.08

# % of very bright pixels required
WHITE_BORDER_MAX_RATIO = 0.03

# ============================================
# SUPPORTED FILE TYPES
# ============================================

SUPPORTED_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff"
]

# ============================================
# CREATE OUTPUT DIRECTORY
# ============================================

Path(OUTPUT_DIR).mkdir(exist_ok=True)

# ============================================
# DYNAMIC BORDER ANALYSIS
# ============================================

def determine_dynamic_border_mode(img):
    """
    Determine border mode based on
    highlight pixel percentages.
    """

    grayscale = img.convert("L")

    histogram = grayscale.histogram()

    total_pixels = sum(histogram)

    # ----------------------------------------
    # Count highlight pixels
    # ----------------------------------------

    bright_pixels = sum(
        histogram[WHITE_THRESHOLD:]
    )

    very_bright_pixels = sum(
        histogram[VERY_BRIGHT_THRESHOLD:]
    )

    bright_ratio = bright_pixels / total_pixels
    very_bright_ratio = very_bright_pixels / total_pixels

    print(f"Bright ratio: {bright_ratio:.3f}")
    print(f"Very bright ratio: {very_bright_ratio:.3f}")

    # ----------------------------------------
    # Dark / low-highlight image
    # ----------------------------------------

    if bright_ratio < NO_BORDER_MAX_RATIO:

        print("Border Mode: NONE")

        return 0

    # ----------------------------------------
    # Moderate highlight image
    # ----------------------------------------

    elif very_bright_ratio < WHITE_BORDER_MAX_RATIO:

        print("Border Mode: WHITE")

        return 1

    # ----------------------------------------
    # Highlight-heavy image
    # ----------------------------------------

    else:

        print("Border Mode: BLACK + WHITE")

        return 2

# ============================================
# CREATE BLURRED BACKGROUND
# ============================================

def create_blurred_background(img):

    bg = img.copy()

    # ----------------------------------------
    # Resize to fill entire canvas
    # ----------------------------------------

    bg = ImageOps.fit(
        bg,
        (OUTPUT_WIDTH, OUTPUT_HEIGHT),
        method=Image.LANCZOS
    )

    # ----------------------------------------
    # Blur
    # ----------------------------------------

    bg = bg.filter(
        ImageFilter.GaussianBlur(radius=BLUR_RADIUS)
    )

    # ----------------------------------------
    # Darken slightly
    # ----------------------------------------

    brightness = ImageEnhance.Brightness(bg)

    bg = brightness.enhance(
        BACKGROUND_BRIGHTNESS
    )

    # ----------------------------------------
    # Optional desaturation
    # ----------------------------------------

    saturation = ImageEnhance.Color(bg)

    bg = saturation.enhance(
        BACKGROUND_SATURATION
    )

    return bg

# ============================================
# CREATE FOREGROUND IMAGE
# ============================================

def create_foreground(img):

    fg = img.copy()

    max_w = int(
        OUTPUT_WIDTH * FOREGROUND_SCALE
    )

    max_h = int(
        OUTPUT_HEIGHT * FOREGROUND_SCALE
    )

    fg.thumbnail(
        (max_w, max_h),
        Image.LANCZOS
    )

    return fg

# ============================================
# SHARPENING
# ============================================

def apply_sharpening(img):

    if ENABLE_SHARPENING:

        img = img.filter(
            ImageFilter.UnsharpMask(
                radius=SHARPEN_RADIUS,
                percent=SHARPEN_PERCENT,
                threshold=SHARPEN_THRESHOLD
            )
        )

    return img

# ============================================
# BORDER ADDITION
# ============================================

def add_borders(img):

    result = img.copy()

    mode = BORDER_MODE

    # ----------------------------------------
    # Dynamic mode
    # ----------------------------------------

    if BORDER_MODE == 3:

        mode = determine_dynamic_border_mode(
            result
        )

    # ----------------------------------------
    # Mode 0
    # No border
    # ----------------------------------------

    if mode == 0:

        return result

    # ----------------------------------------
    # Mode 1
    # White border
    # ----------------------------------------

    elif mode == 1:

        result = ImageOps.expand(
            result,
            border=WHITE_BORDER_SIZE,
            fill="white"
        )

    # ----------------------------------------
    # Mode 2
    # Black + White Border
    # ----------------------------------------

    elif mode == 2:

        # Inner black border

        result = ImageOps.expand(
            result,
            border=BLACK_BORDER_SIZE,
            fill="black"
        )

        # Outer white border

        result = ImageOps.expand(
            result,
            border=OUTER_WHITE_BORDER_SIZE,
            fill="white"
        )

    return result

# ============================================
# MAIN PROCESSING LOOP
# ============================================

input_root = Path(INPUT_DIR)

# --------------------------------------------
# Recursively find all supported images
# --------------------------------------------

all_images = []

for ext in SUPPORTED_EXTENSIONS:
    all_images.extend(
        input_root.rglob(f"*{ext}")
    )

# --------------------------------------------
# Process images
# --------------------------------------------

for filepath in all_images:

    print("\n----------------------------------")
    print(f"Processing: {filepath}")

    # ----------------------------------------
    # Determine parent folder
    # ----------------------------------------

    parent_folder = filepath.parent.name

    output_dir = Path(
        f"output_{parent_folder}"
    )

    output_dir.mkdir(exist_ok=True)

    # ----------------------------------------
    # Open image
    # ----------------------------------------

    img = Image.open(filepath)

    # ----------------------------------------
    # EXIF orientation correction
    # ----------------------------------------

    img = ImageOps.exif_transpose(img)

    # ----------------------------------------
    # Convert to RGB
    # ----------------------------------------

    img = img.convert("RGB")

    # ========================================
    # Create blurred background
    # ========================================

    background = create_blurred_background(
        img
    )

    # ========================================
    # Create foreground
    # ========================================

    foreground = create_foreground(img)

    # ========================================
    # Apply sharpening
    # ========================================

    foreground = apply_sharpening(
        foreground
    )

    # ========================================
    # Add borders
    # ========================================

    foreground = add_borders(
        foreground
    )

    # ========================================
    # Composite foreground onto background
    # ========================================

    x = (
        OUTPUT_WIDTH - foreground.width
    ) // 2

    y = (
        OUTPUT_HEIGHT - foreground.height
    ) // 2

    background.paste(
        foreground,
        (x, y)
    )

    # ========================================
    # Save output
    # ========================================

    output_path = (
        output_dir
        / f"{filepath.stem}_reel.jpg"
    )

    background.save(
        output_path,
        quality=JPEG_QUALITY,
        subsampling=0
    )

    print(f"Saved: {output_path}")

print("\nDone.")
