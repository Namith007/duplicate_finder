import os
import hashlib
from collections import defaultdict

def get_file_hash(filepath, chunk_size=8192):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(root_folder):
    hashes = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_hash = get_file_hash(filepath)
                hashes[file_hash].append(filepath)
            except (PermissionError, FileNotFoundError):
                continue

    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

def report_duplicates(duplicates):
    if not duplicates:
        print("No duplicate files found.")
        return

    total_wasted = 0
    for i, (file_hash, paths) in enumerate(duplicates.items(), 1):
        print(f"\nDuplicate set {i}:")
        for p in paths:
            print(f"  {p}")
        wasted = os.path.getsize(paths[0]) * (len(paths) - 1)
        total_wasted += wasted

    print(f"\nTotal wasted space: {total_wasted / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    folder = input("Enter folder path to scan: ")
    dupes = find_duplicates(folder)
    report_duplicates(dupes)