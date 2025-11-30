# 👾 PixCam

> **Turn your webcam into a living 8-bit VHS tape.**

![PixCam Demo](screenshots/demo.gif)
*(Replace this line with a path to your actual GIF or Screenshot!)*

**PixCam** is a real-time Python application that processes your webcam feed to mimic the aesthetic of early 90s digital hardware. It combines pixel quantization, color crushing, CRT scanlines, and chromatic aberration glitches.

## ✨ Features

* **Real-time Pixelation:** Adjustable downsampling for that crunchy low-res look.
* **Color Quantization:** Reduces millions of colors down to a retro palette (4-16 colors).
* **CRT Scanlines:** Simulates the horizontal raster lines of old monitors.
* **VHS Glitch:** Random (and manual) chromatic aberration effects (RGB channel splitting).
* **Live Timestamp:** Authentic "Camcorder" style date/time overlay.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/PixCam.git](https://github.com/YOUR_USERNAME/PixCam.git)
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
| **`Q`** | Quit the application |
| **`S`** | Save a screenshot (saved with timestamp) |
| **`G`** | Force a "Glitch" effect (Hold down) |

## ⚙️ How it Works

PixCam uses **OpenCV** and **NumPy** to manipulate image arrays in real-time:
1.  **Downscale & Upscale:** Uses `INTER_LINEAR` to shrink and `INTER_NEAREST` to stretch back up, preserving hard pixel edges.
2.  **Bitwise Math:** Colors are crushed using integer division to create "steps" in the gradient.
3.  **Channel Splitting:** The "Glitch" effect physically separates the Blue and Red channels of the image array and shifts them horizontally.

## 🤝 Contributing

Feel free to fork this project and add:
* Different color palettes (GameBoy Green, Sepia, etc.)
* Face tracking (using MediaPipe) to pixelate only the background!

## 📜 License

MIT License. Free to use for whatever retro coolness you create.