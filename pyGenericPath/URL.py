# EMACS settings: -*-  tab-width: 2; indent-tabs-mode: t -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
#
# =============================================================================
#               ____                      _      ____       _   _
#  _ __  _   _ / ___| ___ _ __   ___ _ __(_) ___|  _ \ __ _| |_| |__
# | '_ \| | | | |  _ / _ \ '_ \ / _ \ '__| |/ __| |_) / _` | __| '_ \
# | |_) | |_| | |_| |  __/ | | |  __/ |  | | (__|  __/ (_| | |_| | | |
# | .__/ \__, |\____|\___|_| |_|\___|_|  |_|\___|_|   \__,_|\__|_| |_|
# |_|    |___/
#
# =============================================================================
# Authors:						Patrick Lehmann
#
# Python package:	    A specific implementation for URLs.
#
# Description:
# ------------------------------------
#		TODO
#
# License:
# ============================================================================
# Copyright 2017-2019 Patrick Lehmann - Bötzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
#
from re     import compile as re_compile
from typing import Dict

from flags  import Flags

from .      import RootMixIn, ElementMixIn, PathMixIn


regExp = re_compile(r"^(?:(?P<scheme>\w+)://)?(?:(?P<host>(?:\w+|\.)+)(?:\:(?P<port>\d+))?)?(?P<path>[^?#]*)(?:\?(?P<query>[^#]+))?(?:#(?P<fragment>.+))?$")

class Protocols(Flags):
	TLS =   1
	HTTP =  2
	HTTPS = 3
	FTP =   4
	FTPS =  5
	FILE =  8


class Host(RootMixIn):
	_hostname : str = None
	_port :     int = None

	def __init__(self, hostname, port):
		self._hostname = hostname
		self._port =     port

	@property
	def Hostname(self):
		return self._hostname

	@property
	def Port(self):
		return self._port


class Element(ElementMixIn):
	pass


class Path(PathMixIn):
	ELEMENT_DELIMITER = "/"
	ROOT_DELIMITER =    "/"


	@classmethod
	def Parse(cls, path: str, root=None):
		return super().Parse(path, root, Path, Element)


class URL():
	_scheme:    Protocols = None
	_user:      str =       None
	_password:  str =       None
	_host:      Host =      None
	_path:      Path =      None
	_query:     Dict =      None
	_fragment:  str =       None

	def __init__(self, scheme, user, password, host, path, query, fragment):
		self._scheme =    scheme
		self._user =      user
		self._password =  password
		self._host =      host
		self._path =      path
		self._query =     query
		self._fragment =  fragment

	def __str__(self):
		result = str(self._path)

		if self._host is not None:
			result = str(self._host) + result

		if self._user is not None:
			if self._password is not None:
				result = self._user  + ":" + self._password + "@" + result
			else:
				result = self._user + "@" + result

		if self._scheme is not None:
			result = self._scheme.to_simple_str() + "://" + result

		if self._query is not None:
			params = []
			for key, value in self._query.items():
				params.append(key + "=" + value)
			result = result + "?" + "&".join(params)

		if self._fragment is not None:
			result = result + "#" + self._fragment

		return result

	@property
	def Scheme(self):
		return self._scheme

	@property
	def User(self):
		return self._user

	@property
	def Password(self):
		return self._password

	@property
	def Path(self):
		return self._path

	@property
	def Query(self):
		return self._query

	@property
	def Fragment(self):
		return self._fragment

	# http://semaphore.plc2.de:5000/api/v1/semaphore?name=Riviera&foo=bar#page2
	@classmethod
	def Parse(cls, path):
		matches = regExp.match(path)
		if (matches is not None):
			scheme =    matches.group("scheme")
			user =      None # matches.group("user")
			password =  None # matches.group("password")
			host =      matches.group("host")
			port =      matches.group("port")
			path =      matches.group("path")
			query =     matches.group("query")
			fragment =  matches.group("fragment")

			scheme = None if (scheme is None) else Protocols.from_str(scheme)
			hostObj =  None if (host is None)  else Host(host, port)

			pathObj =    Path.Parse(path, hostObj)

			parameters = {}
			if (query is not None):
				for pair in query.split("&"):
					key, value = pair.split("=")
					parameters[key] = value

			return URL(scheme, user, password, hostObj, pathObj, parameters, fragment)

		else:
			pass