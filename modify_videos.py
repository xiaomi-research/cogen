import os
import argparse
from moviepy.editor import VideoFileClip, clips_array

def process_video(input_path, output_path):
    """
    Process a video with 6 camera views (h*6w) into a 2x3 grid layout (2h*3w).
    Layout: [6, 1, 2] on top, [3, 4, 5] on bottom.
    """
    # Load the input video
    print(f"Loading video: {input_path}")
    video = VideoFileClip(input_path)
    
    # Get video dimensions
    width, height = video.size
    single_width = width // 6
    
    # Extract the 6 camera views
    print("Extracting individual camera views...")
    cam1 = video.crop(x1=0*single_width, y1=0, x2=1*single_width, y2=height)
    cam2 = video.crop(x1=1*single_width, y1=0, x2=2*single_width, y2=height)
    cam3 = video.crop(x1=2*single_width, y1=0, x2=3*single_width, y2=height)
    cam4 = video.crop(x1=3*single_width, y1=0, x2=4*single_width, y2=height)
    cam5 = video.crop(x1=4*single_width, y1=0, x2=5*single_width, y2=height)
    cam6 = video.crop(x1=5*single_width, y1=0, x2=6*single_width, y2=height)
    
    # Arrange in 2x3 layout (top row: 6,1,2, bottom row: 3,4,5)
    print("Rearranging video layout...")
    arranged_clips = clips_array([
        [cam6, cam1, cam2],
        [cam3, cam4, cam5]
    ])
    
    # Write the output video
    print(f"Writing output video to: {output_path}")
    arranged_clips.write_videofile(
        output_path, 
        codec='libx264',
        audio=False,  # Remove if you want to keep audio
        preset='medium',
        threads=4
    )
    
    # Close all clips to free resources
    video.close()
    cam1.close()
    cam2.close()
    cam3.close()
    cam4.close()
    cam5.close()
    cam6.close()
    arranged_clips.close()
    
    print("Video processing completed!")

def process_directory(input_dir, output_dir):
    """Process all videos in a directory"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for filename in os.listdir(input_dir):
        if filename.endswith(('.mp4', '.avi', '.mov')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"rearranged_{filename}")
            try:
                process_video(input_path, output_path)
                print(f"Successfully processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rearrange 6-camera video layout from 1x6 to 2x3")
    parser.add_argument("--input", type=str, help="Input video file or directory")
    parser.add_argument("--output", type=str, help="Output video file or directory")
    parser.add_argument("--batch", action="store_true", help="Process all videos in directory")
    
    args = parser.parse_args()
    
    if args.batch:
        process_directory(args.input, args.output)
    else:
        process_video(args.input, args.output)
