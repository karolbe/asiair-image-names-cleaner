
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

As you can see there are two sets of files, taken on a different day, and what is worse they have the target name set incorrectly. Lets fix it.

The command accepts following parameters:

* -b, basedir, this is where the images are
* -p, pattern, to tell the tool what is the format of the file names
* -r, replacement, the new values to put in place of other file name elements

In this case I want to fix the target name, remove ".0s" from the exposure time, remove "Bin1", put the capture date and time in place of "gain100" and finally fix the counter.

```
python3 renamer.py  -b "/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull" -p "Light_@_@_@_H_@_@" -r "Seagull,300s,#date,,#counter"
```

The basedir is obvious, so lets focus on the pattern and replacement. The pattern specifies what I want to replace in the file name, AsiAir generated files have  elements separated by a "_" character. "@" character on the other hand specifies that a given element should be replaced by a replacement. I want to replace 5 components, lets take a sample file name and split it to the individual elements.

```
Light_Seagull_300.0s_Bin1_H_gain100_0037.fit
```

1. Light
2. Seagull
3. 300.0s
4. Bin1
5. H
6. gain100
7. 00037


From these 7 components I want to replace the second, third and fourth, remove the sixth, and put counter as the 7th one. In the replacements argument I specify the actual replacements values:

"Seagull,300s,#date,,#counter"

1. leave as it is
2. "Seagull"
3. "300s"
4. Capture time - "#date" (instead of Bin1).
5. "H" - leave as it is
6. remove gain completely
7. "#counter"

After running the command I get:

```
❯ python3 renamer.py  -b "/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull" -p "Light_@_@_@_H_@_@" -r "Seagull,300s,#date,,#counter"
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_FOV Center_300.0s_Bin1_H_gain100_0001.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-12T1816_H_0001.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_FOV Center_300.0s_Bin1_H_gain100_0002.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-12T1821_H_0002.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_FOV Center_300.0s_Bin1_H_gain100_0003.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-12T1829_H_0003.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_FOV Center_300.0s_Bin1_H_gain100_0004.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-12T1835_H_0004.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300.0s_Bin1_H_gain100_0001.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-14T1942_H_0005.fit'
mv '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300.0s_Bin1_H_gain100_0002.fit' '/media/kbryd/ASIAIR2/Images/2022-01-30/Seagull/Light_Seagull_300s_2022-02-14T1947_H_0006.fit'
```
  
which can be saved to a script file and ran in bash **after double checking that the 'mv' commands indeed do what they should do!**

  
## Additional features
  
* Date format can be customized using standard Python date formatting features, more here: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

for example:

````
python3 renamer.py  -b "/media/kbryd/ASIAIR2/Images/Horse Head/11-02-2022"  -p "Light_@_@_@_H_@_@" -r "#copy,300s,#date[%Y-%m-%dT%H-%M-%S],#copy,#counter"
````

It will generate dates in format:

Light_HorseHead_300s_**2022-01-10T22-39-06**_H_gain100_0034.fit

* You can copy the original value from the source file name, which can come handy if e.g. you want to preserve gain in the file name and you used different gains by mistake, for example, if you have files like these:

````
Light_NGC1499_300.0s_Bin1_H_gain100_0020.fit
Light_NGC1499_300.0s_Bin1_H_gain100_0021.fit
Light_NGC1499_300.0s_Bin1_H_gain100_0022.fit
Light_NGC1499_300.0s_Bin1_H_gain90_0001.fit
Light_NGC1499_300.0s_Bin1_H_gain90_0002.fit
Light_NGC1499_300.0s_Bin1_H_gain90_0003.fit
````

and run the command:
  
````
python3 renamer.py  -b "/media/kbryd/ASIAIR2/Images/Horse Head/11-02-2022" -p "Light_@_@_@_H_@_@" -r "#copy,300s,,#copy,#counter"
````

It will output these file names, as you can see file name elements target and gain were copied, the exposure time which was changed, Bin1 was removed and a new counter was applied.
  
````
Light_NGC1499_300_H_gain100_0001.fit
Light_NGC1499_300_H_gain100_0002.fit
Light_NGC1499_300_H_gain100_0003.fit
Light_NGC1499_300_H_gain90_0004.fit
Light_NGC1499_300_H_gain90_0005.fit
Light_NGC1499_300_H_gain90_0006.fit
````
  
  
