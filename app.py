from flask import Flask, request, render_template_string, send_file
from flask_socketio import SocketIO, emit
import requests
import os

app = Flask(__name__)
socketio = SocketIO(app)

platforms = [
    "https://github.com/",
    "https://twitter.com/",
    "https://www.instagram.com/",
    "https://www.reddit.com/user/",
    "https://www.facebook.com/",
    "https://www.linkedin.com/in/",
    "https://www.tiktok.com/@",
    "https://www.pinterest.com/",
    "https://www.tumblr.com/",
    "https://www.snapchat.com/add/",
    "https://www.youtube.com/",
    "https://www.twitch.tv/",
    "https://www.medium.com/@",
    "https://www.quora.com/profile/",
    "https://www.flickr.com/people/",
    "https://www.vk.com/",
    "https://www.ok.ru/profile/",
    "https://www.soundcloud.com/",
    "https://www.behance.net/",
    "https://www.dribbble.com/",
    "https://www.deviantart.com/",
    "https://www.goodreads.com/user/show/",
    "https://www.last.fm/user/",
    "https://www.mixcloud.com/",
    "https://www.myspace.com/",
    "https://www.newgrounds.com/",
    "https://www.periscope.tv/",
    "https://www.plurk.com/",
    "https://www.reverbnation.com/",
    "https://www.slideshare.net/",
    "https://www.soundclick.com/",
    "https://www.stumbleupon.com/stumbler/",
    "https://www.vimeo.com/",
    "https://www.weibo.com/",
    "https://www.xing.com/profile/",
    "https://www.yelp.com/user_details?userid="
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form['nickname']
        results = {}
        socketio.emit('log', {'data': f"Никнейм: {nickname}"})
        for platform in platforms:
            url = platform + nickname
            response = requests.get(url)
            if response.status_code == 200:
                results[platform] = url
                socketio.emit('log', {'data': f"Найдено: {url}"})
            else:
                results[platform] = 'Не найдено'
                socketio.emit('log', {'data': f"Не найдено: {url}"})

        filename = f"{nickname}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Результаты для {nickname}:\n")
            file.write(f"Всего платформ проверено: {len(platforms)}\n")
            for platform, result in results.items():
                if result != 'Не найдено':
                    file.write(f"{result}\n")
                else:
                    file.write(f"{platform}: Не найдено\n")

        socketio.emit('log', {'data': f"Результаты сохранены в файл: {filename}"})
        return send_file(filename, as_attachment=True)

    return render_template_string('''
        <form method="post">
            Никнейм: <input type="text" name="nickname">
            <input type="submit" value="Искать">
        </form>
        <div>
            <h3>Логи:</h3>
            <pre id="log"></pre>
        </div>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                background-color: #f2f2f2;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
                background-color: #fff;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
            }
            input[type="text"], input[type="submit"] {
                margin: 20px 0;
                padding: 20px;
                width: 100%;
                max-width: 400px;
                font-size: 18px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
            h3 {
                margin-top: 40px;
                text-align: center;
                font-size: 24px;
            }
            pre {
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
                width: 100%;
                max-width: 700px;
                overflow-x: auto;
                word-wrap: break-word;
                white-space: pre-wrap;
                font-size: 18px;
            }
            @media (max-width: 600px) {
                form, pre {
                    width: 90%;
                }
                h3 {
                    font-size: 20px;
                }
                input[type="text"], input[type="submit"] {
                    padding: 15px;
                    font-size: 16px;
                }
                pre {
                    font-size: 16px;
                }
            }
        </style>
        <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/3.0.3/socket.io.js"></script>
        <script type="text/javascript" charset="utf-8">
            var socket = io();
            socket.on('log', function(msg) {
                document.getElementById('log').innerText += msg.data + '\\n';
            });
        </script>
    ''')

if __name__ == '__main__':
    socketio.run(app, debug=True)