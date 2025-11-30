import cv2
import numpy as np
from datetime import datetime
import random
from PIL import Image
import os

# --- CONFIGURATION ---
PIXEL_BLOCK_SIZE = 8   # Higher = Blockier
COLOR_LEVELS = 8       # Lower = More pixcam palette
GLITCH_CHANCE = 0.1    # Chance of random glitch
OUTPUT_FOLDER = "output"

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
# ---------------------

def pixelate_and_quantize(image, block_size, color_levels):
    """Downscales and quantizes colors to create the 8-bit effect."""
    h, w, _ = image.shape
    if block_size < 1: block_size = 1
    
    # 1. Shrink
    h_small = h // block_size
    w_small = w // block_size
    if h_small == 0 or w_small == 0: return image
    
    img_small = cv2.resize(image, (w_small, h_small), interpolation=cv2.INTER_LINEAR)
    
    # 2. Crush Colors
    factor = 256 // color_levels
    img_small = (img_small // factor) * factor + (factor // 2)
    img_small = np.clip(img_small, 0, 255)
    
    # 3. Stretch back up
    return cv2.resize(img_small, (w, h), interpolation=cv2.INTER_NEAREST)

def apply_scanlines(image):
    """Darkens every 4th row to simulate CRT TV lines."""
    image[::4, :] = image[::4, :] * 0.7 
    return image

def apply_glitch(image):
    """Splits RGB channels to create chromatic aberration."""
    h, w, _ = image.shape
    b, g, r = cv2.split(image)
    
    # Shift Red channel
    offset_r = random.randint(5, 15)
    r_shifted = np.roll(r, offset_r, axis=1)
    
    # Shift Blue channel
    offset_b = random.randint(5, 15)
    b_shifted = np.roll(b, -offset_b, axis=1)
    
    merged = cv2.merge((b_shifted, g, r_shifted))
    
    # Random white digital noise bar
    if random.random() < 0.3:
        y = random.randint(0, h-10)
        h_bar = random.randint(2, 20)
        merged[y:y+h_bar, :] = 255 
        
    return merged

# Initialize Camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

print(f"PixCam Initialized.")
print(f"Files will be saved to: ./{OUTPUT_FOLDER}/")
print("Controls: [Q] Quit | [S] Screenshot | [G] Glitch | [R] Record GIF")

# Variables for GIF recording
is_recording_gif = False
gif_frames = []

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)

    # 1. Apply Base pixcam Effects
    pixcam_img = pixelate_and_quantize(img, PIXEL_BLOCK_SIZE, COLOR_LEVELS)
    
    keys = cv2.waitKey(1) & 0xFF
    
    # 2. Apply Glitch (Random or Forced by 'G' key)
    is_glitching = (random.random() < GLITCH_CHANCE) or (keys == ord('g'))
    if is_glitching:
        pixcam_img = apply_glitch(pixcam_img)

    pixcam_img = apply_scanlines(pixcam_img)

    # 3. Draw UI Layers (Time, Rec status)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d") 
    time_str = now.strftime("%H:%M:%S") 
    
    # Logic to blink the dot/colon
    blink_on = int(now.second * 2) % 2 == 0

    if is_recording_gif:
        # Show RED "REC" text
        if blink_on:
            cv2.circle(pixcam_img, (30, 30), 10, (0, 0, 255), -1)
        cv2.putText(pixcam_img, "REC", (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    else:
        # Show GREEN "PLAY" text
        cv2.putText(pixcam_img, "PLAY", (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
    # Draw Timestamp (Shadow first for contrast)
    cv2.putText(pixcam_img, f"{date_str} {time_str}", (22, 452), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2)
    cv2.putText(pixcam_img, f"{date_str} {time_str}", (20, 450), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    # 4. Capture GIF Frame (AFTER UI is drawn)
    if is_recording_gif:
        # Convert BGR (OpenCV) to RGB (Pillow)
        frame_rgb = cv2.cvtColor(pixcam_img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(frame_rgb)
        gif_frames.append(pil_im)

    # 5. Display on Screen
    cv2.imshow("PixCam", pixcam_img)

    # 6. Handle Controls
    if keys == ord('q'):
        break
        
    elif keys == ord('s'):
        # Save PNG to output folder
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(OUTPUT_FOLDER, f"pixcam_shot_{timestamp}.png")
        cv2.imwrite(filename, pixcam_img)
        print(f"📸 Screenshot saved: {filename}")
        
    elif keys == ord('r'):
        if not is_recording_gif:
            # Start Recording
            is_recording_gif = True
            gif_frames = [] 
            print("🔴 Started recording GIF...")
        else:
            # Stop Recording & Save
            is_recording_gif = False
            if len(gif_frames) > 0:
                print(f"Processing {len(gif_frames)} frames...")
                timestamp = now.strftime('%Y%m%d_%H%M%S')
                filename = os.path.join(OUTPUT_FOLDER, f"pixcam_clip_{timestamp}.gif")
                
                print("💾 Saving GIF file... (Do not close)")
                gif_frames[0].save(
                    filename,
                    save_all=True,
                    append_images=gif_frames[1:],
                    optimize=False,
                    duration=50, # 50ms per frame
                    loop=0
                )
                print(f"✨ GIF Saved: {filename}")
            else:
                print("⚠️ No frames recorded.")

cap.release()
cv2.destroyAllWindows()