from PIL import Image, ImageTk
from tkinter import Tk, Button, PhotoImage, Label
import os
import threading
import pyaudio
import wave

path_v = os.path.join(os.path.dirname(__file__), 'images')

class APP():
    def __init__(self, window):
        window.geometry("600x600+150+150")
        window.title("Change your voice")
        window.resizable(0, 0)
        window.iconbitmap(os.path.join(path_v, 'voice.ico'))
        window.configure(bg="lightblue")

class INMAP():
    def __init__(self, window):
        self.window = window
        self.run = False
        self.record_run = False
        self.listen_run = False
        self.record_thread = None
        self.listen_thread = None

        # Tải hình ảnh tĩnh và hình ảnh động
        self.image_normal_befor = Image.open(os.path.join(path_v, 'voice_im.png'))
        self.image_normal = self.image_normal_befor.resize((50, 50), Image.Resampling.LANCZOS)
        self.image_normal = ImageTk.PhotoImage(self.image_normal)

        self.image_normal_befor_volume = Image.open(os.path.join(path_v, "volume.png"))
        self.image_normal_volume = self.image_normal_befor_volume.resize((50, 50), Image.Resampling.LANCZOS)
        self.image_volume = ImageTk.PhotoImage(self.image_normal_volume)

        self.image_x_befor = Image.open(os.path.join(path_v, "x_red_button.png"))
        self.image_x_after = self.image_x_befor.resize((50, 50), Image.Resampling.LANCZOS)
        self.image_x = ImageTk.PhotoImage(self.image_x_after)

        self.frames = [PhotoImage(file=os.path.join(path_v, 'voice_gi.gif'), format=f"gif -index {i}") for i in range(5)]
        self.count_frame = 0

        # Tạo Label chú thích
        self.note_1 = Label(window, text="TO RECORD!", bg='green').place(relx=0.24, rely=0.46)
        self.note_2 = Label(window, text="TO LISTEN!", bg='green').place(relx=0.64, rely=0.46)

        # Tạo Button ghi âm
        self.button = Button(window, image=self.image_normal, command=self.record)
        self.button.place(relx=0.25, rely=0.5)

        # Tạo Label nhận gif
        self.label = Label(self.window, image=self.frames[0])
        self.label.place(relx=0.28, rely=0.1)

        # Tạo Button phát lại âm thanh
        self.button_xuat = Button(window, image=self.image_volume, command=self.listen)
        self.button_xuat.place(relx=0.65, rely=0.5)

        # Tạo button nhận nút X 
        self.but_x = Button(window, image=self.image_x, command=self.stop_all)

    def record(self):
        self.run = not self.run
        self.record_run = not self.record_run

        if self.record_run:
            self.record_thread = threading.Thread(target=self.record_voice)
            self.record_thread.start()
            self.but_x.place(relx=0.45, rely=0.5)
            self.anime()
        else:
            self.stop_all()

    def listen(self):
        self.run = not self.run
        self.listen_run = not self.listen_run

        if self.listen_run:
            self.listen_thread = threading.Thread(target=self.listen_voice)
            self.listen_thread.start()
            self.anime()
        else:
            self.stop_all()

    def anime(self):
        if self.run:
            self.count_frame = (self.count_frame + 1) % len(self.frames)
            self.label.config(image=self.frames[self.count_frame])
            self.window.after(70, self.anime)

    def listen_voice(self):
        with wave.open("record.wav", "rb") as wave_file:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=audio.get_format_from_width(wave_file.getsampwidth()),
                                channels=wave_file.getnchannels(),
                                rate=wave_file.getframerate(),
                                output=True)
            data = wave_file.readframes(1024)
            while self.listen_run and data:
                stream.write(data)
                data = wave_file.readframes(1024)

            stream.stop_stream()
            stream.close()
            audio.terminate()

    def record_voice(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

        self.frames_voice = []
        while self.record_run:
            data = stream.read(1024)
            self.frames_voice.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open("record.wav", "wb") as wave_file:
            wave_file.setnchannels(1)
            wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wave_file.setframerate(44100)
            wave_file.writeframes(b''.join(self.frames_voice))

    def stop_all(self):
        self.run = False
        self.record_run = False
        self.listen_run = False
        self.but_x.place_forget()

        # Hủy các thread đang chạy an toàn
        if self.record_thread and self.record_thread.is_alive():
            self.record_thread.join()
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join()


root = Tk()
APP(root)
INMAP(root)
root.mainloop()
