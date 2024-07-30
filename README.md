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

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.
