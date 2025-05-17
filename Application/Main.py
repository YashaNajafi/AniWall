<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> c6a8d8e (Initial commit)
#------------<Libs>-----------
import threading
import socket
from flask import Flask, render_template, request
import webview
from Functions import Functions, Wallpaper

#------------<App Config>-----------
app = Flask(__name__)

#------------<Routes>-----------
<<<<<<< HEAD
=======
=======
# from flask import Flask, render_template, request, jsonify
# import webview
# import threading
# import socket
# from Functions import Functions
# import os
# from Functions.Wallpaper import VideoWallpaper
# # ------------<App Config>-----------
# app = Flask(__name__)

# # Global variable to track if wallpaper is active
# wallpaper_active = False

# # ------------<Routes>-----------
# @app.route('/')
# def index():
#     category = request.args.get('category', 'All')
#     search = request.args.get('search', '')
#     selected = request.args.get('selected', None)

#     backgrounds = Functions.GetMainData()["Backgrounds"]

#     if category != 'All':
#         if category == 'Popular':
#             backgrounds = [bg for bg in backgrounds if bg["Popular"]]
#         else:
#             backgrounds = [bg for bg in backgrounds if Functions.GetMainCategory(bg["Categories"]) == category]

#     if search:
#         backgrounds = [bg for bg in backgrounds if search.lower() in bg["Name"].lower()]

#     template_data = {
#         'BackgroundsListData': backgrounds,
#         'current_category': category,
#         'GetMainCategory': Functions.GetMainCategory,  # Pass the function to the template
#         'wallpaper_active': wallpaper_active  # Pass whether wallpaper is active to template
#     }

#     if selected:
#         background_details = Functions.GetDataOfWallpaper("ByName", selected)
#         if background_details:
#             template_data['SelectedBackground'] = background_details
#             # Check if wallpaper exists and pass this info to template
#             template_data['wallpaper_exists'] = Functions.CheckWallpaperExist(selected)

#     return render_template('index.html', **template_data)

# # Global dictionary to track download progress for each wallpaper
# download_progress = {}

# @app.route('/download-wallpaper')
# def DownloadWallpaper():
#     background_name = request.args.get('name', '')
#     if not background_name:
#         return jsonify({'success': False, 'error': 'No background name provided'})

#     try:
#         if Functions.CheckWallpaperExist(background_name):
#             return jsonify({'success': True, 'status': 'already_downloaded'})

#         # Reset progress tracking for this wallpaper
#         download_progress[background_name] = {
#             'progress': 0,
#             'total_size': 0,
#             'current_size': 0,
#             'is_complete': False,
#             'error': None
#         }

#         # Start download in a separate thread to not block the response
#         threading.Thread(
#             target=Functions.DownloadBackground,
#             args=(background_name, download_progress)
#         ).start()

#         return jsonify({'success': True})
#     except Exception as e:
#         if background_name in download_progress:
#             download_progress[background_name]['error'] = str(e)
#         return jsonify({'success': False, 'error': str(e)})

# @app.route('/download-progress')
# def DownloadProgress():
#     background_name = request.args.get('name', '')
#     if not background_name:
#         return jsonify({'success': False, 'error': 'No background name provided'})

#     try:
#         # If we're tracking this download, return its progress
#         if background_name in download_progress:
#             progress_data = download_progress[background_name]

#             # Check if download completed or had an error
#             if progress_data['is_complete']:
#                 return jsonify({
#                     'success': True,
#                     'progress': 100,
#                     'status': 'completed'
#                 })
#             elif progress_data['error']:
#                 return jsonify({
#                     'success': False,
#                     'error': progress_data['error']
#                 })

#             # Calculate progress percentage - use exact calculation
#             if progress_data['total_size'] > 0:
#                 # Get precise progress value with 2 decimal places
#                 progress = (progress_data['current_size'] / progress_data['total_size']) * 100
#                 return jsonify({
#                     'success': True,
#                     'progress': progress,
#                     'current_size': progress_data['current_size'],
#                     'total_size': progress_data['total_size']
#                 })
#             else:
#                 # We don't have total size yet
#                 return jsonify({'success': True, 'progress': 1})

#         # If we're not tracking progress but file exists, it's already completed
#         if Functions.CheckWallpaperExist(background_name):
#             return jsonify({'success': True, 'progress': 100, 'status': 'completed'})

#         # Check if file is partially downloaded but we're not tracking it
#         full_name = f"{background_name}.mp4"
#         current_file = os.path.abspath(__file__)
#         base_dir = os.path.dirname(current_file)
#         videos_dir = os.path.join(base_dir, "Videos")
#         file_path = os.path.join(videos_dir, full_name)

#         if os.path.exists(file_path):
#             # Get current file size
#             current_size = os.path.getsize(file_path)

#             # Get total file size from background data
#             backgrounds_data = Functions.GetMainData()
#             backgrounds = backgrounds_data.get("Backgrounds", [])
#             background_info = next((bg for bg in backgrounds if bg["Name"] == background_name), None)

