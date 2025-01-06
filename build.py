import PyInstaller.__main__
import os
import shutil
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, List
import semver
from datetime import datetime

class BuildConfig:
    def __init__(self, version: str):
        self.version = version
        self.root_dir = Path(__file__).parent
        self.src_dir = self.root_dir / "src"
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        self.resource_dir = self.src_dir / "resources"
        self.platform = sys.platform

    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "platform": self.platform,
            "paths": {
                "root": str(self.root_dir),
                "src": str(self.src_dir),
                "build": str(self.build_dir),
                "dist": str(self.dist_dir),
                "resources": str(self.resource_dir)
            }
        }

class ApplicationBuilder:
    def __init__(self):
        self.config = self._load_build_config()
        
    def _load_build_config(self) -> BuildConfig:
        """Load version from pyproject.toml or version.json"""
        version_file = Path("version.json")
        if version_file.exists():
            with open(version_file) as f:
                data = json.load(f)
                version = data.get("version", "0.1.0")
        else:
            version = "0.1.0"
        
        return BuildConfig(version)

    def _get_build_args(self) -> List[str]:
        """Get platform-specific PyInstaller arguments"""
        common_args = [
            'src/main.py',
            f'--name=CommandR-{self.config.version}',
            '--windowed',
            '--onedir',
            '--add-data=src/resources:resources',
            '--hidden-import=customtkinter',
            '--hidden-import=cohere',
            '--hidden-import=python-dotenv',
            '--clean',
            f'--workpath={self.config.build_dir}',
            f'--distpath={self.config.dist_dir}'
        ]

        if self.config.platform == "darwin":
            common_args.extend([
                '--icon=src/resources/cohere_icon.icns',
                '--target-arch=universal2'
            ])
        elif self.config.platform == "win32":
            common_args.extend([
                '--icon=src/resources/cohere_icon.ico',
                '--win-private-assemblies'
            ])
        else:  # Linux
            common_args.extend([
                '--icon=src/resources/cohere_icon.png'
            ])

        return common_args

    def build(self) -> bool:
        """Execute full build process"""
        try:
            self._clean_directories()
            self._create_directories()
            self._build_application()
            self._copy_resources()
            self._create_platform_specific()
            self._create_build_manifest()
            return True
        except Exception as e:
            print(f"Build failed: {e}")
            return False

    def _clean_directories(self):
        """Clean build and dist directories"""
        for directory in [self.config.build_dir, self.config.dist_dir]:
            if directory.exists():
                shutil.rmtree(directory)

    def _create_directories(self):
        """Create necessary directories"""
        for directory in [self.config.build_dir, self.config.dist_dir, self.config.resource_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def _build_application(self):
        """Build the application using PyInstaller"""
        PyInstaller.__main__.run(self._get_build_args())

    def _copy_resources(self):
        """Copy resources to distribution"""
        if self.config.resource_dir.exists():
            dist_resources = self.config.dist_dir / f"CommandR-{self.config.version}" / "resources"
            shutil.copytree(
                self.config.resource_dir,
                dist_resources,
                dirs_exist_ok=True
            )

    def _create_platform_specific(self):
        """Create platform-specific bundles"""
        if self.config.platform == "darwin":
            self._create_macos_app()
        elif self.config.platform == "win32":
            self._create_windows_installer()

    def _create_macos_app(self):
        """Create macOS .app bundle"""
        app_name = f"CommandR-{self.config.version}.app"
        app_path = self.config.dist_dir / app_name
        
        if app_path.exists():
            shutil.rmtree(app_path)

        # Create app bundle structure
        contents = app_path / "Contents"
        macos = contents / "MacOS"
        resources = contents / "Resources"
        
        for directory in [contents, macos, resources]:
            directory.mkdir(parents=True)

        # Create Info.plist
        info_plist = self._generate_info_plist()
        with open(contents / "Info.plist", "w") as f:
            f.write(info_plist)

        # Copy files
        exe_path = self.config.dist_dir / f"CommandR-{self.config.version}" / f"CommandR-{self.config.version}"
        shutil.copy(exe_path, macos / f"CommandR-{self.config.version}")
        shutil.copytree(
            self.config.resource_dir,
            resources,
            dirs_exist_ok=True
        )

    def _create_windows_installer(self):
        """Create Windows installer using NSIS"""
        try:
            import nsist
            # Implementation for Windows installer
            pass
        except ImportError:
            print("NSIS not available - skipping installer creation")

    def _create_build_manifest(self):
        """Create build manifest with metadata"""
        manifest = {
            "build_config": self.config.to_dict(),
            "timestamp": datetime.now().isoformat(),
            "platform": sys.platform,
            "python_version": sys.version
        }
        
        manifest_path = self.config.dist_dir / "build_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

    def _generate_info_plist(self) -> str:
        """Generate Info.plist content for macOS"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
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
    <string>{self.config.version}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleExecutable</key>
    <string>CommandR-{self.config.version}</string>
    <key>CFBundleIconFile</key>
    <string>cohere_icon.icns</string>
</dict>
</plist>
"""

if __name__ == "__main__":
    builder = ApplicationBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)