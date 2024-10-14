# SLiB_Browser_PRO_2.0

SLiB_Browser_PRO_2.0 is an open-source revival of the original SLiB Browser from CGfront, tailored for modern Autodesk Maya versions. With the original website no longer available and downloads scarce, this project aims to bring back and update the SLiB Browser for the community.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Branches](#branches)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

The SLiB Browser was a valuable tool for many Maya users, but it has become abandonware with the disappearance of CGfront. This project is a community-driven effort to:

- Open-source the SLiB Browser.
- Update it for compatibility with modern versions of Maya.
- Ensure it continues to be a useful tool for artists and developers.

## Features

- **Compatibility with Maya 2025**: The `2025` branch includes updates for Maya 2025, including necessary Python changes.
- **Original Version Preserved**: The `master` branch holds the untouched, clean version of SLiB Browser.
- **Community-Driven Development**: Open to contributions for further improvements and updates.

## Branches

- **Master**: Contains the original, unmodified SLiB Browser.
- **2025**: Updated for Maya 2025 with Python updates and compatibility fixes.

## Installation

### Prerequisites

- Autodesk Maya (preferably version 2025 for the updated branch)
- Python (compatible with your Maya version)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/SLiB_Browser_PRO_2.0.git
   ```

2. **Checkout the Desired Branch**

   - For the original version:

     ```bash
     git checkout master
     ```

   - For Maya 2025 compatibility:

     ```bash
     git checkout 2025
     ```

3. **Set Up in Maya**

   - Copy the SLiB Browser files to your Maya scripts directory.
   - Ensure that Python paths are correctly set if using the updated version.

## Usage

1. **Launch Maya**.

2. **Load the SLiB Browser Script**

   - Run the script or add it to your shelves for quick access:

     ```python
     import slib_browser
     slib_browser.launch()
     ```

3. **Enjoy Enhanced Workflow**

   - Use the SLiB Browser to manage assets, materials, and more within Maya.

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**

   - Click the "Fork" button at the top-right corner of the repository page.

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your feature"
   ```

4. **Push to Your Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Create a Pull Request**

   - Go to your forked repository and click on "New Pull Request".


## Acknowledgments

- **CGfront**: Original creators of the SLiB Browser.
- **Community Contributors**: Thanks to everyone helping to keep this project alive.
