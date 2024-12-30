# Command R Assistant GUI

A modern, desktop GUI application that interfaces with Cohere's Command R model, providing a seamless experience for natural language interactions and system automation.

## Features

### Core Functionality

- **Modern Interface**: Built with CustomTkinter for a clean, modern look that respects system appearance settings
- **Real-time Interaction**: Supports both streaming and non-streaming responses
- **Keyboard Shortcuts**:
  - `Command+R` to launch the application
  - `Enter` to generate responses
  - `Command+K` to clear output

### AI Capabilities

- **General Chat**: Open-ended conversations with Command R model
- **Calendar Integration**: Natural language meeting scheduling that integrates with macOS Calendar
- **Temperature Control**: Adjustable creativity in responses via temperature slider
- **Stream Toggle**: Option to see responses appear in real-time or wait for complete responses

### System Integration

- **Calendar Events**: Creates calendar events directly in macOS Calendar using AppleScript
- **Environment Variables**: Secure API key management through .env files
- **Error Handling**: Robust error handling and user feedback through status bar

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/command-r-assistant.git
cd command-r-assistant
```

2. Install required packages:

```bash
pip install customtkinter cohere python-dotenv
```

3. Create a .env file with your Cohere API key:

```bash
echo "COHERE_API_KEY=your_api_key_here" > .env
```

4. Set up the Command+R shortcut in System Preferences:
   - Open System Preferences > Keyboard > Shortcuts
   - Add new shortcut pointing to the script location

## Usage

### Basic Interaction

- Launch the app using Command+R
- Type your query in the input box
- Press Enter to generate a response
- Use the temperature slider to adjust response creativity
- Toggle streaming to see responses in real-time

### Calendar Features

Example commands:

- "Schedule a team meeting tomorrow at 2pm for 1 hour"
- "Set up a project review for next Monday at 10am"
- "Schedule a 30-minute coffee chat with John for Friday afternoon"

## Potential Improvements

### Model Integration

1. **RAG Integration**:

   - Add document upload capability
   - Implement context window management
   - Add source attribution in responses

2. **Tool Use Enhancement**:

   - Expand beyond calendar to other system tools
   - Add API integration capabilities
   - Implement structured tool response handling

3. **Model Performance**:
   - Add prompt templates for different use cases
   - Implement retry logic for failed requests
   - Add response quality metrics

### Technical Improvements

1. **GUI Enhancements**:

   - Add conversation history management
   - Implement chat memory
   - Add markdown rendering in output
   - Add syntax highlighting for code
   - Support for multiple chat sessions in tabs

2. **System Integration**:

   - Add support for multiple calendar providers
   - Implement email integration
   - Add file system operations
   - Support for task management systems

3. **Development Features**:
   - Add logging system
   - Implement telemetry for usage patterns
   - Add unit and integration tests
   - Create plugin system for extensions

### User Experience

1. **Interface**:

   - Add conversation export
   - Implement themes and customization
   - Add keyboard shortcut customization
   - Implement autocomplete suggestions

2. **Productivity**:

   - Add templates for common requests
   - Implement batch operations
   - Add scheduled operations
   - Create macro system for repeated tasks

3. **Accessibility**:
   - Add voice input support
   - Implement screen reader compatibility
   - Add keyboard navigation improvements
   - Support for multiple languages

## Contributing to Cohere's Ecosystem

### Model Feedback

1. **Data Collection**:

   - Track successful vs failed queries
   - Collect user corrections and adjustments
   - Monitor response quality and relevance
   - Gather performance metrics

2. **Feature Requests**:

   - Document common user requests
   - Track feature usage patterns
   - Identify integration opportunities
   - Report edge cases and limitations

3. **Integration Testing**:
   - Test model in real-world scenarios
   - Validate system integration capabilities
   - Benchmark performance metrics
   - Document integration patterns

### Development Support

1. **SDK Improvements**:

   - Suggest new SDK features
   - Report bug findings
   - Document usage patterns
   - Create example implementations

2. **Community Resources**:
   - Share implementation examples
   - Create tutorials and guides
   - Document best practices
   - Build reusable components

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

## License

[Insert License Information]

## Acknowledgments

- Cohere team for the Command R model
- CustomTkinter for the modern UI framework
- Contributors and testers
