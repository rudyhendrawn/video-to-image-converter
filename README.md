# Balinese Dance Video to Image Sequence Converter

A Python project that converts a dataset of Balinese dance videos into image sequences. Each video is converted into frames at 10 frames per second (FPS) and resized to 224x224 pixels. The original dataset structure is preserved, and new CSV files are generated to reflect the updated dataset.

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Features

- Converts videos into image sequences at 10 FPS.
- Resizes images to 224x224 pixels.
- Maintains the original directory structure.
- Generates new CSV files reflecting the updated dataset.
- Managed using [Poetry](https://python-poetry.org/) for modern dependency management.

## Directory Structure
tari_bali_image_converter/ 
├── README.md 
├── pyproject.toml 
├── poetry.lock 
├── tari_bali_image_converter 
	├── init.py 
	└── convert_videos.py 


## Installation

### Prerequisites

- Python 3.7 or higher
- [Poetry](https://python-poetry.org/docs/#installation)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. **Install dependencies**

   ```bash
   poetry install

3. **Activate the virtual environment**

   ```bash
   poetry shell

4. Prepare the dataset

	Ensure your Tari Bali directory and CSV files (train.csv, val.csv, test.csv) are placed in the root of the dataset directory.

### Dependencies

The project uses the following Python packages:
- OpenCV (opencv-python) for video processing.
- Pandas for handling CSV files.
- tqdm for displaying progress bars.
- These are specified in pyproject.toml and managed by Poetry.