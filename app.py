from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# ডাউনলোড ফোল্ডার
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    base_url = request.host_url
    if request.method == "POST":
        url = request.form.get("url")
        try:
            # সরাসরি ডাউনলোড শুরু
            ydl_opts = {
                'format': 'bv*+ba/best',  # ভিডিও + অডিও (সর্বোচ্চ মানে)
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'postprocessors': [],  # কোনো রূপান্তর নয়
                'merge_output_format': 'mp4'  # ffmpeg না থাকলেও MP4 হবে
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            return send_file(filename, as_attachment=True)
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template("index.html", message=message, base_url=base_url)

if __name__ == "__main__":
    app.run(debug=True)
