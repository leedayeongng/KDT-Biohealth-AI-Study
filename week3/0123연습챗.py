import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup


class BasicScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Web Scraper")
        self.root.geometry("500x300")

        # URL 입력
        ttk.Label(root, text="Target URL:").pack(pady=5)
        self.url_var = tk.StringVar(value="https://n.news.naver.com/mnews/article/243/0000091783")
        self.url_entry = ttk.Entry(root, textvariable=self.url_var, width=50)
        self.url_entry.pack(pady=5)

        # 스크랩 버튼
        self.scrape_btn = ttk.Button(root, text="Scrape Info", command=self.scrape_website)
        self.scrape_btn.pack(pady=10)

        # 결과 표시 프레임
        self.info_frame = ttk.LabelFrame(root, text="Extracted Information")
        self.info_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(self.info_frame, text="Page Title:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_label = ttk.Label(self.info_frame, text="---")
        self.title_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(self.info_frame, text="Main Heading (h1):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.heading_label = ttk.Label(self.info_frame, text="---")
        self.heading_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    def scrape_website(self):
        url = self.url_var.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL")
            return

        try:
            # 1️⃣ URL 요청
            response = requests.get(url)

            # 2️⃣ 요청 성공 확인
            if response.status_code != 200:
                messagebox.showerror(
                    "Error",
                    f"Failed to retrieve page. Status code: {response.status_code}"
                )
                return

            # 3️⃣ HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # 4️⃣ <title> 태그 추출
            page_title = soup.title.string.strip() if soup.title else "No title found"

            # 5️⃣ 첫 번째 <h1> 태그 추출
            h1_tag = soup.find('h1')
            main_heading = h1_tag.text.strip() if h1_tag else "No h1 found"

            # 결과 화면에 업데이트
            self.title_label.config(text=page_title)
            self.heading_label.config(text=main_heading)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BasicScraperApp(root)
    root.mainloop()
