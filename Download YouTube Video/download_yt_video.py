import yt_dlp
import os

def list_available_formats(info):
    """List all available formats and return a dictionary mapping format_id to resolution."""
    format_dict = {}
    print(f"Available formats for '{info['title']}':\n")
    for fmt in info['formats']:
        if fmt.get('vcodec') != 'none':  # Check if it's a video format
            resolution = f"{fmt.get('height')}p" if fmt.get('height') else "Audio Only"
            file_type = fmt.get('ext')
            size = fmt.get('filesize', 'Unknown')
            format_id = fmt.get('format_id')
            print(f"ID: {format_id}, Resolution: {resolution}, Format: {file_type}, Size: {size}")
            format_dict[format_id] = resolution
    return format_dict


def download_video_by_format(youtube_url, output_path=".", format_id=None):
    """Download video based on user-selected format."""
    if output_path is None:
        output_path = os.path.expanduser("~/Downloads")  # Save to Downloads folder

    ydl_opts = {
        'format': format_id if format_id else 'bestvideo+bestaudio',  # Download best available if no format_id is given
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Output filename format
        'merge_output_format': 'mp4',  # Merge video and audio into mp4
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Ensure output is mp4
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information and list formats if format_id not provided
            info = ydl.extract_info(youtube_url, download=False)

            if format_id is None:  # If no format is provided, show available formats
                format_dict = list_available_formats(info)
                format_id = input("\nEnter the format ID you want to download (best available if left blank): ")
                if not format_id:
                    format_id = 'bestvideo+bestaudio'  # Fallback to best

                print(f"Downloading format {format_id} for '{info['title']}'...")

            # Download the selected format
            ydl_opts['format'] = format_id  # Update options with the selected format
            ydl.download([youtube_url])

            print(f"Download completed successfully in format {format_id}!")
    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage
# youtube_url = "https://www.youtube.com/watch?v=DCfC2P0weKo"  
youtube_url = 'https://www.youtube.com/watch?v=WO2b03Zdu4Q'
download_video_by_format(youtube_url)
