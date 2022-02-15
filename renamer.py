import os
import sys
import re
from astropy.io import fits
from dateutil import parser
import getopt

class Replacements:
    def __init__(self, replacements):
        self.replacement_fields = re.split(',', replacements)

    def get(self, metadata, counter):
        result = []
        for replacement in self.replacement_fields:
            if replacement[:1] != '#':
                result.append(replacement)
            elif replacement == '#counter':
                result.append("{:04d}".format(counter))
            elif replacement[:5] == '#date':
                format = replacement[6:-1] if replacement[5:6] == '[' else '%Y-%m-%dT%H%M'
                result.append(str(parser.parse(metadata.header['DATE-OBS']).strftime(format)))
            elif replacement == '#copy':
                result.append(replacement)

        return result

class Renamer:
    def __init__(self, basedir, pattern, replacements):
        self.basedir = basedir
        self.pattern = pattern
        self.replacements = Replacements(replacements)
        self.pattern_fields = re.split('_|\.', pattern)
        self.find_symbol_positions()
        self.scan_fit_files_for_dates()

    def process_all(self):
        counter = 1
        for file in self.fits:
            matched = self.process_file(file[0], file[2], counter)
            if matched != None:
                print("mv '" + os.path.join(self.basedir, file[0]) + "' '" + os.path.join(self.basedir, matched) + "'")
                counter += 1


    def scan_fit_files_for_dates(self):
        self.fits = []
        for file in os.listdir(self.basedir):
            if file.endswith(".fit"):
                hdul = fits.open(os.path.join(self.basedir, file))
                self.fits.append([file, parser.parse(hdul[0].header['DATE-OBS']), hdul[0]])
        self.fits = sorted(self.fits, key=lambda file: file[1])

    def find_symbol_positions(self):
        self.variable_pos = []
        pos = 0
        for elem in self.pattern_fields:
            if elem == '@':
                self.variable_pos.append(pos)
            pos += 1

    def check_file_match(self, file):
        p = 0
        for elem in self.pattern_fields:
            if elem == '@':
                p += 1
                continue
            else:
                if elem != file[p]:
                    return False
            p += 1

        return True

    def process_file(self, file, metadata, counter):
        splitted = os.path.splitext(file)
        file_split = splitted[0].split("_")
        if not self.check_file_match(file_split):
            return
        r = 0
        replacements = self.replacements.get(metadata, counter)
        for elem in self.variable_pos:
            if replacements[r] != '#copy':
                file_split[elem] = replacements[r]
            r += 1

        file_split = [s for s in file_split if s != ""]
        return "_".join(file_split) + splitted[1]

def main(argv):
   basedir = ''
   pattern = ''
   replacements = ''
   try:
      opts, args = getopt.getopt(argv,"hb:p:r:",["basedir=","pattern=", "replacements="])
   except getopt.GetoptError:
      print('test.py -b <basedir> -p <pattern> -r <replacements>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -b <basedir> -p <pattern> -r <replacements>')
         sys.exit()
      elif opt in ("-b", "--basedir"):
         basedir = arg
      elif opt in ("-p", "--pattern"):
         pattern = arg
      elif opt in ("-r", "--replacements"):
         replacements = arg

   renamer = Renamer(basedir, pattern, replacements)
   renamer.process_all()

if __name__ == "__main__":
   main(sys.argv[1:])