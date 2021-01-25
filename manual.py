import os
import shutil

def main():
	# Opening .markdown file
	mdFile = open("/Users/nick/Desktop/staticWebsite/posts/cronos/cronos.markdown", "r")
	lines = mdFile.readlines()
	mdFile.close()

	parse(lines)

def parse(lines):
	htmlList = []
	headerStuff = (\
"<head>\n\
	<link rel=\"stylesheet\" href=\"../main.css\">\n\
</head>\n\
<body>\n\
	<header class=\"header\">\n\
		<div class=\"topnav-left\">\n\
			<h1>\n\
				Hybryx Cyber Security\n\
			</h1>\n\
		</div>\n\
		<div class=\"topnav-right\">\n\
			<a href=\"/\">Home</a>\n\
			<a href=\"/about.html\">About</a>\n\
		</div>\n\
	</header>\n\
	<main>"
	)
	htmlList.append(headerStuff)
	inList = False
	inCode = False

	for line in lines:
		if len(line.strip()) == 0:
			continue

		lineType = line.split()[0]

		# H1
		if lineType == "#":
			htmlList.append("<h1>")
			htmlList.append("\t" + line.strip("#").strip())
			htmlList.append("</h1>")
		# H2
		elif lineType == "##":
			if inList == True:
				inList = False
				htmlList.append("</ul>")
			htmlList.append("<h2>")
			htmlList.append("\t" + line.strip("#").strip())
			htmlList.append("</h2>")
		# List, unordered
		# TODO: Add ordered list?
		elif lineType == "*":
			if inList == False:
				inList = True
				htmlList.append("<ul>")
			# TODO: Add sub lists
			htmlList.append("<li>")
			htmlList.append("\t" + line.strip("*").strip())
			htmlList.append("</li>")
		# Code block
		elif lineType == "~~~":
			if inCode == False:
				inCode = True
				htmlList.append("<pre>")
				htmlList.append("<code>")
			elif inCode == True:
				inCode = False
				htmlList.append("</code>")
				htmlList.append("</pre>")
		# Image 
		elif lineType[0:2] == "![":
			imgPath = line.split("(")[1].split(")")[0]
			imgName = line.split("[")[1].split("]")[0]
			imgPath = os.path.join("..", "assets", "cronos", imgPath)
			htmlList.append("<img src=\"" + imgPath + "\" alt=\"" + imgName + "\">")

		# Paragraph
		else:
			if inList == True:
				inList = False
				htmlList.append("</ul>")
			elif inCode == True:
				htmlList.append(line.strip() + "<br>")
			else:
				htmlList.append("<p>")
				htmlList.append("\t" + line.strip())
				htmlList.append("</p>")

	if inList == True:
		inList = False
		htmlList.append("</ul>")
	
	endingString = ("\
	</main>\
	<footer class=\"footer\">\
	</footer>\
	</body>\
	"
	)
	htmlList.append(endingString)
	
	final = ""
	for line in htmlList:
		final += line + "\n"

	#print(final)

	rawFile = open("/Users/nick/Desktop/staticWebsite/site/posts/cronos.html", "w+")
	rawFile.write(final)

main()