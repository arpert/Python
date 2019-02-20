import os,sys, time
from PIL import Image
from PIL.ExifTags import TAGS

cwd = os.getcwd()
print('CWD:', cwd)
curdir = os.path.split(cwd)[::-1][0]
print('Processing files in path:', curdir)

for fname in os.listdir():
  print("file: %s" % fname, end = ' ')
  #exit()
  if os.path.isfile(fname):
    stat = os.stat(fname)
#    print("file:", time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(stat.st_mtime)), end='')
    destdir = time.strftime('%Y%m%d', time.localtime(stat.st_mtime))
    dateFrom = 'file'
    try:
       exif = Image.open(fname)._getexif()
  
       if exif != None:
         exfdtstr = exif.get(306)
#         print(", exif: %s" % exfdtstr, end='')
         if exfdtstr != None:
           exfdt = time.strptime(exfdtstr, '%Y:%m:%d %H:%M:%S')
           destdir = time.strftime('%Y%m%d', exfdt)
           dateFrom = 'exif'
#           print(", %s" % time.strftime('%Y.%m.%d %H:%M:%S', exfdt), end = '\n')
       else:
         print()
    except Exception as e:
      print(" ", str(e))
    if destdir != curdir:
      if not(os.path.exists(destdir)):
        os.mkdir(destdir)
      print("moving to %s (%s)" % (destdir, dateFrom))
      try:
        os.rename(fname, destdir + '/' + fname)  
      except Exception as e:
        print(" ", str(e))
    else:
      print('- already in proper directory')
  else:
    print()


exit()
for (k,v) in exif.items():
   if k == 37500:
     print('%s - %s = %s' % (k, TAGS.get(k), ''.join([str(chr(x & 0x7f)) for x in v])))
   else:
     print('%s - %s = %s' % (k, TAGS.get(k), v))
