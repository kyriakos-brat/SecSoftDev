# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import string
import win32file
from ctypes import windll

import os


def get_logical_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drive_name = letter + ':\\'
            drives.append(drive_name)
        bitmask >>= 1
    return drives


def get_drive_info(drive_name):
    drives_map = {win32file.DRIVE_UNKNOWN: 'Unknown',
                  win32file.DRIVE_NO_ROOT_DIR: 'No Root Directory',
                  win32file.DRIVE_REMOVABLE: 'Removable Drive',
                  win32file.DRIVE_FIXED: 'Local Drive',
                  win32file.DRIVE_REMOTE: 'Network Drive',
                  win32file.DRIVE_CDROM: 'CDROM',
                  win32file.DRIVE_RAMDISK: 'RAM Drive'}

    drive_type = drives_map[win32file.GetDriveType(drive_name)]
    #
    sec_per_clust, bytes_per_sec, num_free_clust, num_total_clust = win32file.GetDiskFreeSpace(drive_name)
    bytes_per_clust = sec_per_clust * bytes_per_sec
    volume = num_total_clust * bytes_per_clust
    occupied = (num_total_clust - num_free_clust) * bytes_per_clust
    free = num_free_clust * bytes_per_clust
    storage_info = (volume, occupied, free)
    #
    return drive_type, storage_info


def task1():
    drives_list = get_logical_drives()
    print("List of drives:")
    for i, drive in enumerate(drives_list):
        print(i, ". ", drive)
    disk_num = int(input("\nChoose disk to get info: "))
    if (disk_num < 0) or (disk_num >= len(drives_list)):
        print("Number of disk is inappropriate!")
        return
    drive_type, storage_info = get_drive_info(drives_list[disk_num])
    print("Drive type: ", drive_type)
    print(f"Storage volume: {storage_info[0] // (1024*1024)}MB")
    print(f"Storage occupied: {storage_info[1] // (1024*1024)}MB")
    print(f"Storage free: {storage_info[2] // (1024*1024)}MB")


class FileWorker:
    def __init__(self):
        self.files = []

    def get_files_list(self):
        self.files = []
        for file in os.listdir():
            if file.endswith(".txt"):
                self.files.append(file)
        print("List of files: ")
        for n in self.files:
            print("\t", n)

    def create_file(self):
        name = input("Enter filename: ")
        my_file = open(name, "w+")
        my_file.close()
        print(f"File {name} created.")

    def remove_file(self):
        name = input("Enter filename: ")
        os.remove(name)

    def write_to_file(self):
        name = input("Enter filename: ")
        my_file = open(name, "w+")
        my_file.write(input("Enter string to write: "))
        my_file.close()
        print("String written successfully.")

    def get_from_file(self):
        name = input("Enter filename: ")
        my_file = open(name, "r+")
        print("File contains: ", my_file.read())
        my_file.close()


def task2():
    fw = FileWorker()
    menu = "\nMenu:\n   1. Show files list\n   2. Create file\n   3. Remove file\n   4. Write data in file\n   5. Read data from file\n   0. Exit\n\n"
    while True:
        print(menu)
        c = input("Chose option: ")
        if c == "1":
            fw.get_list_files()
        elif c == "2":
            fw.create_file()
        elif c == "3":
            fw.remove_file()
        elif c == "4":
            fw.enter_to_file()
        elif c == "5":
            fw.get_from_file()
        elif c == "0":
            break


if __name__ == '__main__':
    task1()
