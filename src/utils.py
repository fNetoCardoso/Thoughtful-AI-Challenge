import os
import requests
from openpyxl import Workbook

def save_to_excel(news_items, output_dir):
    wb = Workbook()
    ws = wb.active
    ws.append(["Title", "Date", "Description", "Image Filename"])
    
    for item in news_items:
        ws.append([
            item["title"], 
            item["date"], 
            item["description"],
            item["picture_filename"]
        ])
    
    wb.save(os.path.join(output_dir, "news_data.xlsx"))

def download_image(url, output_dir):
    filename = os.path.basename(url)
    filepath = os.path.join(output_dir, filename)
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)
    return filename
