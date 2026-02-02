# 🧮 Calculator Pro

A modern, robust, and responsive desktop calculator application built with Python and Tkinter. It features a clean user interface, history tracking, and utility features like "Always on Top".

## ✨ Features

*   **Standard & Scientific Math:** Basic arithmetic (+, -, *, /) plus Square Root (`√`), Power (`xʸ`), and Percentage (`%`).
*   **Modern UI:** Clean design with hover effects on buttons and a distinct, high-contrast display area.
*   **History Log:** Displays the current operation chain (e.g., `50 + 10`) above the main input field.
*   **Always on Top:** "Options" menu allows the calculator to stay above other windows (great for multitasking).
*   **Keyboard Support:** Full support for Numpad, Enter, Backspace, and Escape keys.
*   **Responsive Design:** The window and buttons resize dynamically with the drag of a mouse.
*   **Error Handling:** Prevents crashes on division by zero or invalid inputs.

## 🚀 How to Run

### Prerequisites
*   Python 3.x installed on your system.
*   Tkinter (usually included with Python).

### Running the Source Code
1.  Clone or download this repository.
2.  Open your terminal/command prompt.
3.  Run the application:
    ```bash
    python calculator_app.py
    ```

## ⌨️ Keyboard Shortcuts

| Key | Action |
| :--- | :--- |
| **0-9, .** | Input numbers |
| **+, -, *, /** | Basic Operations |
| **Enter** | Calculate Result (=) |
| **Esc** | Clear All (C) |
| **Backspace** | Delete last digit (←) |
| **%** | Percentage |

## 📦 Building the Executable (.exe)

To convert this Python script into a standalone `.exe` file for Windows, use **PyInstaller**.

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Run the build command (ensure `calc.ico` is in the folder):
    ```bash
    pyinstaller --noconsole --onefile --icon=calc.ico --add-data "calc.ico;." calculator.py
    ```

    *   `--noconsole`: Hides the terminal window.
    *   `--onefile`: Bundles everything into a single .exe file.
    *   `--add-data`: Ensures the icon is bundled inside the app logic.

3.  Locate your app in the `dist/` folder.

## 🛠️ Built With

*   **Python** - Core logic.
*   **Tkinter** - GUI Framework.

## 📝 License

This project is open-source and available for personal and educational use.