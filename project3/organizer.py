import os
import shutil
from pathlib import Path

# Define extension mapping dictionary for automatic categorization
EXTENSION_MAP = {
    # Documents
    '.pdf': 'Documents', '.docx': 'Documents', '.doc': 'Documents',
    '.txt': 'Documents', '.xlsx': 'Documents', '.xls': 'Documents',
    '.pptx': 'Documents', '.csv': 'Documents',
    # Images
    '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
    '.gif': 'Images', '.bmp': 'Images', '.svg': 'Images',
    # Videos
    '.mp4': 'Videos', '.mkv': 'Videos', '.avi': 'Videos', '.mov': 'Videos', 
    # Archives
    '.zip': 'Archives', '.rar': 'Archives', '.tar': 'Archives', '.gz': 'Archives', # Compressed files
    # Code & Scripts
    '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code',
    '.cpp': 'Code', '.json': 'Code', '.sql': 'Code',
    # Audio
    '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio'
}

def get_unique_destination(dest_dir, filename):
    """
    Handles naming collisions by appending a counter suffix if a file 
    with the exact same name already exists in the destination folder.
    """
    dest_path = Path(dest_dir) / filename
    if not dest_path.exists():
        return dest_path
        
    base_name = dest_path.stem
    extension = dest_path.suffix
    counter = 1
    
    while True:
        new_filename = f"{base_name}_{counter}{extension}"
        new_dest_path = Path(dest_dir) / new_filename
        if not new_dest_path.exists():
            return new_dest_path
        counter += 1

def organize_directory(target_path):
    """Scans the target directory and organizes files into category subfolders."""
    source_dir = Path(target_path)
    
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"❌ Error: The path '{target_path}' is not a valid directory.")
        return

    print(f"\n📂 Scanning directory: {source_dir.resolve()}")
    
    moved_counts = {}
    total_files_moved = 0
    
    # Iterate through all items in the target directory
    try:
        with os.scandir(source_dir) as entries:
            for entry in entries:
                # Process only files (skip directories)
                if entry.is_file():
                    file_path = Path(entry.path)
                    
                    # Skip the script itself if it's in the same folder
                    if file_path.name == Path(__file__).name:
                        continue
                        
                    file_ext = file_path.suffix.lower()
                    
                    # Determine category folder name (default to 'Others' if unmapped)
                    category = EXTENSION_MAP.get(file_ext, 'Others')
                    
                    # Define destination folder path
                    dest_folder = source_dir / category
                    
                    # Create destination subfolder if it doesn't exist
                    os.makedirs(dest_folder, exist_ok=True)
                    
                    # Get safe destination path (resolves naming collisions)
                    dest_path = get_unique_destination(dest_folder, file_path.name)
                    
                    try:
                        # Safely move the file
                        shutil.move(str(file_path), str(dest_path))
                        print(f"✔ Moved: {file_path.name} ➔ {category}/{dest_path.name}")
                        
                        # Update tracking counts
                        moved_counts[category] = moved_counts.get(category, 0) + 1
                        total_files_moved += 1
                        
                    except PermissionError:
                        print(f"⚠️ Permission Denied: Could not move '{file_path.name}'. File may be in use.")
                    except Exception as e:
                        print(f"❌ Error moving '{file_path.name}': {e}")
                        
    except Exception as e:
        print(f"❌ Error scanning directory: {e}")

    # Print Formatted Execution Summary
    print("\n" + "=" * 50)
    print("             FILE ORGANIZATION SUMMARY              ")
    print("=" * 50)
    if total_files_moved > 0:
        for category, count in sorted(moved_counts.items()):
            print(f"• {category:<12}: {count} file(s) relocated")
        print("-" * 50)
        print(f"Total Files Relocated: {total_files_moved}")
    else:
        print("No files were moved. Directory was already clean or empty.")
    print("=" * 50)

if __name__ == "__main__":
    print("=" * 50)
    print("      AUTOMATED FILE ORGANIZER & CLEANUP UTILITY    ")
    print("=" * 50)
    
    # Prompt user for path or use current directory as default
    user_path = input("Enter path of the directory to organize (leave blank for current folder): ").strip()
    
    if not user_path:
        target_directory = "."
    else:
        target_directory = user_path.strip('"\'') # Strip wrapping quotes if path was pasted
        
    organize_directory(target_directory)