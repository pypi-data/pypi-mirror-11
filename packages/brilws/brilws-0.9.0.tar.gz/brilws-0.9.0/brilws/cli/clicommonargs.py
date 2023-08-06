from brilws import api,params,RegexValidator
import re,time,os,sys
from datetime import datetime
import calendar
from schema import And, Or, Use
from dateutil import tz
from ConfigParser import SafeConfigParser
import yaml
def parseservicemap(authfile):
    '''
    parse service config ini file
    output: {servicealias:[protocol,user,passwd,descriptor]}
    '''
    result={}
    parser = SafeConfigParser()
    parser.read(authfile)
    for s in parser.sections():
        protocol = parser.get(s,'protocol')
        user = parser.get(s,'user')
        passwd = parser.get(s,'pwd')
        descriptor = parser.get(s,'descriptor')
        result[s] = [protocol,user,passwd,descriptor]
    return result

class parser(object):
    def __init__(self,argdict):
        self._argdict = argdict
        self._dbconnect = None 
        self._authpath = None
        self._beamstatus = None
        self._egev = None
        self._datatagname = None
        self._amodetag = None
        self._fillmin = None
        self._fillmax = None
        self._runmin = None
        self._runmax = None
        self._tssecmin = None
        self._tssecmax = None
        self._runlsSeries = None
        self._iovtagSelect = None
        self._withBX = False
        self._byls = False
        self._bybit = False
        self._pathinfo = False
        self._chunksize = None
        self._lumitype = None
        self._ofilename = '-'
        self._fh = None
        self._totable = False
        self._name = None
        self._comments = ''
        self._outputstyle = 'tab'
        self._applyto = ''
        self._scalefactor = 1.
        self._cerntime = False
        self._tssec = False
        self._withoutcorrection = False
        self._yamlobj = None
        self._servicemap = {}
        self._parse()
        
    def _parse(self):

        self._dbconnect = self._argdict['-c']
        if self._argdict.has_key('-p'):
            self._authpath = self._argdict['-p']
            if not self._authpath:
                self._authpath = os.path.dirname(os.path.abspath(__file__))
                self._authpath = os.path.join(os.path.sep,self._authpath,'../data/readdb3.ini')
            self._servicemap = parseservicemap(self._authpath)
        if self._argdict.has_key('-b') and self._argdict['-b']:
            self._beamstatus = self._argdict['-b'].upper()            
        if self._argdict.has_key('--beamenergy'):
            self._egev = self._argdict['--beamenergy']
        if self._argdict.has_key('--datatag'):
            self._datatagname = self._argdict['--datatag']
        if self._argdict.has_key('--amodetag'):
            self._amodetag = self._argdict['--amodetag']
        if self._argdict.has_key('--chunk-size'):
            self._chunksize = self._argdict['--chunk-size']
        if self._argdict.has_key('--output-style'):
            self._outputstyle = self._argdict['--output-style']
        if self._argdict.has_key('--name'):
            self._name = self._argdict['--name']
        if self._argdict.has_key('--comments'):
            self._comments = self._argdict['--comments']
        if self._argdict.has_key('--xing'):
            self._withBX = self._argdict['--xing']
        if self._argdict.has_key('--byls'):
            self._byls = self._argdict['--byls']
        if self._argdict.has_key('--bitinfo'):
            self._bybit = self._argdict['--bitinfo']
        if self._argdict.has_key('--pathinfo'):
            self._pathinfo = self._argdict['--pathinfo']
        if self._argdict.has_key('--type'):
            self._lumitype = self._argdict['--type']
        if self._argdict.has_key('--applyto'):
            self._applyto = self._argdict['--applyto']
        if self._argdict.has_key('-y'):
            self._yamlfile = self._argdict['-y']            
        if self._argdict.has_key('-n'):
            self._scalefactor = self._argdict['-n']
        if self._argdict.has_key('--cerntime'):
            self._cerntime = self._argdict['--cerntime']
        if self._argdict.has_key('--tssec'):
            self._tssec = self._argdict['--tssec']
        if self._argdict.has_key('--without-correction'):
            self._withoutcorrection = self._argdict['--without-correction']
        if self._argdict.has_key('-f') and self._argdict['-f'] :
            self._fillmin = self._argdict['-f']
            self._fillmax = self._argdict['-f']
        if self._argdict.has_key('--normtag') and self._argdict['--normtag']:
            normtagfileorpath = self._argdict['--normtag']
            self._iovtagSelect = api.parseiovtagselectionJSON(normtagfileorpath)
        if self._argdict.has_key('-i') and self._argdict['-i']: # -i has precedance over -r
            fileorpath = self._argdict['-i']
            self._runlsSeries = api.parsecmsselectJSON(fileorpath)
            #self._runlsSeries = api.parseselectionJSON(fileorpath)
        elif self._argdict.has_key('-r') and self._argdict['-r'] :
            self._runmin = self._argdict['-r']
            self._runmax = self._argdict['-r']
        s_beg = None
        s_end = None
        if self._argdict.has_key('-f') and not self._argdict['-f'] and self._argdict.has_key('-r') and not self._argdict['-r']:
            if self._argdict.has_key('--begin') and self._argdict['--begin']:
                s_beg = self._argdict['--begin']
                for style,pattern in {'fill':params._fillnum_pattern,'run':params._runnum_pattern, 'time':params._time_pattern}.items():
                    if re.match(pattern,s_beg):
                        if style=='fill':
                            self._fillmin = int(s_beg)
                        elif style=='run':
                            self._runmin = int(s_beg)
                        elif style=='time':
                            dt_obj = datetime.strptime(s_beg,params._datetimefm)                            
                            self._tssecmin = calendar.timegm(dt_obj.timetuple())
            if self._argdict.has_key('--end') and self._argdict['--end']:
                s_end = self._argdict['--end']
                for style,pattern in {'fill':params._fillnum_pattern,'run':params._runnum_pattern, 'time':params._time_pattern}.items():
                      if re.match(pattern,s_end):
                        if style=='fill':
                            self._fillmax = int(s_end)
                        elif style=='run':
                            self._runmax = int(s_end)
                        elif style=='time':
                            dt_obj = datetime.strptime(s_end,params._datetimefm)
                            self._tssecmax = calendar.timegm(dt_obj.timetuple())
        
        if self._argdict.has_key('-o') and self._argdict['-o'] or self._outputstyle == 'csv':
            if self._argdict['-o']:
                self._outputstyle = 'csv'                
                self._ofilename = self._argdict['-o']
                self._fh = open(self._ofilename,'w')                
            else:
                self._fh = sys.stdout
        else:
            self._totable = True
        
    @property
    def dbconnect(self):
        return self._dbconnect
    @property
    def authpath(self):
        return self._authpath
    @property
    def beamstatus(self):
        return self._beamstatus
    @property
    def beamstatusid(self):
        if not self._beamstatus: return None
        return params._beamstatustoid[self._beamstatus]
    @property
    def egev(self):
        return self._egev
    @property
    def datatagname(self):
        return self._datatagname
    @property
    def amodetag(self):
        return self._amodetag
    @property
    def amodetagid(self):
        if not self._amodetag: return None
        return params._amodetagtoid[self._amodetag]
    @property
    def fillmin(self):
        return self._fillmin
    @property
    def fillmax(self):
        return self._fillmax
    @property
    def runmin(self):
        return self._runmin
    @property
    def runmax(self):
        return self._runmax
    @property
    def tssecmin(self):
        return self._tssecmin
    @property
    def tssecmax(self):
        return self._tssecmax
    @property
    def runlsSeries(self):
        return self._runlsSeries
    @property
    def iovtagSelect(self):
        return self._iovtagSelect
    @property
    def withBX(self):
        return self._withBX
    @property
    def byls(self):
        return self._byls
    @property
    def chunksize(self):
        return self._chunksize
    @property
    def ofilehandle(self):
        return self._fh
    @property
    def outputstyle(self):
        return self._outputstyle
    @property
    def totable(self):
        return self._totable    
    @property
    def bybit(self):
        return self._bybit
    @property
    def pathinfo(self):
        return self._pathinfo
    @property
    def name(self):
        return self._name
    @property
    def comments(self):
        return self._comments
    @property
    def lumitype(self):
        return self._lumitype
    @property
    def applyto(self):
        return self._applyto
    @property
    def scalefactor(self):
        return self._scalefactor
    @property
    def cerntime(self):
        return self._cerntime
    @property
    def tssec(self):
        return self._tssec
    @property
    def withoutcorrection(self):
        return self._withoutcorrection
    @property
    def connecturl(self):
        if not os.path.isfile(self._dbconnect):
            if not self._servicemap.has_key(self._dbconnect): raise ValueError('service %s is not defined'%self._dbconnect)
            protocol = self._servicemap[self._dbconnect][0]
            if protocol!='oracle': raise ValueError('protocol %s is not supported'%protocol)
            user = self._servicemap[self._dbconnect][1]
            passwd = self._servicemap[self._dbconnect][2].decode('base64')
            descriptor = self._servicemap[self._dbconnect][3]
            connecturl = 'oracle+cx_oracle://%s:%s@%s'%(user,passwd,descriptor)
            return connecturl
        else:
            return self._dbconnect
        
    @property
    def yamlfile(self):
        return self._yamlfile
    
    @property
    def yamlobj(self):
        with open(self._yamlfile,'r') as f:
            self._yamlobj = yaml.safe_load(f)
        return self._yamlobj
    
