from models import Show, MovieClip, Producer

f = open('thrones.xml')
xml = f.read()
s = Show(xml=xml)
s.save()

print s
