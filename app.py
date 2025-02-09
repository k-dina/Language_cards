import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import sqlite3
from tools import update_data, FILE_PATH
from database_manager import CardManager, TopicManager


class WritingFrame(tk.Frame):
    def __init__(self, parent, card_manager=None):
        tk.Frame.__init__(self, parent)
        self.right_answers = 0
        self.wrong_answers = 0

        self.card_manager = card_manager

        # widgets
        self.text_label = tk.Label(self, text="")
        self.inputtxt = tk.Text(self, height=5, width=20)
        self.answer_label = tk.Label(self, text='')
        self.next_task_button = tk.Button(self, text='Следующее задание', command=lambda: self._next_task(parent), state=tk.DISABLED)
        self.check_button = tk.Button(self, text='Проверить ответ', command=lambda: self._check_answer())

        task_label = tk.Label(self, text='переведи на английский и запиши ответ:')
        quit_button = tk.Button(self, text='Закончить тренировку', command=lambda: self._quit_game(parent))

        # widget placement
        task_label.place(relx=0.5, rely=0.1, anchor='center')
        self.text_label.place(relx=0.5, rely=0.2, anchor='center')
        self.inputtxt.place(relx=0.5, rely=0.3, relwidth=0.6, relheight=0.1, anchor='center')
        self.check_button.place(relx=0.25, rely=0.45, anchor='center')
        self.next_task_button.place(relx=0.5, rely=0.45, anchor='center')
        quit_button.place(relx=0.75, rely=0.45, anchor='center')
        self.answer_label.place(relx=0.5, rely=0.75, anchor='center')

    def _check_answer(self):
        inp = self.inputtxt.get(1.0, 'end-1c')
        inp = inp.strip()
        inp = inp.lower()
        if self.card_manager.check_input(inp):
            self.answer_label.config(text='Молодец! Ты ответил правильно: ' + inp, fg='green')
            self.right_answers += 1
        else:
            self.answer_label.config(text='Ой! Правильный ответ: ' + self.card_manager.current_card[1] + '.', fg='red')
            self.wrong_answers += 1
        self.next_task_button.config(state=tk.ACTIVE)
        self.check_button.config(state=tk.DISABLED)

    def _next_task(self, parent):
        if self.card_manager.next_card():
            self.inputtxt.delete(1.0, 'end')
            self.text_label.config(text=self.card_manager.current_card[0])
            self.answer_label.config(text="")
            self.next_task_button.config(state=tk.DISABLED)
            self.check_button.config(state=tk.ACTIVE)
        else:
            self._quit_game(parent)

    def _quit_game(self, parent):
        mb.showinfo('Тренировка закончена', f'Ты ответил правильно на {self.right_answers}/{self.right_answers + self.wrong_answers} вопросов!')
        parent.start_app()

    def clear(self):
        self.right_answers = 0
        self.wrong_answers = 0
        self.inputtxt.delete(1.0, 'end')
        self.answer_label.config(text="")
        self.check_button.config(state=tk.ACTIVE)
        self.next_task_button.config(state=tk.DISABLED)


class RevisionFrame(tk.Frame):
    def __init__(self, parent, card_manager=None):
        tk.Frame.__init__(self, parent)

        self.card_manager = card_manager

        # widgets
        self.text_label = tk.Label(self, text="")
        self.hint_label = tk.Label(self, text="")
        self.next_task_button = tk.Button(self, text='Следующее задание', command=lambda: self._next_task(parent))
        self.hint_button = tk.Button(self, text="Подсказка", command=lambda: self._show_hint())

        task_label = tk.Label(self, text='переведи на английский:')
        quit_button = tk.Button(self, text='Закончить тренировку', command=lambda: self._quit_game(parent))

        # widget placement
        task_label.place(relx=0.5, rely=0.1, anchor='center')
        self.text_label.place(relx=0.5, rely=0.2, anchor='center')
        self.hint_label.place(relx=0.5, rely=0.3, anchor='center')
        self.hint_button.place(relx=0.25, rely=0.45, anchor='center')
        self.next_task_button.place(relx=0.5, rely=0.45, anchor='center')
        quit_button.place(relx=0.75, rely=0.45, anchor='center')

    def _next_task(self, parent):
        if self.card_manager.next_card():
            self.text_label.config(text=self.card_manager.current_card[0])
            self.hint_label.config(text="")
        else:
            self._quit_game(parent)

    def _show_hint(self):
        hint = self.card_manager.current_card[1]
        masked_hint = hint[0] + '*' * (len(hint) - 1)
        self.hint_label.config(text=masked_hint)

    @staticmethod
    def _quit_game(parent):
        mb.showinfo('Тренировка закончена', f'Ты молодец!')
        parent.start_app()

    def clear(self):
        self.hint_label.config(text="")
        self.forget()


class TopicSelectionFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="<- Выбери темы (если хочешь повторить все сразу, пропусти этот шаг)")
        label.place(relx=0.5, rely=0.1, anchor="center")
        topics = TopicManager()
        self.selected_topics = {}

        for topic, topic_id in topics.topics.items():
            self.selected_topics[topic_id] = tk.BooleanVar()
            cb = ttk.Checkbutton(self, text=topic, variable=self.selected_topics[topic_id])
            cb.pack(anchor="w")

        btn = ttk.Button(self, text="Готово", command=lambda: self._proceed(parent))
        btn.pack(pady=10)

    def _proceed(self, parent):
        selected_topics_ids = [topic_id for topic_id, var in self.selected_topics.items() if var.get()]
        parent.current_topics = selected_topics_ids
        parent.show_frame(MainFrame)

    def clear(self):
        for topic_id in self.selected_topics:
            self.selected_topics[topic_id].set(False)


class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # widgets
        label = tk.Label(self, text='Выбери режим:', font=('Arial', 12))
        revision_button = tk.Button(self, text='Повторять слова', command=lambda: parent.start_game('revision'))
        writing_button = tk.Button(self, text='Писать', command=lambda: parent.start_game('writing'))

        # widget placement
        label.place(relx=0.5, rely=0.1, anchor='center')
        revision_button.place(relx=0.3, rely=0.45, anchor='center')
        writing_button.place(relx=0.7, rely=0.45, anchor='center')

    def clear(self):
        pass


class TkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        update_data()
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('800x600')
        self.title('English learning game')
        self.frames = {}
        self.current_topics = []

        for F in (TopicSelectionFrame, MainFrame, WritingFrame, RevisionFrame):
            frame = F(self)
            self.frames[F] = frame
        self.current_frame = self.frames[TopicSelectionFrame]

        self.start_app()

    def show_frame(self, new_frame):
        self.current_frame.clear()
        self.current_frame.forget()
        self.current_frame = self.frames[new_frame]
        self.current_frame.pack(side='top', fill='both', expand=True)

    def start_app(self):
        self.clear()
        self.show_frame(TopicSelectionFrame)

    def clear(self):
        self.current_topics = []

    def start_game(self, mode):
        cards = CardManager(self.current_topics)
        if mode == 'revision':
            self.frames[RevisionFrame].card_manager = cards
            self.frames[RevisionFrame].text_label.config(text=cards.current_card[0])
            self.show_frame(RevisionFrame)
        elif mode == 'writing':
            self.frames[WritingFrame].card_manager = cards
            self.frames[WritingFrame].text_label.config(text=cards.current_card[0])
            self.show_frame(WritingFrame)
        else:
            sys.exit()


if __name__ == '__main__':
    app = TkinterApp()
    app.mainloop()
