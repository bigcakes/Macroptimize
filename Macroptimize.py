import sublime, sublime_plugin, dis, inspect, os, glob

class MacroptimizeCommand(sublime_plugin.TextCommand):
	items = []

	def run(self, edit):
		self.items = [] #refresh the items in the list each new run

		packagesRoot = sublime.packages_path()
		baseDirectory = os.path.basename(packagesRoot)

		for root, dirs, files in os.walk(packagesRoot):
			relativeDirectory = os.path.relpath(root, packagesRoot)

			for file in files:
				if file.endswith(".sublime-macro"):
					relativeAndBase = os.path.join(baseDirectory, relativeDirectory)
					relativeFilePath = os.path.join(relativeAndBase, file)

					#not sure if Sublime requires this format on all OS's, need to test
					self.items.append(macro(file, relativeFilePath.replace("\\", "/")))

		#Ask user which macro to run
		sublime.active_window().show_quick_panel(self.getUserChoices(), self.handleMacro)
	
	def handleMacro(self, choice):
		if (choice > -1):
			self.view.run_command("run_macro_file", {"file":self.items[choice].fullPath})

	def getUserChoices(self):
		return [str(index) + " " + macro.prettyText for index, macro in enumerate(self.items)]

#Simple class for holding macro information
class macro:
	def __init__(self, prettyText, fullPath):
		self.fullPath = fullPath
		self.prettyText = prettyText