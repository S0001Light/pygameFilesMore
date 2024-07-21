import os

b = 1
for b in range(0, 20000):
    d = '\\'
    d = d[:1-1]
    c = d + 'File' + str(b)
    f = os.path.join(c)
    g = str(os.mkdir(f))
    e = open(g, 'a')
    print(e.write(g))
    h = 'swj'
    i = 'File' + str(b) + '\\' + h + str(b) + '.html'
    document = open(i, 'a')
    document.write('<!html>')
    document.write('<heading>')
    document.write('<title></title>')
    document.write('<style>')
    document.write('</style>')
    document.write('</heading>')
    document.write('<body>')
    document.write('</body>')
    document.write('</html>')
    document.close()
    b = b + 1
