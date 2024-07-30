# LLM-Powered Video Editor

This application utilizes Large Language Models (LLM) and FFmpeg to automate video editing tasks based on user instructions. Built with a Tkinter GUI, the tool offers a seamless and efficient way to edit videos with natural language commands.

## Features
- **Intuitive GUI**: Simple and user-friendly interface for video selection and instruction input.
- **Advanced FFmpeg Command Generation**: Automatically generates FFmpeg commands from user-provided instructions.
- **Real-time Progress Tracking**: Displays processing progress and status updates.
- **Detailed Output Logging**: Logs FFmpeg command execution and results.

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/sanskar9999/llm_video_editor.git
   cd llm_video_editor
   ```
2. Install the required dependencies:
   ```bash
   pip install tkinter subprocess re groq
   ```
3. Run the application:
   ```bash
   python llm_video_editor.py
   ```

## Usage
1. Open the application.
2. Use the 'Browse' button to select a video file.
3. Enter your editing instructions in natural english language in the text box.
4. Click 'Process Video' to start the editing process.
5. Monitor the progress and view the output logs within the application.

## Example Instructions
- "Convert video to black and white"
- "Add subtitles from file subs.srt"
- "Trim the video to the first 30 seconds"

## Future Improvements 
1. Error handling: Add more robust error handling, especially around the FFmpeg execution. Catch and display specific errors that may occur.
2. Input validation: Add checks to ensure the video file exists and is a valid format before processing.
3. Command preview: Allow users to preview and optionally edit the generated FFmpeg command before execution.
4. Multiple operations: Support chaining multiple editing operations in a single session.
5. Save/load instructions: Add functionality to save and load editing instruction presets.
6. Progress tracking: Implement more detailed progress tracking for long-running operations.
7. Undo functionality: Allow users to undo the last operation or revert to the original video.
8. Video preview: Add a basic video player to preview the input and output videos.
9. Batch processing: Support processing multiple videos with the same instructions.
10. Custom output naming: Allow users to specify custom output file names.
11. Settings: Add a settings menu to configure API keys, default folders, etc.
12. Help/Documentation: Include a help section explaining how to use the app and common editing tasks.
13. Logging: Implement logging to help with debugging and tracking usage.
14. Multithreading improvements: Consider using a thread pool for better resource management.
15. GUI improvements: Add tooltips, keyboard shortcuts, and improve the overall layout and styling.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.
