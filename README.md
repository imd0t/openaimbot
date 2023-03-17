# Fortnite Aim Assist

This program provides a simple aim assist for Fortnite using computer vision techniques. It tracks the second furthest player on screen and moves the mouse to their head position. The program has adjustable parameters and can be toggled on and off using function keys.

**Note**: The use of AI-assisted aiming in online games may be against the terms of service, and you should be aware of the consequences of using such programs.

## Requirements

- Python 3.6 or higher
- `pip` to install the required packages

## Installation

1. Clone the repository or download the source code:
git clone <https://github.com/imd0t/openaimbot.git>
2. Change the working directory to the project folder:

cd openaimbot
3. Install the required packages using `pip`:

pip install -r requirements.txt

## Usage

1. Run the program:
python openaimbot.py

2. Use the following function keys to control the program:

- `F1`: Toggle between aiming down sights and hipfire modes.
- `F2`: Toggle the aim assist on and off.

3. Close the GUI window to stop the program.

## Customization

You can modify the adjustable parameters in the `openaimbot.py` file, such as `interpolation_fps`, `confidence_threshold`, and `strength`.
