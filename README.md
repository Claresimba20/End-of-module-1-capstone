## End of module 1 capstone
This is a desktop application built with python and Tkinter to automatically generate a weekly duty rota for nurses in the hospital
## Rota rules applied
1. A nurse  can only work a maximum of 5 shifts in a week
2. A nurse cannot be assigned more than 1 shift in the  same day
3. If a nurse reports for Night shift today, they wont be given morning shift the next  day
4. Morning and Night shift needs 2  nurses and evening shift needs 1 nurse
5. Nurses are randomly assigned but balanced to avoid overloading anyone
The app tracks which day a nurse is not assigned any shift which is displayed as off days in the table

## Main features of the app
1. Add Nurse: User  types in a nurse's name and the app saves it to a list
2. Generate schedule: Automatically assigns nurse to Morning, Evening and Night shifts
3. Export CSV: Saves  the schedule to a csv file
4. Reset: Clears all added nurses  and schedules

## How it works
The nurse management adds nurses through the GUI.
Each nurse has  a name and can optionally have availability.
The app loops through each day and each shift and randomly selects available nurses to fill each shift while following the set rules. 

## How the GUI (Tkinter) works
1. Entry box: This is where you type the nurse's name
2. Button: Each button runs  a function;Add nurse, Generate, Export, Reset
3. Treeview  table:Displays the full schedule and off days in a clean table format

After generating a schedule, clicking export CSV lets you save it to a file.
The .csv file includes all daily shifts  and the assigned nurses  and a list of nurses with their off days.
