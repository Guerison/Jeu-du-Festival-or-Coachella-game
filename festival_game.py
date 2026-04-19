import tkinter as tk
from tkinter import messagebox
import random

# ===== CONFIG =====
BUDGET_DEPART = 50_000_000

artistes = {
    "Drake": 8000000,
    "Travis Scott": 7000000,
    "Bad Bunny": 6500000,
    "The Weeknd": 6000000,
    "Kendrick Lamar": 5500000,
    "Booba": 4000000,
    "Ninho": 3500000,
    "Gazo": 2500000,
    "Central Cee": 2500000,
    "Lil Baby": 3000000,
    "Doja Cat": 2500000,
    "Ice Spice": 1500000,
    "Tyla": 1500000,
    "Aya Nakamura": 2000000,
    "Hamza": 1800000,
    "La Fève": 1000000,
    "Yeat": 1500000,
    "Destroy Lonely": 1200000,
    "Rema": 1500000,
    "SDM": 1300000,
    "David Guetta": 3000000,
    "Calvin Harris": 3500000,
    "DJ Snake": 2500000,
    "Fred again..": 2000000,
    "Skrillex": 2500000
}

class FestivalGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Jeu du Festival")

        self.joueurs = []
        self.artistes_list = list(artistes.items())
        random.shuffle(self.artistes_list)

        self.current_artist = None
        self.current_bid = 0

        self.players_in_round = []
        self.current_player_index = 0
        self.last_raiser_index = None
        self.mode = "normal"

        self.main_menu()

    # ===== MENU =====
    def main_menu(self):
        self.clear()

        tk.Label(self.root, text="Jeu du Festival", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Nouvelle Partie", command=self.setup_players).pack(pady=10)
        tk.Button(self.root, text="Quitter", command=self.root.quit).pack(pady=10)

    def setup_players(self):
        self.clear()

        tk.Label(self.root, text="Nombre de joueurs").pack()
        self.nb_entry = tk.Entry(self.root)
        self.nb_entry.pack()

        tk.Button(self.root, text="Valider", command=self.create_players).pack(pady=10)

    def create_players(self):
        try:
            nb = int(self.nb_entry.get())
        except:
            return

        self.clear()
        self.names_entries = []

        for i in range(nb):
            tk.Label(self.root, text=f"Nom joueur {i+1}").pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.names_entries.append(entry)

        tk.Button(self.root, text="Commencer", command=self.start_game).pack(pady=10)

    # ===== INITIALISATION =====
    def start_game(self):
        self.joueurs = []

        for entry in self.names_entries:
            self.joueurs.append({
                "nom": entry.get(),
                "budget": BUDGET_DEPART,
                "artistes": []
            })

        self.next_artist()

    def next_artist(self):
        if not self.artistes_list:
            self.end_game()
            return

        self.current_artist, self.current_bid = self.artistes_list.pop()

        self.players_in_round = self.joueurs.copy()
        self.current_player_index = 0
        self.last_raiser_index = None
        self.mode = "normal"

        self.show_auction()

    # ===== AFFICHAGE =====
    def show_auction(self):
        self.clear()

        joueur = self.players_in_round[self.current_player_index]

        tk.Label(self.root, text=f"Artiste : {self.current_artist}", font=("Arial", 16)).pack()
        tk.Label(self.root, text=f"Mise actuelle : {self.current_bid} €").pack()
        tk.Label(self.root, text=f"Tour : {joueur['nom']} (Budget: {joueur['budget']} €)").pack()

        self.raise_entry = tk.Entry(self.root)
        self.raise_entry.pack()

        if self.mode == "normal":
            tk.Button(self.root, text="Enchérir", command=self.raise_bid).pack(pady=5)
            tk.Button(self.root, text="Rester", command=self.stay).pack(pady=5)
            tk.Button(self.root, text="Laisser", command=self.fold).pack(pady=5)
        else:
            tk.Button(self.root, text="Suivre (Call)", command=self.call).pack(pady=5)
            tk.Button(self.root, text="Relancer (Raise)", command=self.raise_bid).pack(pady=5)
            tk.Button(self.root, text="Passer (Fold)", command=self.fold).pack(pady=5)

        # 👉 Tableau des scores
        self.show_scoreboard()

    # ===== ACTIONS =====
    def raise_bid(self):
        joueur = self.players_in_round[self.current_player_index]

        try:
            amount = int(self.raise_entry.get())
        except:
            return

        if joueur["budget"] >= self.current_bid + amount:
            self.current_bid += amount
            self.last_raiser_index = self.current_player_index
            self.mode = "poker"
            self.next_turn()
        else:
            messagebox.showerror("Erreur", "Pas assez d'argent")

    def stay(self):
        self.mode = "poker"
        self.next_turn()

    def call(self):
        self.next_turn()

    def fold(self):
        joueur = self.players_in_round.pop(self.current_player_index)

        if len(self.players_in_round) == 1:
            gagnant = self.players_in_round[0]
            gagnant["budget"] -= self.current_bid
            gagnant["artistes"].append(self.current_artist)

            messagebox.showinfo("Résultat",
                                f"{gagnant['nom']} gagne {self.current_artist} pour {self.current_bid}€")

            self.next_artist()
            return

        if self.current_player_index >= len(self.players_in_round):
            self.current_player_index = 0

        self.show_auction()

    # ===== TOUR =====
    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players_in_round)

        if self.last_raiser_index is not None and self.current_player_index == self.last_raiser_index:
            gagnant = self.players_in_round[self.last_raiser_index]
            gagnant["budget"] -= self.current_bid
            gagnant["artistes"].append(self.current_artist)

            messagebox.showinfo("Résultat",
                                f"{gagnant['nom']} gagne {self.current_artist} pour {self.current_bid}€")

            self.next_artist()
        else:
            self.show_auction()

    # ===== SCOREBOARD =====
    def show_scoreboard(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="JOUEUR", width=15, borderwidth=1, relief="solid").grid(row=0, column=0)
        tk.Label(frame, text="BUDGET", width=15, borderwidth=1, relief="solid").grid(row=0, column=1)
        tk.Label(frame, text="ARTISTES", width=60, borderwidth=1, relief="solid").grid(row=0, column=2)

        for i, j in enumerate(self.joueurs):
            tk.Label(frame, text=j["nom"], borderwidth=1, relief="solid", width=15).grid(row=i+1, column=0)
            tk.Label(frame, text=f"{j['budget']} €", borderwidth=1, relief="solid", width=15).grid(row=i+1, column=1)
            tk.Label(frame, text=", ".join(j["artistes"]), borderwidth=1, relief="solid", width=60).grid(row=i+1, column=2)

    # ===== FIN =====
    def end_game(self):
        self.clear()

        tk.Label(self.root, text="Fin de la partie", font=("Arial", 18)).pack()

        self.show_scoreboard()

        tk.Button(self.root, text="Retour menu", command=self.main_menu).pack(pady=10)

    # ===== UTILS =====
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ===== LANCEMENT =====
root = tk.Tk()
app = FestivalGame(root)
root.mainloop()