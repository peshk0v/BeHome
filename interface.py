import myhelp.filework as mf
import myhelp.interface as mi
import customtkinter
from PIL import Image, ImageTk
import requests

customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sett = mf.load("config.toml", 1)

        weather = self.getWeather()
        self.width = 1920
        self.height = 1080
        self.title("BeHome")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.attributes("-fullscreen", True)

        current_path = self.sett["path"]["curentPath"]
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + self.sett["path"]["bgImagePath"]),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.mainFrame = customtkinter.CTkFrame(self, corner_radius=0)
        self.mainFrame.grid(row=0, column=0, sticky="ns")

        self.mainTitle = customtkinter.CTkLabel(self.mainFrame, text="BeHome",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.mainTitle.grid(row=0, column=0, padx=30, pady=(20, 15))
        self.weatherTitle = customtkinter.CTkLabel(self.mainFrame, text=f"{self.sett['userData']['city']}: {weather}℃",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.weatherTitle.grid(row=1, column=0, padx=30, pady=(20, 15))

    def getWeather(self):
        params = {"APPID": self.sett["userData"]["openmapKey"], "q": self.sett["userData"]["city"], "units": "metric"}
        result = requests.get(self.sett["userData"]["openmapUrl"], params=params)
        weather = result.json()
        return int(round(weather["main"]["temp"], 0))

    def getOutDataaaaaaa(self):
        pass
if __name__ == "__main__":
    app = App()
    app.mainloop()