argvalidators = {
    '--amodetag': Or(None,And(str,lambda s: s.upper() in params._amodetagChoices), error='--amodetag must be in '+str(params._amodetagChoices) ),
    '--beamenergy': Or(None,And(Use(int), lambda n: n>0), error='--beamenergy should be integer >0'),
    '-b': Or(None, And(str, lambda s: s.upper() in params._beamstatusChoices), error='-b must be in '+str(params._beamstatusChoices) ),
    '--begin': Or(None, And(str,Use(RegexValidator.RegexValidator(params._timeopt_pattern))), error='wrong format'),
    '--end': Or(None, And(str,Use(RegexValidator.RegexValidator(params._timeopt_pattern))), error='wrong format'),
    '--output-style': And(str,Use(str.lower), lambda s: s in params._outstyle, error='--output-style choice must be in '+str(params._outstyle) ),
    '--chunk-size':  And(Use(int), lambda n: n>0, error='--chunk-size should be integer >0'),
    '--type': Or(None, And(str, lambda s: s.upper() in params._lumitypeChoices), error='--type must be in '+str(params._lumitypeChoices) ),
    '--applyto': Or(None, And(str, lambda s: s.upper() in params._applytoChoices), error='--applyto must be in '+str(params._applytoChoices) ),
    '--siteconfpath': Or(None, str, error='--siteconfpath should be string'),
    '-c': str,
    '-p': Or(None,os.path.exists, error='AUTHPATH should exist'),
    '-y': And(os.path.exists, error='YAMLFILE should exist'),
    '--normtag': Or(None,str),
    '-i': Or(None,str),
    '-o': Or(None,str),    
    '-f': Or(None, And(Use(RegexValidator.RegexValidator(params._fillnum_pattern)),Use(int)), error='-f FILL has wrong format'), 
    '-n': And(Use(float), lambda f: f>0, error='-n SCALEFACTOR should be float >0'),      
    '-r': Or(None, And(Use(RegexValidator.RegexValidator(params._runnum_pattern)),Use(int)), error='-r RUN has wrong format'),
    str:object # catch all
}
