# Installation Guide: Wagner-Whitin Algorithm Script

This guide provides step-by-step instructions to set up and run the Wagner-Whitin algorithm script (`Wagner-Whitin Simpel algoritme.py`).

**Date:** May 14, 2025

## 1. Prerequisites

Before you begin, ensure you have the following installed on your Windows system:

- **Python:** Version 3.7 or higher is recommended. You can download Python from [python.org](https://www.python.org/downloads/).
  - During installation, make sure to check the box that says **"Add Python to PATH"**.
- **pip:** Python's package installer. It is usually installed automatically with Python. You can verify by opening PowerShell or Command Prompt and typing `pip --version`.

## 2. Setup Steps

Follow these steps to set up the project and its dependencies:

### Step 2.1: Obtain the Script

Ensure you have the `Wagner-Whitin Simpel algoritme.py` file in your desired project directory. For this guide, we'll assume your project is located at `C:\Users\ankhs\repos\jks\`.

### Step 2.2: Open PowerShell or Command Prompt

Navigate to your project directory.

1.  Open File Explorer and go to `C:\Users\ankhs\repos\jks\`.
2.  In the address bar of File Explorer, type `pwsh` and press Enter. This will open PowerShell directly in your project folder. Alternatively, you can open PowerShell or Command Prompt separately and use the `cd` command:
    ```powershell
    cd C:\Users\ankhs\repos\jks
    ```

### Step 2.3: Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project-specific dependencies. This keeps your global Python installation clean.

1.  **Create the virtual environment** (e.g., named `venv`):

    ```powershell
    python -m venv venv
    ```

    This command creates a new folder named `venv` in your `jks` directory.

2.  **Activate the virtual environment:**

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

The script requires the `numpy` library.

1.  **Ensure your virtual environment is active.**
2.  **Install `numpy` using pip:**
    ```powershell
    pip install numpy
    ```
    This will download and install `numpy` and its dependencies into your `venv`.

## 3. Running the Script

Once the setup is complete and the virtual environment is active, you can run the script:

```powershell
python "Wagner-Whitin Simpel algoritme.py"
```

The script will execute, and if it includes print statements (like the example usage in the provided code), you will see the output in your PowerShell window. For example:

```
Minimum total cost: <calculated_cost>
Order schedule (order periods): [<period1>, <period2>, ...]
```

## 4. Deactivating the Virtual Environment

When you are finished working on the project, you can deactivate the virtual environment:

```powershell
deactivate
```

This command works for both PowerShell and Command Prompt. The `(venv)` prefix will disappear from your prompt.

## 5. Troubleshooting Tips

- **`python` or `pip` is not recognized:**

  - This usually means Python was not added to your system's PATH during installation. Reinstall Python, ensuring the "Add Python to PATH" option is checked.
  - Alternatively, you might need to use the full path to the Python executable or use the `py` launcher: `py -m venv venv` or `py "Wagner-Whitin Simpel algoritme.py"`.

- **`ModuleNotFoundError: No module named 'numpy'`:**

  - Ensure your virtual environment is activated before running the script.
  - If activated, try reinstalling `numpy`: `pip install numpy`.
  - Make sure you are running the script using the Python interpreter from the virtual environment.

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

- **Incorrect Output or Errors from the Script:**
  - Double-check the input data (`demand`, `setup_cost`, `holding_cost`) in the `if __name__ == "__main__":` block of the script.
  - Ensure the data types and lengths of these lists/arrays are consistent with what the `wagner_whitin` function expects.

This guide should help you get the Wagner-Whitin script running smoothly. If you encounter other issues, ensure your Python and pip installations are correct and that the `numpy` library is properly installed within your active virtual environment.
