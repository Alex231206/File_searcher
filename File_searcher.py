import os, shutil, zipfile
import datetime
from pprint import pprint

annotation: str = open('annotation.txt', 'r', encoding = 'utf-8').read()

while True:
    print(annotation)

    users_choice: str = input('Enter your choice (0 or 1): ')

    if users_choice == '0':
        print('The program was ended\nSee you soon!')
        break

    if users_choice == '1':
        abs_path: str = input('Enter the absolute path to the directory for searching: ')

        try:
            os.chdir(abs_path)

        except FileNotFoundError:
            print('The path you entered is incorrect')
            continue

        else:
            files_extensions: str = input('Enter the extensions of files you want to receive (separated by a space): ')

            files_extensions_list: list = files_extensions.split()

            result_location: str = input('Enter the location of the future results of the program (absolute path): ')


            if os.path.isabs(result_location):
                files_dict: dict = {}
                all_files_list: list = []

                date = datetime.datetime.today()

                try:
                    os.makedirs(f'{result_location}\\result_{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}')

                except FileExistsError:
                    print('The directory for saving results already exists. Delete it or rename it\n')
                    continue

                else:
                    for extension in files_extensions_list:
                        files_dict[extension] = []
                        os.chdir(f'{result_location}\\result_{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}')
                        os.makedirs(f'{result_location}\\result_{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}\\{extension}')

                    for folder_name, subfolders, filenames in os.walk(abs_path):
                        for file in filenames:
                            for extension in files_extensions_list:
                                if file.endswith(extension):

                                    each_file_dict: dict = {
                                        'Filename': '',
                                        'Location': '',
                                        'Size(bytes)': ''
                                    }

                                    file_location = f'{folder_name}\\{file}'
                                    file_size = os.path.getsize(file_location)

                                    each_file_dict['Filename'] = file
                                    each_file_dict['Location'] = file_location
                                    each_file_dict['Size(bytes)'] = file_size

                                    files_dict[extension] += [each_file_dict]

                                    if file not in all_files_list:
                                        all_files_list.append(file)
                                        files_dict[extension] += [each_file_dict]
                                        shutil.copy(f'{folder_name}\\{file}', f'{result_location}\\result_{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}\\{extension}')



                    os.chdir(f'{result_location}\\result_{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}')

                    result = open(f'result.txt', 'w')

                    result.write(f'Date: {date}\n')

                    try:
                        pprint(files_dict, stream = result)

                    except UnicodeEncodeError:
                        result.write("There's a problem with encoding suddenly occured\n")

                    else:
                        print('The program has successfully finished working\n')

                    finally:
                        result.close()

            else:
                print("The folder you entered didn't exist\n")
                continue
