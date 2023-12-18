import random
import re
class ApptGenerator:
    
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.facultyNames = []
        self.studentListGrads = []
        self.studentListNonGrads = []
        self.studentPref = []
        self.parseFile()

        #create dictionary of profs to hold 12 appointments each as values
        self.facultyMap = {name: 12 for name in self.facultyNames}

        self.gradNumber = len(self.studentListGrads)
        self.studentMasterList = self.studentListGrads + self.studentListNonGrads

    def parseFile(self):
        self.facultyNames.clear()
        self.studentListGrads.clear()
        self.studentListNonGrads.clear()
        try:
            with open(self.file_path, 'r') as file:
                currentSection = None
                for line in file:
                    line = line.strip()  # Remove leading/trailing whitespaces
                    if not line:
                        continue  # Skip empty lines

                    # Check for section start and end markers
                    if "FACULTY" in line:
                        currentSection = "FACULTY"
                    elif "STUDENTS_GRAD" in line:
                        currentSection = "STUDENTS_GRAD"
                    elif "STUDENTS_NONGRAD" in line:
                        currentSection = "STUDENTS_NONGRAD"
                    elif "END_FACULTY" in line:
                        currentSection = None
                    elif "END_STUDENTS_GRAD" in line:
                        currentSection = None
                    elif "END_STUDENTS_NONGRAD" in line:
                        currentSection = None
                    else:
                        # Add line to the appropriate list based on the current section
                        if currentSection == "FACULTY":
                            self.facultyNames.append(line)
                        elif currentSection == "STUDENTS_GRAD":
                            self.studentListGrads.append(line)
                        elif currentSection == "STUDENTS_NONGRAD":
                            self.studentListNonGrads.append(line)

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            self.content = ""

        print('\n')
        print(self.studentListGrads)
        print('\n')
        print(self.facultyNames)

    def preferenceParse(self): #set up appt slots, set grad number and parse preferences
        

        for index, student in enumerate(self.studentMasterList):
            # Find the index of the first digit
            match = re.search(r'\d', student)
            if match:
                start_index = match.start()
                # Extract the preference list from the string
                prefSelection = student[start_index:]
                self.studentPref.append(prefSelection)

                #print('\n')
                #print('STUDENT PREFERENCES WHILE ITERATING')
                #print(self.studentPref)
                
                # Modify the corresponding student in the master list
                self.studentMasterList[index] = student[:start_index]
            else:
                # Handle cases where no digits are found
                self.studentPref.append("No Preferences")
        
        #split studentpref into a list of lists
        #print('\n')
        #print('STUDENT PREFERENCES BEFORE SPLIT')
        #print(self.studentPref)

        #if isinstance(self.studentPref[1], str):
        self.studentPref = [[int(num) for num in pref.split(',')] for pref in self.studentPref]
        print('\n')
        print('STUDENT PREFERENCES BELOW')
        print(self.studentPref)
        


    def generateOrder(self): #generate order which students choose prof appts. removed  -> List[int]

        #generate list of grad order from 1 to gradnumber
        gradOrder = list(range(0, self.gradNumber))
        #generate random list of non grad order from gradnumber to 40
        otherStudentOrder = list(range(self.gradNumber, 40))
        
        random.shuffle(gradOrder)
        random.shuffle(otherStudentOrder)

        self.totalOrder = gradOrder + otherStudentOrder
        #make a list of lists out of totalorder
        print('\n')
        print('TOTAL ORDER AFTER GENERATEORDER BEFORE PREF LIST')
        print(self.totalOrder)

    def pickAppts(self):

        #iterate through list assigning Appt slot to each student in turn from remaining available slot
        #run 3 times until 3 slots for each student chosen

        self.unsortedFacultyAppts = [[] for name in self.facultyNames]

        for picks in range(3):
            for order in range(len(self.totalOrder)):
                option = 0
                
                while True:
                    # Ensure choice is within the range of facultyNames
                    if option >= len(self.facultyNames):
                        print("outside range of faculty")
                        break

                    if order >= len(self.totalOrder):
                        break

                    student = self.totalOrder[order]

                    student_pref_list = self.studentPref[order]  # This should be a list of preferences
                    print('\n')
                    print('student ' + str(student))
                    print('STUDENT_PREF_LIST BELOW')
                    print(student_pref_list)

                    # Assign first preference to option (index 0 initially)
                    temp_preference = student_pref_list[option]  # or student_pref_list[some_other_index]

                    print('\n')
                    print('temp_preference ' + str(temp_preference))

                    # Use this preference to get the corresponding faculty name
                    professor_key = self.facultyNames[temp_preference - 1]

                    #Check if the selected faculty member is available
                    if self.facultyMap[professor_key] > 0 and student not in self.unsortedFacultyAppts[self.facultyNames.index(professor_key)]:
                        self.facultyMap[professor_key] -= 1
                        professor_index = self.facultyNames.index(professor_key)  # Find the index of the faculty
                        self.unsortedFacultyAppts[professor_index].append(student)
                        print('\n')
                        print('student ' + str(student))
                        print('PROFESSOR INDEX AFTER ADD')
                        print(self.facultyNames[professor_index])
                        print(self.unsortedFacultyAppts[professor_index])
                        break
                    else:
                        option += 1
                
        print('\n')
        print('UNSORTED APPTS')
        print(self.unsortedFacultyAppts)

    
    def sortAppts(self):
        #given 12 * 12 list of students for each prof ensure that no student number occurs > once in the same index
        #The original list of lists (a 12x12 matrix) is transposed. 
        #This means that what were originally rows (each list in list of lists) become columns.
        
        # Find the length of the longest list
        max_length = max(len(sublist) for sublist in self.unsortedFacultyAppts)

        # Pad shorter lists with None to make all lists of equal length
        padded_lists = [sublist + [None] * (max_length - len(sublist)) for sublist in self.unsortedFacultyAppts]

        # Transpose the matrix
        transposed = list(map(list, zip(*padded_lists)))

        # Shuffle each 'row' in the transposed matrix
        for row in transposed:
            # Filter out None before shuffling
            filtered_row = [x for x in row if x is not None]
            random.shuffle(filtered_row)
            # Add None back to maintain the row length
            row[:len(filtered_row)] = filtered_row

        # Transpose back to original orientation and remove None
        self.sortedFacultyAppts = [list(filter(None.__ne__, sublist)) for sublist in zip(*transposed)]

    def printAppts(self, file=None):
        self.preferenceParse()
        self.generateOrder()
        self.pickAppts()
        self.sortAppts()

        #make a list of lists using facultyNames
        masterList = [['\n' + name + ':'] for name in self.facultyNames]

        #return self.studentMasterList
        #return self.facultyNames
        #return self.facultyMap
        #return self.unsortedFacultyAppts
        print('SORTED FACULTY APPTS IN PRINTAPPS')
        print(self.sortedFacultyAppts)
        #return self.studentPref
        #return masterList
        
        for prof_sublist, student_indices in zip(masterList, self.sortedFacultyAppts):
        # prof_sublist[0] is the professor's name
        # student_indices is a list of indices corresponding to students for this professor
            for student_index in student_indices:
                # Append the student name to the professor's sublist
                # Ensure that the index is valid
                if 0 <= student_index <= len(self.studentMasterList):
                    prof_sublist.append('\n  ' + self.studentMasterList[student_index - 1])

        #return self.studentMasterList
        #return self.studentListGrads
        #return self.facultyNames

        #return self.sortedFacultyAppts
        #return self.totalOrder
        #for name in range(len(masterList)):
            #output = '\n' + str(masterList[name])
        for sublist in masterList:
            output = ' '.join(sublist)
            if file:
                print(output, file=file)
            else:
                print(output)

generator = ApptGenerator('data/studentProfInput.txt')  # Create an instance of ApptGenerator
#appointments = generator.printAppts()  # Call the printAppts method we were calling this twice breaking things

#print(appointments)

with open('output.txt', 'w') as file:
    generator.printAppts(file=file)

        
        