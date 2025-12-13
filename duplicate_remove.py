import os
import hashlib

def file_hash(path, block_size=65536):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def remove_duplicates(directory):
    hashes = {}
    deleted_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                h = file_hash(file_path)

                if h in hashes:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                else:
                    hashes[h] = file_path

            except Exception as e:
                print(f"Hata oluştu: {file_path} -> {e}")

    print("Silinen duplicate dosyalar:")
    for f in deleted_files:
        print(f)

if __name__ == "__main__":
    target_directory = r"C:\ornek\klasor\yolu"  # BURAYI DEĞİŞTİR
    remove_duplicates(target_directory)
