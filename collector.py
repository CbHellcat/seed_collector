import mimetypes, os, re, errno, shutil
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

tempf = "temp.txt"
WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
rx = re.compile(r'[a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8} [a-z]{3,8}')

def get_docx_text(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)

def temp_write(file):
    print "Adding: " + file
    try:
        with open(tempf, "a+") as temp:
            temp.write(file + "\n")
            temp.close()
    except Exception as e:
        print e

for root, dirs, files in os.walk('C:\\'):
    for filename in files:
        try:
            file=os.path.join(root,filename)
            type_test = mimetypes.guess_type(file)
            if type_test[0] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                text = get_docx_text(file)
                for match in rx.finditer(text):
                    temp_write(file)
            else:        
                with open(file) as df:
                    try:
                        data = df.read()
                    except Exception as e:
                        print file
                        pass
                for match in rx.finditer(data):
                    print "trying: " + file
                    df.close()
                    temp_write(file)
                df.close()
        except IOError as e:
            print "I/O error({0}): {1}, {2}".format(e.errno, e.strerror, file)
            pass

try: 
    if not os.path.exists("C:\\seed_files"):
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
