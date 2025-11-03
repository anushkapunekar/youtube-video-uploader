import os
import argparse
import subprocess
from PIL import Image
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import sys 

# ensure emoji printing works on Windows
sys.stdout.reconfigure(encoding='utf-8')

# OAuth2 scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# ---------- OAuth Handling ----------
def get_authenticated_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

# ---------- Detect if Video is a Short ----------
def is_vertical_video(video_path):
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0",
            video_path
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8").strip()
        width, height = map(int, output.split("x"))
        print(f"📐 Video dimensions: {width}x{height}")
        return height >= width  # Vertical or square
    except Exception as e:
        print(f"⚠️ Could not detect video orientation: {e}")
        return False

# ---------- Thumbnail Validation ----------
def validate_thumbnail(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Thumbnail file not found.")

    file_size = os.path.getsize(path)
    if file_size > 2 * 1024 * 1024:
        raise ValueError("Thumbnail must be under 2 MB.")

    with Image.open(path) as img:
        width, height = img.size
        fmt = img.format.lower()
        if fmt not in ["jpeg", "jpg", "png"]:
            raise ValueError("Thumbnail must be JPG or PNG.")
        if width < 640 or height < 360:
            raise ValueError("Thumbnail too small. Minimum 640×360.")
        print(f"✅ Thumbnail OK — {width}×{height}px, {fmt.upper()}, {round(file_size/1024,1)} KB")

# ---------- Upload Video ----------
def upload_video(youtube, file, title, description, category, privacy):
    if is_vertical_video(file):
        print("📱 Detected vertical video — marking as #Shorts.")
        if "#Shorts" not in title:
            title += " #Shorts"
        if "#Shorts" not in description:
            description += "\n#Shorts"

    body = {
        "snippet": {"title": title, "description": description, "categoryId": category},
        "status": {"privacyStatus": privacy},
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    print("🌙 Uploading video…")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    print(f"✅ Upload complete! Video ID: {response['id']}")
    return response["id"]

# ---------- Upload Thumbnail ----------
def upload_thumbnail(youtube, video_id, thumbnail_path):
    print("🌼 Uploading thumbnail…")
    validate_thumbnail(thumbnail_path)
    request = youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_path))
    response = request.execute()
    print("✅ Thumbnail uploaded successfully!")
    return response

# ---------- Main ----------
def main():
    parser = argparse.ArgumentParser(description="Upload a YouTube video with thumbnail and Shorts detection")
    parser.add_argument("--file", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--category", default="22")
    parser.add_argument("--privacy", choices=["private", "public", "unlisted"], default="private")
    parser.add_argument("--thumbnail", help="Path to thumbnail image (JPG/PNG, <2 MB)")

    args = parser.parse_args()
    youtube = get_authenticated_service()
    video_id = upload_video(youtube, args.file, args.title, args.description, args.category, args.privacy)

    if args.thumbnail:
        upload_thumbnail(youtube, video_id, args.thumbnail)

if __name__ == "__main__":
    main()
