#!/usr/bin/env python
#
# Por Ivan Rios @ivanrios
#
import random
import os
import logging
import urllib2,base64,simplejson
from xml.sax.saxutils import unescape
from datetime import datetime, timedelta

from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.runtime import DeadlineExceededError
from google.appengine.api.urlfetch import DownloadError 


class Latido(db.Model):
  Tipo = db.IntegerProperty();
  UltimoLatido = db.DateTimeProperty(auto_now_add=True)

class Mensajes(db.Model):
  Tipo = db.IntegerProperty()
  usuario = db.StringProperty()
  foto    = db.StringProperty()
  mensaje = db.TextProperty()
  random = db.FloatProperty(default=random.random()) 

def Randomea(mensajes):
	total_de_mensajes = 50
	keys = []
	i = 0
	for result in mensajes:
		keys.append(result)
	random.shuffle(keys)
	limitados = []
	for mensaje in keys:
		i += 1
		if i < total_de_mensajes:
			limitados.append(result)
	return limitados
	

def ObtieneTwitts():
	minutos_de_espera = 15
	busquedas = {}
	busquedas["1"] = "mexico%2Bhermoso%2Bpais"
	busquedas["2"] = "mexico%2B%22mi%2Bpais"
	busquedas["3"] = "amo%2B%22mi%2Bmexico"
	busquedas["4"] = "bello%2B%22mi%2Bmexico"
	latidos = db.GqlQuery("SELECT * FROM Latido")
	recargar = True
	tipo = 0
	for latido in latidos:
		tipo = latido.Tipo
		recargar =  datetime.now() - latido.UltimoLatido >= timedelta(minutes = minutos_de_espera)
		logging.info('__Log_Ultima descarga '+ str(latido.UltimoLatido))
	if tipo == None:
		tipo = 0
	if recargar: 	
		if tipo < 4:
			tipo = tipo + 1
		else:
			tipo = 1
		texto = busquedas[str(tipo)]
		logging.info('___Ya paso el tiempo suficiente, recargar twitts')
		theurl = 'http://search.twitter.com/search.json?lang=es&rpp=50&q=%s'%(texto)		
		handle = urllib2.Request(theurl)
		twitts = {}
		try:
			try:
				logging.info('Listo para obtener localmente. '+theurl)
				try:
					twitts = simplejson.load(urllib2.urlopen(handle))['results']
				except BaseException:
					results = 0
				except:
					pass
				q = db.GqlQuery("SELECT * FROM Mensajes where Tipo="+str(tipo))
				results = q.fetch(1000)
				logging.info('________ ya se solicitó al API ')
				if len(twitts)>0:
					db.delete(results)
					for twit in twitts:
						mensaje = Mensajes()
						mensaje.usuario = twit["from_user"]
						mensaje.foto = twit["profile_image_url"]
						mensaje.mensaje = unescape(twit["text"])
						mensaje.Tipo = tipo
						mensaje.random = random.random()
						mensaje.put()
				q = db.GqlQuery("SELECT * FROM Latido")
				results = q.fetch(1000)
				db.delete(results)
				latido = Latido()
				latido.UltimoLatido = datetime.now()
				latido.Tipo = tipo
				latido.put()
			except IOError, e:
				results = 0
		except DeadlineExceededError:
			self.response.clear()
			self.response.set_status(500)
			self.response.out.write("Algo vailó madre...")
			results = 0
	mensajes = db.GqlQuery("SELECT * FROM Mensajes LIMIT 250")
	return Randomea(mensajes.fetch(1000))

class AcercaHandler(webapp.RequestHandler):
		def get(self):
			data = {}
			data["head"] = template.render("views/header.html", data)
			data["footer"] = template.render("views/footer.html", data)
			path = os.path.join(os.path.dirname(__file__), 'views/acerca.html')
			self.response.out.write(template.render(path, data))

	
class MainHandler(webapp.RequestHandler):
	def get(self):
		data = {}
		data["head"] = template.render("views/header.html", data)
		data["footer"] = template.render("views/footer.html", data)
  	  	data["res"] = ObtieneTwitts()
		path = os.path.join(os.path.dirname(__file__), 'views/index.html')
		self.response.out.write(template.render(path, data))

def main():
  application = webapp.WSGIApplication([('/', MainHandler), ('/acerca', AcercaHandler)],debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
    main()