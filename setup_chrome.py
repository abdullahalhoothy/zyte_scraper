#!/usr/bin/env python3
"""
Chrome Setup Verification and Auto-Installation Script
This script checks if Chrome and ChromeDriver are properly installed
and attempts to install them if missing.
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import tempfile

def run_command(command, capture_output=True, shell=True):
    """Run a system command and return the result"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        else:
            result = subprocess.run(command, shell=shell)
            return result.returncode == 0, "", ""
    except Exception as e:
        return False, "", str(e)

def check_chrome_installed():
    """Check if Google Chrome is installed"""
    commands = [
        "google-chrome --version",
        "google-chrome-stable --version", 
        "chromium --version",
        "chromium-browser --version"
    ]
    
    for cmd in commands:
        success, output, error = run_command(cmd)
        if success and output:
            return True, output, cmd.split()[0]
    
    return False, "", ""

def check_chromedriver_installed():
    """Check if ChromeDriver is installed"""
    success, output, error = run_command("chromedriver --version")
    if success and output:
        return True, output
    return False, ""

def get_chrome_version():
    """Get the installed Chrome version"""
    success, output, binary = check_chrome_installed()
    if success:
        # Extract version number from output like "Google Chrome 91.0.4472.124"
        version_parts = output.split()
        for part in version_parts:
            if '.' in part and part.replace('.', '').isdigit():
                return part.split('.')[0]  # Return major version
    return None

def install_chrome_linux():
    """Install Google Chrome on Linux"""
    print("Installing Google Chrome on Linux...")
    
    # Install system dependencies first
    print("Installing system dependencies...")
    dependencies_cmd = (
        "sudo apt-get update && "
        "sudo apt-get install -y wget curl unzip xvfb libxss1 libappindicator1 "
        "libindicator7 fonts-liberation libasound2 libnspr4 libnss3 "
        "libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 "
        "libxtst6 libgconf-2-4 libxrandr2 libpangocairo-1.0-0 "
        "libatk1.0-0 libcairo-gobject2 libgtk-3-0 libgdk-pixbuf2.0-0"
    )
    
    success, output, error = run_command(dependencies_cmd, capture_output=False)
    if not success:
        print(f"Failed to install system dependencies: {error}")
        return False
    
    commands = [
        "wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -",
        'sudo sh -c \'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list\'',
        "sudo apt-get update",
        "sudo apt-get install -y google-chrome-stable"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        success, output, error = run_command(cmd, capture_output=False)
        if not success:
            print(f"Command failed: {cmd}")
            print(f"Error: {error}")
            return False
    
    return True

def install_chromedriver_linux():
    """Install ChromeDriver on Linux"""
    print("Installing ChromeDriver on Linux...")
    
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("Cannot determine Chrome version for ChromeDriver compatibility")
        return False
    
    try:
        # Get compatible ChromeDriver version
        version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_version}"
        with urllib.request.urlopen(version_url) as response:
            chromedriver_version = response.read().decode().strip()
        
        print(f"Installing ChromeDriver version {chromedriver_version} for Chrome {chrome_version}")
        
        # Download ChromeDriver
        download_url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_linux64.zip"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "chromedriver.zip")
            
            print(f"Downloading from: {download_url}")
            urllib.request.urlretrieve(download_url, zip_path)
            
            # Extract ChromeDriver
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            chromedriver_path = os.path.join(temp_dir, "chromedriver")
            
            # Move to system path
            success, output, error = run_command(f"sudo mv {chromedriver_path} /usr/local/bin/")
            if not success:
                print(f"Failed to move ChromeDriver to /usr/local/bin/: {error}")
                return False
            
            # Make executable
            success, output, error = run_command("sudo chmod +x /usr/local/bin/chromedriver")
            if not success:
                print(f"Failed to make ChromeDriver executable: {error}")
                return False
        
        return True
        
    except Exception as e:
        print(f"Failed to install ChromeDriver: {e}")
        return False

def test_selenium_chrome():
    """Test if Selenium can work with Chrome"""
    print("Testing Selenium with Chrome...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1200,800")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Selenium test successful! Page title: {title}")
        return True
        
    except ImportError:
        print("❌ Selenium not installed. Install with: pip install selenium")
        return False
    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
        return False

def setup_chrome_environment():
    """Complete Chrome environment setup"""
    system = platform.system().lower()
    
    print(f"Setting up Chrome environment on {system}...")
    print(f"Running in CI/CD: {os.environ.get('CI', 'false')}")
    
    if system != "linux":
        print(f"❌ This script currently only supports Linux. Your system: {system}")
        print("For Windows, please install Chrome manually from https://www.google.com/chrome/")
        return False
    
    # Check current status
    chrome_installed, chrome_version, chrome_binary = check_chrome_installed()
    chromedriver_installed, chromedriver_version = check_chromedriver_installed()
    
    print(f"Chrome installed: {chrome_installed}")
    if chrome_installed:
        print(f"Chrome version: {chrome_version}")
    
    print(f"ChromeDriver installed: {chromedriver_installed}")
    if chromedriver_installed:
        print(f"ChromeDriver version: {chromedriver_version}")
    
    # Install what's missing
    if not chrome_installed:
        print("Installing Chrome...")
        if not install_chrome_linux():
            print("❌ Failed to install Chrome")
            return False
        
        chrome_installed, chrome_version, chrome_binary = check_chrome_installed()
        if not chrome_installed:
            print("❌ Chrome installation verification failed")
            return False
    
    if not chromedriver_installed:
        print("Installing ChromeDriver...")
        if not install_chromedriver_linux():
            print("❌ Failed to install ChromeDriver")
            return False
        
        chromedriver_installed, chromedriver_version = check_chromedriver_installed()
        if not chromedriver_installed:
            print("❌ ChromeDriver installation verification failed")
            return False
    
    # Set up virtual display for CI/CD environments
    if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
        print("Setting up virtual display for CI/CD environment...")
        success, output, error = run_command("sudo apt-get install -y xvfb", capture_output=False)
        if success:
            # Start Xvfb in background
            run_command("Xvfb :1 -screen 0 1024x768x16 &", capture_output=False)
            os.environ['DISPLAY'] = ':1'
            print("Virtual display configured")
        else:
            print("Warning: Could not set up virtual display")
    
    # Test the setup
    if not test_selenium_chrome():
        print("❌ Final test failed")
        return False
    
    print("✅ Chrome environment setup completed successfully!")
    return True

def main():
    """Main function"""
    print("Chrome and ChromeDriver Setup Script")
    print("=" * 40)
    
    # Check if running as root for installations
    if platform.system().lower() == "linux" and os.geteuid() != 0:
        print("Note: Some operations may require sudo privileges")
    
    success = setup_chrome_environment()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("\nYour environment is ready for traffic analysis.")
        print("\nTo use in your Python code:")
        print("from selenium import webdriver")
        print("from selenium.webdriver.chrome.options import Options")
        print("chrome_options = Options()")
        print("chrome_options.add_argument('--headless')")
        print("driver = webdriver.Chrome(options=chrome_options)")
    else:
        print("\n❌ Setup failed!")
        print("Please check the error messages above and try manual installation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
