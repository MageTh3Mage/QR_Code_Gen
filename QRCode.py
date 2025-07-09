import qrcode
import tkinter as tk
from PIL import ImageTk, Image, ImageOps
import random
import string
import keyboard
import re
from urllib.parse import urlparse

def generate_filename(data):
    if re.match(r'^https?://', data, re.IGNORECASE):
        try:
            parsed = urlparse(data)
            domain = parsed.netloc
            domain = re.sub(r'^(www\d*\.|m\.|mobile\.|api\.|app\.|web\.|static\.)', '', domain, flags=re.IGNORECASE)
            domain_parts = domain.split('.')
            if len(domain_parts) > 2 and len(domain_parts[-2]) <= 3:
                main_part = domain_parts[-3]
            else:
                main_part = domain_parts[0]
            main_part = re.sub(r'[^\w-]', '', main_part).lower()
            path = parsed.path.strip('/')
            if path:
                path_part = re.sub(r'[^\w-]', '_', path.split('/')[0]).lower()
                if len(path_part) > 3 and len(path_part) < 20:
                    return f"{main_part}_{path_part}.png"
            return f"{main_part}.png"
        except:
            pass
    clean_text = re.sub(r'[^\w\s-]', '', data).strip().lower()
    words = re.split(r'\s+', clean_text)
    if len(words) > 3:
        return '_'.join(words[:3]) + '.png'
    elif clean_text:
        return clean_text.replace(' ', '_') + '.png'
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".png"

def create_qr_window(data):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=121,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#8A2BE2", back_color="black")
    if not isinstance(img, Image.Image):
        img = Image.frombytes('RGB', img.size, img.tobytes())
    if img.width != img.height:
        size = max(img.width, img.height)
        img = ImageOps.pad(img, (size, size), color='black')
    img = img.resize((500, 500), Image.NEAREST)
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.configure(bg='black')
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=tk_img, bg='black')
    label.pack()
    root.geometry("500x500")
    root.update_idletasks() 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 500) // 2
    root.geometry(f"+{x}+{y}")
    def save_image():
        filename = generate_filename(data)
        img.save(filename)
        print(f"Saved as {filename}")
    keyboard.add_hotkey('f1', save_image)
    keyboard.add_hotkey('esc', root.destroy)
    label.image = tk_img
    root.mainloop()

if __name__ == "__main__":
    data = input("Enter text/URL for QR code: ").strip()
    if data:
        create_qr_window(data)
    else:
        print("No input provided")
