import pyperclip, tkinter, time, threading, logging, base64
from PIL import Image, ImageTk
from ico import ico
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(message)s')


class Clip_list(tkinter.Tk):
	def __init__(self):
		super().__init__()
		
#--------------------------------------------------------------------------		
		logging.debug('start app')		
		self.protocol('WM_DELETE_WINDOW', lambda: self.exit_sequence())
		self.title('Clipboard History')		
		#vars
		self.geometry('325x360')
		self.resizable('false', 'false')
		self._clip_wath = True
		self._FINISH = False
		self.text_lines_obj = []
		self.button_obj = []
		self.remove_button_obj = []
		self.clips = []

		self.ico_data = base64.b64decode(ico)
		self.ico_obj = ImageTk.PhotoImage(data = self.ico_data)
		self.wm_iconphoto(True, self.ico_obj)
		self.background = tkinter.Label(self, image = self.ico_obj)
		self.background.place(anchor = 'center', relx = 0.5, rely = 0.5)
		
		self.bind('<Button-3>', self.about_window)
		
		self.watch_thread = threading.Thread(target = lambda: self.clip_watch())
		self.watch_thread.start()
#--------------------------------------------------------------------------		
	def about_window(self, event):
		self.child = About_w(self)
		
	#Exit seq
	def exit_sequence(self):
		logging.debug('exit_sequence')
		self._FINISH = True
		time.sleep(1)
		self.watch_thread.join()
		self.destroy()

	#Check if clip was changed
	def clip_watch(self):
		logging.debug('clip watch')
		while True:
			if pyperclip.paste() != '':
				if pyperclip.paste() not in self.clips:
					logging.debug('add to line')
					self.clips.insert(0, pyperclip.paste())
					self.clip_change()
				if pyperclip.paste() in self.clips and pyperclip.paste() != self.clips[0]:
					logging.debug('replace order')			
					self.clips.remove(pyperclip.paste())
					self.clips.insert(0, pyperclip.paste())
					self.clip_change()
			time.sleep(0.05)
			if self._FINISH == True:
				logging.debug('clip_watch finish = true')
				return 0
	#remove button
	def button_remove_action(self, n):
		self.clips.remove(self.clips[n])
		self.clip_change()
		
	#If clip was changed, redraw whole lines and buttons			
	def clip_change(self):
		logging.debug('clip_change')
		for i in range(len(self.text_lines_obj)):
			self.text_lines_obj[i].destroy()
			time.sleep(0.01)
		for i in self.text_lines_obj:
			self.text_lines_obj.remove(i)
		
		for i in range(len(self.button_obj)):
			self.button_obj[i].destroy()
		for i in self.button_obj:
			self.button_obj.remove(i)
			
		for i in range(len(self.remove_button_obj)):
			self.remove_button_obj[i].destroy()
		for i in self.remove_button_obj:
			self.remove_button_obj.remove(i)

		if len(self.clips) > 15:
			self.clips = self.clips[:15]
		if len(self.button_obj) > 15:
			self.button_obj = self.button_obj[:15]
		
		for i in range(len(self.clips)):
			task_text = tkinter.Text(self, height = 1, relief = 'solid', borderwidth = 1, width = 37, font = ('calibri', '10'))
			task_text.insert('1.0', self.clips[i])
			task_button = tkinter.Button(self, bg = 'white', text = '\u2192', relief = 'solid', borderwidth = 1, command = lambda i=i: pyperclip.copy(self.clips[i]), font = ('calibri', '8'))
			task_remove_button = tkinter.Button(self, bg = 'white', text = ' X ', relief = 'solid', borderwidth = 1, command = lambda i=i: self.button_remove_action(i) , font = ('calibri', '8'))
			task_text.config(state = 'disable')
			task_text.grid(row = i, column = 2, padx = 3)
			task_button.grid(row = i, column = 1, padx = 3)
			task_remove_button.grid(row = i, column = 3, padx = 3)
			self.text_lines_obj.append(task_text)
			self.button_obj.append(task_button)
			self.remove_button_obj.append(task_remove_button)
			time.sleep(0.05)
#--------------------------------------------------------------------------------	
class About_w(tkinter.Toplevel):
	def __init__(self, parent):
		super().__init__()

		self.parent = parent	
		self.geometry('300x200')
		self.title('Aboit window')
		self.grid_columnconfigure(1, weight = 1)
		self.label = tkinter.Label(self, text = 'About\n.................................\nToDo', font = ('calibri', '12'))
		self.label.grid(column = 1, row = 1)
		self.button_ok = tkinter.Button(self, text = 'OK', command = lambda: self.button_ok_action())
		self.button_ok.grid(column = 1, row = 2)
		
	def button_ok_action(self):
		self.destroy()
			
if __name__ == '__main__':
	clip_w = Clip_list()
	clip_w.mainloop()
