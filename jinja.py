import os
from jinja2 import Template
import shutil

def main():
	# Path to site folder
	siteFolder = os.path.join(os.getcwd(), "site")
	postsFolder = os.path.join(os.getcwd(), "posts")

	# Removing old site folder
	try:
		shutil.rmtree(siteFolder)
	except Exception as e:
		print(e)

	# Creating new site dir
	os.mkdir(siteFolder)

	# Creating the posts subdir
	postsSubDir = os.path.join(siteFolder, "posts")
	os.mkdir(postsSubDir)

	# Creating the assets subdir
	assetsSubDir = os.path.join(siteFolder, "assets")
	os.mkdir(assetsSubDir)

	# Creating static subdir
	staticSubdir = os.path.join(siteFolder, assetsSubDir, "static")
	os.mkdir(staticSubdir)

	# Moving css from templates to static subdir
	source = os.path.join(os.getcwd(), "templates", "main.css")
	dest = os.path.join(staticSubdir, "main.css")
	shutil.copyfile(source, dest)

	posts = []

	# Building each sub page
	for obj in os.listdir(postsFolder):
		if os.path.isdir(os.path.join(postsFolder, obj)):
			# Creating asset folder for that site
			os.mkdir(os.path.join(assetsSubDir, obj))
			relPath = os.path.join("..", "assets", obj)

			for file in os.listdir(os.path.join(postsFolder, obj)):
				if file.split(".")[-1].lower() == "png":
					source = os.path.join(postsFolder, obj, file)
					dest = os.path.join(assetsSubDir, obj, file)
					shutil.copyfile(source, dest)
				if file.split(".")[-1].lower() == "markdown":
					fPath = os.path.join(postsFolder, obj, file)
					markdownFile = open(fPath)
					markdownLines = markdownFile.readlines()
					markdownFile.close()
					
					builtHtml, tile, description = parse(markdownLines, relPath)

					# Opening posts template
					mainFile = open(os.path.join(os.getcwd(), "templates", "posts.html"), "r")
					mainTemplate = mainFile.read()
					mainFile.close()

					blogName = "Hybryx Cyber Security"

					tm = Template(mainTemplate)
					msg = tm.render(blogName=blogName, blogContent=builtHtml)

					pathToFile = os.path.join(os.getcwd(), "site", "posts", obj) + ".html"
					htmlpost = open(pathToFile, "w+")
					htmlpost.write(msg)
					htmlpost.close()

					relPath = os.path.join("posts", (obj + ".html"))
					posts.append((relPath, tile, description))
	
	# Now building index.html, or main page
	postsSection = ""

	# Opening individual template
	indivFile = open(os.path.join(os.getcwd(), "templates", "individualPost.html"), "r")
	indivTemplate = indivFile.read()
	indivFile.close()

	# Building the posts section
	for post in posts:
		singlePost = Template(indivTemplate)
		singlePostHtml = singlePost.render(relPath=post[0], postName=post[1], postDesc=post[2])
		postsSection += singlePostHtml + "\n"

	# Opening main template
	mainFile = open(os.path.join(os.getcwd(), "templates", "main.html"), "r")
	mainTemplate = mainFile.read()
	mainFile.close()

	blogName = "Hybryx Cyber Security"

	tm = Template(mainTemplate)
	msg = tm.render(blogName=blogName, postsList=postsSection)

	indexPath = os.path.join(siteFolder, "index.html")

	indexFile = open(indexPath, "w+")
	indexFile.write(msg)
	indexFile.close()

def parse(markdownLines, relPath):
	htmlList = []
	
	inList = False
	inCode = False
	inMeta = False
	
	# Metadata
	tile = ""
	description = ""

	for line in markdownLines:
		#print(inMeta)
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
			imgPath = os.path.join(relPath, imgPath)
			htmlList.append("<div class=\"text-center\">")
			htmlList.append("<img src=\"" + imgPath + "\" alt=\"" + imgName + "\">")
			htmlList.append("</div>")
		# Metadata 
		elif lineType.strip() == "@@@":
			if inMeta == False:
				inMeta = True
			elif inMeta == True:
				inMeta = False
		# Paragraph
		else:
			if inList == True:
				inList = False
				htmlList.append("</ul>")
			elif inCode == True:
				htmlList.append(line.strip() + "<br>")
			elif inMeta == True:
				if line.split("=")[0].lower() == "title":
					tile = line.split("=")[1]
				elif line.split("=")[0].lower() == "description":
					description = line.split("=")[1]
			else:
				htmlList.append("<p>")
				htmlList.append("\t" + line.strip())
				htmlList.append("</p>")

	if inList == True:
		inList = False
		htmlList.append("</ul>")
	
	
	final = ""
	for line in htmlList:
		final += line + "\n"

	return final, tile, description

main()