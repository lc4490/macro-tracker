# Macro Tracker GUI Application

This Python script provides a graphical user interface (GUI) for tracking and calculating macros (macronutrients) for recipes using the Tkinter library. Users can create and manage recipes, add ingredients, and calculate the nutritional information of each recipe based on ingredient macros. The application stores ingredient and recipe data in text files for future use.

## Prerequisites

To run this script, you'll need:

- Python installed on your system.
- The `tkinter` library for creating the graphical user interface.

## How to Use

1. Open a terminal and navigate to the directory containing the `macroTracker.py` script.

2. Run the script using the command:

   ```bash
   python macroTracker.py
   ```

3. The application window will appear, allowing you to interact with the GUI.

## Features

- Add, edit, and delete recipes.
- Add, edit, and delete ingredients with macronutrient information (calories, protein, carbs, fats).
- Calculate and display the total macros for each recipe based on ingredient quantities.
- Data persistence: The application stores ingredient and recipe data in `ingredients.txt` and `recipes.txt` respectively, so you can resume using the data later.

## Note

- The script uses the `tkinter` library for GUI components. The interface may vary depending on your operating system's theme and settings.

- Macro calculations are based on user-input ingredient quantities and their associated macronutrient percentages.

- This application doesn't replace professional dietary advice or nutritional calculations. Use it as a tool to estimate macros for recipes.

## Disclaimer

This script is provided as-is and may not have full error handling or extensive testing. Use it responsibly and feel free to modify it to suit your needs.

For more information about the script's implementation and `tkinter` library functions, refer to the script's comments and the [Tkinter documentation](https://docs.python.org/3/library/tkinter.html).

**Author**: Leo Chao

**Date**: 2022/07/27
