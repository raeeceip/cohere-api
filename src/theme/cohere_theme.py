# src/theme/cohere_theme.py
import customtkinter as ctk
import json
import os

class CohereTheme:
    COLORS = {
        "primary": "#7E6BD9",
        "secondary": "#5046E4",
        "accent": "#FF7A5C",
        "light": {
            "background": "#FAFBFC",
            "surface": "#FFFFFF",
            "metallic": "#F0F2F5",
            "text": "#1A1B1E",
            "text_secondary": "#6B6C6F",
            "border": "#E2E4E9",
            "message_user": "#F0F2F5",
            "message_assistant": "#FFFFFF"
        },
        "dark": {
            "background": "#1E1F23",
            "surface": "#27282D",
            "metallic": "#2A2B30",
            "text": "#FFFFFF",
            "text_secondary": "#A0A0A0",
            "border": "#3A3B3E",
            "message_user": "#2D2E33",
            "message_assistant": "#2A2B30"
        }
    }

    @classmethod
    def setup_theme(cls, mode: str = "system"):
        ctk.set_appearance_mode(mode)
        cls._configure_theme_colors()
        cls._configure_widgets()
    
    @classmethod
    def _configure_theme_colors(cls):
        theme_data = {
            "CTk": {
                "fg_color": [cls.COLORS["light"]["background"], cls.COLORS["dark"]["background"]]
            },
            "CTkFrame": {
                "fg_color": [cls.COLORS["light"]["surface"], cls.COLORS["dark"]["surface"]],
                "border_color": [cls.COLORS["light"]["border"], cls.COLORS["dark"]["border"]],
                "border_width": 1,
                "corner_radius": 12
            },
            "CTkButton": {
                "fg_color": cls.COLORS["primary"],
                "hover_color": cls.COLORS["secondary"],
                "text_color": ["#FFFFFF", "#FFFFFF"],
                "corner_radius": 8
            },
            "CTkTextbox": {
                "fg_color": ["transparent", "transparent"],
                "border_color": [cls.COLORS["light"]["border"], cls.COLORS["dark"]["border"]],
                "text_color": [cls.COLORS["light"]["text"], cls.COLORS["dark"]["text"]],
                "border_width": 1,
                "corner_radius": 8
            },
            "CTkScrollableFrame": {
                "fg_color": [cls.COLORS["light"]["background"], cls.COLORS["dark"]["background"]],
                "corner_radius": 8
            }
        }
        
        resource_path = os.getenv("RESOURCE_PATH", "resources")
        if not os.path.exists(resource_path):
            os.makedirs(resource_path)
            
        with open(os.path.join(resource_path, "theme.json"), "w") as f:
            json.dump(theme_data, f, indent=2)

    @classmethod
    def _configure_widgets(cls):
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)

    @classmethod
    def get_message_colors(cls, role: str, mode: str = "dark"):
        theme = cls.COLORS[mode.lower()]
        return {
            "user": {
                "bg": theme["message_user"],
                "text": theme["text"]
            },
            "assistant": {
                "bg": theme["message_assistant"],
                "text": theme["text"]
            }
        }.get(role.lower(), {"bg": theme["message_assistant"], "text": theme["text"]})