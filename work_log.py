"""
    Project 3: Work Log
    Team Treehouse Python Techdegree

    Author: Kevin Valverde
    Created: 7/28/2016
    Last Updated: 7/28/2016

    Features
    1. Add a new entry or lookup existing
    2. date, task name, time spent, notes
    3. lookup by date, time spent, exact search, regular expression pattern
    4. give list of dates and allow one to be selected
    5. exact string search should look through name or notes and return corresponding entries
    6. regular expression pattern should look through name or notes and return corresponding entries
"""

import csv
from datetime import datetime
import re
import sys


class WorkLog:
    def __init__(self):
        print('----------------------------------------\n'
              '--------- Welcome to Work Log! ---------\n\n'
              'Instructions are wrapped in parentheses.\n'
              'Example: (C)reate means you type the letter C to run the Create command\n\n'
              'Type MENU at any time to return to the main menu.\n'
              'Type QUIT at any time to exit Work Log.\n')

        # look for csv file. if not found then create. if found then proceed!
        try:
            with open('work_log.csv', newline='') as csvfile:
                log_reader = csv.DictReader(csvfile, delimiter=',')
                self.rows = list(log_reader)
        except FileNotFoundError:
            with open('work_log.csv', 'a') as csvfile:
                fieldnames = ['Date', 'Task Name', 'Task Notes', 'Time Spent']
                log_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
                log_writer.writeheader()
            with open('work_log.csv', newline='') as csvfile:
                log_reader = csv.DictReader(csvfile, delimiter=',', lineterminator='\n')
                self.rows = list(log_reader)

    def main(self):
        while True:
            print('Main Menu:')
            user_input = input('What would you like to do? (C)reate new record or (L)ookup existing? ').lower()
            self.check_input(user_input)

            if user_input == 'c':
                print('Great! Let\'s create a new log entry!\n')
                self.create_entry()
            elif user_input == 'l':
                print('Awesome! Let\'s look up some entries!\n')
                self.lookup_entry()

    def create_entry(self):
        date_input = input('What date did this take place on? (MM/DD/YYYY) ')
        self.check_input(date_input)

        while True:
            try:
                datetime.strptime(date_input, '%m/%d/%Y')
                break
            except ValueError:
                date_input = input('Whoops, I don\'t understand that date format. Try again: (MM/DD/YYYY) ')
                self.check_input(date_input)

        name_input = input('First give the entry a name: ')
        self.check_input(name_input)
        notes_input = input('Now, write in some notes for the entry: ')
        self.check_input(notes_input)
        min_input = input('How many minutes? (example: 30.5) ')
        self.check_input(min_input)

        while True:
            try:
                float(min_input)
                break
            except ValueError:
                min_input = input(
                    'Whoops, something is wrong with your input. How many minutes was that? (example 1.75) ')
        while True:
            proceed = input('\nDoes this look right?\n\nDate: {}, Name: {}, Notes: {},  Duration: {} minutes\n\n'
                            '(Y/N): '.format(date_input, name_input, notes_input, min_input)).lower()
            self.check_input(proceed)

            if proceed == 'y':
                # update CSV with entry
                entry = {'Date': date_input, 'Task Name': name_input, 'Task Notes': notes_input,
                         'Time Spent': min_input}
                self.add_to_csv(entry)
                print('Entry successfully created!\n')
                break
            elif proceed == 'n':
                temp_input = input('Shoot!, would you like to try that again? (Y/N) ').lower()
                self.check_input(temp_input)

                if temp_input == 'y':
                    self.create_entry()
                elif temp_input == 'n':
                    self.main()
            else:
                print('Sorry, didn\'t catch that. Type Y for "Yes, that looks good" or N for "No, that is wrong."')

    def lookup_entry(self):
        search_type = 0
        print('How would you like to search?\n'
              '1. Exact date\n'
              '2. Date range\n'
              '3. Exact string match (searches for matches in Task Name and Notes)\n'
              '4. String pattern match (accepts a regular expression to search Task Name and Notes)\n'
              '5. Time spent\n'
              '6. Range of time spent\n')

        search_type = input("Enter the number corresponding to how would you like to search (1-4)? ")
        self.check_input(search_type)

        while search_type not in ['1', '2', '3', '4', '5', '6']:
            search_type = input("Sorry, please choose a 1, 2, 3, 4, 5, or 6. ")
            self.check_input(search_type)

        if search_type == '1':
            self.date_search()
        elif search_type == '2':
            self.date_range_search()
        elif search_type == '3':
            self.exact_search()
        elif search_type == '4':
            self.pattern_search()
        elif search_type == '5':
            self.duration_search()
        elif search_type == '6':
            self.duration_range_search()

        self.another_search()

    def process_input(self, input):
        pass

    def add_to_csv(self, entry):
        """Takes an entry and adds it to the csv file"""

        with open('work_log.csv', 'a') as csvfile:
            fieldnames = ['Date', 'Task Name', 'Task Notes', 'Time Spent']
            log_writer = csv.DictWriter(csvfile, lineterminator='\n', fieldnames=fieldnames)
            log_writer.writerow(entry)

        self.rows.append(entry)

    def date_search(self):
        date_to_search = input("Enter the date to search (MM/DD/YYYY): ")
        self.check_input(date_to_search)

        while True:
            try:
                date_to_search = datetime.strptime(date_to_search, '%m/%d/%Y')
                break
            except ValueError:
                date_to_search = input("Whoops, wrong date format. Try again. (MM/DD/YYYY): ")

        print("Ok, searching for entries with date:" + datetime.strftime(date_to_search, '%m/%d/%Y') + " ...\n")

        # find entries
        found_entries = list()
        for row in self.rows:
            if datetime.strptime(row['Date'], '%m/%d/%Y') == date_to_search:
                found_entries.append(row)

        self.print_entries(found_entries, datetime.strftime(date_to_search, '%m/%d/%Y'))

    def date_range_search(self):
        date1 = input("Enter the beginning date (MM/DD/YYYY): ")
        self.check_input(date1)
        while True:
            try:
                date1 = datetime.strptime(date1, '%m/%d/%Y')
                break
            except ValueError:
                date1 = input("Whoops, wrong date format. Try again. (MM/DD/YYYY): ")

        date2 = input("Enter the ending date (MM/DD/YYYY): ")
        self.check_input(date2)
        while True:
            try:
                date2 = datetime.strptime(date2, '%m/%d/%Y')
                break
            except ValueError:
                date2 = input("Whoops, wrong date format. Try again. (MM/DD/YYYY): ")

        if date1 <= date2:
            pass
        else:
            print('Looks like your dates are incorrectly ordered. Please try again.')
            self.date_range_search()

        print("Ok, searching for entries within date range: " + datetime.strftime(date1, '%m/%d/%Y')
              + " - " + datetime.strftime(date2, '%m/%d/%Y') + "...\n")

        # find entries
        found_entries = list()
        for row in self.rows:
            if date1 <= datetime.strptime(row['Date'], '%m/%d/%Y') <= date2:
                found_entries.append(row)

        self.print_entries(found_entries, datetime.strftime(date1, '%m/%d/%Y') + "-" + datetime.strftime(date2, '%m/%d/%Y'))

    def exact_search(self):
        string_to_search = input("Enter the text to search for: ")
        self.check_input(string_to_search)

        found_entries = list()
        for row in self.rows:
            if row['Task Name'].find(string_to_search) > 0:
                found_entries.append(row)
            if row['Task Notes'].find(string_to_search) > 0:
                found_entries.append(row)

        print("Ok, searching for entries with text:" + string_to_search + " ...\n")

        self.print_entries(found_entries, string_to_search)

    def pattern_search(self):
        pattern_to_search = input("Enter the regular expression pattern to search: ")
        self.check_input(pattern_to_search)

        if pattern_to_search[:2] == "r'":
            pattern_to_search = pattern_to_search[2:]
        if pattern_to_search[-1:] == "'":
            pattern_to_search = pattern_to_search[:-1]

        found_entries = list()
        for row in self.rows:
            if re.search(r'{}'.format(pattern_to_search), row['Task Name']) is not None:
                found_entries.append(row)
                continue
            if re.search(r'{}'.format(pattern_to_search), row['Task Notes']) is not None:
                found_entries.append(row)

        print("Ok, searching for entries with regular expression: " + pattern_to_search + " ...\n")

        self.print_entries(found_entries, pattern_to_search)

    def duration_search(self):
        mins_to_search = input("Enter the number of minutes to search for: ")
        self.check_input(mins_to_search)

        found_entries = list()
        for row in self.rows:
            if row['Time Spent'] == mins_to_search:
                found_entries.append(row)

        print("Ok, searching for entries with duration of " + mins_to_search + " minutes...\n")

        self.print_entries(found_entries, mins_to_search)

    def duration_range_search(self):
        mins1 = input("Enter the least amount of time (in minutes): ")
        self.check_input(mins1)
        while True:
            try:
                float(mins1)
                break
            except ValueError:
                mins1 = input(
                    'Whoops, something is wrong with your input. How many minutes was that? (example 1.75) ')

        mins2 = input("Enter the most amount of time (in minutes): ")
        self.check_input(mins2)
        while True:
            try:
                float(mins2)
                break
            except ValueError:
                mins2 = input(
                    'Whoops, something is wrong with your input. How many minutes was that? (example 1.75) ')

        if float(mins1) <= float(mins2):
            pass
        else:
            temp_mins = mins1
            mins1 = mins2
            mins2 = temp_mins

        found_entries = list()
        for row in self.rows:
            if float(mins1) <= float(row['Time Spent']) <= float(mins2):
                found_entries.append(row)

        print("Ok, searching for entries with time spent between " + mins1 + " and " + mins2 + " minutes...\n")

        self.print_entries(found_entries, mins1 + " - " + mins2 + " minutes")

    def print_entries(self, found_entries, search_item):
        if found_entries is not None:
            if len(found_entries) > 0:
                print('Found {} entries\n'.format(len(found_entries)))
                i = 1
                for entry in found_entries:
                    print("{}) Date: ".format(i) + entry['Date'])
                    print("   Task Name: ".format(i) + entry['Task Name'])
                    print("   Task Notes: ".format(i) + entry['Task Notes'])
                    print("   Time Spent: ".format(i) + entry['Time Spent'] + " minutes")
                    i += 1
                print('')
            else:
                print('No entries found matching ' + search_item + '.\n')

    def another_search(self):
        response = input('Would you like to try another search? (Y/N) ').lower()
        self.check_input(response)

        while True:
            if response not in ['y', 'n']:
                response = input(
                    "Sorry, I didn't catch that. Type Y for 'Yes, another search' or N for 'No, not another'. ").lower()
                self.check_input(response)
            else:
                break

        if response == 'y':
            self.lookup_entry()
        elif response == 'n':
            self.main()

    def check_input(self, input):
        if input.lower() == 'quit':
            self.quit()
        elif input.lower() == 'menu':
            print('')
            self.main()

    def quit(self):
        print('\nGoodbye!')
        sys.exit()


if __name__ == '__main__':
    work_log = WorkLog()
    work_log.main()
