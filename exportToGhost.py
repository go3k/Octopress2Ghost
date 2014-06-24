# !DOCTYPE python
# encoding: utf-8
# exportToGhost.py
# Author: go3k
# ==============================
# This script is used for export posts in octopress into a ghost required format .sql file.
# ==============================

# implement step
# 1. use python buildin uuid module create uuid for each post
# 2. generate slug or use the slug in octopress
# 3. read content of .mk files in octopress
# 4. read content of .html files in octopress ----- can't use this .html, cause there are so many inserted tags, we don't need them at all.
# 5. get the create/update/publish time in right format

import os,sys
import uuid
import codecs
import markdown
from xml.etree import ElementTree as ET

# list and compare .mk files with html output files
mkPath = "./source/_posts"
htmlPath = "./public/blog"

mks = []
for dirpath, dirnames, filenames in os.walk(mkPath):
	filenames = [f for f in filenames if not f[0] == '.']

	for filename in filenames:
		mks.append(dirpath + '/' + filename)
		# print("filename " + filename)

htmls = []
for dirpath, dirnames, filenames in os.walk(htmlPath):
	if dirpath == htmlPath:
		dirnames[:] = [d for d in dirnames if d != 'archives' and d != 'categories' and d != 'page']

	for filename in filenames:
		htmls.append(dirpath + '/' + filename)

# getKey: get key word of markdown filename, filename formate is '2012-09-12-thinking0.markdown'
# make a sub string from 11 to the last '.'
def getKey(name):
	# last '/'
	idx1 = name.rfind('/')
	name = name[idx1 + 1:]
	idx2 = name.find('.')
	return name[11:idx2]

# search and get html file via key, return filename if find, or return -1
def gethtml(key, htmls):
	retfile = -1
	for html in htmls:
		if html.find(key) != -1:
			retfile = html
			break
	return retfile

def getAttri(header, key):
	idx1 = header.find(key)
	idx2 = header[idx1 + len(key):].find('\n')
	attri = header[idx1 + len(key):idx1 + len(key) + idx2]
	return attri

# title, slug, markdown, html, create time
def readAttriFromMK(filename):
	f = open(filename, 'r')
	# f = codecs.open(filename, mode="r", encoding="utf-8")
	fcontent = f.read()
	# part 1: descript header part of this markdown
	idx1 = fcontent.find("---")
	idx2 = fcontent[idx1 + 4:].find("---")
	header = fcontent[idx1 + 4: idx1 + 4 + idx2]
	mdstr = fcontent[idx1 + 4 + idx2 + 4:]

	# mdstr is a utf-8 stream, we need to convert it into a unicode array, becuase markdown only accepts unicode input.
	tmpstr = unicode(mdstr, 'utf-8')
	# html is a unicode array too.
	html = markdown.markdown(tmpstr)
	html = html.encode('utf-8')
	# print("html " + html)

	key = "title: "
	title = getAttri(header, key)
	key = "slug: "
	slug = getKey(mk)
	key = "date: "
	date = getAttri(header, key)

	title = title.replace("'", "''");
	slug = slug.replace("'", "''");
	print(filename + " slug " + slug)
	mdstr = mdstr.replace("'", "''");
	html = html.replace("'", "''");
	return [title, slug, mdstr, html, date]

#============Main process==============
# The sql content is mainly as this:
# INSERT INTO `posts` (`uuid`, `title`, `slug`, `markdown`, `html`, `image`, `featured`, `page`, `status`, `language`, `meta_title`, `meta_description`, `author_id`, `created_at`, `created_by`, `updated_at`, `updated_by`, `published_at`, `published_by`) VALUES
# ('c8039906-f6f6-4176-92a4-d8b905fe23af', 'import article', 'welcome-to-imp', '# yeah yeah!', '<p>oh no</p>', NULL, 0, 0, 'published', 'en_US', NULL, NULL, 1, '2014-05-29 10:18:05', 1, '2014-05-29 10:18:05', 1, '2014-05-29 10:18:05', 1)

f = open("import.sql", 'w')
record = "INSERT INTO `posts` (`uuid`, `title`, `slug`, `markdown`, `html`, `image`, `featured`, `page`, `status`, `language`, `meta_title`, `meta_description`, `author_id`, `created_at`, `created_by`, `updated_at`, `updated_by`, `published_at`, `published_by`) VALUES "
f.write(record)
index = 0
for mk in mks:
	index += 1
	key = getKey(mk)
	find = gethtml(key, htmls)
	status = "'published'"

	# 1. makefile is the accurate amount of articles, if there is no html file for a markdown file, I assume
	# that this article is not pushlished, so we record the mk file content and mark the post status as 
	# unpublish
	# if key == "helloworld":
	if find == -1:
		status = "'draft'"

	# title, slug, markdown, html, create time
	attris = readAttriFromMK(mk)

	record = "("
	# uuid
	uuidstr = str(uuid.uuid4())

	record += "'" + str(uuidstr) + "', "
	record += "'" + attris[0] + "', "
	record += "'" + attris[1] + "', "
	record += "'" + attris[2] + "', "
	record += "'" + attris[3] + "', "
	record += "NULL, 0, 0, "
	record += status + ", "
	record += "'en_US', "
	record += "NULL, NULL, "
	record += "1, "
	record += "'" + attris[4] + "', "
	record += "1, "
	record += "'" + attris[4] + "', "
	record += "1, "
	record += "'" + attris[4] + "', "
	record += "1"
	record += ")"
	
	if index < len(mks):
		record += ", "

	f.write(record)




