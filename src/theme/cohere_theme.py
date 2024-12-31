

import customtkinter as ctk
import json
import os
from pathlib import Path
from typing import Dict, Optional

class CohereTheme:
    # Cohere brand colors
    COLORS = {
        "primary": "#7E6BD9",      # Cohere purple
        "secondary": "#5046E4",    # Deep purple
        "accent": "#FF7A5C",       # Coral accent
        "success": "#4CAF50",
        "warning": "#FFC107",
        "error": "#FF5252",
        
        # Light theme colors
        "light": {
            "background": "#FFFFFF",
            "surface": "#F5F6F8",
            "text": "#2A2B2E",
            "text_secondary": "#6B6C6F",
            "border": "#E2E4E9"
        },
        
        # Dark theme colors
        "dark": {
            "background": "#1A1B1E",
            "surface": "#2A2B2E",
            "text": "#FFFFFF",
            "text_secondary": "#A0A0A0",
            "border": "#3A3B3E"
        }
    }

    @classmethod
    def setup_theme(cls, mode: str = "system"):
        """Set up the Cohere theme for the application"""
        # Set appearance mode
        ctk.set_appearance_mode(mode)
        
        # Configure theme colors
        cls._configure_theme_colors()
        
        # Configure widgets
        cls._configure_widgets()
    
    @classmethod
    def _configure_theme_colors(cls):
        """Configure color theme for both light and dark modes"""
        theme_data = {
            "CTk": {
                "fg_color": [cls.COLORS["light"]["background"], cls.COLORS["dark"]["background"]]
            },
            "CTkFrame": {
                "fg_color": [cls.COLORS["light"]["surface"], cls.COLORS["dark"]["surface"]],
                "border_color": [cls.COLORS["light"]["border"], cls.COLORS["dark"]["border"]],
                "border_width": 1,
                "corner_radius": 10
            },
            "CTkButton": {
                "fg_color": cls.COLORS["primary"],
                "hover_color": cls.COLORS["secondary"],
                "border_color": cls.COLORS["primary"],
                "border_width": 0,
                "text_color": ["#FFFFFF", "#FFFFFF"],
                "text_color_disabled": [cls.COLORS["light"]["text_secondary"], 
                                     cls.COLORS["dark"]["text_secondary"]]
            },
            "CTkTextbox": {
                "fg_color": [cls.COLORS["light"]["surface"], cls.COLORS["dark"]["surface"]],
                "border_color": [cls.COLORS["light"]["border"], cls.COLORS["dark"]["border"]],
                "text_color": [cls.COLORS["light"]["text"], cls.COLORS["dark"]["text"]],
                "border_width": 1,
                "corner_radius": 8
            }
        }
        
        # Save theme to file for persistence
        theme_file = Path(os.getenv("RESOURCE_PATH")) / "theme.json"
        with open(theme_file, "w") as f:
            json.dump(theme_data, f, indent=2)
        

    
    @classmethod
    def _configure_widgets(cls):
        """Configure default widget properties"""
        ctk.set_widget_scaling(1.0)  # Ensure consistent scaling
        ctk.set_window_scaling(1.0)
