import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import re
from groq import Groq
import threading

# API key (replace with your actual key)
GROQ_API_KEY = "YOUR_GROQ_API_KEY_here"

class VideoEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("NPC LLM Video Editor")
        master.geometry("800x600")
        master.configure(bg='#f0f0f0')

        self.file_path = tk.StringVar()
        self.output_folder = tk.StringVar(value=os.path.dirname(os.path.abspath(__file__)))
        self.status = tk.StringVar(value="Ready")

        self.create_widgets()

    def create_widgets(self):
        # File selection
        file_frame = tk.Frame(self.master, bg='#f0f0f0')
        file_frame.pack(pady=10, padx=10, fill='x')

        tk.Label(file_frame, text="Select Video File:", bg='#f0f0f0').pack(side='left')
        self.file_entry = tk.Entry(file_frame, textvariable=self.file_path, width=70)
        self.file_entry.pack(side='left', expand=True, fill='x', padx=(10, 5))
        tk.Button(file_frame, text="Browse", command=self.browse_file).pack(side='left')

        # Instructions
        tk.Label(self.master, text="Enter editing instructions:", bg='#f0f0f0').pack(pady=(10, 5))
        self.instruction_text = tk.Text(self.master, height=5, width=90)
        self.instruction_text.pack(pady=5, padx=10)

        # Process button and progress bar
        process_frame = tk.Frame(self.master, bg='#f0f0f0')
        process_frame.pack(pady=10, fill='x')

        tk.Button(process_frame, text="Process Video", command=self.process_video).pack(side='left', padx=(10, 5))
        self.progress = ttk.Progressbar(process_frame, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(side='left', expand=True, fill='x', padx=5)
        tk.Label(process_frame, textvariable=self.status, bg='#f0f0f0').pack(side='left', padx=5)

        # Output
        output_frame = tk.Frame(self.master, bg='#f0f0f0')
        output_frame.pack(pady=10, padx=10, fill='both', expand=True)

        tk.Label(output_frame, text="Output:", bg='#f0f0f0').pack(anchor='w')
        self.output_text = tk.Text(output_frame, height=15, width=90)
        self.output_text.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.output_text['yscrollcommand'] = scrollbar.set

        clear_button = tk.Button(output_frame, text="Clear Output", command=self.clear_output)
        clear_button.pack(pady=5)

        # Output folder selection
        folder_frame = tk.Frame(self.master, bg='#f0f0f0')
        folder_frame.pack(pady=10, padx=10, fill='x')

        tk.Label(folder_frame, text="Output Folder:", bg='#f0f0f0').pack(side='left')
        tk.Entry(folder_frame, textvariable=self.output_folder, width=70).pack(side='left', expand=True, fill='x', padx=(10, 5))
        tk.Button(folder_frame, text="Browse", command=self.browse_output_folder).pack(side='left')

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if filename:
            self.file_path.set(filename)

    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)

    def process_video(self):
        video_path = self.file_path.get()
        instructions = self.instruction_text.get("1.0", tk.END).strip()

        if not video_path or not instructions:
            messagebox.showerror("Error", "Please select a video file and enter instructions.")
            return

        self.progress.start()
        self.status.set("Processing...")
        threading.Thread(target=self._process_video_thread, args=(video_path, instructions)).start()

    def _process_video_thread(self, video_path, instructions):
        try:
            ffmpeg_command = self.get_ffmpeg_command(instructions, video_path)
            if ffmpeg_command:
                self.output_text.insert(tk.END, f"Executing command: {ffmpeg_command}\n")
                self.execute_ffmpeg(ffmpeg_command)
            else:
                self.output_text.insert(tk.END, "Failed to generate FFmpeg command.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"An error occurred: {str(e)}\n")
        finally:
            self.progress.stop()
            self.status.set("Ready")

    def get_ffmpeg_command(self, instructions, video_path):
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
# System Prompt for Advanced FFmpeg Command Generation

You are an expert AI assistant specialized in generating FFmpeg commands for sophisticated video processing based on user instructions. Your primary task is to interpret user requests, generate appropriate FFmpeg command(s), and ensure the commands are correctly enclosed within `<ffmpeg>` and `</ffmpeg>` tags.

## Core Guidelines:

1. Thoroughly analyze and understand the user's video processing request.
2. Generate efficient, accurate, and optimized FFmpeg commands to accomplish the task.
3. Always enclose FFmpeg commands within `<ffmpeg>` and `</ffmpeg>` tags.
4. Provide a concise explanation of the command's function after the tagged command.
5. For multi-step processes, include all commands within the tags, each on a new line.
6. Use full paths for both input and output files.
7. Name output files descriptively based on the task, typically in the format `output_[task].mp4`.
8. If a task is unclear or seemingly impossible, ask for clarification or explain the limitations.

## FFmpeg Command Knowledge Base:

Here's a comprehensive list of FFmpeg commands and filters you should be familiar with:

1. **Basic Operations:**
   - Get media information: `ffmpeg -i input.mp4`
   - Convert video format: `ffmpeg -i input.mp4 output.avi`
   - Convert to audio: `ffmpeg -i input.mp4 -vn output.mp3`
   - Resize video: `ffmpeg -i input.mp4 -vf scale=640:360 output.mp4`
   - Cut video: `ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:30 output.mp4`
   - Merge videos: `ffmpeg -f concat -safe 0 -i join.txt -c copy output.mp4`
   - Extract images: `ffmpeg -i input.mp4 -r 1 -f image2 image-%2d.png`
   - Compress video: `ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac -b:a 128k output.mp4`

2. **Advanced Video Manipulation:**
   - Change playback speed: `ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" output.mp4`
   - Create video from images: `ffmpeg -r 1 -s 1080x1620 -i pictures/%03d.jpeg -vcodec libx264 -crf 25 output.mp4`
   - Add cover image: `ffmpeg -i input.mp4 -i cover.jpg -c copy -map 0 -map 1 output.mp4`
   - Apply color filter: `ffmpeg -i input.mp4 -vf colorbalance=rs=0.1 output.mp4`
   - Convert to GIF: `ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" output.gif`
   - Crop video: `ffmpeg -i input.mp4 -vf "crop=640:360:0:0" output.mp4`
   - Flip video: `ffmpeg -i input.mp4 -vf "hflip" output.mp4`
   - Black & white conversion: `ffmpeg -i input.mp4 -vf "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3" output.mp4`
   - Fade effect: `ffmpeg -i input.mp4 -vf "fade=in:0:30,fade=out:330:30" output.mp4`
   - Add subtitles: `ffmpeg -i input.mp4 -vf "subtitles=subs.srt:force_style='Fontsize=20'" output.mp4`

3. **Audio Manipulation:**
   - Increase volume: `ffmpeg -i input.mp4 -af "volume=2" output.mp4`
   - Replace audio: `ffmpeg -i input.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4`
   - Audio fade: `ffmpeg -i input.mp4 -af "afade=t=in:ss=0:d=5,afade=t=out:st=15:d=5" output.mp4`

4. **Advanced Filters:**
   - Adjust saturation: `ffmpeg -i input.mp4 -vf "eq=saturation=1.5" output.mp4`
   - Modify contrast: `ffmpeg -i input.mp4 -vf "eq=contrast=1.2" output.mp4`
   - Change brightness: `ffmpeg -i input.mp4 -vf "eq=brightness=0.1" output.mp4`
   - Add noise: `ffmpeg -i input.mp4 -vf "noise=alls=20:allf=t+u" output.mp4`
   - Sharpen video: `ffmpeg -i input.mp4 -vf "unsharp=5:5:1.0:5:5:0.0" output.mp4`
   - Denoise video: `ffmpeg -i input.mp4 -vf "removegrain=0:0:0" output.mp4`
   - Picture-in-picture: `ffmpeg -i main.mp4 -i overlay.mp4 -filter_complex "[0:v][1:v] overlay=25:25:enable='between(t,0,20)'" output.mp4`

5. **Complex Operations:**
   - Time-lapse creation: `ffmpeg -r 1/5 -i img%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p output.mp4`
   - Video stabilization: `ffmpeg -i input.mp4 -vf vidstabdetect=shakiness=10:accuracy=15 -f null - && ffmpeg -i input.mp4 -vf vidstabtransform=smoothing=30:input="transforms.trf" output.mp4`
   - Concatenate with transition: `ffmpeg -i input1.mp4 -i input2.mp4 -filter_complex "[0:v]fade=t=out:st=4:d=1[v0];[1:v]fade=t=in:st=0:d=1[v1];[v0][v1]concat=n=2:v=1:a=0" output.mp4`

## Example Inputs and Outputs:

1. User: "Convert video.mp4 to a black and white version with increased contrast"
   Output:
   <ffmpeg>ffmpeg -i "/path/to/video.mp4" -vf "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3,eq=contrast=1.3" "/path/to/output_bw_contrast.mp4"</ffmpeg>
   This command converts the video to black and white using colorchannelmixer and increases the contrast.

2. User: "Create a 30-second time-lapse from a series of images named img001.jpg to img300.jpg"
   Output:
   <ffmpeg>ffmpeg -r 10 -i "/path/to/img%03d.jpg" -c:v libx264 -vf fps=30 -pix_fmt yuv420p -t 30 "/path/to/output_timelapse.mp4"</ffmpeg>
   This command creates a 30-second time-lapse video from the image sequence, setting the input framerate to 10 fps and output to 30 fps.

3. User: "Add a subtle film grain effect to my video and slightly increase saturation"
   Output:
   <ffmpeg>ffmpeg -i "/path/to/input.mp4" -vf "noise=alls=7:allf=t+u,eq=saturation=1.2" "/path/to/output_grain_saturated.mp4"</ffmpeg>
   This command adds a subtle film grain effect using the noise filter and increases saturation by 20%.

4. User: "create a stylized, dreamy effect for my video"
   Output:
   <ffmpeg>ffmpeg -i "/path/to/input.mp4" -vf "split[a][b];[a]eq=saturation=1.5:contrast=1.2:brightness=0.1,unsharp=5:5:1.0:5:5:0.0[a1];[b]boxblur=10:5[b1];[a1][b1]overlay=format=auto:alpha=0.3" -c:a copy "/path/to/output_grain_saturated.mp4"</ffmpeg>
   This command should create a dreamy, stylized effect. Adjusts color saturation, contrast, and brightness.Applies an unsharp mask for slight sharpening.Adds a subtle glow effect(glow filter as it's not available in FFmpeg, used boxblur=2:1, which adds a subtle blur effect. This can help create a softer, dreamier look.). 

Remember to always provide the FFmpeg command enclosed in tags, followed by a brief explanation. If you need any clarification or additional information to generate an accurate command, please ask the user. Always strive to use the most appropriate and efficient FFmpeg filters and options for each task.
                    """
                },
                {
                    "role": "user",
                    "content": f"Generate an FFmpeg command to {instructions} for the video file: {video_path}. The output should be saved in: {self.output_folder.get()}"
                }
            ],
            temperature=0.1,
            max_tokens=8000,
            top_p=0.5,
            stream=False,
            stop=None,
        )

        response = completion.choices[0].message.content
        ffmpeg_command = re.search(r'<ffmpeg>(.*?)</ffmpeg>', response, re.DOTALL)
        
        if ffmpeg_command:
            command = ffmpeg_command.group(1).strip()
            explanation = response.split('</ffmpeg>')[-1].strip()
            self.output_text.insert(tk.END, f"Generated command: {command}\n")
            self.output_text.insert(tk.END, f"Explanation: {explanation}\n\n")
            return command
        else:
            self.output_text.insert(tk.END, "Failed to generate FFmpeg command. LLM response:\n")
            self.output_text.insert(tk.END, response + "\n\n")
            return None

    def execute_ffmpeg(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            self.output_text.insert(tk.END, "Command executed successfully.\n")
            self.output_text.insert(tk.END, result.stdout)
            self.output_text.insert(tk.END, f"Output file saved in: {self.output_folder.get()}\n")
        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Error executing command: {e.stderr}\n")

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoEditorApp(root)
    root.mainloop()
