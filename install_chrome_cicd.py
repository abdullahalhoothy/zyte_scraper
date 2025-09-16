#!/usr/bin/env python3
"""
Simple Chrome Installation Script for CI/CD
Lightweight script specifically designed for GitHub Actions and CI/CD environments
"""

import os
import sys
import subprocess
import tempfile
import urllib.request
import zipfile
import json

import os
import sys
import subprocess
import urllib.request
import zipfile
import tempfile

def check_chrome_installed():
    """Check if Google Chrome is already installed"""
    try:
        result = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"Chrome already installed: {version}")
            return True, version
    except FileNotFoundError:
        pass
    
    # Try alternative commands
    for cmd in ["google-chrome-stable", "chromium", "chromium-browser"]:
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"Chrome variant found: {version}")
                return True, version
        except FileNotFoundError:
            continue
    
    print("Chrome not found")
    return False, ""

def check_chromedriver_installed():
    """Check if ChromeDriver is already installed"""
    try:
        result = subprocess.run(["chromedriver", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"ChromeDriver already installed: {version}")
            return True, version
    except FileNotFoundError:
        print("ChromeDriver not found")
        return False, ""

def run_command(command):
    """Run a system command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            # Don't print errors for 'which' commands as they're just checks
            if not command.startswith("which "):
                print(f"Command failed: {command}")
                print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        if not command.startswith("which "):
            print(f"Exception running command '{command}': {e}")
        return False

def install_chrome_dependencies():
    """Install system dependencies for Chrome"""
    print("Installing Chrome system dependencies...")
    
    # Check if some key dependencies are already installed
    key_deps = ["wget", "curl", "unzip", "xvfb"]
    missing_deps = []
    
    for dep in key_deps:
        if not run_command(f"which {dep}"):
            missing_deps.append(dep)
    
    if not missing_deps:
        print("Key dependencies already installed, updating package list...")
        return run_command("sudo apt-get update")
    
    print(f"Installing missing dependencies: {', '.join(missing_deps)}")
    
    # First, update the package list
    if not run_command("sudo apt-get update"):
        print("Warning: Failed to update package list, continuing anyway...")
    
    # Install core dependencies first
    core_deps = ["wget", "curl", "unzip", "xvfb"]
    core_cmd = f"sudo apt-get install -y {' '.join(core_deps)}"
    if not run_command(core_cmd):
        print("Failed to install core dependencies")
        return False
    
    # Install Chrome-specific dependencies with fallbacks
    chrome_deps = [
        "libxss1", "fonts-liberation", "libnspr4", "libnss3", 
        "libx11-xcb1", "libxcomposite1", "libxcursor1", "libxdamage1", 
        "libxi6", "libxtst6", "libxrandr2", "libpangocairo-1.0-0", 
        "libatk1.0-0", "libcairo-gobject2", "libgtk-3-0", "libgdk-pixbuf2.0-0"
    ]
    
    # Try to install Chrome dependencies, but don't fail if some are missing
    chrome_cmd = f"sudo apt-get install -y {' '.join(chrome_deps)}"
    if not run_command(chrome_cmd):
        print("Warning: Some Chrome dependencies failed to install, but continuing...")
    
    # Try alternative packages for problematic ones
    fallback_deps = [
        "sudo apt-get install -y libappindicator3-1 || sudo apt-get install -y libayatana-appindicator3-1 || echo 'App indicator not available'",
        "sudo apt-get install -y libasound2-dev || sudo apt-get install -y libasound2 || echo 'Audio library not available'",
        "sudo apt-get install -y libgconf-2-4 || echo 'GConf not available (deprecated)'",
    ]
    
    for cmd in fallback_deps:
        run_command(cmd)
    
    return True

def install_chrome():
    """Install Google Chrome if not already installed"""
    # Check if Chrome is already installed
    chrome_exists, chrome_version = check_chrome_installed()
    if chrome_exists:
        print("Chrome is already installed, skipping installation")
        return True
    
    print("Installing Google Chrome...")
    
    # Method 1: Try official Google repository
    commands = [
        "wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -",
        'sudo sh -c \'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list\'',
        "sudo apt-get update",
        "sudo apt-get install -y google-chrome-stable"
    ]
    
    success = True
    for cmd in commands:
        if not run_command(cmd):
            success = False
            break
    
    if success:
        # Verify installation
        chrome_exists, chrome_version = check_chrome_installed()
        if chrome_exists:
            print(f"Chrome installation successful: {chrome_version}")
            return True
    
    # Method 2: Try direct download if repository method failed
    print("Repository method failed, trying direct download...")
    try:
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            deb_path = os.path.join(temp_dir, "google-chrome-stable.deb")
            
            # Download the latest Chrome .deb package
            download_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
            urllib.request.urlretrieve(download_url, deb_path)
            
            # Install the package
            install_cmd = f"sudo dpkg -i {deb_path} || sudo apt-get install -f -y"
            if run_command(install_cmd):
                # Verify installation
                chrome_exists, chrome_version = check_chrome_installed()
                if chrome_exists:
                    print(f"Chrome installation successful via direct download: {chrome_version}")
                    return True
    
    except Exception as e:
        print(f"Direct download method failed: {e}")
    
    print("Chrome installation verification failed")
    return False

def install_chromedriver():
    """Install ChromeDriver compatible with installed Chrome if not already installed"""
    # Check if ChromeDriver is already installed
    chromedriver_exists, chromedriver_version = check_chromedriver_installed()
    if chromedriver_exists:
        print("ChromeDriver is already installed, checking compatibility...")
        
        # Check if Chrome version is compatible with ChromeDriver version
        chrome_exists, chrome_version = check_chrome_installed()
        if chrome_exists:
            try:
                # Extract major version numbers for comparison
                chrome_major = chrome_version.split()[2].split('.')[0] if len(chrome_version.split()) > 2 else chrome_version.split('.')[0]
                chromedriver_major = chromedriver_version.split()[1].split('.')[0] if len(chromedriver_version.split()) > 1 else chromedriver_version.split('.')[0]
                
                if chrome_major == chromedriver_major:
                    print("ChromeDriver version is compatible with Chrome, skipping installation")
                    return True
                else:
                    print(f"Version mismatch - Chrome: {chrome_major}, ChromeDriver: {chromedriver_major}")
                    print("Updating ChromeDriver to match Chrome version...")
            except Exception as e:
                print(f"Could not verify version compatibility: {e}")
                print("Proceeding with ChromeDriver update...")
        else:
            print("Chrome not found, but ChromeDriver exists. This might cause issues.")
            return True
    
    print("Installing ChromeDriver...")
    
    try:
        # Get Chrome version
        chrome_exists, chrome_version = check_chrome_installed()
        if not chrome_exists:
            print("Chrome not installed, cannot determine compatible ChromeDriver version")
            return False
        
        # Extract full version from Chrome version string
        chrome_version_number = chrome_version.split()[2] if len(chrome_version.split()) > 2 else chrome_version
        chrome_major_version = int(chrome_version_number.split('.')[0])
        print(f"Chrome major version: {chrome_major_version}")
        
        # For Chrome 115+, use the new Chrome for Testing API
        if chrome_major_version >= 115:
            print("Using Chrome for Testing API for ChromeDriver download...")
            
            # Get the latest stable ChromeDriver version for this Chrome version
            import json
            api_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
            
            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read().decode())
            
            # Find the matching version
            compatible_version = None
            for version_info in reversed(data['versions']):  # Start from latest
                version_major = int(version_info['version'].split('.')[0])
                if version_major == chrome_major_version:
                    # Check if chromedriver download is available for linux64
                    if 'chromedriver' in version_info['downloads']:
                        for download in version_info['downloads']['chromedriver']:
                            if download['platform'] == 'linux64':
                                compatible_version = version_info['version']
                                download_url = download['url']
                                break
                        if compatible_version:
                            break
            
            if not compatible_version:
                print(f"No compatible ChromeDriver found for Chrome {chrome_major_version}")
                return False
            
            print(f"Installing ChromeDriver version {compatible_version}")
            
        else:
            # For older Chrome versions, use the legacy API
            print("Using legacy ChromeDriver API...")
            version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_major_version}"
            with urllib.request.urlopen(version_url) as response:
                compatible_version = response.read().decode().strip()
            
            print(f"Installing ChromeDriver version {compatible_version}")
            download_url = f"https://chromedriver.storage.googleapis.com/{compatible_version}/chromedriver_linux64.zip"
        
        # Download and install ChromeDriver
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "chromedriver.zip")
            
            print(f"Downloading from: {download_url}")
            urllib.request.urlretrieve(download_url, zip_path)
            
            # Extract ChromeDriver
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the chromedriver executable (it might be in a subdirectory for newer versions)
            chromedriver_path = None
            for root, dirs, files in os.walk(temp_dir):
                if 'chromedriver' in files:
                    chromedriver_path = os.path.join(root, 'chromedriver')
                    break
            
            if not chromedriver_path:
                print("ChromeDriver executable not found in downloaded archive")
                return False
            
            # Move to system path and make executable
            if not run_command(f"sudo mv {chromedriver_path} /usr/local/bin/"):
                return False
            
            if not run_command("sudo chmod +x /usr/local/bin/chromedriver"):
                return False
        
        # Verify installation
        chromedriver_exists, chromedriver_version = check_chromedriver_installed()
        if chromedriver_exists:
            print(f"ChromeDriver installation successful: {chromedriver_version}")
            return True
        else:
            print("ChromeDriver installation verification failed")
            return False
        
    except Exception as e:
        print(f"Failed to install ChromeDriver: {e}")
        
        # Fallback: try using webdriver-manager
        print("Attempting fallback installation using webdriver-manager...")
        try:
            # Install webdriver-manager if not available
            subprocess.run([sys.executable, "-m", "pip", "install", "webdriver-manager"], 
                         capture_output=True, check=True)
            
            # Use webdriver-manager to install ChromeDriver
            import subprocess
            result = subprocess.run([
                sys.executable, "-c", 
                "from webdriver_manager.chrome import ChromeDriverManager; "
                "import shutil; "
                "driver_path = ChromeDriverManager().install(); "
                "shutil.copy2(driver_path, '/usr/local/bin/chromedriver'); "
                "print(f'Copied ChromeDriver to /usr/local/bin/chromedriver')"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                run_command("sudo chmod +x /usr/local/bin/chromedriver")
                chromedriver_exists, chromedriver_version = check_chromedriver_installed()
                if chromedriver_exists:
                    print(f"ChromeDriver fallback installation successful: {chromedriver_version}")
                    return True
            
        except Exception as fallback_error:
            print(f"Fallback installation also failed: {fallback_error}")
        
        return False

def verify_installation():
    """Verify Chrome and ChromeDriver are working"""
    print("Verifying installation...")
    
    # Check Chrome
    chrome_exists, chrome_version = check_chrome_installed()
    if not chrome_exists:
        print("❌ Chrome verification failed")
        return False
    
    # Check ChromeDriver
    chromedriver_exists, chromedriver_version = check_chromedriver_installed()
    if not chromedriver_exists:
        print("❌ ChromeDriver verification failed")
        return False
    
    # Test with Selenium
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Selenium test successful! Page title: {title}")
        return True
        
    except ImportError:
        print("⚠️ Selenium not installed, skipping Selenium test")
        return True  # Chrome/ChromeDriver are installed, Selenium test is optional
    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
        return False

def main():
    """Main installation function"""
    print("Chrome CI/CD Installation Script")
    print("=" * 40)
    
    # Check if running on Linux
    if os.name != 'posix':
        print("❌ This script only supports Linux environments")
        sys.exit(1)
    
    # Check current status
    print("Checking current installation status...")
    chrome_exists, chrome_version = check_chrome_installed()
    chromedriver_exists, chromedriver_version = check_chromedriver_installed()
    
    print(f"Chrome installed: {chrome_exists}")
    if chrome_exists:
        print(f"  Version: {chrome_version}")
    
    print(f"ChromeDriver installed: {chromedriver_exists}")
    if chromedriver_exists:
        print(f"  Version: {chromedriver_version}")
    
    # Install dependencies if Chrome needs to be installed
    if not chrome_exists:
        print("\nInstalling Chrome dependencies...")
        if not install_chrome_dependencies():
            print("❌ Failed to install Chrome dependencies")
            sys.exit(1)
    else:
        print("\nChrome already exists, skipping dependency installation")
    
    # Install Chrome if needed
    if not install_chrome():
        print("❌ Failed to install Chrome")
        sys.exit(1)
    
    # Install ChromeDriver if needed
    if not install_chromedriver():
        print("❌ Failed to install ChromeDriver")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("❌ Installation verification failed")
        sys.exit(1)
    
    print("✅ Chrome installation completed successfully!")
    
    # Set up environment variables for CI/CD
    print("\nEnvironment setup:")
    print("export DISPLAY=:1")
    print("export CHROME_BIN=/usr/bin/google-chrome")
    print("export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver")

if __name__ == "__main__":
    main()
