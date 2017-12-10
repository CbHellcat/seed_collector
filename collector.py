import os, re, errno, shutil
tempf = "temp.txt"

rx = re.compile(r'[a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8}')


for root, dirs, files in os.walk('C:\\'):
    for filename in files:
        try:
            file=os.path.join(root,filename)
            with open(file) as df:
                try:
                    data = df.read()
                except Exception as e:
                    print file
                    pass
            for match in rx.finditer(data):
                df.close()
                try:
                    with open(tempf, "a+") as temp:
                        temp.write(file + "\n")
                        temp.close()
                except Exception as e:
                    raise e
            df.close()
        except IOError as e:
            print "I/O error({0}): {1}, {2}".format(e.errno, e.strerror, file)
            pass

try: 
    os.mkdir("C:\\seed_files")
    with open(tempf) as temp:
        for line in temp:

            try:
                shutil.copy2(line.rstrip(),"C:\\seed_files")
            except Exception as e:
                print e
                pass
    temp.close()
    os.remove(tempf)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
