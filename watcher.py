import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} has been modified. Restarting server...')
            self.process.kill()
            time.sleep(1)  # Чекаємо перед перезапуском
            self.process = subprocess.Popen(['python', 'app.py'])


if __name__ == "__main__":
    # Запускаємо сервер Flask спочатку
    process = subprocess.Popen(['python', 'app.py'])

    # Створюємо спостерігач для змін у файлах
    event_handler = ChangeHandler(process)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()