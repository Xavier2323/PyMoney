import sys
import datetime

#the overall structure
#class1 : Record
#           mem fun1 : constructor
#           @prop getter methods
#========================================
#class2 : Records
#           mem fun1 : constructor
#           mem fun2 : add
#           mem fun3 : view
#           mem fun4 : delete
#           mem fun5 : find
#           mem fun6 : save
#========================================
#class3 : Categories
#           mem fun1 : constructor
#           mem fun2 : view
#           mem fun3 : is_category_valid
#           mem fun4 : find_subcategorie
#========================================
#try-except build a user interface

#===============================================================================================================================================================

class Record:
    """Represent a record"""

    def __init__(self, category, description, amount, record_time):
        """initialize the category, description, amount, record_time"""
        self._category = category
        self._description = description
        self._amount = amount
        self._time = record_time
        
    @property
    def category(self):
        """get the category"""
        return self._category
    @property
    def description(self):
        """get the descroption"""
        return self._description
    @property
    def amount(self):
        """get the amount"""
        return self._amount
    @property
    def time(self):
        """get the time that user input a record at"""
        return self._time

#========================================================================================================================================================================
class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """ initialize the record"""
        self._records = []
        try:
            with open('record.txt', 'r') as fh:     
                self._initial_money = int(fh.readline())
                L = fh.readlines()
                for item in L:
                    record = item.strip('\n').split(', ')
                    self._records.append(Record(record[0],record[1],int(record[2]),record[3]))
                print('Welcome back!')  #if the record.txt is not empty, it indicate that it is not the first use.
        except FileNotFoundError:   #record.txt not found
            self._initial_money = int(input('How much money do you have? '))  
        except ValueError:  #not integer
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n') #if the input is illegal, set initial to 0
            self._initial_money = int(0) 
        
    def add(self, categories): 
        """add new expense or incomes"""
        while True :
            record = input('\nAdd an expense or income record with category, description and amount:(separate by space)\n')
            try:
                record = record.split()     #record may be like ['meal','lunch','-50']
                if categories.is_category_valid(record[0]) == True:
                    self._records.append(Record(record[0], record[1], int(record[2]), datetime.datetime.now().strftime("%Y-%m-%d")))       #('meal','lunch',-50)
                else:
                    sys.stderr.write('\nThe specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to record\n')
            except (IndexError, ValueError):    #Wrong format
                sys.stderr.write('\nI Invalid input. Fail to add a record.\nThe correct form should be like:meal lunch -70\n')
            mode = input('Stay in the add mode?(Y/n): ')
            if mode not in {'Y','y'}:
                print('Exit add mode.'); break

    def view(self):
        """let user to view all the expense, income, current money."""
        
        print(f"{'Date':<13s}{'Categorie':<20s}{'Description':<20s}{'Amount':s}")  
        print('===========  ==================  ==================  ==========')
        
        total = int(0)
        for item in self._records: 
            date = item.time
            print(f'{date:<13s}{item.category:<20s}{item.description:<20s}{item.amount:d}')
            total += item.amount
        print('===========  ==================  ==================  ==========')
        print(f'Now you have {self._initial_money + total} dollars.')

    def delete(self):
        """let user to delete one of the data"""
        try:
            while True :
                del_item = input('Which description do you want to delete?\n')
                target = []
                for i, item in enumerate(self._records):
                    if item.description == del_item: 
                        target.append([i,item])

                if len(target) == 0: 
                    print('\nThis description do not exist.\nFail to delete a record.')
                else:
                    print(f"{'label':<8s}{'Description':<20s}{'Amount':<11s}{'Time':s}")
                    print('======  ==================  =========  ========================')
                    for i, item in target: 
                        print(f'{i:<7d} {item.description:<20s}{item.amount:<11d}{item.time:s}')
                    print('======  ==================  =========  ========================')
                    
                    del_label = input('\nEnter the label number you want to delete: ')
                    if int(del_label) < 0 or (int(del_label) + 1) > len(self._records) or self._records[int(del_label)].description != del_item : 
                        print('Invalid label')
                    else:
                        self._records.pop(int(del_label))
                mode = input('Stay in the delete mode?(Y/n): ')
                if mode not in {'Y','y'}:
                    print('Exit delete mode.'); break

        except ValueError:
            sys.stderr.write('\nPlease enter label number(int)\nRestart delete\n')
            self.delete()

    def find(self, target_categories):
        """check out the content in some category"""
        if target_categories == []:
            sys.stderr.write('\nThis category does not exist.\n')
        else:
            target = list(filter(lambda n: n.category in target_categories, self._records))
            
            print(f"{'Date':<13s}{'Categorie':<20s}{'Description':<20s}{'Amount':s}")  
            print('===========  ==================  ==================  ==========')
            total = int(0)
            for item in target:    
                print(f'{item.time:<13s}{item.category:<20s}{item.description:<20s}{item.amount:d}')
                total += item.amount

            print('===========  ==================  ==================  ==========')
            print(f'The total amount above is {total}.')

    def save(self):
        """save the record"""
        with open('record.txt', 'w') as fh:
            fh.write(str(self._initial_money) + '\n')
            for record in self._records:
                fh.write(str(record.category)+', '+str(record.description)+', '+str(record.amount)+', '+str(record.time) + '\n')

#========================================================================================================================================================
class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """initialize all the categories"""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway'],'other'], 'income', ['salary', 'bonus']]

    def view(self,categories = [],level = 0):
        """let user to view all the categories"""
        if categories == []:
            categories = self._categories
        if type(categories) == list:
            for sub in categories:
                self.view(sub,level+1)
        else:
            print(f'{" "*2*(level-1)}- {categories}')

    def is_category_valid(self, category):
        """check whether the input category is valid"""
        if len(self.find_subcategories(category)) > 0:
            return True
        else :
            return False

    def find_subcategories(self, category):
        """let user to find out the item inside"""
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list: # recursive case
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child,found=found)
                    if child == category and index+1 < len(categories) and type(categories[index+1]) == list:
                        yield from find_subcategories_gen(category,categories[index+1],found=True)
            else: # base case
                if categories == category or found == True:
                    yield categories

        return  [x for x in find_subcategories_gen(category,self._categories)]

#=======================================================================================================================================================

try:
    records = Records()
    categories = Categories()

    while True:
        command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
        if command == 'add':
            records.add(categories)
        elif command == 'view':
            records.view()
        elif command == 'delete':
            records.delete()
        elif command == 'view categories':
            categories.view()
        elif command == 'find':
            category = input('Which category do you want to find? ')
            target_categories = categories.find_subcategories(category)
            records.find(target_categories)
        elif command == 'exit':
            records.save()
            break
        elif command == '':
            continue
        else:
            sys.stderr.write('Invalid command. Try again.\n')
except EOFError:
    records.save()
    sys.stderr.write('\nUser EOF out.')
#======================================================================================================================================================