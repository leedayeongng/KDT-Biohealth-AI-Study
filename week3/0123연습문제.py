import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup


class BasicScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Web Scraper (Template)")
        self.root.geometry("500x300")

        # URL Input
        ttk.Label(root, text="Target URL:").pack(pady=5)
        self.url_var = tk.StringVar(value="https://example.com")
        self.url_entry = ttk.Entry(root, textvariable=self.url_var, width=50)
        self.url_entry.pack(pady=5)

        # Scrape Button
        self.scrape_btn = ttk.Button(root, text="Scrape Info", command=self.scrape_website)
        self.scrape_btn.pack(pady=10)

        # Results Frame
        self.info_frame = ttk.LabelFrame(root, text="Extracted Information")
        self.info_frame.pack(fill="x", padx=10, pady=10)

        # Page Title
        ttk.Label(self.info_frame, text="Page Title:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_label = ttk.Label(self.info_frame, text="---")
        self.title_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Main Heading (h1)
        ttk.Label(self.info_frame, text="Main Heading (h1):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.heading_label = ttk.Label(self.info_frame, text="---")
        self.heading_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    def scrape_website(self):
        url = self.url_var.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL")
            return

        try:
            # ---------------------------------------------------------
            # ---------------------------------------------------------
            # TODO 1: 'requests' 라이브러리를 사용하여 URL에 GET 요청을 보내세요.
            # 힌트: response = requests.get(url)
            # ---------------------------------------------------------
            pass  # Remove this pass

            # ---------------------------------------------------------
            # ---------------------------------------------------------
            # TODO 2: 요청이 성공했는지 확인하세요 (상태 코드 200).
            # 힌트: if response.status_code == 200:
            # ---------------------------------------------------------

            # ---------------------------------------------------------
            # ---------------------------------------------------------
            # TODO 3: BeautifulSoup을 사용하여 HTML 내용을 파싱하세요.
            # 힌트: soup = BeautifulSoup(response.text, 'html.parser')
            # ---------------------------------------------------------
            pass  # Remove this pass

            # ---------------------------------------------------------
            # ---------------------------------------------------------
            # TODO 4: <title> 태그를 찾고 텍스트를 추출하세요.
            # 힌트: page_title = soup.title.string if soup.title else "No title found"
            # ---------------------------------------------------------
            page_title = "TODO: Title 추출"

            # ---------------------------------------------------------
            # ---------------------------------------------------------
            # TODO 5: 첫 번째 <h1> 태그를 찾고 텍스트를 추출하세요.
            # 힌트: h1_tag = soup.find('h1')
            # ---------------------------------------------------------
            main_heading = "TODO: H1 태그 추출"

            # Update GUI
            self.title_label.config(text=page_title)
            self.heading_label.config(text=main_heading)

            # else:
            #     messagebox.showerror("Error", f"Failed to retrieve page using request. status code: {response.status_code}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BasicScraperApp(root)
    root.mainloop()