#             if background_info and "FileSize" in background_info:
#                 total_size = background_info["FileSize"]
#                 progress = (current_size / total_size) * 100
#                 return jsonify({'success': True, 'progress': progress})

#         # Default - not started or unknown status
#         return jsonify({'success': True, 'progress': 0})

#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# @app.route('/set-wallpaper')
# def set_wallpaper():
#     global wallpaper_active
#     background_name = request.args.get('name', '')
#     if not background_name:
#         return jsonify({'success': False, 'error': 'No background name provided'})

#     # Check if wallpaper exists before attempting to set it
#     if not Functions.CheckWallpaperExist(background_name):
#         return jsonify({'success': False, 'error': 'Wallpaper not downloaded yet'})

#     try:
#         # First backup the original wallpaper
#         Functions.BackupOriginalWallpaper()

#         # Get the full path to the wallpaper file
#         current_file = os.path.abspath(__file__)
#         base_dir = os.path.dirname(current_file)
#         videos_dir = os.path.join(base_dir, "Videos")
#         wallpaper_path = os.path.join(videos_dir, f"{background_name}.mp4")

#         # Start the wallpaper process in a separate thread
#         def run_wallpaper():
#             import sys
#             from PyQt5.QtWidgets import QApplication

#             app = QApplication(sys.argv)
#             wallpaper = VideoWallpaper(wallpaper_path)
#             app.exec_()

#         # Run in a separate thread to not block the server
#         wallpaper_thread = threading.Thread(target=run_wallpaper)
#         wallpaper_thread.daemon = True  # Allow the thread to be terminated when the main program exits
#         wallpaper_thread.start()

#         # Set the wallpaper_active flag to true
#         wallpaper_active = True

#         return jsonify({'success': True})
#     except ImportError as e:
#         return jsonify({'success': False, 'error': f"Missing required modules: {str(e)}"})
#     except FileNotFoundError as e:
#         return jsonify({'success': False, 'error': f"File not found: {str(e)}"})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# @app.route('/disable-wallpaper')
# def disable_wallpaper():
#     global wallpaper_active

#     try:
#         # Call the function to disable the animated wallpaper
#         success = Functions.DisableAnimatedWallpaper()

#         if success:
#             wallpaper_active = False
#             return jsonify({'success': True})
#         else:
#             return jsonify({'success': False, 'error': 'Failed to disable wallpaper'})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# @app.route('/wallpaper-status')
# def wallpaper_status():
#     # Check if wallpaper is running
#     try:
#         is_running = Functions.IsWallpaperRunning()
#         return jsonify({'success': True, 'is_active': is_running})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# # ------------<Get Free Random Port>-----------
# def GetPort():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(('', 0))
#         return s.getsockname()[1]

# # ------------<App Management And Run>-----------
# def RunFlask(port):
#     app.run(port=port, debug=True, use_reloader=False)

# if __name__ == '__main__':
#     port = GetPort()
#     flask_thread = threading.Thread(target=RunFlask, args=(port,))
#     flask_thread.daemon = True
#     flask_thread.start()

#     window = webview.create_window('AniWall', f'http://127.0.0.1:{port}', confirm_close=True, frameless=False, resizable=False)

#     def on_loaded():
#         def lock_maximize():
#             window.maximize()
#             window.resizable = False
#         window.events.shown += lock_maximize

#     webview.start(on_loaded)
from flask import Flask, render_template, request, jsonify
import webview
import threading
import socket
from Functions import Functions
import os

# ------------<App Config>-----------
app = Flask(__name__)

# ------------<Routes>-----------
>>>>>>> f0ac188 (Initial commit)
>>>>>>> c6a8d8e (Initial commit)
@app.route('/')
def index():
    category = request.args.get('category', 'All')
    search = request.args.get('search', '')
    selected = request.args.get('selected', None)

    backgrounds = Functions.GetMainData()["Backgrounds"]

    if category != 'All':
        if category == 'Popular':
            backgrounds = [bg for bg in backgrounds if bg["Popular"]]
        else:
            backgrounds = [bg for bg in backgrounds if Functions.GetMainCategory(bg["Categories"]) == category]

    if search:
        backgrounds = [bg for bg in backgrounds if search.lower() in bg["Name"].lower()]

    template_data = {
        'BackgroundsListData': backgrounds,
        'current_category': category,
<<<<<<< HEAD
        'GetMainCategory': Functions.GetMainCategory  # Pass the function to the template
=======
<<<<<<< HEAD
        'GetMainCategory': Functions.GetMainCategory  # Pass the function to the template
=======
        'GetMainCategory': Functions.GetMainCategory,
>>>>>>> f0ac188 (Initial commit)
>>>>>>> c6a8d8e (Initial commit)
    }

    if selected:
        background_details = Functions.GetDataOfWallpaper("ByName", selected)
        if background_details:
            template_data['SelectedBackground'] = background_details
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> c6a8d8e (Initial commit)

    return render_template('index.html', **template_data)

