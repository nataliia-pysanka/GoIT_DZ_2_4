"""
Work with files
"""
from pathlib import Path
from log import logger

IMAGES = []
VIDEO = []
DOCUMENTS = []
AUDIO = []
ARCHIVES = []
OTHERS = []
KNOWN_EXT = []
UNKNOWN_EXT = []
FOLDERS = []

IMAGES_EXT = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO_EXT = ('AVI', 'MP4', 'MOV', 'MKV')
DOCUMENTS_EXT = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
AUDIO_EXT = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVES_EXT = ('ZIP', 'GZ', 'TAR')

EXT = [IMAGES_EXT, VIDEO_EXT, DOCUMENTS_EXT, AUDIO_EXT, ARCHIVES_EXT]

REGISTER_EXTENSIONS = {
    IMAGES_EXT: IMAGES,
    VIDEO_EXT: VIDEO,
    DOCUMENTS_EXT: DOCUMENTS,
    AUDIO_EXT: AUDIO,
    ARCHIVES_EXT: ARCHIVES
}

EXCLUSION_SET = ('archives', 'video', 'audio', 'documents', 'images', 'others')


def pick_ext(file: Path):
    """
    Sorts files by the extensions
    :param file: Path
    :return: None
    """
    ext = file.suffix[1:].upper()
    if not ext:
        OTHERS.append(file)
        return
    for item in EXT:
        if ext in item:
            REGISTER_EXTENSIONS[item].append(file)
            KNOWN_EXT.append(ext)
            return
    OTHERS.append(file)
    UNKNOWN_EXT.append(ext)
    return


def scan_folder(folder: Path):
    """
    Goes through the folder and sorts the files
    :param folder: Path
    :return: None
    """
    if not folder.exists():
        return False
    for file in folder.iterdir():
        if file.is_dir():
            if file.name not in EXCLUSION_SET:
                scan_folder(file)
                FOLDERS.append(file)
            continue
        if file.is_file():
            pick_ext(file)
    return True


def print_lst():
    """
    Prints the lists with sorted files
    """
    if IMAGES:
        logger.info('IMAGES:')
        for image in IMAGES:
            logger.info(f'\t{image.name}')

    if VIDEO:
        logger.info(f'VIDEO:')
        for video in VIDEO:
            logger.info(f'\t{video.name}')

    if DOCUMENTS:
        logger.info(f'DOCUMENTS:')
        for doc in DOCUMENTS:
            logger.info(f'\t{doc.name}')

    if AUDIO:
        logger.info(f'AUDIO:')
        for audio in AUDIO:
            logger.info(f'\t{audio.name}')

    if ARCHIVES:
        logger.info(f'ARCHIVES:')
        for arch in ARCHIVES:
            logger.info(f'\t{arch.name}')

    if OTHERS:
        logger.info(f'OTHERS:')
        for other in OTHERS:
            logger.info(f'\t{other.name}')

    if FOLDERS:
        logger.info(f'FOLDERS:')
        for folder in FOLDERS:
            logger.info(f'\t{folder.name}')
    print()
    if KNOWN_EXT:
        logger.info(f'Known extensions: {" ".join(set(KNOWN_EXT))}')
    if UNKNOWN_EXT:
        logger.info(f'Unknown extensions: {" ".join(set(UNKNOWN_EXT))}')