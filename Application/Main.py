#------------<Libs>-----------
import threading
import socket
from flask import Flask, render_template, request
import webview
from Functions import Functions, Wallpaper

#------------<App Config>-----------
app = Flask(__name__)

#------------<Routes>-----------
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
        'GetMainCategory': Functions.GetMainCategory  # Pass the function to the template
    }

    if selected:
        background_details = Functions.GetDataOfWallpaper("ByName", selected)
        if background_details:
            template_data['SelectedBackground'] = background_details

    return render_template('index.html', **template_data)

#------------<Get Free Random Port>-----------
def GetPort():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

#------------<App Management And Run>-----------
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
  
