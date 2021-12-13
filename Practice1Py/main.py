import string
import win32file
from ctypes import windll
#
import os
#
import json
#
import xml.etree.ElementTree as ET
#
import zipfile

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


def exercise1():
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
        print("List of TXT files: ")
        for filename in self.files:
            print("\t", filename)

    def create_file(self):
        name = input("Enter filename: ")
        if not name.endswith(".txt"):
            name = name + ".txt"
        file = open(name, "w+")
        file.close()
        print(f"File {name} created.")

    def remove_file(self):
        name = input("Enter filename: ")
        os.remove(name)

    def write_to_file(self):
        name = input("Enter filename: ")
        file = open(name, "w+")
        file.write(input("Enter string to write: "))
        file.close()
        print("String written successfully.")

    def get_from_file(self):
        name = input("Enter filename: ")
        file = open(name, "r+")
        print("File contains: ", file.read())
        file.close()


def exercise2():
    fw = FileWorker()
    menu = "Menu:\n" \
           "1. Show files list\n" \
           "2. Create file\n" \
           "3. Remove file\n" \
           "4. Write data in file\n" \
           "5. Read data from file\n" \
           "0. Exit\n"
    while True:
        print(menu)
        file_option = input("Chose option: ")
        if file_option == "1":
            fw.get_files_list()
        elif file_option == "2":
            fw.create_file()
        elif file_option == "3":
            fw.remove_file()
        elif file_option == "4":
            fw.enter_to_file()
        elif file_option == "5":
            fw.get_from_file()
        elif file_option == "0":
            break


def exercise3():
    dump_data = {'Name': 'Kirill', 'Age': 22, 'DesiredMark': 9001, 'Etc.': ':)'}
    json_file = open('file.json', 'w+')
    json.dump(dump_data, json_file)
    json_file.close()
    json_file = open('file.json', 'r+')
    print(json_file.read())
    json_file.close()
    os.remove(json_file.name)


def exercise4():
    parent_node = ET.Element('parent')
    child_node1 = ET.SubElement(parent_node, 'child_first')
    tree = ET.ElementTree(parent_node)
    tree.write('file.xml')
    #
    tree = ET.parse('file.xml')
    root_node = tree.getroot()
    ET.SubElement(root_node[0], 'child_second')
    tree.write('file.xml')
    #
    ET.dump(tree)
    #
    os.remove('file.xml')


class ZipWorker:
    def __init__(self):
        self.zip = []

    def get_list_files(self):
        self.zip = []
        for file in os.listdir():
            if file.endswith(".zip"):
                self.zip.append(file)
        print("List of ZIP files: ")
        for archive_name in self.zip:
            print("\t", archive_name)

    def create_zip(self):
        zip_name = input("Enter filename: ")
        if not zip_name.endswith(".zip"):
            zip_name = zip_name + ".zip"
        filename = input("Enter filename which will be added to archive: ")
        zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        zip_file.write(filename)
        zip_file.close()
        print(f"Archive {zip_name} created.")

    def remove_file(self):
        name = input("Enter filename: ")
        os.remove(name)
        print("Archive deleted successfully.")

    def unpack_zip(self):
        zip_name = input("Enter filename: ")
        zip_file = zipfile.ZipFile(zip_name, 'r', zipfile.ZIP_DEFLATED)
        zip_file.extractall()
        print("Archive unzipped successfully. Here is unzipped files: ")
        zip_file.printdir()
        zip_file.close()


def exercise5():
    fw = ZipWorker()
    menu = "Menu:\n" \
           "1. Show list of archives\n" \
           "2. Create archive with file\n" \
           "3. Delete archive\n" \
           "4. Unzip archive\n" \
           "0. Exit\n"
    while True:
        print(menu)
        archive_option = input("Chose option: ")
        if archive_option == "1":
            fw.get_list_files()
        elif archive_option == "2":
            fw.create_zip()
        elif archive_option == "3":
            fw.remove_file()
        elif archive_option == "4":
            fw.unpack_zip()
        elif archive_option == "0":
            break


if __name__ == '__main__':
    while True:
        print("Exercises:")
        print("1. Exercise №1\n"
              "2. Exercise №2\n"
              "3. Exercise №3\n"
              "4. Exercise №4\n"
              "5. Exercise №5\n"
              "0. Exit\n")
        chosen_exercise = input("Chose exercise: ")
        if chosen_exercise == "1":
            exercise1()
        elif chosen_exercise == "2":
            exercise2()
        elif chosen_exercise == "3":
            exercise3()
        elif chosen_exercise == "4":
            exercise4()
        elif chosen_exercise == "5":
            exercise5()
        elif chosen_exercise == "0":
            break
