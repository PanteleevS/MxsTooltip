import sublime, sublime_plugin, re, os

functionArgsFilename = os.path.dirname(os.path.realpath(__file__)) + "\maxscript_functions_with_args.txt"

def getCurrentWord(self):
    doc = self.view.substr(sublime.Region(0, self.view.size()))
    offset = (self.view.sel())[0].begin()
    x = y = offset
    excludedChars = {' ','\n','\t','\r','	','(',')','[',']','\'','"',":",";",","}
    for i in range(offset,len(doc)):
        if doc[i] in excludedChars:
            break
        else:
            y += 1
    for i in range(offset-1,-1,-1):
        if doc[i] in excludedChars:
            break
        else:
            x -= 1    
    return (doc[x:y]).strip()
    


class MxsTooltipCommand(sublime_plugin.TextCommand):

    def run(self, view):
        # print('\n'*100)
        word = getCurrentWord( self )

        # print("query: " + word)
        if len(word) > 0:
            header = "<style>html { background-color:#223344; } body {color: #bbb;margin: 10px;font-size: 14px;font-family: monospace;}span {display:block;}</style>"
            lines = ""
            regex = re.compile(r'(^[^\s]+)', re.M|re.I)
            with open(functionArgsFilename, 'r') as searchfile:
                for line in searchfile:
                    if re.search( r'' + word + '', line, re.M|re.I):
                        line = re.sub(r"&","&amp;",line)
                        line = re.sub(r"<","&lt;",line)
                        line = re.sub(r">","&gt;",line)
                        line = regex.sub(r'<b style="color:#dedede">\1</b>', line)
                        lines += line
            if len(lines) > 0:
                lines = lines.splitlines()                            
                lines = sorted(lines)
                lines = [ line + "\n" for line in lines ]
                for i in range(0,len(lines)):
                    if i % 2 != 0:
                        lines[i] = "<span style='background-color:#283848;'>" + lines[i] + "</span>"
                    else:
                        lines[i] = "<span>" + lines[i] + "</span>"                
                lines = ''.join(lines)
                lines = re.sub(r"\n","<br>",lines)
                self.view.show_popup( header + lines, max_width = 1024, max_height = 300, flags=sublime.HTML )
				
class OnHoverEventCommand(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        # run hover only if its text
        if hover_zone == sublime.HOVER_TEXT:
            a = MxsTooltipCommand(view);
            a.run('');

class TextInputCommand(sublime_plugin.TextCommand):
    
	def run( self, edit):
	    print( ">>>" )
