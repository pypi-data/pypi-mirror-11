# Barrels, python module for handle many small files
Barrels sticks files into barrels,
the barrels look like csv file (tab seperated)
the meta information is readable, the content of each files is gziped and b64 encoded.

```Python
import barrels
# new barrel
b = barrels.Barrel("items/demo")
# store data in a barrel
b.add(name="filename or key", data="this is the content of the file")

# get files from barrel, using itterators
print("Content of file - single ")
for meta, content in b.filter():
    print(meta)
    print(content)
    #BarrelHead(created=datetime.datetime(2015, 9, 19, 6, 25, 16, 826920), mime=u'unspecified', name=u'filename or key', sha1=u'bUaveapRE71+amf66atSKGSNP4E', length=31)
    #this is the content of the file

# add more files
for i in range(3):
    b.add(name="key-%d"%i, data="this is the content of the file%d"%i)

# the file looks like this (items/demo.barrel):
# 2015-09-19T06:30:22.753443  unspecified filename or key bUaveapRE71+amf66atSKGSNP4E 31  eJwrycgsVgCikoxUheT8vJLUvBKF/DQwNy0zJxUAta0LRw==
# 2015-09-19T06:30:22.754352  unspecified key-0   vG5ClVS/bZtnV7BS8f4C2zuQGEM 32  eJwrycgsVgCikoxUheT8vJLUvBKF/DQwNy0zJ9UAAMEkC3c=
# 2015-09-19T06:30:22.754518  unspecified key-1   74QD32oTnJH4zDY92DneevxVhSc 32  eJwrycgsVgCikoxUheT8vJLUvBKF/DQwNy0zJ9UQAMElC3g=
# 2015-09-19T06:30:22.754662  unspecified key-2   Dp5K6ogePEZ89pyGLQ0aUbMRhGc 32  eJwrycgsVgCikoxUheT8vJLUvBKF/DQwNy0zJ9UIAMEmC3k=

# you can specifify the mime
b.add(name="mime file", data="this is the content of the file", mime="abc/123")

print("Meta, files")
for meta, content in b.filter():
    print(meta)
    # BarrelHead(created=datetime.datetime(2015, 9, 19, 6, 35, 32, 952108), mime=u'unspecified', name=u'filename or key', sha1=u'bUaveapRE71+amf66atSKGSNP4E', length=31)
    # BarrelHead(created=datetime.datetime(2015, 9, 19, 6, 35, 32, 953340), mime=u'unspecified', name=u'key-0', sha1=u'vG5ClVS/bZtnV7BS8f4C2zuQGEM', length=32)
    # BarrelHead(created=datetime.datetime(2015, 9, 19, 6, 35, 32, 953565), mime=u'unspecified', name=u'key-1', sha1=u'74QD32oTnJH4zDY92DneevxVhSc', length=32)
    # BarrelHead(created=datetime.datetime(2015, 9, 19, 6, 35, 32, 953771), mime=u'unspecified', name=u'key-2', sha1=u'Dp5K6ogePEZ89pyGLQ0aUbMRhGc', length=32)
    # BarrelHead(created=datetime.datetime(2015, 9, 19, 6, 35, 32, 953963), mime=u'abc/123', name=u'mime file', sha1=u'bUaveapRE71+amf66atSKGSNP4E', length=31)


# You can also partition the barrels,
b = barrels.PBarrel("items/demop", size=0.1) #partion size 0.1 mb, if larger create new file

#create some partioned barrels
for i in range(20):
    b.add(name="key-%d"%i, data=str(i)*10000000)

# ls -lah
# -rw-rw-r-- 1 oskar oskar  635 sep 19 20:20 demo.barrel
# -rw-rw-r-- 1 oskar oskar  77K sep 19 20:20 demop.barrel
# -rw-rw-r-- 1 oskar oskar 102K sep 19 20:20 demop.D2bfDRx6EmEMqdlWWUnN8uUmO3U.barrel
# -rw-rw-r-- 1 oskar oskar 102K sep 19 20:20 demop.fMhB-zM-sOCIaEbbEHrJ7UJnY6k.barrel
# -rw-rw-r-- 1 oskar oskar 103K sep 19 20:20 demop.NGu0EtXSfKmzGteUbNbD31AHHsM.barrel

# You interface the PBarrel as a Barrel
# i.e.
print "Partioned barrel"
heads =  b.meta.heads
for e,h in enumerate(heads):
    print e, h

# Partioned barrel
# 0 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 38, 689988), mime=u'unspecified', name=u'key-13', sha1=u'ozWQyIn7qxzdljqoElP8XQiPpg4', length=20000000)
# 1 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 38, 865767), mime=u'unspecified', name=u'key-14', sha1=u'fKghYO3v3fkRul/J3DRt3Dhvpjg', length=20000000)
# 2 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 39, 41536), mime=u'unspecified', name=u'key-15', sha1=u'frSylobUXdejQ513Kt3UwVvD0+I', length=20000000)
# 3 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 39, 212197), mime=u'unspecified', name=u'key-16', sha1=u'nEuBg69Hncr6qLnBUqLk77HZQ6Q', length=20000000)
# 4 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 899957), mime=u'unspecified', name=u'key-8', sha1=u'8RQxNhXMwtw9o/LfSCJqyQge2og', length=10000000)
# 5 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 983437), mime=u'unspecified', name=u'key-9', sha1=u'evCJQTdqGrJRCoR3iUttvE8vJyQ', length=10000000)
# 6 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 38, 156672), mime=u'unspecified', name=u'key-10', sha1=u'aCk3ZBUERzPT83oRk7bs5BbcdkA', length=20000000)
# 7 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 38, 330716), mime=u'unspecified', name=u'key-11', sha1=u'WwWxiRVvkRdHrTlWFBBSqUTq5yE', length=20000000)
# 8 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 38, 501095), mime=u'unspecified', name=u'key-12', sha1=u'wfm2CUinxhFyTmTkVsTJh0aemN8', length=20000000)
# 9 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 229069), mime=u'unspecified', name=u'key-0', sha1=u'2l5UvEzMRZox82yko2acd6gd7Ok', length=10000000)
# 10 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 315726), mime=u'unspecified', name=u'key-1', sha1=u'TgvDs37eBwHcOIw2CoulhJcAc5w', length=10000000)
# 11 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 400158), mime=u'unspecified', name=u'key-2', sha1=u'ej5G+6Kd01beohkUFdD2eCFCH3s', length=10000000)
# 12 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 485073), mime=u'unspecified', name=u'key-3', sha1=u'ZdC4EAAagYb1gl35BNemLWDt1Ug', length=10000000)
# 13 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 568192), mime=u'unspecified', name=u'key-4', sha1=u'BVtkebuI9D6p6eB4W+VGAtyA6yQ', length=10000000)
# 14 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 650567), mime=u'unspecified', name=u'key-5', sha1=u'Z1WG6zlD3sDaQhyb8jnZvREug6o', length=10000000)
# 15 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 733357), mime=u'unspecified', name=u'key-6', sha1=u'Dz8v9BhL0y0znHicKSCu1uY/8Dc', length=10000000)
# 16 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 37, 815705), mime=u'unspecified', name=u'key-7', sha1=u'2VTBk8+BDtw8Ehgdx4+cB0MlNEI', length=10000000)
# 17 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 39, 385249), mime=u'unspecified', name=u'key-17', sha1=u'+YyOLGARvvvlciwBgNC32wgAxwE', length=20000000)
# 18 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 39, 560305), mime=u'unspecified', name=u'key-18', sha1=u'OWbZQIb7FArYr0Hd91/YCtC7v/c', length=20000000)
# 19 BarrelHead(created=datetime.datetime(2015, 9, 19, 18, 23, 39, 735275), mime=u'unspecified', name=u'key-19', sha1=u'5GowG35BpX9NqsSS1Rc4CFSq06U', length=20000000)

```