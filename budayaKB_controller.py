#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)

Last update: 23 November 2019

"""
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template, redirect, flash
from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()


#merender tampilan default(index.html)
@app.route('/')
def index():
	return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("imporBudaya.html")

	elif request.method == "POST":
		global databasefilename
		f = request.files['file']

		if f.filename.split(".")[-1] != "csv":
			warning = 1
			return render_template("imporBudaya.html", warning=warning)
		else:
			databasefilename=f.filename
			result_impor=budayaData.importFromCSV(f.filename)
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			warning = 0
			return render_template("imporBudaya.html", result=result_impor, fname=f.filename, warning=warning)

@app.route('/tambahBudaya', methods=['GET','POST'])
def tambahBudaya():
	if request.method == "GET":
		return render_template("tambahBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']
		tipe = request.form['tipe']
		provinsi = request.form['provinsi']
		url = request.form['url']

		if databasefilename != "":
			tambahState = budayaData.tambah(nama,tipe,provinsi,url)
		else:
			tambahState = 0

		try:
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			warning = 0
		except FileNotFoundError:
			warning = 1
		return render_template("tambahBudaya.html", tambahState=tambahState, nama=nama, warning=warning)	

@app.route('/ubahBudaya', methods=['GET','POST'])
def ubahBudaya():
	if request.method == "GET":
		return render_template("ubahBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']
		tipe = request.form['tipe']
		provinsi = request.form['provinsi']
		url = request.form['url']

		if databasefilename != "":
			ubahState = budayaData.ubah(nama,tipe,provinsi,url)
		else:
			ubahState = 0

		try:
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			warning = 0
		except FileNotFoundError:
			warning = 1
		return render_template("ubahBudaya.html", ubahState=ubahState, nama=nama, warning=warning)

@app.route('/hapusBudaya', methods=['GET','POST'])
def hapusBudaya():
	if request.method == "GET":
		return render_template("hapusBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']

		if databasefilename != "":
			hapusState = budayaData.hapus(nama)
		else:
			hapusState = 0

		try:
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			warning = 0
		except FileNotFoundError:
			warning = 1
		return render_template("hapusBudaya.html", hapusState=hapusState, nama=nama, warning=warning)

@app.route('/cariBudaya', methods=['GET','POST'])
def cariBudaya():
	if request.method == "GET":
		return render_template("cariBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']

		if nama.split() != []:
			if request.form['metode pencarian'] == "nama":
				cariState = budayaData.cariByNama(nama)
			elif request.form['metode pencarian'] == "tipe":
				cariState = budayaData.cariByTipe(nama)
			elif request.form['metode pencarian'] == "provinsi":
				cariState = budayaData.cariByTipe(nama)
		else:
			cariState = budayaData.cariSemua()

		length = len(cariState)

		# try:
		# 	budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
		# 	warning = 0
		# except FileNotFoundError:
		# 	warning = 1
		return render_template("cariBudaya.html",length=length, cariState=cariState, nama=nama)

@app.route('/statsBudaya', methods=['GET','POST'])
def statsBudaya():
	if request.method == "GET":
		return render_template("statsBudaya.html")

	elif request.method == "POST":
		nama = request.form['metode pencarian']

		if request.form['metode pencarian'] == "nama":
			cariState = budayaData.stat()
			length = cariState
			nama = "Nama"
		elif request.form['metode pencarian'] == "tipe":
			cariState = budayaData.statByTipe()
			length = len(cariState)
			nama = "Tipe"
		elif request.form['metode pencarian'] == "provinsi":
			cariState = budayaData.statByProv()
			length = len(cariState)
			nama = "Provinsi"

		# try:
		# 	budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
		# 	warning = 0
		# except FileNotFoundError:
		# 	warning = 1
		return render_template("statsBudaya.html",length=length, cariState=cariState, nama=nama)

# run main app
if __name__ == "__main__":
	app.run(debug=True)



