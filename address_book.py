# address_book.py
# Author : Ganesh Girase
# Date: 2016-11-08
#
# Description : Address book which provide facilities to add/edit Person/Group Details, Search Contacts
#

import json
import re
import os

class CAddressBook(object):
	#
	# Base Class
	# Description : Contains database activities like contact addition,
	# 				modification, user/group search
	
	def get_new_uuid(this):
		# Returns uuid for every new record
		if len(this.db['Contacts']) == 0:
			uuid = 0
		else:
			uuid = this.db['Contacts'][-1]['Uuid'] + 1
		return uuid
		
	# Add Person details to database
	def add_contact(this, record):		
		groupId = 'COMMON' if len(record['Group']) == 0 else record['Group']
		uuid = this.get_new_uuid()
		record.update({'Uuid': uuid, 'Group': groupId})
		this.db['Contacts'].append(record)					
		
	# Edit person details.
	def update_contact(this, record): 
		this.db['Contacts'][record['Uuid']] = record
		return True
		
	# Delete user record from database
	def delete_contact(this, record): 
		del this.db['Contacts'][record['Uuid']]
		return True
		
	def search_by_uuid(this):
		# Search database records by uuid
		uuid = int(raw_input("Please provide uuid: ").strip())
		if 0 <= uuid < len(this.db['Contacts']):
			return this.db['Contacts'][uuid]
		else:
			print " !! No record found !! "
			return False	
			
	def search_by_key(this, key): 
		# Search database record by given key
		search_term = raw_input("Please provide %s: " %key).strip()
		return [ rec['Uuid'] for rec in this.db['Contacts'] if rec[key] == search_term ]
	
	
	# Give database records provided on search key and it's value
	def search(this):
		print "\n\tSearch contact you want to update using below params"
		search_terms = ['Uuid', 'First Name', 'Last Name', 'Email']
		for num, sub in enumerate(search_terms):
			print "%s) %s" %(num + 1, sub)
		num = int(raw_input("Please provide option: ").strip())
		if 0 < num < 5:
			if num == 1:
				return this.search_by_uuid()
			else:
				records = this.search_by_key(search_terms[num - 1])
				if len(records) > 0:
					return this.db['Contacts'][records[0]]
				else:
					print "No record found"
		else:
			print "Error ==> Invalid options !! "
	## 
	# Initializes json database from file
	def __init__(this, db_file="address_book.json"):
		print "Welcome to address book !! "
		this.database_file = db_file
		this.db = dict()		
		if os.path.exists(this.database_file):
			with open(db_file) as database_file:				
				this.db = json.load(database_file)
		else:
			this.db['Contacts'] = []
			this.db['Uids'] = []			
				
	
	def fini(this):	
		# Write database structure to file in json format.
		#
		with open(this.database_file, 'w') as database_file:
			json.dump(this.db, database_file)
		
			
class CPersonContact(CAddressBook, object): 
	#
	# Class for adding person related information.
	# 
	def add_personal_details(this):
		# Add personal details 
		print "\n\tPlease fill below form to add new user"
		data = dict()
		for field in ('First Name', 'Last Name', 'Street Address', 'Email', 'PhoneNo', 'Group'):
			data[field] = raw_input("\t%s: " %field).strip()
		return this.add_contact(data)
		
	def update_person_contact(this):
		# Update person contact on the basis of uuid		
		rec = this.search()
		if rec.keys() and len(rec.keys()) > 0:
			print "Your searched record is as below:- "
			print rec
			print "Please provide which key you want to modify !! "
			key = raw_input("Key need to modify: ").strip()
			val = raw_input("New value for key '%s': " %key).strip()
			rec[key] = val
			return this.update_contact(rec)			
		else:
			print "No record found\n"
			return False
			
	def delete_person_contact(this):		
		# Delete person from address book
		print "\n\tSearch contact you want to delete using below params"
		rec = this.search()	
		if len(rec.keys()) > 0:
			print "Your searched record is as below:- "
			print rec
			return this.delete_contact(rec)			
		else:
			print "No record found\n"
			return False
		
class CGroup(CAddressBook, object): pass
class CRunAddressBook(CPersonContact, CGroup, object): 
	# This class is user interface which ask user
	# for various details like if person/group detail 
	# if he want to add person details.
	
	def run(this):
		# Running address book
		print "Please select option from below services.."
		print "1) Add Contact\n2) Edit Contact\n3) Delete contact\n4) Search Contact\n5) Add Group"
		num = int(raw_input("Please enter your choice number: ").strip())
		if num == 1:
			this.add_personal_details()
			print "Thanks. Record added successfully !!"
		elif num == 2:
			this.update_person_contact()
			print "Thanks. Record updated successfully !!"	
		elif num == 3:
			this.delete_person_contact()
			print "Thanks. Record deleted successfully !!"		
		elif num == 4:			
			print "Below is your record:-\n %s\n" %this.search()
		ans = raw_input("Do you want to run service again ?[Y/N]: ").strip()
		if ans == 'Y':	this.run()
		
	
		
if __name__ == "__main__":
	obj = CRunAddressBook()
	obj.run()
	obj.fini()
