"""
Copyright (C) 2023 Michael Assefa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""

import tkinter as tk
import os
import uuid
from tkinter import ttk
import random
import time
import sqlite3
import datetime
from tkinter import font
import pandas as pd
from graphics import GraphWin, Circle, Point, Text

class FittsLawApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fitts' Law Experiment")
        self.geometry("800x600")

        self.consent_frame = ConsentFrame(self)
        self.consent_frame.pack(fill="both", expand=True)

class ConsentFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title_label = tk.Label(self, text="Welcome to Fitts' Law Experiment", font=("Times New Roman", 24))
        self.title_label.pack(pady=(20, 10))

        self.instruction_text = ("You have been invited to take part in a Fitts' Law study. The goal of this experiment"
                                 " is to see how Fitts' Law affects your ability to use a computer mouse. The study"
                                 " will take between 1-5 minutes to complete. Your participation in this research is"
                                 " entirely voluntary. Your participation in this study is completely confidential and"
                                 " You may withdraw at any time if you are uncomfortable. By clicking I Consent, you"
                                 " acknowledge that you have read and comprehended the information contained in this"
                                 " consent form and that you voluntarily agree to participate in this study.")

        self.text_widget = tk.Text(self, wrap=tk.WORD, padx=20, pady=20, width=80, height=12, font=("Times New Roman", 12))
        self.text_widget.insert(tk.END, self.instruction_text)
        self.text_widget.config(state=tk.DISABLED, relief=tk.FLAT, bg=self.cget('bg'))
        self.text_widget.pack(pady=(20, 20), padx=20)

        self.button = tk.Button(self, text="I Consent", command=self.consent)
        self.button.pack()

        self.footer_label = tk.Label(self, text="This project was developed and created by Michael Assefa", font=("Times New Roman", 12))
        self.footer_label.pack(side="bottom", pady=(20, 10))


    def consent(self):
        self.pack_forget()
        self.demographics_frame = DemographicsFrame(self.parent)
        self.demographics_frame.pack(fill="both", expand=True)

def create_database_and_tables():
    connection = sqlite3.connect("fitts_law_experiment.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            occupation TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER,
            trial_id TEXT,
            time REAL,
            error_status TEXT,
            FOREIGN KEY (participant_id) REFERENCES participants (id)
        )
    """)

    connection.commit()
    connection.close()

class DemographicsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title_label = tk.Label(self, text="Demographic Information", font=("Times New Roman", 24))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=1, column=0, padx=(120, 10), pady=10, sticky="e")

        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, "Type here")
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.age_label = tk.Label(self, text="Age:")
        self.age_label.grid(row=2, column=0, padx=(120, 10), pady=10, sticky="e")

        self.age_entry = tk.Entry(self)
        self.age_entry.insert(0, "Type here")
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)

        self.gender_label = tk.Label(self, text="Gender:")
        self.gender_label.grid(row=3, column=0, padx=(120, 10), pady=10, sticky="e")

        self.gender_entry = tk.Entry(self)
        self.gender_entry.insert(0, "Type here")
        self.gender_entry.grid(row=3, column=1, padx=10, pady=10)

        self.occupation_label = tk.Label(self, text="Occupation:")
        self.occupation_label.grid(row=4, column=0, padx=(120, 10), pady=10, sticky="e")

        self.occupation_entry = tk.Entry(self)
        self.occupation_entry.insert(0, "Type here")
        self.occupation_entry.grid(row=4, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=5, column=1, padx=10, pady=10)

        self.footer_label = tk.Label(self, text="This project was developed and created by Michael Assefa", font=("Times New Roman", 12))
        self.footer_label.grid(row=10, column=0, columnspan=2, pady=(20, 10))


    def submit(self):
        self.name = self.name_entry.get()
        self.age = self.age_entry.get()
        self.gender = self.gender_entry.get()
        self.occupation = self.occupation_entry.get()

        connection = sqlite3.connect("fitts_law_experiment.db")
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO participants (name, age, gender, occupation)
            VALUES (?, ?, ?, ?)
        """, (self.name, self.age, self.gender, self.occupation))
        connection.commit()

        self.participant_id = cursor.lastrowid

        connection.close()

        self.pack_forget()
        self.instructions_frame = InstructionsFrame(self.parent, self.name, self.age, self.gender, self.occupation, self.participant_id)
        self.instructions_frame.pack(fill="both", expand=True)


class InstructionsFrame(tk.Frame):
    def __init__(self, parent, name, age, gender, occupation, participant_id):
        super().__init__(parent)

        self.parent = parent
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.participant_id = participant_id

        self.title_label = tk.Label(self, text="Instructions", font=("Times New Roman", 24))
        self.title_label.pack(pady=(20, 10))

        self.instructions = (
            "1. A red circle will appear in one of the four corners of the screen.\n"
            "2. Move your mouse cursor to the red circle as quickly and accurately as possible.\n"
            "3. The red circle will disappear once you reach it.\n"
            "4. Repeat the process until the test is complete.\n"
            "5. Click on the 'Begin' button to start the test."
        )

        self.text_widget = tk.Text(self, wrap=tk.WORD, padx=20, pady=20, width=80, height=12, font=("Times New Roman", 12))
        self.text_widget.insert(tk.END, self.instructions)
        self.text_widget.config(state=tk.DISABLED, relief=tk.FLAT, bg=self.cget('bg'))
        self.text_widget.pack(pady=(20, 20), padx=20)

        self.begin_button = tk.Button(self, text="Begin", command=self.begin_experiment)
        self.begin_button.pack()

        self.footer_label = tk.Label(self, text="This project was developed and created by Michael Assefa", font=("Times New Roman", 12))
        self.footer_label.pack(side="bottom", pady=(20, 10))

    def begin_experiment(self):
        self.pack_forget()
        self.parent.withdraw()
        participant_id = str(uuid.uuid4())
        start_time = time.time()
        run_fitts_law_experiment(start_time, self.name, self.age, self.gender, self.occupation, participant_id)
        self.parent.deiconify()
        

def run_fitts_law_experiment(start_time, name, age, gender, occupation, participant_id):

    circle_diameters = [50, 75, 100, 125]
    circle_distances = [100, 200, 300, 400]
    circle_directions = ["left", "right"]

    num_trials_per_block = 32
    num_blocks = 1

    results = {"trials": [], "errors": [], "times": [], "error_status": []}

    win = GraphWin("Fitts' Law Experiment", 1280, 800)

    MAX_TRIALS = 32

    for block in range(num_blocks):
        print("Starting block", block + 1)
        trials = []
        for diameter in circle_diameters:
            for distance in circle_distances:
                for direction in circle_directions:
                    trial_id = "{}-{}-{}".format(diameter, distance, direction)
                    trials.append((diameter, distance, direction, trial_id))
        random.shuffle(trials)

        for i, trial_info in enumerate(trials):
            if i == MAX_TRIALS:
                break

            diameter, distance, direction, trial_id = trial_info
            print("Starting trial", i + 1)

            if direction == "left":
                x_position = 400 - distance
            else:
                x_position = 400 + distance

            circle = Circle(Point(x_position, 300), diameter / 2)
            circle.setFill('red')
            circle.draw(win)

            start_trial_time = time.time()
            clicked = False
            success = False
            while not clicked:
                current_time = time.time()
                if current_time - start_trial_time >= 3:
                    break

                click = win.checkMouse()
                if click:
                    x, y = click.getX(), click.getY()
                    if abs(x - x_position) <= diameter / 2 and abs(y - 300) <= diameter / 2:
                        clicked = True
                        success = True
                        print("Success")
                    else:
                        print("Error")
                        results["errors"].append(trial_id)

            end_time = time.time()
            trial_duration = end_time - start_trial_time
            results["trials"].append(trial_id)
            results["times"].append(trial_duration)

            if not success:
                error = "Fail"
                results["errors"].append(trial_id)
            else:
                error = "Success"

            results["error_status"].append(error)
            circle.undraw()

    win.close()

    connection = sqlite3.connect("fitts_law_experiment.db")
    cursor = connection.cursor()

    for trial_id, trial_time, error_status in zip(results["trials"], results["times"], results["error_status"]):
        cursor.execute("""
            INSERT INTO trials (participant_id, trial_id, time, error_status)
            VALUES (?, ?, ?, ?)
        """, (participant_id, trial_id, trial_time, error_status))

    connection.commit()
    connection.close()

    df = pd.DataFrame({"trial": [t[:3] for t in trials[:MAX_TRIALS]], "trial_id": [t[3] for t in trials[:MAX_TRIALS]], "time": results["times"], "error_status": results["error_status"]})
    
    df["mean_time"] = df.groupby("trial_id")["time"].transform("mean")

    
    mean_mt = df.groupby("trial_id").mean()["time"].reset_index()

    filename = f"fitts_law_results_{name.replace(' ', '_')}.xlsx"
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    workbook = writer.book
    worksheet = workbook.add_worksheet("Results")
    
    worksheet.write("A1", "Participant Info")
    worksheet.write("A2", "Name")
    worksheet.write("A3", name)
    worksheet.write("B2", "Age")
    worksheet.write("B3", age)
    worksheet.write("C2", "Gender")
    worksheet.write("C3", gender)
    worksheet.write("D2", "Occupation")
    worksheet.write("D3", occupation)
   
    modified_df = pd.DataFrame()
    modified_df["Number of trial executed"] = range(1, len(df) + 1)
    modified_df["trial_id"] = df["trial_id"]
    modified_df["mean_time"] = df["mean_time"]
    modified_df["error_status"] = df["error_status"]

    modified_df.to_excel(writer, sheet_name="Results", startrow=5, startcol=0, index=False)

    
    for i, col in enumerate(modified_df.columns):
        if i == 0:
            continue  
    if col == "trial_id":
        col = "Trial_3D"  
    worksheet.write(4, i, col)
    
    worksheet.write(40, 1, "Mean Movement Times")
    for i, col in enumerate(mean_mt.columns):
        if col == "trial_id" or col == "time":
            continue  
        worksheet.write(6 + len(modified_df), i, col)
        for j, value in enumerate(mean_mt[col]):
            if col == "trial":
                value = str(value) 
            worksheet.write(7 + len(modified_df) + j, i, value)

    mean_average = modified_df["mean_time"].mean()
    worksheet.write(6 + len(modified_df), 0, "Mean Average")
    worksheet.write(6 + len(modified_df), 1, mean_average)

    writer.save()

    finish_app = tk.Tk()
    finish_app.title("Fitts' Law Experiment")
    finish_app.geometry("800x600")
    finish_app.configure(bg="#FFFFFF")
    
    heading_font = font.Font(family="Times New Roman", size=24, weight="bold")
    text_font = font.Font(family="Times New Roman", size=16)

    content_frame = tk.Frame(finish_app, bg="#FFFFFF")
    content_frame.pack(expand=True, pady=60)

    finish_label = tk.Label(content_frame, text="Thank you for participating!", font=heading_font, bg="#FFFFFF")
    finish_label.pack(pady=10)

    finish_text = (
        "Your experiment is now complete! Your final results will be saved to 'fitts_law_results.xlsx'. "
        "We appreciate your time and contribution to this study."
    )
    finish_text_label = tk.Label(content_frame, text=finish_text, font=text_font, wraplength=600, justify="center", bg="#FFFFFF")
    finish_text_label.pack(pady=20)

    quit_button = tk.Button(content_frame, text="Quit", command=finish_app.destroy, font=text_font, bg="#007BFF", fg="#FFFFFF", padx=30, pady=10)
    quit_button.pack(pady=10)

    footer_frame = tk.Frame(finish_app, bg="#FFFFFF")
    footer_frame.pack(side="bottom", pady=10)

    footer_text = "This project was developed and created by Michael Assefa"
    footer_label = tk.Label(footer_frame, text=footer_text, font=text_font, bg="#FFFFFF")
    footer_label.pack()

    finish_app.mainloop()

if __name__ == "__main__":
    create_database_and_tables()  
    app = FittsLawApp()
    app.mainloop()



