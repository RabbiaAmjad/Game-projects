import tkinter as tk
from tkinter import messagebox

from game_core import Game

class EnchantedTilesGUI:
    def __init__(self, root):
        self.root = root
        root.title("The Enchanted Tiles")
        root.geometry("500x400")
        root.configure(bg="#fce4ec")
        self.game = Game()


        title = tk.Label(
            root,
            text="✨ THE ENCHANTED TILES ✨",
            font=("Georgia", 20, "bold"),
            bg="#fce4ec"
        )
        title.pack(pady=30)

        start_btn = tk.Button(
            root,
            text="🌷 Begin Journey",
            width=20,
            command=self.start_game
        )
        start_btn.pack(pady=10)

        load_btn = tk.Button(
            root,
            text="📂 Continue Journey",
            width=20,
            command=self.load_game
        )
        load_btn.pack(pady=10)

        exit_btn = tk.Button(
            root,
            text="❌ Exit",
            width=20,
            command=root.quit
        )
        exit_btn.pack(pady=10)

    def start_game(self):
       self.clear_screen()
       self.show_tile_floor()


    def load_game(self):
        messagebox.showinfo("Load", "Game will load here")

    def clear_screen(self):
       """prepares window for next screen"""
       for widget in self.root.winfo_children():
        widget.destroy()

    # 12 tiles grid screen 
    def show_tile_floor(self):
       """12 tiles screen"""
       title = tk.Label(
        self.root,
        text="🧩 Choose a Tile",
        font=("Georgia", 18, "bold"),
        bg="#fce4ec"
    )
       title.pack(pady=20)

       grid_frame = tk.Frame(self.root, bg="#fce4ec")
       grid_frame.pack()
 
       self.tile_buttons = []

       for index, tile in enumerate(self.game.tiles):
         btn = tk.Button(
            grid_frame,
            text=tile.name,
            width=12,
            height=3,
            state=tk.NORMAL if tile.unlocked else tk.DISABLED,
            command=lambda i=index: self.tile_clicked(i)
        )

         row = index // 4
         col = index % 4
         btn.grid(row=row, column=col, padx=10, pady=10)

         self.tile_buttons.append(btn)

    def tile_clicked(self, index):
      tile = self.game.tiles[index]

      if not tile.unlocked:
        messagebox.showwarning("Locked", "🔒 This tile is still sealed.")
        return

      result = self.game.play_tile(index)

      if result:
        self.refresh_tiles()
    
# refreshing tiles method to sync
    def refresh_tiles(self):
      for i, tile in enumerate(self.game.tiles):
        if tile.unlocked:
            self.tile_buttons[i].config(state=tk.NORMAL)




root = tk.Tk()
app = EnchantedTilesGUI(root)
root.mainloop()
