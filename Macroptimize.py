import sublime, sublime_plugin, os, collections

class MacroptimizeCommand(sublime_plugin.TextCommand):
	items = []

	def run(self, edit):
		self.items = [] #refresh the items in the list each new run

		#Thanks to FichteFoll for letting me know about this much easier to use API
		macroFiles = sublime.find_resources("*.sublime-macro")

		for file in macroFiles:
			self.items.append(Macro(os.path.basename(file), file))

		#Ask user which macro to run
		sublime.active_window().show_quick_panel(self.getUserChoices(), self.handleMacro)
	
	def handleMacro(self, choice):
		if (choice > -1):
			self.view.run_command("run_macro_file", {"file":self.items[choice].fullPath})

	def getUserChoices(self):
		return ["%d %s" % (index, macro.prettyText) for index, macro in enumerate(self.items)]

#Simple class for holding macro information
Macro = collections.namedtuple("Macro", ["prettyText", "fullPath"])