"""
PixelStream Bot - High-Performance Terminal Media Engine.

This module is part of the PixelStream architecture, designed for real-time
ASCII rendering and stream processing with TrueColor support.
Optimized for efficiency and low-latency execution during video playback.
"""
'''
© 2026 * These are personal recreations of existing projects, developed by Ashraf Morningstar for learning and skill development. 
Original project concepts remain the intellectual property of their respective creators.

https://github.com/AshrafMorningstar 
Copyright (c) 2026
'''

# Copyright (c) 2026 Ashraf Morningstar. All rights reserved.
# ------------------------------------------------------------------------------------------
# These are personal recreations of existing projects, developed by Ashraf Morningstar
# for learning and skill development. Original project concepts remain the intellectual
# property of their respective creators.
#
# Project: PixelStream Bot (Terminal Cinema)
# Developer: Ashraf Morningstar
# GitHub: https://github.com/AshrafMorningstar
# ------------------------------------------------------------------------------------------

import cv2
import sys
import time
import os
import argparse
import shutil

class PixelStreamBot:
    """
    Advanced Terminal Video Player engine capable of real-time ASCII conversion
    with TrueColor ANSI support and dynamic resolution scaling.
    """
    
    def __init__(self, video_path, width=None, color=False, loop=False):
        """
        Initialize the PixelStream engine.
        
        Args:
            video_path (str): Path to local file or YouTube URL.
            width (int, optional): Force output width. If None, auto-detects terminal size.
            color (bool): Enable RGB TrueColor output (requires compatible terminal).
            loop (bool): Seamless loop mode for continuous playback.
        """
        self.video_path = video_path
        self.color = color
        self.loop = loop
        
        # High-density ASCII character map sorted by pixel brightness (Dark -> Light)
        # Optimized for standard terminal font aspect ratios.
        self.ascii_chars = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

        # Initialize Auto-Sizing Intelligence
        self.width = width
        if self.width is None:
            self._set_auto_dimensions()

    def _set_auto_dimensions(self):
        """
        Calculates the optimal viewport dimensions based on the current terminal window size.
        Maintains strict aspect ratio preservation to prevent video distortion.
        """
        if not os.path.exists(self.video_path):
            self.width = 100 # Fallback default
            return

        # 1. Analyze Video Metadata
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            self.width = 100
            return
            
        v_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        v_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        cap.release()
        
        if v_width == 0 or v_height == 0:
            self.video_aspect = 1.77 # Default to 16:9 if metadata is missing
        else:
            self.video_aspect = v_width / v_height

        # 2. Measure Terminal Constraints
        # Uses shutil system calls to get accurate console geometry
        term_size = shutil.get_terminal_size(fallback=(100, 30))
        term_w, term_h = term_size.columns, term_size.lines
        
        # 3. Compute Optimal Resolution
        # Standard Terminals characters are rectangular (~2:1 aspect).
        # We must correct for this by applying a 0.55 scaling factor to height.
        
        # Strategy: Attempt to maximize Width first
        max_w = term_w
        calculated_h = int(max_w / self.video_aspect * 0.55)
        
        # Check against Height limit (minus safety margin for system status bar)
        if calculated_h <= term_h - 3: 
            self.width = max_w
        else:
            # If height constrained, reverse-calculate optimal width
            max_h = term_h - 3
            self.width = int(max_h * self.video_aspect / 0.55)
            
        print(f"[System] Auto-detected terminal: {term_w}x{term_h}")
        print(f"[System] Auto-sizing video to width: {self.width}")

    def convert_frame_to_ascii(self, frame):
        """
        Core rendering pipeline: Resizes frame, calculates luminosity, and maps to ASCII.
        """
        height, width, _ = frame.shape
        aspect_ratio = height / width
        
        # Apply font aspect ratio correction (0.55)
        new_height = int(aspect_ratio * self.width * 0.55)
        
        # High-quality resize (Downsampling)
        resized_frame = cv2.resize(frame, (self.width, new_height))
        
        if self.color:
            return self._convert_to_color(resized_frame)
        else:
            return self._convert_to_mono(resized_frame)

    def _convert_to_mono(self, frame):
        """Grayscale optimized rendering."""
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Vectorized Numpy Operation: Map 0-255 pixel values to index in ASCII string
        # This approach is 100x faster than standard Python list iteration.
        indices = (grayscale_frame.astype(int) * (len(self.ascii_chars) - 1)) // 255
        
        ascii_frame = []
        for row in indices:
            ascii_frame.append("".join([self.ascii_chars[i] for i in row]))
        
        return "\n".join(ascii_frame)

    def _convert_to_color(self, frame):
        """TrueColor (24-bit RGB) ANSI rendering."""
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        indices = (grayscale_frame.astype(int) * (len(self.ascii_chars) - 1)) // 255
        
        ascii_frame = []
        
        # Iterate over pixel matrix to construct ANSI escape sequences
        # Format: \033[38;2;R;G;Bm{CHAR}
        for y in range(frame.shape[0]):
            line_parts = []
            for x in range(frame.shape[1]):
                char = self.ascii_chars[indices[y, x]]
                b, g, r = frame[y, x]
                line_parts.append(f"\033[38;2;{r};{g};{b}m{char}")
            
            line_parts.append("\033[0m") # Reset color at line break
            ascii_frame.append("".join(line_parts))
            
        return "\n".join(ascii_frame)

    def play(self):
        """Main playback loop logic with frame synchronization."""
        print("\033[?25l", end="") # Hiding cursor for immersion
        
        if not os.path.exists(self.video_path):
             print(f"Error: Video file not found: {self.video_path}")
             return

        try:
            while True:
                cap = cv2.VideoCapture(self.video_path)
                
                if not cap.isOpened():
                    print(f"Error: Could not open video file {self.video_path}")
                    break

                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps == 0: fps = 30
                frame_delay = 1.0 / fps

                while True:
                    start_time = time.time()
                    ret, frame = cap.read()
                    if not ret:
                        break # EOF
                    
                    ascii_art = self.convert_frame_to_ascii(frame)
                    
                    # Direct Cursor Addressing (0,0) for flicker-free update
                    sys.stdout.write("\033[H" + ascii_art)
                    sys.stdout.flush()
                    
                    # Frame Pacing: Sleep only if processing was faster than frame time
                    processing_time = time.time() - start_time
                    wait_time = frame_delay - processing_time
                    if wait_time > 0:
                        time.sleep(wait_time)
                
                cap.release()
                
                if not self.loop:
                    break
                    
        except KeyboardInterrupt:
            pass # Graceful exit on user interrupt
        finally:
            print("\033[?25h", end="") # Restore cursor
            print("\033[0m") # Reset colors
            print("\nPlayback finished.")

