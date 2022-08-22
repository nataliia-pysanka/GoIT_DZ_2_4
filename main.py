"""
Скрипт принимает один аргумент при запуске — это имя папки, в которой он будет
проводить сортировку. Допустим файл с программой называется sort.py, тогда,
чтобы отсортировать папку /user/Desktop/Хлам, надо запустить скрипт командой
python sort.py /user/Desktop/Хлам
"""
import sys
from shutil import unpack_archive
from pathlib import Path
import parsing as parser
from normalization import normalize
from log import logger
from datetime import datetime
from threading import Thread, Semaphore


def handle_files(semaphore: Semaphore, file_name: Path, target_folder: Path):
    with semaphore:
        target_folder.mkdir(exist_ok=True, parents=True)
        normalized_name = normalize(normalize(file_name.stem)) + file_name.suffix
        logger.info(f'...replacing {file_name.name}')
        file_name.replace(target_folder / normalized_name)


def handle_archives(semaphore: Semaphore, file_name: Path,
                    target_folder: Path):
    with semaphore:
        target_folder.mkdir(exist_ok=True, parents=True)
        name = normalize(file_name.stem)
        normalized_name = name + file_name.suffix
        full_name = target_folder / normalized_name
        file_name.replace(full_name)
        target_folder.mkdir(exist_ok=True, parents=True)
        new_dir = target_folder / name
        new_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f'...unpacking archive {file_name.name}')
        unpack_archive(full_name, new_dir)


def handle_folder(semaphore: Semaphore, file_name: Path):
    with semaphore:
        logger.info(f'...deleting {file_name.name}')
        file_name.rmdir()


def scan(folder: Path):
    parser.scan_folder(folder)
    semaphore = Semaphore(20)

    counter_img = 0
    for file in parser.IMAGES:
        thread = Thread(target=handle_files,
                        args=(semaphore, file, folder / 'images',))
        thread.name = f'ImagesThread-{counter_img}'
        thread.start()
        counter_img += 1

    counter_video = 0
    for file in parser.VIDEO:
        thread = Thread(target=handle_files,
                        args=(semaphore, file, folder / 'video',))
        thread.name = f'VideoThread-{counter_video}'
        thread.start()
        counter_video += 1

    counter_audio = 0
    for file in parser.AUDIO:
        thread = Thread(target=handle_files,
                        args=(semaphore, file, folder / 'audio',))
        thread.name = f'AudioThread-{counter_audio}'
        thread.start()
        counter_audio += 1

    counter_doc = 0
    for file in parser.DOCUMENTS:
        thread = Thread(target=handle_files,
                        args=(semaphore, file, folder / 'documents',))
        thread.name = f'DocThread-{counter_doc}'
        thread.start()
        counter_doc += 1

    counter_others = 0
    for file in parser.OTHERS:
        thread = Thread(target=handle_files,
                        args=(semaphore, file, folder / 'others',))
        thread.name = f'OtherThread-{counter_others}'
        thread.start()
        counter_others += 1

    counter_arch = 0
    for file in parser.ARCHIVES:
        thread = Thread(target=handle_files,
                        args=(semaphore, file, folder / 'archives',))
        thread.name = f'ArchivesThread-{counter_arch}'
        thread.start()
        counter_arch += 1

    counter_folder = 0
    for file in parser.FOLDERS:
        thread = Thread(target=handle_folder,
                        args=(semaphore, file,))
        thread.name = f'FolderThread-{counter_folder}'
        thread.start()
        counter_folder += 1


def main():
    try:
        folder_for_scan = Path(sys.argv[1])
    except IndexError:
        folder_for_scan = Path('dir')
    if not folder_for_scan.exists():
        logger.info(f'No folder "{folder_for_scan}" in current directory')
    else:
        logger.info(f'Work with "{folder_for_scan}" folder...')
        time_start = datetime.now()
        scan(folder_for_scan.resolve())
        time_delta = datetime.now() - time_start
        logger.info(f'Folder was scanned for {time_delta} sec')


if __name__ == '__main__':
    main()
