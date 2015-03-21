# Copyright 2015 James William Graham.

import sys
import sqlite3
import re

def main():
  if len(sys.argv) >= 3:
    fileName = sys.argv[1]
    human_name = sys.argv[2]
  else:
    print "must pass file and human name"
    return
  file = open(fileName, "rU")
  if file is None:
    print "cannot read file... corrupted?"
    return
  else:
    formatAndWriteToDBWithFileWithHumansName(file, human_name)
    print "working..."
  print "Finished!"

def formatAndWriteToDBWithFileWithHumansName(file, name_of_human):
  connection = sqlite3.connect(r"./device_data.db")
  cursor = connection.cursor()
  cursor.execute("""
                  CREATE TABLE IF NOT EXISTS data (name text, milliseconds, g_x, g_y, g_z, a_x, a_y, a_z)
                 """)
  #insert data
  for line in file:
    match = re.findall(r"([XYZT]: [\w\-\.\d]+)", line)
    should_interpret_point_as_gyroscope = False #assumes gryo precedes accelerometer data

    g_x = match[0].split()[1]
    g_y = match[1].split()[1]
    g_z = match[2].split()[1]
    a_x = match[3].split()[1]
    a_y = match[4].split()[1]
    a_z = match[5].split()[1]
    tim = match[6].split()[1]
    connection.execute("""INSERT INTO data (g_x, g_y, g_z, a_x, a_y, a_z, milliseconds) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""" % (g_x, g_y, g_z, a_x, a_y, a_z, tim))

  connection.commit()
  connection.close()


if __name__ == '__main__':
  main()
