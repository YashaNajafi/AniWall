from flask import Flask, render_template, request, jsonify
import webview
import threading
import socket
from Functions import Functions
import os
import time

# ------------<App Config>-----------
app = Flask(__name__)

# ------------<Routes>-----------
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
        'GetMainCategory': Functions.GetMainCategory,
    }

    if selected:
        background_details = Functions.GetDataOfWallpaper("ByName", selected)
        if background_details:
            template_data['SelectedBackground'] = background_details
            template_data['wallpaper_exists'] = Functions.CheckWallpaperExist(selected)

    return render_template('index.html', **template_data)

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
def SetWallpaper():
    background_name = request.args.get('name', '')
    if not background_name:
        return jsonify({'success': False, 'error': 'No background name provided'})

    if not Functions.CheckWallpaperExist(background_name):
        return jsonify({'success': False, 'error': 'Wallpaper not downloaded yet'})

    try:
        backup_success = Functions.BackupOriginalWallpaper()
        if not backup_success:
            print("Warning: Failed to backup original wallpaper")

        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(current_file)
        videos_dir = os.path.join(base_dir, "Videos")
        wallpaper_path = os.path.join(videos_dir, f"{background_name}.mp4")

        success = Functions.SetAnimatedWallpaper(wallpaper_path)

        time.sleep(1)

        is_running = Functions.IsWallpaperRunning()

        if success and is_running:
            return jsonify({'success': True, 'is_active': True})
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to set wallpaper',
                'process_started': success,
                'process_running': is_running
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/disable-wallpaper')
def DisableWallpaper():
    try:
        success = Functions.DisableAnimatedWallpaper()

        is_running = Functions.IsWallpaperRunning()

        if success and not is_running:
            return jsonify({'success': True})
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to disable wallpaper',
                'wallpaper_restored': success,
                'process_still_running': is_running
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/wallpaper-status')
def WallpaperStatus():
    try:
        is_running = Functions.IsWallpaperRunning()
        return jsonify({'success': True, 'is_active': is_running})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ------------<Get Free Random Port>-----------
def GetPort():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# ------------<App Management And Run>-----------
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
