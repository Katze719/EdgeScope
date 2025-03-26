# 🌟 EdgeScope

EdgeScope is a Python-based graphical application for real-time edge detection on a selected screen area. It uses the PyQt5 library for the graphical user interface and OpenCV for image processing. The application is designed to work on Wayland-based systems and leverages the `grim` tool for capturing screen areas.

## ✨ Features

- 🖼️ **Screen Area Selection**: Allows users to select a specific area of the screen for edge detection.
- ⚡ **Real-Time Edge Detection**: Continuously processes the selected screen area and displays the detected edges.
- 🎛️ **Adjustable Parameters**:
  - **Lower Threshold**: Adjust the lower threshold for the Canny edge detection algorithm.
  - **Upper Threshold**: Adjust the upper threshold for the Canny edge detection algorithm.
  - **Aperture Size**: Choose the aperture size (3, 5, or 7) for the Sobel operator used in the Canny algorithm.
- 🌓 **Inverted Grayscale Processing**: Inverts the grayscale image before applying edge detection for better visibility.

## 📋 Requirements

- 🐍 Python 3.10 or higher
- 🖥️ Wayland display server
- 📦 The following Python libraries:
  - `PyQt5`
  - `opencv-python`
  - `numpy`
- 📸 The `grim` tool for screen capturing on Wayland.

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/EdgeScope.git
   cd EdgeScope
   ```

2. Install the required Python libraries:
   ```bash
   pip install PyQt5 opencv-python numpy
   ```

3. Ensure `grim` is installed on your system. On most Linux distributions, you can install it using your package manager. For example:
   ```bash
   sudo apt install grim
   ```

## 🛠️ Usage

1. Run the application:
   ```bash
   python3 main.py
   ```

2. A full-screen window will appear, allowing you to select a specific area of the screen. Use your mouse to draw a rectangle over the desired area.

3. After selecting the area, an overlay window will appear displaying the real-time edge detection output.

4. Use the sliders in the overlay window to adjust the following parameters:
   - **Lower Threshold**: Controls the minimum intensity gradient for edge detection.
   - **Upper Threshold**: Controls the maximum intensity gradient for edge detection.
   - **Aperture Size**: Sets the size of the Sobel kernel (3, 5, or 7).

5. The edge detection output will update in real-time as you adjust the sliders.

## 🧠 How It Works

1. **Screen Capture**: The application uses the `grim` tool to capture the selected screen area as an image.
2. **Grayscale Conversion**: The captured image is converted to grayscale using OpenCV.
3. **Inversion**: The grayscale image is inverted to enhance edge visibility.
4. **Edge Detection**: The Canny edge detection algorithm is applied to the inverted image using the user-defined parameters.
5. **Display**: The processed image is displayed in the overlay window.

## ⚠️ Known Issues

- The application is designed for Wayland and may not work on X11 or other display servers.
- The `grim` tool must be installed and functional for the application to work.

## 🌟 Future Improvements

- Add support for saving the processed edge detection output as an image.
- Extend compatibility to X11-based systems.
- Improve error handling and user feedback.

## 📜 License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) for the GUI framework.
- [OpenCV](https://opencv.org/) for image processing.
- [grim](https://github.com/emersion/grim) for screen capturing on Wayland.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.