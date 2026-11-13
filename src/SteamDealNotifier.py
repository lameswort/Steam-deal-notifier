"""Please Install the customtkinter library, we rely on it for function."""

import json
import os
from queue import Empty, Queue
from threading import Thread
from urllib.parse import urlencode
from urllib.request import urlopen

import customtkinter as ctk

BG = "#101826"
PANEL = "#172437"
ROW = "#203149"
BLUE = "#2468c9"
MUTED = "#a8b9ce"
ROW_HEIGHT = 58

def load_steam_catalog(api_key):
    endpoint = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
    games = {}
    cursor = 0
    while True:
        params = {"include_games": True, "max_results": 50000, "last_appid": cursor}
        query = urlencode({"key": api_key, "input_json": json.dumps(params)})
        with urlopen(endpoint + "?" + query, timeout=20) as response:
            page = json.load(response)["response"]
        for app in page["apps"]:
            if app["name"].strip():
                games[app["appid"]] = app["name"]
        if not page.get("have_more_results"):
            return tuple(games.items())
        next_cursor = page["last_appid"]
        if next_cursor <= cursor:
            raise ValueError("Steam returned an error, sorry!")
        cursor = next_cursor


def find_games(query, catalog):
    query = query.strip().casefold()
    if not query:
        return []
    return [game for game in catalog if query in game[1].casefold()]


class SteamDealNotifier(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Steam Deal Notifier")
        self.geometry("1000x690")
        self.minsize(680, 650)
        self.configure(fg_color=BG)
        self.tracked = {}
        self.results_window = None
        self.api_key = "ENTER_STEAM_API_KEY HERE."
        self.catalog = None
        self.catalog_updates = Queue()
        self.catalog_loading = False

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=34, pady=24)
        self.label(main, "Steam Deal Notifier", 34, bold=True).pack(anchor="w")
        self.label(main, "Steam catalog • Tracking resets when the app closes as of now, this will be changed.", 14,
                   color=MUTED).pack(anchor="w", pady=(3, 20))

        search = ctk.CTkFrame(main, fg_color="transparent")
        search.pack(fill="x")
        self.query = ctk.CTkEntry(search, height=44, corner_radius=12,
                                  placeholder_text="Search by game title")
        self.query.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.query.bind("<Return>", self.open_results)
        self.button(search, "Search", self.open_results).pack(side="right")
        self.search_message = self.label(main, "", 13, color=MUTED)
        self.search_message.pack(anchor="w", pady=(3, 8))

        section = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=16)
        section.pack(fill="x")
        heading = ctk.CTkFrame(section, fg_color="transparent")
        heading.pack(fill="x", padx=18, pady=(14, 7))
        self.label(heading, "Tracked Games", 23, bold=True).pack(side="left")
        self.count = self.label(heading, "", 14, color=MUTED)
        self.count.pack(side="right")
        self.tracked_list = ctk.CTkScrollableFrame(
            section, height=5 * (ROW_HEIGHT + 6), fg_color=PANEL,
            scrollbar_button_color="#526b89", scrollbar_button_hover_color="#7997b9",
        )
        self.tracked_list.pack(fill="x", padx=12, pady=(0, 12))
        self.refresh_tracked()

    @staticmethod
    def label(parent, text, size, bold=False, color="#edf4ff"):
        return ctk.CTkLabel(parent, text=text, text_color=color,
                            font=ctk.CTkFont(size=size, weight="bold" if bold else "normal"))

    @staticmethod
    def button(parent, text, command, color=BLUE):
        return ctk.CTkButton(parent, text=text, command=command, fg_color=color,
                             corner_radius=12, height=36, width=96)

    def game_row(self, parent, title, action, command, color=BLUE, enabled=True):
        row = ctk.CTkFrame(parent, fg_color=ROW, corner_radius=10, height=ROW_HEIGHT)
        row.pack(fill="x", pady=(0, 6), padx=(2, 6))
        row.pack_propagate(False)
        button = self.button(row, action, command, color)
        button.pack(side="right", padx=12)
        if not enabled:
            button.configure(state="disabled")
        self.label(row, title, 16, bold=True).pack(side="left", padx=14)

    def refresh_tracked(self):
        self.count.configure(text=f"{len(self.tracked)} tracked")
        for child in self.tracked_list.winfo_children():
            child.destroy()
        for app_id, title in self.tracked.items():
            self.game_row(self.tracked_list, title, "Remove",
                          lambda app_id=app_id: self.remove_game(app_id), "#3b4c66")
        if not self.tracked:
            self.label(self.tracked_list, "Search for a game to begin.",
                       15, color=MUTED).pack(pady=22)

    def fetch_catalog(self):
        try:
            self.catalog_updates.put(load_steam_catalog(self.api_key))
        except (OSError, ValueError, KeyError, TypeError):
            self.catalog_updates.put(None)

    def check_catalog(self):
        try:
            self.catalog = self.catalog_updates.get_nowait()
        except Empty:
            self.after(100, self.check_catalog)
            return

        self.catalog_loading = False
        if self.catalog is None:
            self.search_message.configure(
                text="Error, API KEY NOT FOUND!!!"
            )
        else:
            self.search_message.configure(text="")
            self.open_results()

    def open_results(self, event=None):
        query = self.query.get().strip()
        if not query:
            self.search_message.configure(text="Enter a game title to search.")
            return
        if not self.api_key:
            self.search_message.configure(text="placeholder")
            return
        if self.catalog is None:
            if not self.catalog_loading:
                self.catalog_loading = True
                self.search_message.configure(text="Loading the Steam game catalog…")
                Thread(target=self.fetch_catalog, daemon=True).start()
                self.after(100, self.check_catalog)
            return
        self.search_message.configure(text="")
        self.matches = find_games(query, self.catalog)[:100]
        if self.results_window is None or not self.results_window.winfo_exists():
            self.results_window = ctk.CTkToplevel(self)
            self.results_window.title("Search Results")
            self.results_window.geometry("640x440")
            self.results_window.minsize(440, 300)
            self.results_window.configure(fg_color=BG)
            self.results_window.transient(self)
            self.results_heading = self.label(self.results_window, "", 21, bold=True)
            self.results_heading.pack(anchor="w", padx=20, pady=(14, 8))
            self.results_list = ctk.CTkScrollableFrame(self.results_window, fg_color=PANEL)
            self.results_list.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        count = "first 100" if len(self.matches) == 100 else str(len(self.matches))
        self.results_heading.configure(text=f"Search results ({count})")
        self.refresh_results()
        self.results_window.lift()
        self.results_window.focus_set()

    def refresh_results(self):
        if self.results_window is None or not self.results_window.winfo_exists():
            return
        for child in self.results_list.winfo_children():
            child.destroy()
        for app_id, title in self.matches:
            tracked = app_id in self.tracked
            self.game_row(self.results_list, title, "Tracked" if tracked else "Track",
                          lambda app_id=app_id, title=title: self.add_game(app_id, title),
                          enabled=not tracked)
        if not self.matches:
            self.label(self.results_list, "No matching games in the catalog.",
                       15, color=MUTED).pack(pady=22)

    def add_game(self, app_id, title):
        self.tracked.setdefault(app_id, title)
        self.refresh_tracked()
        self.refresh_results()

    def remove_game(self, app_id):
        self.tracked.pop(app_id, None)
        self.refresh_tracked()
        self.refresh_results()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    SteamDealNotifier().mainloop()