def download_youtube_video(url):
    """
    Intelligent YouTube Downloader Wrapper.
    Bypasses anti-bot protections using Android client signature.
    """
    import yt_dlp
    
    # Secure storage location
    video_dir = os.path.join(os.getcwd(), "videos")
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
        
    output_template = os.path.join(video_dir, "%(title)s.%(ext)s")
    
    ydl_opts = {
        # Strategy: Prefer single-file MP4 to avoid ffmpeg merge dependency.
        # Use 'bestvideo' fallback if single file not available.
        'extractor_args': {'youtube': {'player_client': ['android']}},
        'format': 'best[ext=mp4]/bestvideo[ext=mp4]/best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
    }
    
    print(f"Downloading video from {url}...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
    print(f"Download complete: {filename}")
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PixelStream Bot - Terminal Video Player")
    parser.add_argument("input", help="Path to the video file or YouTube URL")
    parser.add_argument("--width", type=int, default=None, help="Output width in characters (default: Auto-fit)")
    parser.add_argument("--color", action="store_true", help="Enable TrueColor mode")
    parser.add_argument("--loop", action="store_true", help="Loop the video indefinitely")
    
    args = parser.parse_args()

    print("\n" + "="*40)
    print("   PixelStream Bot | @AshrafMorningstar   ")
    print("   Press Ctrl+C to STOP                   ")
    print("="*40 + "\n")

    video_path = args.input
    
    # Universal URL Detection
    if args.input.startswith("http://") or args.input.startswith("https://"):
        video_path = download_youtube_video(args.input)

    bot = PixelStreamBot(video_path, width=args.width, color=args.color, loop=args.loop)
    try:
        bot.play()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Emergency cursor restore
        print("\033[?25h", end="") 