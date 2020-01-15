from collections import Counter

import module
import tutor
import ReaderWriter
import timetable
import random
import math

from pip._vendor.msgpack.fallback import xrange


class Scheduler:

	def __init__(self,tutorList, moduleList):
		self.tutorList = tutorList
		self.moduleList = moduleList

	#Using the tutorlist and modulelist, create a timetable of 5 slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, Smith, CS101, "module")
	#This line will set the session slot '1' on Monday to the module CS101, taught by tutor Smith. 
	#Note here that Smith is a tutor object and CS101 is a module object, they are not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3. 
	#Tutor (3rd argument) and module (4th argument) can be assigned any value, but if the tutor or module is not in the original lists, 
	#	your solution will be marked incorrectly. 
	#The final, 5th argument, is the session type. For task 1, all sessions should be "module". For task 2 and 3, you should assign either "module" or "lab" as the session type.
	#Every module needs one "module" and one "lab" session type. 
	
	#moduleList is a list of Module objects. A Module object, 'm' has the following attributes:
	# m.name  - the name of the module
	# m.topics - a list of strings, describing the topics that module covers e.g. ["Robotics", "Databases"]

	#tutorList is a list of Tutor objects. A Tutor object, 't', has the following attributes:
	# t.name - the name of the tutor
	# t.expertise - a list of strings, describing the expertise of the tutor. 

	#For Task 1:
	#Keep in mind that a tutor can only teach a module if the module's topics are a subset of the tutor's expertise. 
	#Furthermore, a tutor can only teach one module a day, and a maximum of two modules over the course of the week.
	#There will always be 25 modules, one for each slot in the week, but the number of tutors will vary.
	#In some problems, modules will cover 2 topics and in others, 3.
	#A tutor will have between 3-8 different expertise fields. 

	#For Task 2 and 3:
	#A tutor can only teach a lab if they have at least one expertise that matches the topics of the lab
	#Tutors can only manage a 'credit' load of 4, where modules are worth 2 and labs are worth 1.
	#A tutor can not teach more than 2 credits per day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need. 
	#Furthermore, you should not import anything else beyond what has been imported above. 

	# This method should return a timetable object with a schedule that is legal according to all constraints of task 1.
	def createSchedule(self):
		# Do not change this line
		timetableObj = timetable.Timetable(1)
		
		# Here is where you schedule your timetable

		# This line generates a random timetable, that may not be valid. You can use this or delete it.
	#	self.randomModSchedule(timetableObj)
		self.lab(timetableObj)
		# Do not change this line
		return timetableObj

	#Now, we have introduced lab sessions. Each day now has ten sessions, and there is a lab session as well as a module session.
	#All module and lab sessions must be assigned to a slot, and each module and lab session require a tutor.
	#The tutor does not need to be the same for the module and lab session.
	#A tutor can teach a lab session if their expertise includes at least one topic covered by the module.
	#We are now concerned with 'credits'. A tutor can teach a maximum of 4 credits. Lab sessions are 1 credit, module sessiosn are 2 credits.
	#A tutor cannot teach more than 2 credits a day.
	def createLabSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)
		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.		
		self.randomModAndLabSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#It costs £500 to hire a tutor for a single module.
	#If we hire a tutor to teach a 2nd module, it only costs £300. (meaning 2 modules cost £800 compared to £1000)
	#If those two modules are taught on consecutive days, the second module only costs £100. (meaning 2 modules cost £600 compared to £1000)

	#It costs £250 to hire a tutor for a lab session, and then £50 less for each extra lab session (£200, £150 and £100)
	#If a lab occurs on the same day as anything else a tutor teaches, then its cost is halved. 

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible. 
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here. 
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		self.randomModAndLabSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	# This simplistic approach merely assigns each module to a random tutor, iterating through the timetable.
	def randomModSchedule(self, timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "module")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	def lab(self, timetableObj):
		# Legal module Schedule - used in task1
		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		num = 0
		chck = 0
		available = list()
		for module in self.moduleList:
			for tutor in self.tutorList:
				# TODO - Constraint checking
				# 1 - Is tutor an expert at module ?
				# 2 - Is tutor already teaching a module on that chosen day ?
				# 3 - Is tutor already teaching 2 times ?
				if set(module.topics) <= set(tutor.expertise):
					if sessionNumber == 1 and dayNumber ==0:
						timetableObj.addSession(days[dayNumber], sessionNumber, tutor, module, "module")
					else:
						available.append((tutor.name, module.name))
						for i in range(0, len(available), 5):
							avb = available[i:i + 5]
							# if set(available[i]).intersection(set(available[i+1])):
							# 	print(available[i])
							for j in range(0, len(avb)):
								if avb[0] != avb[j]:
									res = self.remove_duplicates(available)
									timetableObj.addSession(days[dayNumber], sessionNumber, tutor, module, "module")

			sessionNumber = sessionNumber + 1
			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber+1
		print(len(available))
		print(available[2][0])

		res = self.remove_duplicates(available)
		print(res)
		print(len(res))
		#res = list(set(tuple(sorted(sub)) for sub in available))
		#print(res)
		#print(len(res))

		# counted = Counter(available)
		#
		# temp_lst = []
		# for el in counted:
		# 	if counted[el] > 2:
		# 		temp_lst.append(el)
		#
		# res_lst = []
		# for el in available:
		# 	if el not in temp_lst:
		# 		res_lst.append(el)
		# print(res_lst)
		# print(len(res_lst))


		#print(available[2][0])
		# for i in range(0, len(available)):
		# 	for j in range(i+1, len(available)):
		# 	#	print(available[i][0])
		# 		#print(available[i][0])
		# 		#sol.append(available[j][0])
		# 		if available[i][0] == available[j][0]:
		# 			#print(i,j)
		# 			if (chck >= 2):
		# 				chck = 1
		# 			chck = chck +1
					#print(chck)
					#print(i,j)

						#available.remove(available[j][0])
					#	del available[j][0]

					#print(available[i])

		print("=============dda=========")
		print(len(available))
		#print(available[2][0])
			#print(avb)
		#print(avb)
		print("======================")
	#	print(available)
	# Legal module schedule
	def remove_duplicates(self,lista):
		lista2 = []
		if lista:
			for item in lista[0:len(lista)][0]:
				if item not in lista2:  # is item in lista2 already?
					lista2.append(item)
		else:
			return lista
		return lista2
	def legalModSchedule(self, timetableObj):

		# List of tutors who have already tutored on that day
		constraintOneADay = []
		# List of tutors who have tutored twice already in the week
		constraintTwoAWeek = []

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		tutorCounter = 0

		for module in self.moduleList:
			# TODO - before adding to the session we need to check:
			# (1) is tutor expert at module ?
			# (2) is tutor already teaching that day? - could remove them from the list ?
			# (3) is tutor already teaching more than 2 a day - could remove them from the list ?

			for tutor in self.tutorList:

				# Observe current tutor for constraints
				currentTutor = tutor.name

				if module.topics == tutor.expertise:
					# Hes an expert !
					# TODO doesnt Satisfy (2/3)
					if timetableObj.getSession(days[dayNumber], sessionNumber) == currentTutor:
						# Tutor has already taught on that day - 1st constraint violated
						break
					#  Need to check if the tutor teaches more than twice a week
					elif constraintTwoAWeek.count(currentTutor) > 2:
						break
					else:
						# Before adding we need to check has it been inserted before ?
						if not timetableObj.addSession(days[dayNumber],  sessionNumber):
							timetableObj.addSession(days[dayNumber], sessionNumber, tutor, module, "module")
							constraintTwoAWeek.append(currentTutor)
							constraintOneADay.append(currentTutor)
							sessionNumber += 1

							if sessionNumber == 6:
								sessionNumber = 1
								dayNumber += 1




	#This simplistic approach merely assigns each module and lab to a random tutor, iterating through the timetable.
	def randomModAndLabSchedule(self, timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "module")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "lab")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1


























