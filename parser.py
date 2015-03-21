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
    match = re.findall(r"([XYZT]: [\w\-\.\d]+)", line)
    should_interpret_point_as_gyroscope = False #assumes gryo precedes accelerometer data
    for point in match:
      if "X" in point.split()[0]:
        should_interpret_point_as_gyroscope = not should_interpret_point_as_gyroscope
      if "T" in point.split()[0]:
        continue
      time = match[len(match) - 1]
      handleDataPointWithConnectionAndFlagForGyroOrAccelWithTimestamp(point, connection, should_interpret_point_as_gyroscope, time)
  connection.commit()
  connection.close()

def handleDataPointWithConnectionAndFlagForGyroOrAccelWithTimestamp(point, conn, flag_as_gyro, timestamp):
  #print point + " " + str(flag_as_gyro) + " " + timestamp
  #GOING FOR READABILITY OVER DRY-ABILITY
  #EXPLICATING ALL SIX CASES (3 points, gyro and accel 2 * 3 = 6)
  value = point.split()[1]

  if "X" in point and flag_as_gyro: #gyroscope x value
    conn.execute("INSERT INTO data (g_x) VALUES (%s)" % value)
  if "Y" in point and flag_as_gyro:     #gyroscope y value
    conn.execute("INSERT INTO data (g_y) VALUES (%s)" % value)
  if "Z" in point and flag_as_gyro:     #gyroscope z value
    conn.execute("INSERT INTO data (g_z) VALUES (%s)" % value)

  if "X" in point and not flag_as_gyro: #accelerometer x value
    conn.execute("INSERT INTO data (a_x) VALUES (%s)" % value)
  if "Y" in point and not flag_as_gyro: #accelerometer y value
    conn.execute("INSERT INTO data (a_y) VALUES (%s)" % value)
  if "Z" in point and not flag_as_gyro: #accelerometer z value
    conn.execute("INSERT INTO data (a_z) VALUES (%s)" % value)


if __name__ == '__main__':
  main()
