#coding=GBK
import queue
import threading
import urllib2
import time
import re
from BeautifulSoup import *
from urlparse import urljoin
import pyodbc
from PAM30 import PAMIE
import Queue
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

