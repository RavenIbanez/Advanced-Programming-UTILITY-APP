import tkinter as tk
from tkinter import ttk
import requests

def get_teams_by_league_id(league_id):
    url = f"https://www.thesportsdb.com/api/v1/json/3/lookup_all_teams.php?id={league_id}"

    try:
        response = requests.get(url)
        data = response.json()

        print(data)

        return data["teams"]
    except Exception as e:
        print("Error:", e)
        return None
    
class SportsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Team Lookup")
        self.root.geometry("700x500")

        tk.Label(
            root,
            text="Sports Team Lookup",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Entering the League ID
        self.league_entry = tk.Entry(root, font=("Arial", 12), width=40)
        self.league_entry.insert(0, "4328") # the id for English Premier League
        self.league_entry.pack(pady=5)

        tk.Label(
            root,
            text="Enter League ID (e.g. 4328 = English Premier League)",
            font=("Arial", 10)
        ).pack()

        #Load Button
        ttk.Button(
            root,
            text="Load Teams",
            command=self.load_teams
        ).pack(pady=10)

        #listbox for the teams
        self.team_listbox = tk.Listbox(root, width=50, height=10)
        self.team_listbox.pack(pady=10)

        #Button for showing details
        ttk.Button(
            root,
            text="Show Team Details",
            command=self.show_team_details
        ).pack(pady=5)

        #Text box for showing details
        self.details_text = tk.Text(root, width=80, height=10)
        self.details_text.pack(pady=10)

        self.team_data = None
    
    def load_teams(self):
        self.team_listbox.delete(0, tk.END)
        self.details_text.delete("1.0", tk.END)

        league_id = self.league_entry.get()
        teams = get_teams_by_league_id(league_id)

        if teams:
            self.team_data = teams
            for team in teams:
                self.team_listbox.insert(tk.END, team["strTeam"])
        else:
            self.team_listbox.insert(tk.END, "No teams found. Check League ID.")

    def show_team_details(self):
        selection = self.team_listbox.curselection()

        if selection and self.team_data:
            index = selection[0]
            team = self.team_data[index]

            self.details_text.delete("1.0", tk.END)

            details = (
                f"Team Name: {team.get('strTeam', 'N/A')}\n" 
                f"Country: {team.get('strCountry', 'N/A')}\n"
                f"League: {team.get('strLeague', 'N/A')}\n"
                f"Stadium: {team.get('strStadium', 'N/A')}\n\n"
                f"Description: \n{team.get('strDescriptionEN', 'No Description Available.')}"
            )

            self.details_text.insert(tk.END, details)


if __name__ == "__main__":
    root = tk.Tk()
    app = SportsApp(root)
    root.mainloop()




