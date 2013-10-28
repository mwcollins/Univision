from models import Show, MovieClip, Producer

s = Show(id=1000)
print "Clip Duration: %s" % (s.total_clip_duration())

