import psutil
import subprocess
import platform
import time


def start_core(xray_path='./xray', config_file_path='./config.json'):
    system = platform.system()
    if system == 'Windows':
        xray_path = xray_path + '.exe'

    command = [xray_path, '-c', config_file_path]
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(1)

        if process.poll() is None:
            return {'pid': process.pid}
        else:
            return None

    except Exception as e:
        print(f"Error running {xray_path}: {e}")
        return None


def stop_task(pid):
    try:
        system = platform.system()

        if system == 'Windows':
            if not psutil.pid_exists(pid):
                return False

            command = ['taskkill', '/F', '/PID', str(pid)]
        else:
            command = ['kill', '-9', str(pid)]

        subprocess.run(command, capture_output=True, text=True, check=True)
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while terminating process with PID {pid}: {e}")
        return False

    except Exception as e:
        print(f"Error occurred while terminating process with PID {pid}: {e}")
        return False


def find_xray_pid():

    procname = 'xray.exe' if platform.system() == 'Windows' else 'xray'
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == procname:
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


def chek_task(pid: int):
    return psutil.pid_exists(pid)
