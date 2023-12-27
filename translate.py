import os
import re
import hashlib
import argparse
import shutil
from google.cloud import translate_v2 as translate
from concurrent.futures import ThreadPoolExecutor
import logging

# Opsæt Google Cloud Translation
translate_client = translate.Client()

def get_file_hash(file_path):
    """ Generer et hash for en fils indhold for at tjekke for ændringer """
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return hashlib.md5(file_content).hexdigest()

def translate_text(text, target_language):
    """
    Oversætter tekst til målsproget ved hjælp af Google Cloud Translation.
    Håndterer eventuelle fejl, der opstår under oversættelsen.
    """
    try:
        translation = translate_client.translate(text, target_language=target_language)
        return translation['translatedText']
    except Exception as e:
        logging.error(f"Fejl under oversættelse: {e}")
        return text

def extract_and_translate_strings(file_path, target_language, min_length, dry_run, regex):
    """
    Udtrækker strenge fra en fil ved hjælp af det angivne regex, oversætter dem,
    og skriver ændringerne tilbage. Springer oversættelse over, hvis filen ikke er ændret.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Tjek, om filen er blevet ændret siden sidste kørsel
        current_hash = get_file_hash(file_path)
        old_hash = hashes.get(file_path, '')
        if current_hash == old_hash:
            logging.info(f"Springer uændret fil over: {file_path}")
            return

        # Find alle strenge, der matcher regex i filen
        matches = re.findall(regex, content)

        # Oversæt og erstat hver streng
        translated_content = content
        for match in matches:
            if len(match) >= min_length:
                translated_text = translate_text(match, target_language)
                translated_content = re.sub(fr'(?<!\\)["\']{re.escape(match)}(?<!\\)["\']', f'"{translated_text}"', translated_content)

        # Skriv ændringerne til filen, hvis ikke i dry run mode
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(translated_content)
            hashes[file_path] = current_hash

        logging.info(f"Oversat fil: {file_path}")
    except Exception as e:
        logging.error(f"Fejl ved behandling af fil {file_path}: {e}")

def translate_directory(directory_path, target_language, min_length, dry_run, regex, exclude):
    """
    Oversætter alle strenge i PHP- og JS-filer inden for den angivne mappe.
    Bruger ThreadPoolExecutor til parallel forarbejdning.
    """
    with ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.php') or file.endswith('.js'):
                    file_path = os.path.join(root, file)
                    # Udeluk bestemte filer
                    if file_path not in exclude:
                        futures.append(executor.submit(extract_and_translate_strings, file_path, target_language, min_length, dry_run, regex))

        for future in futures:
            future.result()

def main():
    """
    Hovedfunktionen til at analysere argumenter og starte oversættelsesprocessen.
    Inkluderer muligheder for dry run, brugerdefineret regex og udelukkelse af filer.
    """
    parser = argparse.ArgumentParser(description="Oversæt strenge i PHP- og JS-filer.")
    parser.add_argument('directory', help="Mappe, der indeholder de filer, der skal oversættes")
    parser.add_argument('target_language', help="Målsprogets kode (fx 'da' for dansk)")
    parser.add_argument('--min_length', type=int, default=5, help="Minimumslængde af strenge, der skal oversættes")
    parser.add_argument('--dry_run', action='store_true', help="Kør scriptet i dry run mode uden faktisk at skrive til filerne")
    parser.add_argument('--regex', default=r'(?<!\\)["\'](.*?)(?<!\\)["\']', help="Regulært udtryk for matching af strenge")
    parser.add_argument('--exclude', nargs='*', help="Liste over filstier, der skal udelukkes fra oversættelse")
    parser.add_argument('--verbose', action='store_true', help="Aktiver detaljeret output")

    args = parser.parse_args()

    # Opsæt logging med det passende niveau baseret på verbose flag
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(filename='translation_script.log', level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    global hashes
    hashes = {}

    # Backup mappen før der foretages ændringer
    backup_directory = args.directory + '_backup'
    shutil.copytree(args.directory, backup_directory)
    logging.info(f"Backup oprettet på {backup_directory}")

    # Start oversættelsesprocessen
    translate_directory(args.directory, args.target_language, args.min_length, args.dry_run, args.regex, args.exclude or [])
    logging.info("Oversættelsesprocessen afsluttet.")

if __name__ == "__main__":
    main()
