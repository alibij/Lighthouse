import subprocess


def start_core (xray_exe_path = r'.\xray.exe'  ,config_file_path = r'.\config.json'):
    command = [xray_exe_path, '-c', config_file_path]
    try:
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {'pid': process.pid}

    except Exception as e:
        print(f"Error running xray.exe: {e}")


def stop_task (pid):

    try:
        command = ['taskkill', '/F', '/PID', str(pid)]
        subprocess.run(command, capture_output=True, text=True, check=True)
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while terminating process with PID {pid}: {e}")
        return False
    
    except Exception as e:
        print(f"Error occurred while terminating process with PID {pid}: {e}")
        return False


