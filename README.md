# CommandR Assistant (Experimental Prototype)

## ⚠️ Prototype Status
This is an experimental prototype of a desktop GUI for Cohere's Command model. It is currently in early development and contains known issues. This release is intended for testing and feedback purposes only.

## Project Description
CommandR Assistant is an experimental desktop GUI application that provides a simple interface for interacting with Cohere's Command model. Built with CustomTkinter and designed for macOS, it attempts to integrate natural language processing with system operations like calendar management.

## 🧪 v0.1.0-alpha (Initial Prototype)

### Features
- Basic chat interface with Cohere's Command model
- Experimental calendar event creation (highly unstable)
- Temperature adjustment for responses
- Stream/non-stream response toggle
- Dark mode interface

### Known Issues
- Calendar integration may fail or behave unexpectedly
- Async operations can cause UI freezes
- Response generation sometimes requires multiple attempts
- Return key handling is inconsistent
- Memory usage grows over time
- No proper error recovery for failed API calls
- Stream mode may display incomplete responses
- Settings are not persisted between sessions

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/command-r-assistant.git
cd command-r-assistant

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "COHERE_API_KEY=your_api_key_here" > .env

# Run the application
python src/main.py
```

### Requirements
- Python 3.8+
- macOS (calendar features are macOS-specific)
- Cohere API key
- Minimum 512MB RAM
- Internet connection

### Usage Warning
⚠️ This software is experimental and not intended for production use. It may:
- Crash unexpectedly
- Create invalid calendar entries
- Fail to handle errors gracefully
- Consume excessive system resources
- Lose conversation history
- Generate unexpected responses

### Development Status
This project is in active development but is currently:
- Missing proper testing
- Lacking error handling in many areas
- Using experimental async patterns
- Not optimized for performance
- Missing many planned features

### Planned Improvements
1. Proper async/sync handling
2. Robust error recovery
3. Persistent settings storage
4. Memory optimization
5. Proper calendar integration
6. Cross-platform support
7. Conversation history
8. Response validation
9. Unit tests
10. CI/CD pipeline

### Contributing
This is an experimental project and contributions are welcome. However, please note that the codebase is rapidly changing and may be significantly refactored.

### License
MIT License - See LICENSE file for details

---

## Setup Instructions for Developers

### Environment Setup
```bash
# Required environment variables
COHERE_API_KEY=your_api_key_here

# Optional configuration
DEBUG=True
LOG_LEVEL=DEBUG
```

### Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Running Tests (Not Yet Implemented)
```bash
pytest tests/
```

### Project Structure
```
command-r-assistant/
├── src/
│   ├── components/
│   ├── theme/
│   ├── validators/
│   ├── views/
│   └── main.py
├── tests/
├── .env
├── requirements.txt
└── README.md
```

### Debug Mode
To run in debug mode with additional logging:
```bash
python src/main.py --debug
```

---

## Future Directions

1. **Expanded Capabilities**:

   - Multi-model support
   - Cross-platform compatibility
   - Mobile companion app
   - Web interface option

2. **Enterprise Features**:

   - Team collaboration tools
   - Custom model fine-tuning interface
   - Advanced security features
   - Audit logging

3. **Integration Platform**:
   - API gateway functionality
   - Custom connector framework
   - Workflow automation tools
   - Integration marketplace

## Acknowledgments

- Cohere team for the Command R model
- CustomTkinter for the modern UI framework


⚠️ Final Note: This is a prototype release intended for testing and feedback. Use at your own risk and please report any issues you encounter.
