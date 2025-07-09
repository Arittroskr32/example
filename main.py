import subprocess
import os
import threading

# Define all sub-app folders and their ports
apps = {
    'flask_cookie': 4001,
    'intuder': 4002,
    'jwt_bruteforce': 4003,
    'jwt_decode': 4004,
    'request_manupulate': 4005,
    'sequencer': 4006
}

def stream_output(process, name):
    def _stream(pipe):
        for line in iter(pipe.readline, ''):
            if line:
                print(f"[{name}] {line.strip()}")
    threading.Thread(target=_stream, args=(process.stdout,), daemon=True).start()
    threading.Thread(target=_stream, args=(process.stderr,), daemon=True).start()

processes = []

for folder, port in apps.items():
    app_path = os.path.join(folder, "app.py")
    print(f"Launching {folder} on port {port}...")

    # Start each Flask app with live output
    p = subprocess.Popen(
        ["python", app_path, str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stream_output(p, folder)
    processes.append(p)

# Wait for all processes to exit (CTRL+C to kill)
try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("\nStopping all apps...")
    for p in processes:
        p.terminate()
