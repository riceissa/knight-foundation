#!/usr/bin/env python3

import csv
import datetime

def main():
    with open("data.csv", "r") as f:
        reader = csv.DictReader(f)
        first = True
        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries, affected_states,
        affected_cities, affected_regions, donation_earmark) values""")

        for row in reader:
            amount = float(row['Amount'].replace("$", "").replace(",", "").strip())
            if row['Date Awarded']:
                donation_date = datetime.datetime.strptime(row['Date Awarded'], "%m/%d/%Y").strftime("%Y-%m-%d")
                donation_date_precision = "day"
            else:
                donation_date = ""
                donation_date_precision = ""

            notes = (("grant period: " + row['Period'] + "; "
                      if row['Period'] else "") +
                     ("part of the challenge: " + row['Challenge'] + "; "
                      if row['Challenge'] else "") +
                     ("goal: " + trimmed(row['Goal']) + "; "
                      if row['Goal'] else ""))
            notes = notes.strip(" ;")
            notes = notes[0].upper() + notes[1:]

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Knight Foundation"),  # donor
                mysql_quote(row['Project Team']),  # donee
                str(amount),  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote(donation_date_precision),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(row['Focus Area']),  # cause_area
                mysql_quote(row['url']),  # url
                mysql_quote(""),  # donor_cause_area_url
                mysql_quote(notes),  # notes
                mysql_quote(""),  # affected_countries
                mysql_quote(""),  # affected_states
                mysql_quote(""),  # affected_cities
                mysql_quote(""),  # affected_regions
                mysql_quote(row['grantee']),  # donation_earmark
            ]) + ")")
            first = False
        print(";")


def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def trimmed(goal, num=200):
    """Trim the goal column to ``num`` words so it fits in the notes column."""
    words = goal.split()
    trimmed_words = words[:num]
    joined = " ".join(trimmed_words)
    if len(trimmed_words) < len(words):
        # trimmed_words is actually shorter than words, so we have cut
        # something out
        joined += " […]"
    return joined


if __name__ == "__main__":
    main()
