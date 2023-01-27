import argparse
from pathlib import Path
from shutil import copyfile, move
from threading import Thread, Semaphore
import logging


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', required=True)
parser.add_argument('-o', '--output', default='dist')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')

FOLDERS = []


def find_folders(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            FOLDERS.append(el)
            find_folders(el)


def types(extension: str):
    type_dict = {
        "images": ['jpeg', 'png', 'jpg', 'svg'],
        "video": ['avi', 'mp4', 'mov', 'mkv'],
        "documents": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
        "audio": ['mp3', 'ogg', 'wav', 'amr'],
        "archives": ['zip', 'gz', 'tar']
    }
    for key, val in type_dict.items():
        if extension in val:
            return key

    return 'other'

def move_file(path: Path, semaphore: Semaphore):
    with semaphore:
        logging.debug(f"start work with {path.name}")
        for el in path.iterdir():
            if el.is_file():
                stem = el.stem
                extension = el.suffix.replace(".", "")
                new_path = output_folder / types(extension)
                new_path.mkdir(exist_ok=True, parents=True)
                move(el, new_path / stem)


def cleaner(path: Path):
    ''' delet all empty dir'''
    for item in path.iterdir():
        if item.is_dir():
            cleaner(item)
            if not any(item.iterdir()):
                item.rmdir()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    base_folder = Path(source)
    output_folder = Path(output)
    FOLDERS.append(base_folder)
    find_folders(base_folder)
    print(FOLDERS)
    semaphore = Semaphore(2)
    threads = []
    for folder in FOLDERS:
        th = Thread(target=move_file, args=(folder, semaphore))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    cleaner(base_folder)
    base_folder.rmdir()
