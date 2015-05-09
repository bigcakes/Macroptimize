import sublime, sublime_plugin, os, collections

class MacroptimizeCommand(sublime_plugin.TextCommand):
	items = []
	lastMacro = None

	def run(self, edit, runLast):
		if (runLast and self.lastMacro is not None):
			self.view.run_command("run_macro_file", {"file": self.lastMacro})
		else:
			self.items = [] #refresh the items in the list each new run

			#Thanks to FichteFoll for letting me know about this much easier to use API
			macroFiles = sublime.find_resources("*.sublime-macro")

			for file in macroFiles:
				self.items.append(Macro(os.path.basename(file), file))

			#Ask user which macro to run
			sublime.active_window().show_quick_panel(self.getUserChoices(), self.handleMacro)
	
	def handleMacro(self, choice):
		if (choice > -1):
			self.lastMacro = self.items[choice].fullPath
			self.view.run_command("run_macro_file", {"file": self.lastMacro})

	def getUserChoices(self):
		return ["%d %s" % (index, macro.prettyText) for index, macro in enumerate(self.items)]

#Simple class for holding macro information
Macro = collections.namedtuple("Macro", ["prettyText", "fullPath"])