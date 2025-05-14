# Installation Guide: Wagner-Whitin Algorithm Script and Web UI

This guide provides step-by-step instructions to set up and run the Wagner-Whitin algorithm script (`wagner_whitin_simple_algoritme.py`) both via command-line and its web-based user interface.

**Date:** May 14, 2025

## 1. Prerequisites

Before you begin, ensure you have the following installed on your Windows system:

- **Python:** Version 3.7 or higher is recommended. You can download Python from [python.org](https://www.python.org/downloads/).
  - During installation, make sure to check the box that says **"Add Python to PATH"**.
- **pip:** Python's package installer. It is usually installed automatically with Python. You can verify by opening PowerShell or Command Prompt and typing `pip --version`.

## 2. Setup Steps

Follow these steps to set up the project and its dependencies:

### Step 2.1: Obtain the Project Files

Ensure you have the following files and folder structure in your project directory (e.g., `C:\Users\ankhs\repos\jks\`):

- `wagner_whitin_simple_algoritme.py` (the core algorithm script with CLI)
- `app.py` (the Flask web application server)
- `requirements.txt` (listing necessary Python packages)
- `templates/` (folder)
  - `index.html` (the web UI page)

If you cloned a repository or downloaded a ZIP, these should already be in place.

### Step 2.2: Open PowerShell or Command Prompt

Navigate to your project directory.

1. Open File Explorer and go to `C:\Users\ankhs\repos\jks\`.
2. In the address bar of File Explorer, type `pwsh` and press Enter. This will open PowerShell directly in your project folder. Alternatively, you can open PowerShell or Command Prompt separately and use the `cd` command:
   ```powershell
   cd C:\Users\ankhs\repos\jks
   ```

### Step 2.3: Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project-specific dependencies. This keeps your global Python installation clean.

1. **Create the virtual environment** (e.g., named `venv`):

   ```powershell
   python -m venv venv
   ```

   This command creates a new folder named `venv` in your `jks` directory.

2. **Activate the virtual environment:**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   - If you are using Command Prompt (cmd.exe), the activation command is:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - **PowerShell Execution Policy:** If you get an error about script execution being disabled on PowerShell, you might need to change the execution policy for the current session. Run PowerShell as Administrator and execute:
     ```powershell
     Set-ExecutionPolicy RemoteSigned -Scope Process
     ```
     Then, try activating the virtual environment again in your non-administrator PowerShell window.

   Once activated, your PowerShell prompt should be prefixed with `(venv)`, indicating that the virtual environment is active.

### Step 2.4: Install Dependencies

The project requires `numpy` for the algorithm and `Flask` for the web UI. These are listed in `requirements.txt`.

1. Ensure your virtual environment is active.
2. Install dependencies using `pip` and `requirements.txt`:

   ```powershell
   pip install -r requirements.txt
   ```

   This command will read `requirements.txt` and install `numpy` and `Flask` (and their dependencies) into your `venv`.

## 3. Running the Script (Command-Line Interface)

The `wagner_whitin_simple_algoritme.py` script can be run directly from the command line with an interactive prompt for data input.

Once the setup (Steps 1 & 2) is complete and your virtual environment is active:

1. Navigate to your project directory (`C:\Users\ankhs\repos\jks\`) in PowerShell or Command Prompt.
2. Run the script:

   ```powershell
   python wagner_whitin_simple_algoritme.py
   ```

3. The script will first ask if you want to use predefined example data or enter data manually.
   - If you choose **yes**, it uses the hardcoded example.
   - If you choose **no**, it will guide you step-by-step to input:
     - The number of periods.
     - For each period: demand, setup cost, and holding cost.

The script will then print the calculated minimum total cost and the optimal order schedule to your console.

## 4. Running the Web-Based User Interface

The project also includes a web-based GUI powered by Flask.

Once the setup (Steps 1 & 2) is complete and your virtual environment is active:

1. Navigate to your project directory (`C:\Users\ankhs\repos\jks\`) in PowerShell or Command Prompt.
2. Run the Flask web application:

   ```powershell
   python app.py
   ```

3. You will see output in your terminal indicating the Flask development server is running. It usually includes a line like:
   `* Running on http://127.0.0.1:5000/` (or a similar address).
4. Open your web browser (e.g., Chrome, Firefox, Edge).
5. Go to the address shown in your terminal (typically `http://127.0.0.1:5000/`).
6. The web page will allow you to input demand, setup costs, and holding costs as comma-separated values for multiple periods. Click "Calculate Optimal Schedule" to see the results on the page.

To stop the Flask web server, go back to your terminal window where `app.py` is running and press `Ctrl+C`.

## 5. Deactivating the Virtual Environment

When you are finished working on the project, you can deactivate the virtual environment:

```powershell
deactivate
```

This command works for both PowerShell and Command Prompt. The `(venv)` prefix will disappear from your prompt.

## 6. Troubleshooting Tips

- **`python` or `pip` is not recognized:**

  - This usually means Python was not added to your system's PATH during installation. Reinstall Python, ensuring the "Add Python to PATH" option is checked.
  - Alternatively, you might need to use the full path to the Python executable or use the `py` launcher: `py -m venv venv` or `py wagner_whitin_simple_algoritme.py` or `py app.py`.

- **`ModuleNotFoundError: No module named 'numpy'` (or `'flask'`)**

  - Ensure your virtual environment is activated before running the script or `app.py`.
  - If activated, try reinstalling dependencies: `pip install -r requirements.txt`.

- **Permission Errors during `pip install` or script execution:**

  - Try running PowerShell or Command Prompt as an Administrator.
  - Check folder permissions for your project directory and the Python installation directory.
  - Antivirus software can sometimes interfere. Temporarily disabling it (with caution) might help diagnose if it's the cause.

- **PowerShell script execution error for `Activate.ps1`:**

  - As mentioned in Step 2.3, you might need to adjust the execution policy:
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope Process
    ```
    Run this in an Administrator PowerShell window if needed, then try activating in your regular PowerShell window.

- **Incorrect Output or Errors from the Script (CLI or Web):**

  - **CLI:** If using manual input, double-check the values you entered.
  - **Web UI:** Ensure inputs are comma-separated numbers.
  - Verify that the number of entries for demand, setup cost, and holding cost are identical.
  - Ensure the data types and lengths of these lists/arrays are consistent with what the `wagner_whitin` function expects.

- **Flask Web Server Issues (e.g., `Address already in use`):**

  - This means another application is using port 5000. You can either stop the other application or modify `app.py` to use a different port. To change the port in `app.py`, modify the last line:

    ```python
    # Change from:
    # app.run(debug=True)
    # To (for example, run on port 5001):
    # app.run(debug=True, port=5001)
    ```

    Then access the web UI at `http://127.0.0.1:5001/`.

This guide should help you get the Wagner-Whitin script and web UI running smoothly. If you encounter other issues, ensure your Python and pip installations are correct and that all dependencies from `requirements.txt` are properly installed within your active virtual environment.
