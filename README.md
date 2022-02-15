
# What it does?

It is a simple script which is useful if you want to cleanup some file names, especially file names produced by AsiAir. Often it happens that the name of the target in AsiAir is not what you want and renaming dozens of files manually is simple too tedious. Or when you image the same target over multiple nights and you want to have all files renamed nicely so that the name of the file has the capture date, there is a proper counter etc.

# How to use it?

You need Python3 plus additional package astropy, install it with:

pip3 install astropy

Let say you have all your images in a folder /media/ASIAIR/Images/2022-01-30/Seagull:

```
❯ ls -al /media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/
total 305920
drwxr-xr-x 2 kbryd users    32768 Feb 15 17:48 .
drwxr-xr-x 3 kbryd users    32768 Feb 15 17:47 ..
-rw-r--r-- 1 kbryd users 52194240 Feb 12 19:16 Light_FOV Center_300.0s_Bin1_H_gain100_0001.fit
-rw-r--r-- 1 kbryd users 52194240 Feb 12 19:21 Light_FOV Center_300.0s_Bin1_H_gain100_0002.fit
-rw-r--r-- 1 kbryd users 52194240 Feb 12 19:30 Light_FOV Center_300.0s_Bin1_H_gain100_0003.fit
-rw-r--r-- 1 kbryd users 52194240 Feb 12 19:35 Light_FOV Center_300.0s_Bin1_H_gain100_0004.fit
-rw-r--r-- 1 kbryd users 52194240 Feb 14 20:43 Light_Seagull_300.0s_Bin1_H_gain100_0001.fit
-rw-r--r-- 1 kbryd users 52188480 Feb 14 20:47 Light_Seagull_300.0s_Bin1_H_gain100_0002.fit
```

As you can see there are two sets of files, taken on different day, and what is worse they have the target name set incorrectly. Lets fix it.

The command accepts following parameters:

* -b, basedir, this is there the images are
* -p, pattern, to tell the tool what is the format of the file names
* -r, replacement, the new values to put in place of other file name elements

In this case I want to fix the target name, remove ".0s" from the exposure time, remove "Bin1", put the capture date and time in place of "gain100" and finally fix the counter.

```
python3 renamer.py  -b "/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull" -p "Light_@_@_@_H_@_@.fit" -r "Seagull,300s,#date,,#counter"
```

The basedir is obvious, so lets focus on the pattern and replacement. The pattern specifies what I want to replace in the file name, AsiAir generated files have  elements separated by a "_" character. "@" character on the other hand specifies that a given element should be replaced with a replacement. I want to replace 5 components, lets take a sample file name:

Light_Seagull_300.0s_Bin1_H_gain100_0037.fit

1. Light
2. Seagull
3. 300.0s
4. Bin1
5. H
6. gain100
7. 00037


From these 7 components I want to replace the second, third and fourth, remove the sixth, and put counter as the 7th one. In the replacements argument I specify the actual replacements values:

"Seagull,300s,#date,,#counter"

1. <leave as it is>
2. "Seagull"
3. "300s"
4. Capture time - "#date" (instead of Bin1).
5. <remove completely>
6. "#counter"

After running the command I get:

```
❯ python3 renamer.py  -b "/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull" -p "Light_@_@_@_H_@_@.fit" -r "Seagull,300s,#date,,#counter"
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_FOV Center_300.0s_Bin1_H_gain100_0001.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-12T1816_H_0001.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_FOV Center_300.0s_Bin1_H_gain100_0002.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-12T1821_H_0002.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_FOV Center_300.0s_Bin1_H_gain100_0003.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-12T1829_H_0003.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_FOV Center_300.0s_Bin1_H_gain100_0004.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-12T1835_H_0004.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300.0s_Bin1_H_gain100_0001.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-14T1942_H_0005.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300.0s_Bin1_H_gain100_0002.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-14T1947_H_0006.fit'
```

which can be saved to a script file and ran in bash **after double checking that the 'mv' commands indeed do what they should do!**
