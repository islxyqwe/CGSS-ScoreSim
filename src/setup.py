from distutils.core import setup
import py2exe
 
setup(
	windows=['main.py'],
	options={
		"py2exe":{
			"unbuffered": True,
			"optimize": 2,
			"bundle_files": 2
		}
	}
)
