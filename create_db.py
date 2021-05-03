# This file creates database automatically
# Please run this only if db.db is not present

import os
import sqlite3

def create_tables(db, cur):
    # Client Table
    cur.execute("""create table if not exists client(Id integer NOT NULL,
        Name text NOT NULL DEFAULT 'NONE',
        Address text NOT NULL DEFAULT 'NONE',
        Gender text NOT NULL DEFAULT 'NONE', 
        DOB text NOT NULL DEFAULT 'NONE',
        Discord_Username text NOT NULL DEFAULT 'NONE',
        Mail text NOT NULL DEFAULT 'NONE',
        Phone text NOT NULL DEFAULT 'NONE',
        Whatsapp text NOT NULL DEFAULT 'NONE',
        Notes text NOT NULL DEFAULT 'NONE')""")

    # Partner Table
    cur.execute("""create table if not exists partner(Partner_Id integer PRIMARY KEY AUTOINCREMENT, 
        Name text NOT NULL DEFAULT 'NONE',
        Discord_Username text NOT NULL DEFAULT 'NONE',
        Address text NOT NULL DEFAULT 'NONE',
        Mail text NOT NULL DEFAULT 'NONE',
        Phone text NOT NULL DEFAULT 'NONE',
        Gender text NOT NULL DEFAULT 'NONE',
        Joined_At text NOT NULL DEFAULT 'NONE',
        Reference text NOT NULL DEFAULT 'NONE',
        Is_Active text NOT NULL DEFAULT 'NONE'
        )""")

    # Community Table
    cur.execute("""create table if not exists community(Id integer PRIMARY KEY AUTOINCREMENT,
        Name text NOT NULL DEFAULT 'NONE',
        Discord_Username text NOT NULL DEFAULT 'NONE',
        Mail text NOT NULL DEFAULT 'NONE',
        Phone text NOT NULL DEFAULT 'NONE',
        Gender text NOT NULL DEFAULT 'NONE',
        Joined_At text NOT NULL DEFAULT 'NONE'
        )""")

    # Project Table
    cur.execute("""create table if not exists project(Id integer PRIMARY KEY AUTOINCREMENT, 
        Name text NOT NULL DEFAULT 'NONE',
        Description text NOT NULL DEFAULT 'NONE',
        Hand_In_Date text NOT NULL DEFAULT 'NONE',
        Deadline text NOT NULL DEFAULT 'NONE',
        Hand_Out_Date text NOT NULL DEFAULT 'NONE',
        Client_Id text NOT NULL DEFAULT 'NONE',
        Amount_Id text NOT NULL DEFAULT 'NONE',
        Type text NOT NULL DEFAULT 'NONE',
        Status text NOT NULL DEFAULT 'NONE',
        Priority text NOT NULL DEFAULT 'NONE',
        Estimated_Amount text NOT NULL DEFAULT 'NONE'
        )""")

    # Task Table
    cur.execute("""create table if not exists task(Id integer PRIMARY KEY AUTOINCREMENT, 
        Title text NOT NULL DEFAULT 'NONE',
        Description text NOT NULL DEFAULT 'NONE',
        Assigned_To text NOT NULL DEFAULT 'NONE',
        Assigned_By text NOT NULL DEFAULT 'NONE',
        Status text NOT NULL DEFAULT 'NONE',
        Estimated_Time text NOT NULL DEFAULT 'NONE',
        Time_Taken text NOT NULL DEFAULT 'NONE',
        Estimated_XP integer NOT NULL DEFAULT 0,
        Given_XP integer NOT NULL DEFAULT 0,
        Project_Id text NOT NULL DEFAULT 'NONE'
        )""")

    # Internal Table
    cur.execute("""create table if not exists internal(Internal_Id integer PRIMARY KEY AUTOINCREMENT,
        Name text NOT NULL DEFAULT 'NONE',
        Address text NOT NULL DEFAULT 'NONE',
        DOB text NOT NULL DEFAULT 'NONE',
        Gender text NOT NULL DEFAULT 'NONE',
        Joined_At text NOT NULL DEFAULT 'NONE',
        Mail text NOT NULL DEFAULT 'NONE',
        Discord_Username text NOT NULL DEFAULT 'NONE',
        Phone text NOT NULL DEFAULT 'NONE',
        Whatsapp text NOT NULL DEFAULT 'NONE',
        Type text NOT NULL DEFAULT 'NONE',
        Is_Active text NOT NULL DEFAULT 'NONE',
        Total_XP integer NOT NULL DEFAULT 0,
        Level integer NOT NULL DEFAULT 0,
        Notes text NOT NULL DEFAULT 'NONE'
        )""")

    # Suggestion Table
    cur.execute("""create table if not exists suggestion(author text NOT NULL DEFAULT 'NONE', 
        number integer PRIMARY KEY AUTOINCREMENT, 
        title text NOT NULL DEFAULT 'NONE', 
        description text NOT NULL DEFAULT 'NONE', 
        reason text NOT NULL DEFAULT 'NONE', 
        is_considered integer NOT NULL DEFAULT 0, 
        considered_by text NOT NULL DEFAULT 'NONE'
        )""")

    # Career At Koders
    cur.execute("""create table if not exists career_at_koders(Id integer PRIMARY KEY AUTOINCREMENT,
      Name text NOT NULL DEFAULT 'NONE',
      Address text NOT NULL DEFAULT 'NONE',
      Gender text NOT NULL DEFAULT 'NONE',
      DOB text NOT NULL DEFAULT 'NONE',
      Joined_At text NOT NULL DEFAULT 'NONE',
      Mail text NOT NULL DEFAULT 'NONE',
      Phone text NOT NULL DEFAULT 'NONE',
      Whatsapp text NOT NULL DEFAULT 'NONE'
      )""")

    db.commit()

os.system('touch db.db') # Creates empty file

db = "db.db" # Database connection
try:
    db = sqlite3.connect(db)
    cur = db.cursor()
    create_tables(db, cur)
except Exception as e:
    print(e) # Prints exception on connection with db

