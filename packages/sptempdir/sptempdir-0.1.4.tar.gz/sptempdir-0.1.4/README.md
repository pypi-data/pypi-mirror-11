# (SP)TEMPDIR

**Function parameters:**

	sptempdir.TemporaryDirectory(suffix="", prefix="", dir=None, delete=True)

By default temporary directory will be deleted when function it is closed.


### Example 1:

The `name` property returns the name of a temporary directory.

```python
import os
import sptempdir

with sptempdir.TemporaryDirectory(prefix="prefbegin_", suffix="_suffend") as temp:
	print('temp.name:', temp.name)  # retrieve the name temporary directory
	print('Inside:', os.path.exists(temp.name))

print('Outside:', os.path.exists(temp.name))	
```

*Terminal output:*

	$ test_create_tempdir.py
	temp.name: /tmp/prefbegin_66XxiFkN6Nm4_suffend
	Inside: True
	Outside: False


### Example 2:

```python
import os
import sptempdir

temp = sptempdir.TemporaryDirectory()
print('temp.name:', temp.name)  # retrieve the name temporary directory
print('Tempdir exists:', os.path.exists(temp.name))

temp.rmtemp()  # manually remove temporary directory
print('Tempdir exists:', os.path.exists(temp.name))
```

*Terminal output:*

	$ test_create_tempdir.py
	temp.name: /tmp/RCgAzfsATQnb
	Tempdir exists: True
	Tempdir exists: False


### Example 3:

If the delete parameter is `delete=False`, the temp directory is not deleted. 

```python
import os
import sptempdir

temp = sptempdir.TemporaryDirectory(delete=False)
print('temp.name:', temp.name)  # retrieve the name temporary directory
print('Tempdir exists:', os.path.exists(temp.name))

temp.rmtemp()  # manually remove temporary directory
print('Tempdir exists:', os.path.exists(temp.name))
```

*Terminal output:*

	$ test_create_tempdir.py
	temp.name: /tmp/kWwCWn42NRsr
	Tempdir exists: True
	Tempdir exists: True


### Example 4:

Specific path where you want to create temporary directory.

```python
import sptempdir

temp = sptempdir.TemporaryDirectory(dir="/home/user/Desktop")
print(temp.name)  # retrieve the name temporary directory
```

*Terminal output:*

	$ test_create_tempdir.py
	/home/user/Desktop/4ZdTvLNqVuyE


### Installation:

	pip install sptempdir
	# or
	pip install https://github.com/sefikail/sptempdir/tarball/master


### License:

	https://creativecommons.org/licenses/by/3.0/

-----------------------

(SP)TEMPDIR = **( S**[efikail](http://sefikail.cz) + **P**[ython](http://python.org) **)** + **TEMPDIR**
