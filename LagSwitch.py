import subprocess
import time
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_traffic():
    try:
        subprocess.run(['netsh', 'advfirewall','firewall', 'add', 'rule', 
                        'name=Test','dir=out', 'action=block', 
                        'protocol=any','enable=yes'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error blocking outbound traffic: {e}")

def unblock_traffic():
    try:
        subprocess.run(['netsh','advfirewall', 'firewall','delete', 'rule', 'name=Test'], check=True)
        print("Outbound traffic is unblocked.")
    except subprocess.CalledProcessError as e:
        print(f"Error unblocking outbound traffic: {e}")

def main():
    if not is_admin():
        print("This script must be run as administrator. Please restart with admin privileges.")
        return

    while True:
        wait_time = input("LagSwitch V2 Block Time (Seconds): ")
        # print(f"User input: {wait_time}")

        if not wait_time.isdigit():
            print("Invalid input! Please enter a valid number.")
            continue

        wait_time = int(wait_time)

        try:
            block_traffic()
            # print("Traffic blocked successfully")

            for remaining_time in range(wait_time, 0, -1):
                print(f"Blocking traffic for {remaining_time} seconds...", end='\r')
                time.sleep(1)

            unblock_traffic()
        except:
            # print("Attempting to unblock traffic")
            unblock_traffic()

if __name__ == "__main__":
    unblock_traffic()
    main()
