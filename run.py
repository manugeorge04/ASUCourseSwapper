import os
import subprocess
import time

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get classes_owned and classes_required from environment variables
classes_owned_env = os.getenv("CLASSES_OWNED")
classes_required_env = os.getenv("CLASSES_REQUIRED")

classes_owned = classes_owned_env.split(',')
classes_required = classes_required_env.split(',')

class_combinations = list(zip(classes_owned, classes_required))

restart_attempts = {combo: 0 for combo in class_combinations}


# Maximum number of restart attempts
max_restart_attempts = 3

def run_script(class1, class2):
    print(f"starting registration for --class1 {class1} --class2 {class2}")
    time.sleep(8)
    print(f"started registration for --class1 {class1} --class2 {class2}")
    command = f"python course_registration.py --class1 {class1} --class2 {class2}"
    process = subprocess.Popen(command, shell=True)
    return process

# Run each combination in a separate subprocess
processes = {combo: run_script(*combo) for combo in class_combinations}

# Wait for all processes to finish
while processes:
    for combo, process in list(processes.items()):
        return_code = process.poll()
        if return_code is not None:
            # Process has completed
            if return_code != 0:
                if restart_attempts[combo] < max_restart_attempts:
                    # Restart the process
                    print(f"Restarting {combo} after {restart_attempts[combo]} attempts.")
                    processes[combo] = run_script(*combo)
                    restart_attempts[combo] += 1
                else:
                    print(f"{combo} failed to restart after {max_restart_attempts} attempts.")
                    del processes[combo]
            else:
                # Process completed successfully
                del processes[combo]
    time.sleep(300)  # Sleep for a short interval before checking again
