
import PyInstaller.__main__
import os
import shutil
import sys
import subprocess
from pathlib import Path

class ApplicationBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.src_dir = self.root_dir / "src"
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        self.resource_dir = self.src_dir / "resources"
        
    def clean_directories(self):
        """Clean build and dist directories"""
        for directory in [self.build_dir, self.dist_dir]:
            if directory.exists():
                shutil.rmtree(directory)
    
    def create_directories(self):
        """Create necessary directories"""
        for directory in [self.build_dir, self.dist_dir, self.resource_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def copy_resources(self):
        """Copy resources to distribution"""
        if self.resource_dir.exists():
            shutil.copytree(
                self.resource_dir,
                self.dist_dir / "CommandR" / "resources",
                dirs_exist_ok=True
            )
    
    def build_application(self):
        """Build the application using PyInstaller"""
        PyInstaller.__main__.run([
            'src/main.py',
            '--name=CommandR',
            '--windowed',
            '--onedir',
            '--icon=src/resources/cohere_icon.ico',
            '--add-data=src/resources:resources',
            '--hidden-import=customtkinter',
            '--hidden-import=cohere',
            '--hidden-import=dotenv',
            '--clean',
            f'--workpath={self.build_dir}',
            f'--distpath={self.dist_dir}'
        ])
    
    def create_macos_app(self):
        """Create macOS .app bundle"""
        if sys.platform != "darwin":
            return
            
        app_path = self.dist_dir / "CommandR.app"
        if app_path.exists():
            shutil.rmtree(app_path)
            
        # Create Info.plist
        info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>CommandR</string>
    <key>CFBundleDisplayName</key>
    <string>CommandR</string>
    <key>CFBundleIdentifier</key>
    <string>com.cohere.commandr</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleExecutable</key>
    <string>CommandR</string>
    <key>CFBundleIconFile</key>
    <string>cohere_icon.icns</string>
</dict>
</plist>
"""
        
        # Create app bundle structure
        contents = app_path / "Contents"
        macos = contents / "MacOS"
        resources = contents / "Resources"
        
        for directory in [contents, macos, resources]:
            directory.mkdir(parents=True)
            
        # Write Info.plist
        with open(contents / "Info.plist", "w") as f:
            f.write(info_plist)
            
        # Copy executable and resources
        shutil.copy(self.dist_dir / "CommandR" / "CommandR", macos)
        shutil.copytree(
            self.resource_dir,
            resources,
            dirs_exist_ok=True
        )
    
    def setup_shortcut(self):
        """Set up Command+R shortcut for macOS"""
        if sys.platform != "darwin":
            return
            
        script = """
        tell application "System Events"
            make new shortcut at end of shortcuts with properties {key code: 15, modifiers: {command down}}
            set shortcut key to "R"
        end tell
        """
        
        try:
            subprocess.run(['osascript', '-e', script])
        except Exception as e:
            print(f"Error setting up shortcut: {e}")
    
    def build(self):
        """Execute full build process"""
        print("Starting build process...")
        
        try:
            self.clean_directories()
            print("Cleaned build directories")
            
            self.create_directories()
            print("Created necessary directories")
            
            self.build_application()
            print("Built application")
            
            self.copy_resources()
            print("Copied resources")
            
            if sys.platform == "darwin":
                self.create_macos_app()
                print("Created macOS application bundle")
                
                self.setup_shortcut()
                print("Set up Command+R shortcut")
            
            print("Build completed successfully!")
            
        except Exception as e:
            print(f"Error during build: {e}")
            sys.exit(1)

if __name__ == "__main__":
    builder = ApplicationBuilder()
    builder.build()
