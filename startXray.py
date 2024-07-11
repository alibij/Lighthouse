import subprocess
import platform
import os

def start_core(xray_path='./xray', config_file_path='./config.json'):
    # Adjust the executable name based on the OS
    system = platform.system()
    if system == 'Windows':
        xray_path = xray_path + '.exe'
        
    command = [xray_path, '-c', config_file_path]
    try:
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {'pid': process.pid}
        
    except Exception as e:
        print(f"Error running {xray_path}: {e}")


def stop_task (pid):

    try:
        system = platform.system()

        if system == 'Windows':
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


