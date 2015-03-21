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
    print "worked!"
  print "Finished!"

def formatAndWriteToDBWithFileWithHumansName(file, name_of_human):
  connection = sqlite3.connect(r"./device_data.db")
  cursor = connection.cursor()
  cursor.execute("""
                  CREATE TABLE IF NOT EXISTS data (name text, milliseconds, g_x, g_y, g_z, a_x, a_y, a_z)
                 """)
  #insert data
  for line in file:
    match = re.findall(r"[XYZT]: [\w\-\.\d]+", line)
    print match
  connection.commit()
  connection.close()


if __name__ == '__main__':
  main()
