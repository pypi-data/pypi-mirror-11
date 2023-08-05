#! python3

"""Simple io module depressing exceptions"""

import os, os.path as path, pprint, glob, time, shutil

def is_file(file):
	"""Check if the file is file."""
	file = path.expanduser(file)

	return path.isfile(file)

def content_write(file, content, append=False):
	"""Write content to file. Content may be str or bytes."""
	file = path.expanduser(file)

	prepare_folder(path.dirname(file))

	original = file

	if append:
		mode = "a"
	else:
		mode = "w"
		if is_file(file):
			file = file + time.strftime("@%Y-%m-%d_%H%M%S")

	if isinstance(content, bytes):
		mode += "b"
		with open(file, mode) as f:
			f.write(content)

	else:
		if not isinstance(content, str):
			content = pprint.pformat(content)

		with open(file, mode, encoding="utf-8") as f:
			f.write(content)

	if file != original:
		os.replace(file, original)

def content_read(file, raw=False):
	"""Read content from file. Return str."""
	file = path.expanduser(file)

	if not path.isfile(file):
		return ""

	if raw:
		with open(file, "rb") as f:
			return f.read()
	else:
		with open(file, "r", encoding="utf-8-sig") as f:
			return f.read()

def prepare_folder(folder):
	"""If the folder does not exist, create it."""
	folder = path.expanduser(folder)

	if not path.isdir(folder):
		os.makedirs(folder)

	return folder

def prepare_file(file):
	"""If the file does not exist, create it."""
	file = path.expanduser(file)

	prepare_folder(path.dirname(file))

	if not path.isfile(file):
		open(file, "w").close()

	return file

def move(src, dest):
	"""Move src files to dest. Should support wildcard."""
	src = path.expanduser(src)
	dest = path.expanduser(dest)

	if "*" in src:
		# Wildcard multiple move
		prepare_folder(dest)

		for file in glob.iglob(src):
			os.rename(file, path.join(dest, path.basename(file)))
	else:
		# just a rename
		if not is_file(src):
			return

		prepare_folder(path.dirname(dest))
		os.rename(src, dest)

def backup(file):
	"""Create backup file."""
	file = path.expanduser(file)
	if "*" in file:
		# Wildcard multiple copy
		for file in glob.iglob(file):
			shutil.copyfile(file, file + time.strftime("@%Y-%m-%d_%H%M%S"))
	else:
		if not is_file(file):
			return
		shutil.copyfile(file, file + time.strftime("@%Y-%m-%d_%H%M%S"))
