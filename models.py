import _mysql
from pyquery import PyQuery as pq

db=_mysql.connect(db="univision",user="univision",passwd="univision",)

class Show:

	def __init__(self,xml=None,attrs=None,id=None):

		self.attrs = {
			'id':        None,
			'name':      None,
			'clips':     [],
			'producers': []
		}

		if xml:
			self.parseXml(xml)

		if id:
			self.load(id)

	def load(self,id):
		db.query('select name from Shows where id="%s"' % (id) )
		r = db.store_result()
		rec = r.fetch_row(how=1)[0]
		self.attrs['id']   = id
		self.attrs['name'] = rec['name']
	
		db.query('''
			select 
				mc.id as id, 
				mc.name as name, 
				mc.description as description,
				mc.start as start,
				mc.stop as stop
			from
				MovieClipsInShows as map,
				MovieClips as mc
			where
				map.showId = "%s" and
				mc.id = map.movieClipId 
			''' % (id) )

		r = db.store_result()
		rows = r.num_rows()

		while rows:	
			rec = r.fetch_row(how=1)[0]
			self.attrs['clips'].append( MovieClip(attrs=rec) )
			rows = rows-1

		db.query('''
			select 
				p.id as id, 
				p.name as name, 
				p.phone as phone, 
				p.email as email 
			from
				ShowHasProducers as map,
				Producers as p
			where
				map.showId = "%s" and
				p.id = map.producerId 
			''' % (id) )

		r = db.store_result()
		rows = r.num_rows()

		while rows:	
			rec = r.fetch_row(how=1)[0]
			self.attrs['producers'].append( Producer(attrs=rec) )
			rows = rows-1

	def parseXml(self,xml):
		dom = pq(xml)
		self.attrs['id']   = dom('show > id').text()
		self.attrs['name'] = dom('show > name').text()

		producers = dom('show > producers > producer')

		for producer in producers:
			producer = pq(producer)
			attrs = {
				'id':    producer.children('id').text(),
				'name':  producer.children('name').text(),
				'email': producer.children('email').text(),
				'phone': producer.children('phone').text(),
			}

			self.attrs['producers'].append( Producer(attrs=attrs) )

		clips = dom('show > clips > clip')

		for clip in clips:
			clip = pq(clip)
			attrs = {
				'id':          clip.children('id').text(),
				'name':        clip.children('name').text(),
				'description': clip.children('description').text(),
				'start':       clip.children('start').text(),
				'stop':        clip.children('stop').text(),
			}

			self.attrs['clips'].append( MovieClip(attrs=attrs) )

	def save(self):
		attrs = self.attrs
		db.query("""replace into Shows (id,name) values ("%s","%s") """ % ( attrs['id'],attrs['name']) )
		
		for producer in attrs['producers']:
			producer.save()
			db.query("""replace into ShowHasProducers (showId,producerId) values("%s","%s")""" % (attrs['id'],producer.attrs['id']) ) 

		for clip in attrs['clips']:
			clip.save()
			db.query("""replace into MovieClipsInShows (showId,movieClipId) values("%s","%s")""" % (attrs['id'],clip.attrs['id']) ) 

		db.store_result()

	def total_clip_duration(self):
		db.query('''
			select time(sum(mc.stop)-sum(mc.start)) as sum
			from
				MovieClipsInShows as map,
				MovieClips as mc
			where
				map.showId = "%s" and
				mc.id = map.movieClipId
			''' % (self.attrs['id']) )

		r = db.store_result()
		return r.fetch_row(how=1)[0]['sum']

	def get_xml(self):
		attrs = self.attrs
		xml = "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
		xml = xml+"<show>\n"
		xml = xml+"\t<id>%s</id>\n" % (attrs['id'])
		xml = xml+"\t<name>%s</name>\n" % (attrs['name'])
		xml = xml+"\t<producers>\n" 
		for producer in attrs['producers']:
			xml = xml+"\t\t<producer>\n"
			for k in ['id','name','email','phone']:
				xml = xml+"\t\t\t<%s>%s</%s>\n" % (k,producer.attrs[k],k)
			xml = xml+"\t\t</producer>\n"
		xml = xml + "\t</producers>\n"
		xml = xml + "\t<clips>\n"
		for clip in attrs['clips']:
			xml = xml+"\t\t<clip>\n"
			for k in ['id','name','description','start','stop']:
				xml = xml+"\t\t\t<%s>%s</%s>\n" % (k,clip.attrs[k],k)
			xml = xml+"\t\t</clip>\n"
		xml = xml + "\t</clips>\n"
		xml = xml+"</show>\n"
		return xml

	def __getattr__(self,name):
		if name is 'producers':
			return "\n\n".join( [ str(producer) for producer in self.attrs['producers'] ] )
				
		elif name is 'clips':
			return "\n\n".join( [ str(clip) for clip in self.attrs['clips'] ] )

	def __str__(self):
		attrs = self.attrs
		return "Show: %s\n\nProducers:\n%s\n\nMovieClips:\n%s" % (attrs['name'],self.producers,self.clips)

class MovieClip:

	def __init__(self,attrs=None):

		if attrs:
			self.attrs = attrs

	def save(self):
		attrs = self.attrs
		query = """replace into MovieClips (id,name,description,start,stop) values ("%s","%s","%s",time('%s'),time('%s')) """ % ( 
			attrs['id'], 
			attrs['name'], 
			attrs['description'], 
			attrs['start'], 
			attrs['stop'] 
		)

		db.query( query )
		db.store_result()

	def __str__(self):
		attrs = self.attrs
		return "\n".join( [ "%s: %s" % (k,attrs[k]) for k in ['name','start','stop','description'] ] )
	
class Producer:

	def __init__(self,attrs=None):
		if attrs:
			self.attrs = attrs

	def __str__(self):
		attrs = self.attrs
		return "\n".join( [ "%s: %s" % (k,attrs[k]) for k in ['name','email','phone'] ] )

	def save(self):
		attrs = self.attrs
		db.query("""replace into Producers (id,name,email,phone) values ("%s","%s","%s","%s") """ % ( attrs['id'],attrs['name'],attrs['email'],attrs['phone'] ) )
		db.store_result()

