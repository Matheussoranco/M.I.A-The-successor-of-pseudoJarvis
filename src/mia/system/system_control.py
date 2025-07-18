"""
System Control: Cross-platform system actions (file, process, clipboard, etc.)
"""
import os
import platform
import shutil
import subprocess
import pyperclip
from ..utils.optional_deps import safe_import

# Optional dependency handling
psutil = safe_import('psutil', 'system process management')

class SystemControl:
    @staticmethod
    def open_file(path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])

    @staticmethod
    def list_files(directory):
        return os.listdir(directory)

    @staticmethod
    def copy_file(src, dst):
        shutil.copy2(src, dst)

    @staticmethod
    def move_file(src, dst):
        shutil.move(src, dst)

    @staticmethod
    def delete_file(path):
        os.remove(path)

    @staticmethod
    def run_command(cmd):
        return subprocess.getoutput(cmd)

    @staticmethod
    def get_clipboard():
        return pyperclip.paste()

    @staticmethod
    def set_clipboard(text):
        pyperclip.copy(text)

    @staticmethod
    def list_processes():
        """List running processes. Returns empty list if psutil not available."""
        if psutil is None:
            return []
        try:
            return [(p.pid, p.name()) for p in psutil.process_iter()]
        except Exception:
            return []

    @staticmethod
    def kill_process(pid):
        """Kill a process by PID. Does nothing if psutil not available."""
        if psutil is None:
            raise RuntimeError("psutil not available - cannot manage processes")
        try:
            p = psutil.Process(pid)
            p.terminate()
        except Exception as e:
            raise RuntimeError(f"Failed to kill process {pid}: {e}")

    # Add more system actions as needed (clipboard, process, etc.)
