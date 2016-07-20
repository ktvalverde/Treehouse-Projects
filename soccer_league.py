"""
    Project 1: Build a soccer league
    Team Treehouse Python Techdegree

    Takes the collection of "Players" and organizes them into teams.
    Balances experience and height to make for even teams.
    Creates a "letter" for each player to inform on team assignment and first practice.

    Author: Kevin Valverde
    Created: 7/19/2016
    Last Updated: 7/20/2016
"""


from random import shuffle


def average_team_height(team):
    """Takes a team and finds the average height of all the players"""
    total_height = 0
    for player in team:
        total_height += team[player]['height']
    avg_height = total_height / len(team)
    return avg_height


def check_heights(dragons, raptors, sharks):
    """checks the average heights to determine if within 1 inch of each other"""
    # first test dragons and raptors
    if abs(average_team_height(dragons) - average_team_height(raptors)) <= 1:
        # good now test dragons and sharks
        if abs(average_team_height(dragons) - average_team_height(sharks)) <= 1:
            # good now test sharks and raptors
            if abs(average_team_height(raptors) - average_team_height(sharks)) <= 1:
                return True

    return False


def write_letter(player, team):
    """Takes a player and their team name and writes a letter to the guardian(s). Then saves to disc."""
    time = '1pm'
    date = 'March 18th'
    if team == 'dragons':
        date = 'March 17th'

    letter_file = open('{}.txt'.format(player['name'].lower().replace(" ", "_")), 'w')
    letter_file.write('Dear {guardian},\n\n{name} has been assigned to team {team}. '
                      'Team {team} will have their first practice on {date} at {time}.\n\n'
                      'Cheers!'
                      .format(guardian=player['guardians'],
                              name=player['name'],
                              team=team,
                              date=date,
                              time=time,
                              )
                      )
    letter_file.close()


def soccer_league_main():
    """Main method for soccer league organization. Should run when file is ran.
    Initializes some variables, organizes the team by experience and height."""

    # collection of players
    players = [
                {'name': 'Joe Smith', 'height': 42, 'experience': True, 'guardians': 'Jim and Jan Smith'},
                {'name': 'Jill Tanner', 'height': 36, 'experience': True, 'guardians': 'Clara Tanner'},
                {'name': 'Bill Bon', 'height': 43, 'experience': True, 'guardians': 'Sara and Jenny Bon'},
                {'name': 'Eva Gordon', 'height': 44, 'experience': False, 'guardians': 'Wendy and Mike Gordon'},
                {'name': 'Matt Gill', 'height': 40, 'experience': False, 'guardians': 'Charles and Sylvia Gill'},
                {'name': 'Kimmy Stein', 'height': 41, 'experience': False, 'guardians': 'Bill and Hillary Stein'},
                {'name': 'Sammy Adams', 'height': 45, 'experience': False, 'guardians': 'Jeff Adams'},
                {'name': 'Karl Saygan', 'height': 42, 'experience': True, 'guardians': 'Heather Bledsoe'},
                {'name': 'Suzane Greenberg', 'height': 44, 'experience': True, 'guardians': 'Henrietta Dumas'},
                {'name': 'Sal Dali', 'height': 41, 'experience': False, 'guardians': 'Gala Dali'},
                {'name': 'Joe Kavalier', 'height': 39, 'experience': False, 'guardians': 'Sam and Elaine Kavalier'},
                {'name': 'Ben Finkelstein', 'height': 44, 'experience': False, 'guardians': 'Aaron and Jill Finkelstein'},
                {'name': 'Diego Soto', 'height': 41, 'experience': True, 'guardians': 'Robin and Sarika Soto'},
                {'name': 'Chloe Alaska', 'height': 47, 'experience': False, 'guardians': 'David and Jamie Alaska'},
                {'name': 'Arnold Willis', 'height': 43, 'experience': False, 'guardians': 'Claire Willis'},
                {'name': 'Phillip Helm', 'height': 44, 'experience': True, 'guardians': 'Thomas Helm and Eva Jones'},
                {'name': 'Les Clay', 'height': 42, 'experience': True, 'guardians': 'Wynonna Brown'},
                {'name': 'Herschel Krustofski', 'height': 45, 'experience': True,
                'guardians': 'Hyman and Rachel Krustofski'},
              ]

    # initialize collections and variables
    dragons = {}
    raptors = {}
    sharks = {}
    league = {}

    dragons_exp = 0
    raptors_exp = 0
    sharks_exp = 0
    experience = [dragons_exp, raptors_exp, sharks_exp]

    dragons_no_exp = 0
    raptors_no_exp = 0
    sharks_no_exp = 0
    no_experience = [dragons_no_exp, raptors_no_exp, sharks_no_exp]

    while True:
        # organizes the teams by dispersing experience and height equally
        for player in players:
            if player['experience']:
                # check count of exp on teams. assign to team with least.
                team_exp = experience.index(min(experience))
                if team_exp == 0:
                    dragons[player['name']] = player
                    experience[0] += 1
                elif team_exp == 1:
                    raptors[player['name']] = player
                    experience[1] += 1
                else:
                    sharks[player['name']] = player
                    experience[2] += 1
            else:
                # check count of no_exp on teams. assign to team with least.
                team_no_exp = no_experience.index(min(no_experience))
                if team_no_exp == 0:
                    dragons[player['name']] = player
                    no_experience[0] += 1
                elif team_no_exp == 1:
                    raptors[player['name']] = player
                    no_experience[1] += 1
                else:
                    sharks[player['name']] = player
                    no_experience[2] += 1
        if check_heights(dragons, raptors, sharks):
            # Perfect! Heights are evenly distributed
            break
        else:
            # Randomly orders players until the above sorting yields an even height distribution within 1 inch
            shuffle(players)

    # created teams are now added to league collection
    league['dragons'] = dragons
    league['raptors'] = raptors
    league['sharks'] = sharks

    # iterate through league collection and call write_letter() for each player
    for team in league:
            for player in league[team]:
                write_letter(league[team][player], team)


if __name__ == "__main__":
    soccer_league_main()
