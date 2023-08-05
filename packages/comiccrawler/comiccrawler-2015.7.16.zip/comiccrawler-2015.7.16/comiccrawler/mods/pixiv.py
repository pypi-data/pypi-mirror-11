#! python3

"""this is pixiv module for comiccrawler

Ex:
	http://www.pixiv.net/member_illust.php?id=2211832

"""

import re, execjs
from html import unescape
from urllib.error import HTTPError

from ..core import Episode, grabhtml
from ..error import LastPageError, SkipEpisodeError, PauseDownloadError
from ..safeprint import safeprint

cookie = {}
domain = ["www.pixiv.net"]
name = "Pixiv"
noepfolder = True
config = {
	"SESSID": "請輸入Cookie中的PHPSESSID"
}

def loadconfig():
	cookie["PHPSESSID"] = config["SESSID"]

def gettitle(html, url):
	if "pixiv.user.loggedIn = true" not in html:
		raise PauseDownloadError("you didn't login!")
	user = re.search("class=\"user\">(.+?)</h1>", html).group(1)
	id = re.search(r"pixiv.context.userId = \"(\d+)\"", html).group(1)
	return "{} - {}".format(id, user)

def getepisodelist(html, url):
	s = []
	root = re.search("https?://[^/]+", url).group()
	base = re.search("https?://[^?]+", url).group()
	while True:
		ms = re.findall(r'<a href="([^"]+)"><h1 class="title" title="([^"]+)">', html)
		for m in ms:
			url, title = m
			uid = re.search("id=(\d+)", url).group(1)
			e = Episode("{} - {}".format(uid, title), root + url)
			s.append(e)

		un = re.search("href=\"([^\"]+)\" rel=\"next\"", html)
		if un is None:
			break
		u = un.group(1).replace("&amp;", "&")
		safeprint(base + u)
		html = grabhtml(base + u)
	return s[::-1]

def getimgurls(html, url):
	if "pixiv.user.loggedIn = true" not in html:
		raise PauseDownloadError("you didn't login!")

	base = re.search(r"https?://[^/]+", url).group()

	# ugoku
	rs = re.search(r"pixiv\.context\.ugokuIllustFullscreenData\s+= ([^;]+)", html)
	if rs:
		json = rs.group(1)
		o = execjs.eval(json)
		return [o["src"]]

	# new image layout (2014/12/14)
	rs = re.search(r'class="big" data-src="([^"]+)"', html)
	if rs:
		return [rs.group(1)]

	rs = re.search(r'data-src="([^"]+)" class="original-image"', html)
	if rs:
		return [rs.group(1)]

	# old image layout
	inner_url = re.search(r'"works_display"><a (?:class="[^"]*" )?href="([^"]+)"', html).group(1)
	html = grabhtml(base + "/" + inner_url, referer=url)

	if "mode=big" in inner_url:
		# single image
		img = re.search(r'src="([^"]+)"', html).group(1)
		return [img]

	if "mode=manga" in inner_url:
		# multiple image
		imgs = []

		for match in re.finditer(r'a href="(/member_illust\.php\?mode=manga_big[^"]+)"', html):
			large_page_url = base + match.group(1)
			large_page_html = grabhtml(large_page_url)
			img = re.search(r'img src="([^"]+)"', large_page_html).group(1)
			imgs.append(img)

		# New manga reader (2015/3/18)
		# http://www.pixiv.net/member_illust.php?mode=manga&illust_id=19254298
		if not imgs:
			for match in re.finditer(r'originalImages\[\d+\] = ("[^"]+")', html):
				img = execjs.eval(match.group(1))
				imgs.append(img)

		return imgs

	# restricted
	rs = re.search('<section class="restricted-content">', html)
	if rs:
		raise SkipEpisodeError

	# error page
	rs = re.search('class="error"', html)
	if rs:
		raise SkipEpisodeError

	# id doesn't exist
	rs = re.search("pixiv.context.illustId", html)
	if not rs:
		raise SkipEpisodeError

def errorhandler(er, ep):
	# http://i1.pixiv.net/img21/img/raven1109/10841650_big_p0.jpg
	if isinstance(er, HTTPError):
		# Private page?
		if er.code == 403:
			raise SkipEpisodeError
