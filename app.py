from flask import Flask, render_template, url_for, request, redirect, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

konekcija = mysql.connector.connect(
	host="192.168.33.10",
	user="root",
	passwd="root",
	database="evIdencija_studenata"
)

kursor = konekcija.cursor(dictionary=True)

def ulogovan():
	if 'ulogovani_korisnik' in session:
		return True
	else: return False

app = Flask(__name__)
app.secret_key = 'nasTajniKljuc'

sid = 0

@app.route('/')
def index():
	if ulogovan(): return redirect(url_for('studenti'))
	else: return redirect(url_for('login'))
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		forma = request.form
		upit = "SELECT * FROM korisnici WHERE email=%s"
		podaci = (forma['email'],)
		kursor.execute(upit, podaci)
		korisnik = kursor.fetchone()
		if korisnik == None:
			flash('E-mail je pogrešan')
			return render_template('login.html')
		if check_password_hash(korisnik['lozinka'], forma['lozinka']):
			session['ulogovani_korisnik'] = str(korisnik)
			return redirect(url_for('studenti'))
		else:
			flash('Šifra je pogrešna')
			return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('ulogovani_korisnik', None)
	return redirect(url_for('login'))

@app.route('/studenti')
def studenti():
	if ulogovan():
		upit = "SELECT * FROM studenti"
		kursor.execute(upit)
		studenti = kursor.fetchall()
		return render_template('studenti.html', studenti=studenti)
	else: return redirect(url_for('login'))
	
