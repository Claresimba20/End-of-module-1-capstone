import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import csv

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["Morning", "Evening", "Night"]
REQUIRED = {"Morning": 2, "Evening": 1, "Night": 2}

#print("Days of the week",DAYS)
#print("Shifts of the day", SHIFTS)
#print("Required nurses per shift",REQUIRED)

#define the class nurse
class Nurse:
    def __init__(self, name, availability=None):
        self.name = name
        self.availability = availability if availability else set(DAYS)

#Test the class
if __name__ == "__main__":
    # Example 1: Nurse with default (full week) availability
    alice = Nurse("Alice")
    #print(f"{alice.name} is available on: {alice.availability}")

    # Example 2: Nurse with limited availability
    Clare = Nurse("Clare", availability={"Monday", "Wednesday", "Friday"})
    #print(f"{Clare.name} is available on: {Clare.availability}")

class RotaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nurse Rota Generator")

        self.nurses = []
        self.schedule = {}
        self.off_days = {}

        self.setup_ui()

    def setup_ui(self):
        frm = tk.Frame(self.root)
        frm.pack()
        label = tk.Label(self.root, text="Nurse Rota Generator App Running!")
        label.pack(padx=20, pady=20)

        tk.Label(frm, text="Nurse Name:").grid(row=0, column=0)
        self.entry = tk.Entry(frm)
        self.entry.grid(row=0, column=1)

        tk.Button(frm, text="Add Nurse", command=self.add_nurse).grid(row=0, column=2, padx=5)
        tk.Button(frm, text="Generate Schedule", command=self.generate_schedule).grid(row=0, column=3, padx=5)
        tk.Button(frm, text="Export CSV", command=self.export_csv).grid(row=0, column=4, padx=5)
        tk.Button(frm, text="Reset", command=self.reset_all).grid(row=0, column=5, padx=5)

        self.tree = ttk.Treeview(self.root, columns=["Day","Shift","Nurses"], show="headings")
        for c in ["Day","Shift","Nurses"]:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        self.tree.pack(padx=10, pady=10)

    def add_nurse(self):
        name = self.entry.get().strip()
        if name:
            self.tree.insert("", "end", values=("Monday", "Morning", name))
            self.entry.delete(0, tk.END)
            messagebox.showinfo("Added", f"Nurse {name} added.")

    def has_back_to_back(self, name, day, shift, assigned_map):
        idx = DAYS.index(day)
        if shift == "Morning" and idx > 0:
            prev = DAYS[idx-1]
            return name in assigned_map.get((prev, "Night"), [])
        if shift == "Night":
            return False
        return False

    def generate_schedule(self):
        if not self.nurses:
            messagebox.showwarning("Error", "Add nurses first.")
            return

        self.schedule.clear()
        self.off_days.clear()

        shifts_count = {n.name: 0 for n in self.nurses}
        day_assigned = {n.name: set() for n in self.nurses}

        for day in DAYS:
            for shift in SHIFTS:
                needed = REQUIRED[shift]
                assigned = []
                available = self.nurses.copy()
                random.shuffle(available)
                for nurse in available:
                    if len(assigned) >= needed:
                        break
                    if (day in nurse.availability and
                        shifts_count[nurse.name] < 5 and
                        day not in day_assigned[nurse.name] and
                        not self.has_back_to_back(nurse.name, day, shift, self.schedule)):
                        assigned.append(nurse.name)
                        shifts_count[nurse.name] += 1
                        day_assigned[nurse.name].add(day)
                self.schedule[(day, shift)] = assigned

        for n in self.nurses:
            worked = {d for (d,s), names in self.schedule.items() if n.name in names}
            self.off_days[n.name] = [d for d in DAYS if d not in worked]

        self.display()

    def display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for (day, shift), names in sorted(self.schedule.items(), key=lambda x:(DAYS.index(x[0][0]), SHIFTS.index(x[0][1]))):
            self.tree.insert("", "end", values=(day, shift, ", ".join(names)))

        self.tree.insert("", "end", values=("", "", ""))
        self.tree.insert("", "end", values=("Off Days", "", ""))
        for n in self.nurses:
            self.tree.insert("", "end", values=(n.name, "", ", ".join(self.off_days[n.name])))

    def export_csv(self):
        if not self.schedule:
            messagebox.showwarning("Error", "Generate schedule first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path:
            return

        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Day","Shift","Nurses"])
            for (day, shift), names in sorted(self.schedule.items(), key=lambda x:(DAYS.index(x[0][0]), SHIFTS.index(x[0][1]))):
                w.writerow([day, shift, ";".join(names)])
            w.writerow([])
            w.writerow(["Nurse","Off Days"])
            for n in self.nurses:
                w.writerow([n.name, ";".join(self.off_days[n.name])])

        messagebox.showinfo("Exported", f"Saved rota to {path}")

    def reset_all(self):
        self.nurses.clear()
        self.schedule.clear()
        self.off_days.clear()
        self.entry.delete(0, tk.END)
        for r in self.tree.get_children():
            self.tree.delete(r)    


if __name__ == "__main__":
    root = tk.Tk()
    app = RotaApp(root)
    root.mainloop()    
