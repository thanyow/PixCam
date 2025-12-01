# 👾 PixCam

> **Turn your webcam into a living 8-bit VHS tape.**

**PixCam** is a real-time Python application that processes your webcam feed to mimic the aesthetic of early 90s digital hardware. It combines pixel quantization, color crushing, CRT scanlines, and chromatic aberration glitches into a live video feed.

## ✨ Features

* **Real-time Pixelation:** Adjustable downsampling for that crunchy low-res look.
* **Color Quantization:** Reduces millions of colors down to a retro palette (8 colors).
* **CRT Scanlines:** Simulates the horizontal raster lines of old monitors.
* **VHS Glitch:** Random (and manual) chromatic aberration effects (RGB channel splitting).
* **GIF Recorder:** Built-in tool to record and save retro loops directly from the app.
* **Smart Saving:** Automatically organizes all screenshots and clips into an `output/` folder.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/thanyow/PixCam.git
    cd PixCam
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app**
    ```bash
    python pixcam.py
    ```

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **`Q`** | **Quit** the application |
| **`S`** | **Screenshot** (Saved to `output/` folder) |
| **`G`** | **Glitch** (Hold down to force the broken VHS effect) |
| **`R`** | **Record GIF** (Press once to start, press again to save) |

## ⚙️ How it Works

PixCam uses **OpenCV** and **NumPy** to manipulate image arrays in real-time:

1.  **Downscale & Upscale:** Uses `INTER_LINEAR` to shrink and `INTER_NEAREST` to stretch back up, preserving hard pixel edges.
2.  **Bitwise Math:** Colors are crushed using integer division to create "steps" in the gradient.
3.  **Channel Splitting:** The "Glitch" effect physically separates the Blue and Red channels of the image array and shifts them horizontally.
4.  **GIF Engine:** Uses **Pillow** to stack frames in memory and export them as an animated GIF when you stop recording.

## 📂 Where are my files?

To keep your project clean, PixCam automatically creates an `output/` folder.
* Screenshots are saved as: `output/pixcam_shot_YYYYMMDD_HHMMSS.png`
* GIFs are saved as: `output/pixcam_clip_YYYYMMDD_HHMMSS.gif`

## 🤝 Contributing

Feel free to fork this project and add:
* Different color palettes (GameBoy Green, Sepia, etc.)
* Face tracking (using MediaPipe) to pixelate only the background!

## 📜 License

Free to use for whatever retro coolness you create.
