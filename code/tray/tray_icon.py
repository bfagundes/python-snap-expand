import pystray
from PIL import Image, ImageDraw
import tkinter
import threading
import queue
import sys, os

class TrayIcon:
    def __init__(self):
        self.icon = pystray.Icon("SnapExpand")
        self.icon.icon = self.create_image()
        self.icon.menu = pystray.Menu(
            pystray.MenuItem('Open', self.open_window),
            pystray.MenuItem('Quit', self.quit_app)
        )

        self.window = None
        self.running = True
        self.queue = queue.Queue()

    def create_image(self):
        image = Image.new('RGBA', (64, 64), (0,0,0,0))
        draw = ImageDraw.Draw(image)

        points = [(24,8), (32,8), (28,24), (36,24), (20,56), (24,32), (16,32)]
        draw.polygon(points, fill=(255, 215, 0))

        return image
    
    def open_window(self, icon=None, item=None):
        self.queue.put(self._open_window)

    def _open_window(self):
        if self.window is None or not self.window.winfo_exists():
            self.window = tkinter.Tk()
            self.window.title("SnapExpander")
            self.window.geometry("300x200")
            self.window.protocol("WM_DELETE_WINDOW", self.hide_window)

            label = tkinter.Label(self.window, text="SnapExpander")
            label.pack(expand=True)

            self.window.mainloop()
        else:
            try:
                self.window.deiconify()
            except:
                pass

    def hide_window(self):
        if self.window:
            self.window.withdraw()

    def quit_app(self, icon, item):
        self.running = False
        self.queue.put(self._quit_app)

    def _quit_app(self):
        try:
            if self.window:
                self.window.destroy()
        except:
            pass

        self.icon.stop()
        os._exit(0)

    def run(self):
        threading.Thread(target=self._process_queue, daemon=True).start()
        self.icon.run_detached()

    def _process_queue(self):
        while self.running:
            try:
                func = self.queue.get(timeout=1)
                func()
            except queue.Empty:
                pass

if __name__ == "__main__":
    tray_icon = TrayIcon()
    tray_icon.run()
