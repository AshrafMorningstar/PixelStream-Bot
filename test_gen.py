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

import cv2
import numpy as np

def create_test_video(filename="test_video.mp4", duration=5, fps=30, width=640, height=480):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    # Bouncing ball state
    x, y = width // 2, height // 2
    dx, dy = 5, 4
    radius = 30
    
    frames = duration * fps
    
    for _ in range(frames):
        # specific background color (dark gray)
        frame = np.full((height, width, 3), 50, dtype=np.uint8)
        
        # Draw ball
        cv2.circle(frame, (x, y), radius, (255, 255, 255), -1)
        
        # Update position
        x += dx
        y += dy
        
        # Bounce
        if x - radius < 0 or x + radius > width:
            dx = -dx
        if y - radius < 0 or y + radius > height:
            dy = -dy
            
        out.write(frame)
        
    out.release()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_test_video()