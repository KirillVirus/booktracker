import json
import random
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ------------------ Класс приложения ------------------
class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x600")

        # Загрузка всех данных из одного файла
        self.data = self.load_data()
        self.quotes = self.data["quotes"]
        self.history = self.data["history"]

        # Переменные для фильтров
        self.filter_author = tk.StringVar(value="Все")
        self.filter_topic = tk.StringVar(value="Все")

        # Построение GUI
        self.create_widgets()
        self.update_history_display()
        self.update_author_filter()
        self.update_topic_filter()

    # ------------------ Работа с единым JSON ------------------
    def load_data(self):
        """Загружает данные из data.json, если файла нет - создаёт с предопределёнными цитатами"""
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # Предопределённые цитаты
            default_quotes = [
                {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "мотивация"},
                {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "жизнь"},
                {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "topic": "творчество"},
                {"text": "Тот, кто может, делает; тот, кто не может, критикует.", "author": "Бернард Шоу", "topic": "критика"},
                {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "успех"},
                {"text": "Сложно работать с людьми, но легко управлять ими.", "author": "Сунь Цзы", "topic": "управление"},
                {"text": "Путь в тысячу миль начинается с одного шага.", "author": "Лао-цзы", "topic": "мудрость"},
                {"text": "Единственный способ делать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "работа"}
            ]
            default_data = {
                "quotes": default_quotes,
                "history": []
            }
            self.save_data(default_data)
            return default_data

    def save_data(self, data=None):
        """Сохраняет данные в data.json"""
        if data is None:
            data = {
                "quotes": self.quotes,
                "history": self.history
            }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_all(self):
        """Сохраняет текущие quotes и history в файл"""
        self.save_data()

    # ------------------ GUI элементы ------------------
    def create_widgets(self):
        # Фрейм для отображения цитаты
        self.quote_frame = tk.LabelFrame(self.root, text="Случайная цитата", padx=10, pady=10)
        self.quote_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.quote_text = tk.Text(self.quote_frame, height=4, wrap="word", font=("Arial", 12))
        self.quote_text.pack(fill="both", expand=True)
        self.quote_text.config(state="disabled")

        self.author_label = tk.Label(self.quote_frame, text="Автор: --", font=("Arial", 10, "italic"))
        self.author_label.pack(anchor="e", pady=5)

        # Кнопка генерации
        self.generate_btn = tk.Button(self.root, text="✨ Сгенерировать цитату", command=self.generate_quote, bg="#4CAF50", fg="white", font=("Arial", 11))
        self.generate_btn.pack(pady=10)

        # Фрейм для фильтров
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация истории", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5, pady=5)
        self.author_filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_author, state="readonly")
        self.author_filter_combo.grid(row=0, column=1, padx=5, pady=5)
        self.author_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())

        tk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5, pady=5)
        self.topic_filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_topic, state="readonly")
        self.topic_filter_combo.grid(row=0, column=3, padx=5, pady=5)
        self.topic_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())

        tk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=0, column=4, padx=10)

        # История
        history_frame = tk.LabelFrame(self.root, text="История цитат", padx=10, pady=5)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_listbox = tk.Listbox(history_frame, font=("Arial", 10))
        self.history_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопка очистки истории
        self.clear_btn = tk.Button(self.root, text="🗑️ Очистить историю", command=self.clear_history, bg="#f44336", fg="white")
        self.clear_btn.pack(pady=5)

        # Форма добавления новой цитаты
        add_frame = tk.LabelFrame(self.root, text="➕ Добавить новую цитату", padx=10, pady=5)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Текст цитаты:").grid(row=0, column=0, sticky="e")
        self.new_text_entry = tk.Entry(add_frame, width=50)
        self.new_text_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky="e")
        self.new_author_entry = tk.Entry(add_frame, width=30)
        self.new_author_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(add_frame, text="Тема:").grid(row=2, column=0, sticky="e")
        self.new_topic_entry = tk.Entry(add_frame, width=20)
        self.new_topic_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Button(add_frame, text="Сохранить цитату", command=self.add_quote, bg="#2196F3", fg="white").grid(row=3, column=1, pady=5, sticky="w")

    # ------------------ Логика работы ------------------
    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Добавьте хотя бы одну цитату в список.")
            return

        quote = random.choice(self.quotes)
        self.display_quote(quote)

        # Добавляем в историю с временной меткой
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "topic": quote["topic"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_all()  # Сохраняем всё сразу
        self.update_history_display()
        self.update_author_filter()
        self.update_topic_filter()

    def display_quote(self, quote):
        self.quote_text.config(state="normal")
        self.quote_text.delete(1.0, tk.END)
        self.quote_text.insert(tk.END, f"«{quote['text']}»")
        self.quote_text.config(state="disabled")
        self.author_label.config(text=f"— {quote['author']} —")

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        filtered = self.filter_history()
        for entry in filtered:
            display_text = f"[{entry['timestamp']}] {entry['author']}: {entry['text'][:70]}..."
            self.history_listbox.insert(tk.END, display_text)

    def filter_history(self):
        author = self.filter_author.get()
        topic = self.filter_topic.get()
        filtered = self.history[:]
        if author and author != "Все":
            filtered = [h for h in filtered if h["author"] == author]
        if topic and topic != "Все":
            filtered = [h for h in filtered if h["topic"] == topic]
        return filtered

    def update_author_filter(self):
        authors = sorted(set(h["author"] for h in self.history))
        self.author_filter_combo["values"] = ["Все"] + authors
        if self.filter_author.get() not in authors and self.filter_author.get() != "Все":
            self.filter_author.set("Все")

    def update_topic_filter(self):
        topics = sorted(set(h["topic"] for h in self.history))
        self.topic_filter_combo["values"] = ["Все"] + topics
        if self.filter_topic.get() not in topics and self.filter_topic.get() != "Все":
            self.filter_topic.set("Все")

    def reset_filters(self):
        self.filter_author.set("Все")
        self.filter_topic.set("Все")
        self.update_history_display()

    def clear_history(self):
        if messagebox.askyesno("Очистка истории", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_all()
            self.update_history_display()
            self.update_author_filter()
            self.update_topic_filter()

    def add_quote(self):
        text = self.new_text_entry.get().strip()
        author = self.new_author_entry.get().strip()
        topic = self.new_topic_entry.get().strip()

        if not text or not author or not topic:
            messagebox.showwarning("Ошибка ввода", "Все поля (текст, автор, тема) должны быть заполнены!")
            return

        new_quote = {"text": text, "author": author, "topic": topic}
        self.quotes.append(new_quote)
        self.save_all()

        # Очищаем поля
        self.new_text_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_topic_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Цитата добавлена в коллекцию!")

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()