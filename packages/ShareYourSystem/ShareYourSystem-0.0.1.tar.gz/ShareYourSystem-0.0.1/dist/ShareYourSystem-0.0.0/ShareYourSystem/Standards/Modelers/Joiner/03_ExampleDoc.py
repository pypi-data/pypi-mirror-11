#/######################/#
# Import
#

#ImportModules
import ShareYourSystem as SYS

#/######################/#
# Define you object
#

#Define a Sumer class
@SYS.ClasserClass()
class SumerClass(SYS.JoinerClass):
								
	def default_init(self,
						_SumingFirstInt=0,
						_SumingSecondInt=0,
						_SumedTotalInt=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ModelerClass.__init__(self,**_KwargVariablesDict)
						
	def do_sum(self):
		
		#debug
		'''
		self.debug(('self.',self,['SumingFirstInt','SumingSecondInt']))
		'''

		#set the SumedTotalInt
		self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#/######################/#
# Build your model
#

#Definition of a Storer instance with a noded data
MySumer=SumerClass(
	**{
			'HdformatingFileKeyStr':'Sums.hdf5',
			'FolderingPathVariable':SYS.Joiner.LocalFolderPathStr
		}
	).mapSet(
		{
			'-Models':[
				('|Parameter',{
					'ModelKeyStrsList':['SumingFirstInt','SumingSecondInt']
				}),
				('|Result',{
					'ModelKeyStrsList':['SumedTotalInt'],
					'-Jonctions':{
							'|/^/|Parameter':{}
						}
					}
				)
			]
		}
	).model(
	)

#/######################/#
# Insert in the model
#

MySumer.mapSet(
		[
			('SumingFirstInt',1),
			('SumingSecondInt',3)
		]
	).sum(
	).command(
		'/-Models/|Result',
		[
			'#call:insert',
			('setSwitch',['insert'])
		]
	).mapSet(
		[
			('SumingFirstInt',3),
			('SumingSecondInt',5)
		]
	).sum(
	).command(
		'/-Models/|Result',
		'#call:insert'
	)

#/######################/#
# Print
#

#print
print('MySumer is ')
SYS._print(MySumer)

#view
print('hdf5 file is : \n'+SYS._str(MySumer.hdfview()))

#close
MySumer.file(_ModeStr='c')
