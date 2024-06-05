import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import os

def extract_websites(url):
    websites = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        posts_list_div = soup.find('div', id='postsList', class_='adds-wrapper row no-margin')
        if posts_list_div:
            listing_urls = posts_list_div.find_all(class_='listing-url')
            for listing_url in listing_urls:
                href = listing_url.get('href')
                if href:
                    websites.append(href)
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
    return websites

def save_results(results, filepath):
    with open(filepath, 'w') as file:
        for result in results:
            file.write(f"{result}\n")
    print(f"Results saved to {filepath}")

def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def process_urls():
    input_path = entry.get()
    if not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid file.")
        return

    with open(input_path, 'r') as file:
        urls = file.read().splitlines()

    all_websites = []
    for url in urls:
        websites = extract_websites(url)
        all_websites.extend(websites)

    output_path = os.path.join(os.path.dirname(input_path), "extracted_websites.txt")
    save_results(all_websites, output_path)
    messagebox.showinfo("Success", f"Websites extracted and saved to {output_path}")

# Setting up the GUI
root = tk.Tk()
root.title("Website Extractor")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Select a file containing URLs:")
label.pack(pady=5)

entry = tk.Entry(frame, width=50)
entry.pack(pady=5)

browse_button = tk.Button(frame, text="Browse", command=browse_files)
browse_button.pack(pady=5)

extract_button = tk.Button(frame, text="Extract Websites", command=process_urls)
extract_button.pack(pady=20)

root.mainloop()
