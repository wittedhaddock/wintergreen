# Copyright 2015 James William Graham.

import sys
import sqlite3
import re

def main():
  if len(sys.argv) >= 4:
    fileName = sys.argv[1]
    human_name = sys.argv[2]
    session_number = sys.argv[3]
  else:
    print "must pass file, human name, and session number"
    return
  file = open(fileName, "rU")
  if file is None:
    print "cannot read file... corrupted?"
    return
  else:
    formatAndWriteToDBWithFileWithHumansNameAndSessionNumber(file, str(human_name), session_number)
    print "working..."
  print "Finished!"

def formatAndWriteToDBWithFileWithHumansNameAndSessionNumber(file, name_of_human, session_num):
  connection = sqlite3.connect(r"./device_data.db")
  cursor = connection.cursor()
  cursor.execute("""
                  CREATE TABLE IF NOT EXISTS data (name text, milliseconds float, session_number int, g_x float, g_y float, g_z float, a_x float, a_y float, a_z float)
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
    t = (name_of_human, g_x, g_y, g_z, a_x, a_y, a_z, tim, session_num)
    connection.execute("""INSERT INTO data (name, g_x, g_y, g_z, a_x, a_y, a_z, milliseconds, session_number) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""" , t )

  connection.commit()
  connection.close()


if __name__ == '__main__':
  main()