@app.route('/student_novi', methods=['GET', 'POST'])
def student_novi():
	if request.method == "GET":
		return render_template('student_novi.html')
	elif request.method == "POST":
		forma = request.form
		upit = """INSERT INTO 
		studenti (ime, ime_roditelja, prezime, broj_indeksa, godina_studija, JMBG, datum_rodjenja, broj_telefona, email)
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		vrednosti = (forma['ime'],forma['ime_roditelja'],forma['prezime'],forma['broj_indeksa'],forma['godina_studija'],forma['JMBG'],forma['datum_rodjenja'],forma['broj_telefona'],forma['email'])
		kursor.execute(upit, vrednosti)
		konekcija.commit()
		return redirect(url_for('studenti'))

@app.route('/student_izmena/<id>', methods=['GET', 'POST'])
def student_izmena(id):
	if request.method == "GET":
		upit = "SELECT * FROM studenti WHERE id=%s"
		vrednost = (id,)
		kursor.execute(upit, vrednost)
		student = kursor.fetchone()
		return render_template('student_izmena.html', student=student)
	elif request.method == "POST":
		forma = request.form
		upit = """UPDATE studenti SET
		ime=%s,
		ime_roditelja=%s,
		prezime=%s,
		broj_indeksa=%s,
		godina_studija=%s,
		JMBG=%s,
		datum_rodjenja=%s,
		broj_telefona=%s,
		email=%s
		WHERE id=%s
		"""
		vrednosti = (forma['ime'],forma['ime_roditelja'],forma['prezime'],forma['broj_indeksa'],forma['godina_studija'],forma['JMBG'],forma['datum_rodjenja'],forma['broj_telefona'],forma['email'],id)
		kursor.execute(upit, vrednosti)
		konekcija.commit()
		return redirect(url_for('studenti'))

@app.route('/student_brisanje/<id>')
def student_brisanje(id):
	upit = "DELETE FROM studenti WHERE id=%s"
	vrednost = (id,)
	kursor.execute(upit, vrednost)
	konekcija.commit()
	return redirect(url_for('studenti'))

@app.route('/student/<id>')
def student(id):
	global sid
	sid = id
	print(sid)
	upit = "SELECT * FROM studenti WHERE id=%s"
	vrednost = (id,)
	kursor.execute(upit, vrednost)
	student = kursor.fetchone()
	upit = "SELECT id, naziv FROM predmeti"
	kursor.execute(upit)
	predmeti = kursor.fetchall()
	upit = """SELECT ocene.id, ocene.ocena, predmeti.sifra, predmeti.naziv, predmeti.godina_studija, predmeti.obavezni_izborni, predmeti.espb
	FROM ocene
	JOIN predmeti ON predmeti.id = ocene.predmet_ID
	WHERE ocene.student_id=%s
	GROUP BY ocene.id
	"""
	kursor.execute(upit, vrednost)
	ocene = kursor.fetchall()
	session['url'] = url_for('student', id=id)
	""" print(session['url'].split("/")[-1])
	print(session['url']) """
	return render_template('student.html', student=student, predmeti=predmeti, ocene=ocene)

updOcena = """UPDATE studenti SET prosek_ocena= 
(
	SELECT AVG(ocena) FROM ocene
	WHERE ocene.student_id = %s
)
WHERE id=%s"""

updESPB = """UPDATE studenti SET espb=
(
	SELECT SUM(espb) FROM ocene
	JOIN predmeti ON predmeti.id = ocene.predmet_id
	WHERE ocene.student_id = %s
)
WHERE id=%s"""

@app.route('/ocena_nova/<id>', methods=['POST'])
def ocena_nova(id):
	forma = request.form
	upit = "INSERT INTO ocene (student_id, predmet_id, ocena, datum) VALUES (%s,%s,%s,%s)"
	vrednosti = (id,forma['predmet'],forma['ocena'],forma['datum'])
	kursor.execute(upit, vrednosti)
	kursor.execute(updOcena, (id,id,))
	kursor.execute(updESPB, (id,id,))
	konekcija.commit()
	return redirect(session['url'])

@app.route('/ocena_izmena/<id>', methods=['GET', 'POST'])
def ocena_izmena(id):
	if request.method == 'GET':
		upit = "SELECT predmeti.naziv, ocene.ocena, ocene.datum FROM ocene JOIN predmeti ON predmeti.id = ocene.predmet_id WHERE ocene.id = %s"
		kursor.execute(upit, (id,))
		podaci = kursor.fetchone()
		return render_template('ocena_izmena.html', podaci=podaci)
	elif request.method == 'POST':
		upit = "UPDATE ocene SET ocena=%s, datum=%s WHERE id=%s"
		forma = request.form
		vrednosti = (forma['ocena'], forma['datum'], id)
		kursor.execute(upit, vrednosti)
		kursor.execute(updOcena, (sid,sid,))
		kursor.execute(updESPB, (sid,sid,))
		konekcija.commit()
		return redirect(url_for('student', id=sid))

@app.route('/ocena_brisanje/<id>')
def ocena_brisanje(id):
	upit = "DELETE FROM ocene WHERE id=%s"
	vrednost = (id,)
	kursor.execute(upit, vrednost)
	student_id = session['url'].split("/")[-1]
	kursor.execute(updOcena, (student_id,student_id,))
	kursor.execute(updESPB, (student_id,student_id,))
	konekcija.commit()
	return redirect(session['url'])

@app.route('/korisnici')
def korisnici():
	if ulogovan():
		sql = "SELECT * FROM korisnici"
		kursor.execute(sql)
		korisnici = kursor.fetchall()
		return render_template('korisnici.html', korisnici=korisnici)
	else:
		return redirect(url_for('login'))

@app.route('/korisnik_novi', methods=['GET', 'POST'])
def korisnik_novi():
	if request.method == 'GET':
		return render_template('korisnik_novi.html')
	elif request.method == 'POST':
		podaci = request.form
		sql = """ INSERT INTO 
				korisnici (ime, prezime, email, lozinka) 
				VALUES (%s,%s,%s,%s)
				"""
		hesmani = generate_password_hash(podaci['lozinka'])
		vrednosti = (podaci['ime'],podaci['prezime'],podaci['email'],hesmani)
		kursor.execute(sql, vrednosti)
		konekcija.commit()
		return redirect(url_for('korisnici'))

@app.route('/korisnik_izmena/<id>', methods=['GET', 'POST'])
def korisnik_izmena(id):
	if request.method == 'GET':
		upit = "SELECT * FROM korisnici WHERE id=%s"
		vrednost = (id,)
		kursor.execute(upit, vrednost)
		korisnik = kursor.fetchone()
		return render_template('korisnik_izmena.html', korisnik=korisnik)
	elif request.method == 'POST':
		upit = """UPDATE korisnici SET
			ime=%s,
			prezime=%s,
			email=%s,
			lozinka=%s
			WHERE id=%s
			"""
		forma = request.form
		hesmani = generate_password_hash(forma['lozinka'])
		vrednosti = (forma['ime'], forma['prezime'], forma['email'], hesmani, id)
		kursor.execute(upit, vrednosti)
		konekcija.commit()
		return redirect(url_for('korisnici'))

@app.route('/korisnik_brisanje/<id>')
def korisnik_brisanje(id):
	upit = "DELETE FROM korisnici WHERE id=%s"
	vrednost = (id,)
	kursor.execute(upit, vrednost)
	konekcija.commit()
	return redirect(url_for('korisnici'))

@app.route('/predmeti')
def predmeti():
	if ulogovan():
		upit = "SELECT * FROM predmeti"
		kursor.execute(upit)
		predmeti = kursor.fetchall()
		return render_template('predmeti.html', predmeti=predmeti)
	else: return redirect(url_for('login'))

@app.route('/predmet_novi', methods=["POST", "GET"])
def predmet_novi():
	if request.method == "GET":
		return render_template('predmet_novi.html')
	elif request.method == "POST":
		forma = request.form
		upit = "INSERT INTO predmeti (sifra, naziv, godina_studija, espb, obavezni_izborni) VALUES (%s,%s,%s,%s,%s)"
		vrednosti = (forma['sifra'],forma['naziv'],forma['godina_studija'],forma['espb'],forma['obavezni_izborni'])
		kursor.execute(upit, vrednosti)
		konekcija.commit()
		return redirect(url_for('predmeti'))

@app.route('/predmet_izmena/<id>', methods=['GET', 'POST'])
def predmet_izmena(id):
	if request.method == "GET":
		upit = "SELECT * FROM predmeti WHERE id=%s"
		vrednost = (id,)
		kursor.execute(upit, vrednost)
		predmet = kursor.fetchone()
		return render_template('predmet_izmena.html', predmet=predmet)
	elif request.method == "POST":
		upit = "UPDATE predmeti SET sifra=%s, naziv=%s, godina_studija=%s, espb=%s, obavezni_izborni=%s WHERE id=%s"
		forma = request.form
		podaci = (forma['sifra'],forma['naziv'],forma['godina_studija'],forma['espb'],forma['obavezni_izborni'],id)
		kursor.execute(upit, podaci)
		konekcija.commit()
		return redirect(url_for('predmeti'))

@app.route('/predmet_brisanje/<id>')
def predmet_brisanje(id):
	upit = "DELETE FROM predmeti WHERE id=%s"
	vrednost = (id,)
	kursor.execute(upit, vrednost)
	konekcija.commit()
	return redirect(url_for('predmeti'))

app.run(debug=True)
