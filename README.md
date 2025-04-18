# Pascal VOC Viewer

A Python-based GUI application to visualize Pascal VOC dataset images along with their bounding box annotations. This tool is built using `Tkinter` for the GUI, `OpenCV` for image processing, and `Pillow` for image rendering.

## Features

- Displays images from the Pascal VOC dataset in a grid format.
- Draws bounding boxes around objects in the images based on their annotations.
- Labels objects as either their class name or "unknown" if the class is not in the predefined set.
- Allows navigation through the dataset using "Next" and "Prev" buttons.

## Requirements

- Python 3.x
- Required Python libraries:
  - `opencv-python`
  - `Pillow`
  - `tkinter` (comes pre-installed with Python)
  - `xml.etree.ElementTree` (comes pre-installed with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pascal-voc-viewer.git
   cd pascal-voc-viewer