import sublime, sublime_plugin, re

str_region_symbol = '#'
str_region_start = 'region'
str_region_end = 'endRegion'

class ToggleRegionsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		
		#region Walla
		comments = view.find_by_selector('comment')
		regions = []
		for region in comments:
			text = view.substr(region)
			if text.find(str_region_symbol + str_region_start) != -1:
				start_region = region
			if text.find(str_region_symbol + str_region_end) != -1:
				end_region = region
				regions.append(self.constructRegion(start_region, end_region))

		regions = filter(lambda region: self.inSelection(region), regions)

		self.toggle(regions)

		#endRegion
		
		#region Same #endRegion

	def inSelection(self, region):
		view = self.view
		selection = view.sel()

		if len(filter(lambda sel: not sel.empty(), selection)) == 0:
			return True

		for sel in selection:
			if region.intersects(sel):
				return True

		return False

	def toggle(self, regions):
		view = self.view
		if len(regions) > 0:
			if view.fold(regions[0]):
				view.fold(regions)
			else:
				view.unfold(regions)

	def constructRegion(self, start_region, end_region):
		view = self.view

		total_region = sublime.Region(start_region.a, end_region.b)
		total_text = view.substr(total_region)

		res = re.search('\n', total_text)

		first_newline = res.start() if res is not None else 0

		start_a = start_region.a + first_newline
		end_b = end_region.b

		if total_text[-1] == '\n':
			end_b -= 1

		return sublime.Region(start_a, end_b)

#region OtherRegionName
#endRegion
