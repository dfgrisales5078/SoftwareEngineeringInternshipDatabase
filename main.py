# Authors: Diego Grisales, Oscar Fox
# Description: Python application used to connect SQLite database using sqlite3 and PySimple GUI libraries
# Course: COP 3710 - Intro to Data Engineering
# Date: 05-02-22


import sqlite3
from sqlite3 import Error
import PySimpleGUI as sg

sg.theme('BlueMono')
film_rank_headings = ['Company', 'Title', 'Term']
film_rank_data = [[]]

layout = [
    [sg.Text('Company Name: '), sg.InputText(key='-internship-'), sg.Button('Display Internships')],
    [sg.Table(values=film_rank_data,
              background_color="LightGray",
              headings=film_rank_headings,
              header_background_color="DarkGreen",
              header_text_color='White',
              auto_size_columns=False,
              col_widths=[10, 65],
              justification='center',
              num_rows=10,
              alternating_row_color='LightBlue',
              key='-Internship-',
              row_height=50,
              tooltip='Internship')]
]


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect("internship_.db")

    except Error as e:
        print(e)

    return conn


# manually search for internships
def search_for_internships(conn):
    """
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("select * from 'Search for internships';")

    rows = cur.fetchall()

    for row in rows:
        print(row)

# manually insert to database
def insert_to_database(conn):
    internship_id = input('Enter internship ID: ')
    internship_description = input('Enter internship description: ')
    company_id = input('Enter internship company ID: ')
    term = input('Enter internship term: ')
    user_id = input('Enter internship user ID: ')
    internship_title = input('Enter internship title: ')

    cur = conn.cursor()
    cur.execute("""insert into internship (internship_id, job_desc, company_id, term, user_id, title)
    values (?, ?, ?, ?, ?, ?) """, (internship_id, internship_description, company_id, term, user_id, internship_title))
    conn.commit()


# Open GUI to display internships
def get_internship(conn, company_name, window):
    """
    get and display the films seen and ranked by
    a respondent and display them in the window
    :param window:
    :param conn:
    :param company_name:
    :return:
    """
    cur = conn.cursor()

    if company_name == '':
        cur.execute("select * from 'Search for internships'")
    else:
        cur.execute("select * from 'Search for internships' where company_name = ?", (company_name,))

    rows = cur.fetchall()
    window['-Internship-'].update(values=rows)


def main():
    conn = create_connection("internship_.db")

    user_input = input('Press 1 to search database\nPress 2 to enter internship data\nPress any other key to exit: \n')

    if user_input == '1':
        window = sg.Window('Software Engineering Internship Database', layout,
                           font='Helvetica 12',)

        # ------ Event Loop ------
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Display Internships':
                get_internship(conn, values['-internship-'], window)

        window.close()

    elif user_input == '2':
        insert_to_database(conn)
    else:
        exit(0)


if __name__ == '__main__':
    main()
