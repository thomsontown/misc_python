#!/usr/bin/env python

'''
This script was written to provide an example function that leverages applescript's 
display dialog handler. By passing arguments to the function from within a python
script, a macOS-style dialog box will be displayed to interact with the user. 

    dialog  -> (Required) The text you want to display in the dialog box. The text can be
               informational or it can be a question to be answered in the prompt.

    title   -> (Optional) The text you want to appear as the title to the dialog box.  

    answer  -> (Optional) To prompt for input a default answer is required, even if it is
               a blank string. 

    hidden  -> (Optional) To conceal the text of an input prompt (answer), this argument
               must be any valid string. 

    buttons -> (Optional) A maximum list of 3 custom button names can be specified.

    button  -> (Optional) Name of the button you want to specify to be the default.

    icon    -> (Optional) Three default icons are available: 'stop', 'note', 'caution'.
               Additionally, a POSIX style path to an icon file (.icns) can be specified
               for a more customized approach.

    timeout -> (Optional) An integer indicating the number of seconds before the dialog-box
               will give up and disappear. 

Author:		Andrew Thomson
Date:		2017-09-18
GitHub:		https://github.com/thomsontown
'''

import inspect, os, subprocess, sys

def main():
	#	message(dialog, title, answer, hidden, buttons, button, icon, timeout)
	results = message('What is the airspeed velocity of an unladen swallow?', 'Monte Python' , '24 mph', None,   ['Cancel','Ok'],  'Ok', '/Applications/Chess.app/Contents/Resources/Chess.icns', 8)

	if 'button returned' in results: print results['button returned']
	if 'text returned' in results: print results['text returned']
	if 'gave up' in results: print results['gave up']
	if 'canceled' in results: print results['canceled']


def message(dialog, title, answer, hidden, buttons, button, icon, timeout):

	#	set single and double-quote variables
	sq = '\''; dq = '\"'

	#	set cmd to include dialog syntax
	cmd = ' display dialog ' + dq + dialog + dq

	#	set cmd to include title syntax
	if title: cmd = cmd + ' with title ' + dq + title + dq

	#	set cmd to include answer syntax
	if answer: cmd = cmd + ' default answer ' + dq + answer + dq

	#	set cmd to include  hidden syntax
	if hidden and not answer: 
		sys.stderr.write('ERROR: A hidden answer was requested without specifying a default answer.')
		exit(inspect.currentframe().f_lineno)
	elif hidden:
		cmd = cmd + ' with hidden answer'

	#	set cmd to include specified buttons
	if buttons:

		#	ensure custom buttons do not exceed 3
		if len(buttons) > 3:
			sys.stderr.write('ERROR: The number of custom buttons cannot exceed 3.')
			exit(inspect.currentframe().f_lineno)

		#	concatenate initial buttons syntax	
		cmd = cmd + ' buttons {'

		#	enumerate custom buttons and include proper syntax
		for index, item in enumerate(buttons):
			cmd = cmd + dq + item + dq

			#	separate custom buttons with a comma
			if index + 1 < len(buttons):
				cmd = cmd + ' , '

		#	concatenate final buttons syntax		
		cmd = cmd + '}'

	#	set cmd syntax to include default button
	if button and buttons:
		if button not in buttons:
			sys.stderr.write('ERROR: The specified default button is not included in the list of custom buttons.')
			exit(inspect.currentframe().f_lineno)
		else:
			cmd = cmd + ' default button ' + dq + button + dq

	#	set cmd syntax to include icon syntax
	if icon:
		if icon in ['stop', 'note', 'caution']:
			cmd = cmd + ' with icon ' + icon
		elif os.path.exists(icon):
			cmd = cmd + ' with icon (POSIX file ' + dq + icon + dq + ')' 

	#	set cmd syntax to include timeout syntax
	if timeout:
		if type(timeout) is int:
			cmd = cmd + ' giving up after ' + str(timeout)

	#	set cmd syntax end with single-quote
	cmd = cmd 

	#	run complete command
	proc_out, proc_err = subprocess.Popen(['/usr/bin/osascript',  '-e',  cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

	#	if cancel button pressed return unique dictionary
	if 'User canceled' in proc_err: 
		return {'canceled' : 'true'}

	#	if no cancel button then parse results in dictionary
	else:
		proc_out = proc_out.split(',')

		#	initiate results dictionary
		results = {}

		#	parse return code to add to results dictionary 
		for item in proc_out:
			item = item.split(':')
			results[item[0].strip()] = item[1].strip()
		results['canceled'] = 'false'
		return results
		

#	initiate main if run directly
if __name__ == '__main__':
    main()