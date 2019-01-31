#!/usr/bin/python3

import sys
import argparse
import configparser
import csv
import sqlite3 as sqlite

# get all the field types from csv file
def get_field_datatypes(csvfile):
    dr = csv.DictReader(csvfile)
    fieldTypes = {}
    for entry in dr:
        feildslLeft = [f for f in dr.fieldnames if f not in fieldTypes.keys()]
        if not feildslLeft: 
            break # We're done
        for field in feildslLeft:
            data = entry[field]

            # Need data to decide
            if len(data) == 0:
                continue

            if data.isdigit():
                fieldTypes[field] = "INTEGER"
            else:
                fieldTypes[field] = "TEXT"

    if len(feildslLeft) > 0:
        raise Exception("Failed to find some columns data types !!!")

    return fieldTypes

def convert(csvfile, dbname, tablename, csvdelimiter, csvquotechar):
    try:
        with open(csvfile, 'r') as csvfile:
            # get all the field types
            fieldtypes = get_field_datatypes(csvfile)

            # get all the field names
            csvfile.seek(0)
            reader = csv.DictReader(csvfile)
            fields = reader.fieldnames
            
            # Set field and its type for the sqlite3 table
            cols = []
            for field in fields:
               cols.append("%s %s" % (field, fieldtypes[field]))

            # create the database
            conn = sqlite.connect(dbname)
            cursor = conn.cursor()

            # drop the old table if it exists
            # then create the table
            cursor.execute('DROP TABLE IF EXISTS {}'.format(tablename))
            # Generate create table statement:
            stmt = "CREATE TABLE {} (%s)".format(tablename) % ",".join(cols)
            cursor.execute(stmt)
            
            csvfile.seek(0)
            # skip the header row
            next(csvfile, None)
            csvreader = csv.reader(csvfile, delimiter=csvdelimiter, quotechar=csvquotechar)

            records = 0
            # iterate through the CSV reader, inserting values into the database
            for row in csvreader:
               cursor.execute('INSERT INTO {} VALUES (?,?,?)'.format(tablename), row)
               records += 1

            # commit changes
            conn.commit()

        # Prints a summary as output e.g N records inserted, total records are N
        print ("{} records inserted".format(records))

    except sqlite.Error as e:
        print("sqlite error %s:" % e)
        sys.exit(1)
    except IOError as e:
        print("IO error %s:" % e)
        sys.exit(1)
    except Exception as e:
        print("error %s:" % e)
        sys.exit(1)

    finally:
        # close the csv file
        if csvfile:
            csvfile.close()
        # close the conn
        if conn:
            conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Reads a csv input file and insert it into a table in a SQLite database.''')
    parser.add_argument('csv_file', type=str, help='Input CSV file')

    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read('convert.ini')
    convert(args.csv_file, config['SQLITE3']['dbname'], config['SQLITE3']['tablename'], config['CSV']['delimiter'], config['CSV']['quotechar'])