#------------<Get Free Random Port>-----------
<<<<<<< HEAD
=======
=======
            template_data['wallpaper_exists'] = Functions.CheckWallpaperExist(selected)

    return render_template('index.html', **template_data)

# Global dictionary to track download progress for each wallpaper
download_progress = {}

@app.route('/download-wallpaper')
def DownloadWallpaper():
    background_name = request.args.get('name', '')
    if not background_name:
        return jsonify({'success': False, 'error': 'No background name provided'})

    try:
        if Functions.CheckWallpaperExist(background_name):
            return jsonify({'success': True, 'status': 'already_downloaded'})

        download_progress[background_name] = {
            'progress': 0,
            'total_size': 0,
            'current_size': 0,
            'is_complete': False,
            'error': None
        }

        threading.Thread(
            target=Functions.DownloadBackground,
            args=(background_name, download_progress)
        ).start()

        return jsonify({'success': True})
    except Exception as e:
        if background_name in download_progress:
            download_progress[background_name]['error'] = str(e)
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download-progress')
def DownloadProgress():
    background_name = request.args.get('name', '')
    if not background_name:
        return jsonify({'success': False, 'error': 'No background name provided'})

    try:
        if background_name in download_progress:
            progress_data = download_progress[background_name]

            if progress_data['is_complete']:
                return jsonify({
                    'success': True,
                    'progress': 100,
                    'status': 'completed'
                })
            elif progress_data['error']:
                return jsonify({
                    'success': False,
                    'error': progress_data['error']
                })

            if progress_data['total_size'] > 0:
                progress = (progress_data['current_size'] / progress_data['total_size']) * 100
                return jsonify({
                    'success': True,
                    'progress': progress,
                    'current_size': progress_data['current_size'],
                    'total_size': progress_data['total_size']
                })
            else:
                return jsonify({'success': True, 'progress': 1})

        if Functions.CheckWallpaperExist(background_name):
            return jsonify({'success': True, 'progress': 100, 'status': 'completed'})

        full_name = f"{background_name}.mp4"
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(current_file)
        videos_dir = os.path.join(base_dir, "Videos")
        file_path = os.path.join(videos_dir, full_name)

        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            backgrounds_data = Functions.GetMainData()
            backgrounds = backgrounds_data.get("Backgrounds", [])
            background_info = next((bg for bg in backgrounds if bg["Name"] == background_name), None)

            if background_info and "FileSize" in background_info:
                total_size = background_info["FileSize"]
                progress = (current_size / total_size) * 100
                return jsonify({'success': True, 'progress': progress})

        return jsonify({'success': True, 'progress': 0})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/set-wallpaper')
def set_wallpaper():
    background_name = request.args.get('name', '')
    if not background_name:
        return jsonify({'success': False, 'error': 'No background name provided'})

    if not Functions.CheckWallpaperExist(background_name):
        return jsonify({'success': False, 'error': 'Wallpaper not downloaded yet'})

    try:
        Functions.BackupOriginalWallpaper()
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(current_file)
        videos_dir = os.path.join(base_dir, "Videos")
        wallpaper_path = os.path.join(videos_dir, f"{background_name}.mp4")

        success = Functions.SetAnimatedWallpaper(wallpaper_path)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to set wallpaper'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/disable-wallpaper')
def disable_wallpaper():
    try:
        success = Functions.DisableAnimatedWallpaper()
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to disable wallpaper'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/wallpaper-status')
def wallpaper_status():
    try:
        is_running = Functions.IsWallpaperRunning()
        return jsonify({'success': True, 'is_active': is_running})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ------------<Get Free Random Port>-----------
>>>>>>> f0ac188 (Initial commit)
>>>>>>> c6a8d8e (Initial commit)
def GetPort():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

<<<<<<< HEAD
#------------<App Management And Run>-----------
=======
<<<<<<< HEAD
#------------<App Management And Run>-----------
=======
# ------------<App Management And Run>-----------
>>>>>>> f0ac188 (Initial commit)
>>>>>>> c6a8d8e (Initial commit)
def RunFlask(port):
    app.run(port=port, debug=True, use_reloader=False)

if __name__ == '__main__':
    port = GetPort()
    flask_thread = threading.Thread(target=RunFlask, args=(port,))
    flask_thread.daemon = True
    flask_thread.start()

    window = webview.create_window('AniWall', f'http://127.0.0.1:{port}', confirm_close=True, frameless=False, resizable=False)

    def on_loaded():
        def lock_maximize():
            window.maximize()
            window.resizable = False
        window.events.shown += lock_maximize

    webview.start(on_loaded)
<<<<<<< HEAD
  
=======
<<<<<<< HEAD
  
=======
>>>>>>> f0ac188 (Initial commit)
>>>>>>> c6a8d8e (Initial commit)
