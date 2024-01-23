import os
import shutil
import argparse
import psutil
import subprocess
from datetime import datetime

def is_unleash_running():
    '''Check if Unleash is running.'''
    for process in psutil.process_iter():
        try:
            if 'UnleashRGB' in process.name().lower():
                return process
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def backup_folders_with_long_names(source_dir, backup_dir):
    '''Iterate through the folders in the source directory 
    and back up the ones with names > 20 characters long'''

    for folder in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder)
        
        # Check if it's a directory and has a long name (indicative of the profile folders)
        if os.path.isdir(folder_path) and len(folder) > 20:
            # Create a timestamped backup folder name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_folder_name = f'{folder}_{timestamp}'
            backup_folder_path = os.path.join(backup_dir, backup_folder_name)
            
            # Copy the folder to the backup directory
            shutil.copytree(folder_path, backup_folder_path)
            print(f'Backed up {folder} to {backup_folder_path}')

def backup_evga_profiles(backup_dir):
    # Define the source directory
    source_dir = os.path.join(os.getenv('APPDATA'), 'EVGA', 'Unleash RGB', 'ProfileManager')
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f'Source directory {source_dir} does not exist.')
        return

    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Iterate through the folders in the source directory
    backup_folders_with_long_names(source_dir, backup_dir)

def delete_new_profile_subdir(long_named_folder_path):
    '''Delete the new profile sub-folder (e.g., 001).'''

    for folder in os.listdir(long_named_folder_path):
        folder_path = os.path.join(long_named_folder_path, folder)
        if os.path.isdir(folder_path) and folder.isdigit():
            shutil.rmtree(folder_path)

def copy_backed_up_folders(backup_dir, long_named_folder_path):
    '''Copy the backed-up profile folders into the new custom profile folder.'''
    
    # Get the most recent backup folder
    most_recent_backup = get_most_recent_backup(backup_dir)
    source_backup_path = os.path.join(backup_dir, most_recent_backup)

    for folder in os.listdir(source_backup_path):
        source_folder_path = os.path.join(source_backup_path, folder)
        target_folder_path = os.path.join(long_named_folder_path, folder)
        if os.path.isdir(source_folder_path) and folder.isdigit():
            shutil.copytree(source_folder_path, target_folder_path)

def get_most_recent_backup(backup_dir):
    '''Get the most recent backup folder based on the timestamp.'''
    backups = [folder for folder in os.listdir(backup_dir) 
               if len(folder) > 20 and os.path.isdir(os.path.join(backup_dir, folder))]
    return max(backups, key=lambda folder: folder.split('_')[1])

def restore_evga_profiles(backup_dir, unleash_path):
    # Prompt the user to create a new custom profile in Unleash
    input('Please create a new custom profile in Unleash and click \'Apply\'.\n' + 
          'Once done, return to this window and press \'Enter\' to continue...')
    
    # Check if Unleash is running and close it
    unleash_process = is_unleash_running()
    if unleash_process:
        print('Closing Unleash...')
        unleash_process.terminate()
        unleash_process.wait()

    # Define the target directory
    target_dir = os.path.join(os.getenv('APPDATA'), 'EVGA', 'Unleash RGB', 'ProfileManager')
     
    # Check if target directory exists
    if not os.path.exists(target_dir):
        print(f'Target directory {target_dir} does not exist.')
        return

    # Identify the long-named folder
    long_named_folders = [folder for folder in os.listdir(target_dir) if len(folder) > 20]
    if not long_named_folders:
        print('No long-named folder found. Please ensure you\'ve created a custom color profile in Unleash.')
        return

    long_named_folder = long_named_folders[0]
    long_named_folder_path = os.path.join(target_dir, long_named_folder)

    delete_new_profile_subdir(long_named_folder_path)
    copy_backed_up_folders(backup_dir, long_named_folder_path)

    print('Restoration completed. You must now select a different profile in order for the changes to take effect.\n' + 
          'Restarting Unleash...')
    
    subprocess.Popen([unleash_path])

def find_unleash_executable():
    '''Search for UnleashRGB.exe in common installation paths.'''
    common_paths = [
        r'C:\Program Files (x86)\EVGA\Unleash RGB\UnleashRGB.exe',
        r'C:\Program Files\EVGA\Unleash RGB\UnleashRGB.exe'
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None

def get_unleash_path(user_provided_path):
    '''Validate the UnleashRGB.exe path and ask user if not found.'''
    if os.path.exists(user_provided_path):
        return user_provided_path

    print(f"UnleashRGB.exe not found at {user_provided_path}. Searching common installation paths...")
    found_path = find_unleash_executable()
    if found_path:
        print(f"UnleashRGB.exe found at {found_path}")
        return found_path

    while True:
        user_input = input("Search unsuccessful. Please enter the correct path to UnleashRGB.exe: ")
        if os.path.exists(user_input):
            print(f"UnleashRGB.exe found at {user_input}")
            return user_input
        print("Invalid path. UnleashRGB.exe not found.")

def main():
    parser = argparse.ArgumentParser(description='Backup and Restore EVGA Z20/Z15 keyboards\' custom key color layers.')
    parser.add_argument('-d', '--directory', default=os.path.dirname(os.path.abspath(__file__)), help='Path to the backup directory. Default is the script directory.')
    parser.add_argument('-r', '--restore', action='store_true', help='Restore profiles from the backup directory.')
    parser.add_argument('-p', '--path', default=r'C:\Program Files (x86)\EVGA\Unleash RGB\UnleashRGB.exe', help='Path to the UnleashRGB.exe executable. Default is \'C:\\Program Files (x86)\\EVGA\\Unleash RGB\\UnleashRGB.exe\'.')
    args = parser.parse_args()

    unleash_path = get_unleash_path(args.path)

    if args.restore:
        restore_evga_profiles(args.directory, unleash_path)
    else:
        backup_evga_profiles(args.directory)

if __name__ == '__main__':
    main()