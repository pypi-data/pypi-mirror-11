
import urllib.parse as p
import urllib.request as r
import datetime as dt
import dateutil.parser as dp
import json
import time
import logging
import collections

from lxml import etree as et
from pandas import Series,to_timedelta,to_datetime,concat
import pandas as pd
from pandas.io.json import json_normalize
from enum import Enum
from sqlalchemy import create_engine

APIV2 = 'https://api.enphaseenergy.com/api/v2'
APIKEYRING = collections.deque()

DEFAULT_MAX_WAIT = 60

class EnphaseErrorHandler(r.BaseHandler):
    def __init__(self, datetimetype, max_wait = DEFAULT_MAX_WAIT):
        super(EnphaseErrorHandler,self).__init__()

        self.dtt = datetimetype
        self.max_wait = max_wait
        logging.debug('Initialized EnphaseErrorHandler')

    def setMaxWait(self, max_wait):
        self.max_wait = max_wait
        logging.debug('Set max_wait to %d' % self.max_wait)

    def setDateTimeType(self, dtt):
        self.dtt = dtt
        logging.debug('Set DateTimeType to %s' % self.dtt.value)

    def http_error_409(self, req, fp, code, msg, hdrs):

        s = fp.read().decode(encoding='UTF-8')
        data = json.loads(s)

        logging.info('Received HTTP Error 409')
        logging.debug(data)

        end = self.dtt.datetimeify('period_end',data['period_end'])
        diff = end.timestamp() - int(time.time())

        if diff < self.max_wait:
            #is there a good way to handle clock skew
            logging.info('Sleeping for %s seconds' % str(diff+5.0))
            time.sleep(diff+5) #sleep +5 to prevent a second 409
            return r.build_opener(self).open(req.get_full_url())

    def http_error_422(self, req, fp, code, msg, hdrs):

        s = fp.read().decode(encoding='UTF-8')
        data = json.loads(s)

        logging.info('Received HTTP Error 422')
        logging.debug(data)

        if 'Failed to parse date' in data['reason']:
            logging.error(req.get_full_url())
            logging.error(data)
            return

        if 'Requested date range is invalid for this system' in data['reason']:
            logging.error(req.get_full_url())
            logging.error(data)
            return

        startAt = self.dtt.datetimeify('start_at',data['start_at'])
        lastInt = self.dtt.datetimeify('last_interval', data['last_interval'])

        if startAt > lastInt:
            endAt = self.dtt.datetimeify('end_at',data['end_at'])
            startAt = dt.combine(endAt.date(),datetime.time())

            s,n,pa,pr,q,f = p.urlparse(req.get_full_url())
            params = dict(p.parse_qsl(q))
            params['start_at'] = self.dtt.stringify('start_at',
                    startAt.timestamp())
            qstring = p.urlencode(params)
            url = p.urlunparse((s,n,pa,pr,qstring,f))
            return r.build_opener(self).open(url)
        #handle other potential error cases

    def http_error_503(self, req, fp, code, msg, hdrs):
        #The api says if you have made to many concurrent requests
        #then you will get a http_error_503, but they say nothing else
        pass

class DateTimeType(Enum):
    Enphase = 'enphase'
    Iso8601 = 'iso8601'
    Epoch   = 'epoch'

    def stringify(self, key, value):
        '''Convert the datetime values to the correct format'''

        d = value.replace(microsecond=0)
        if self is DateTimeType.Enphase:
            if '_date' in key:
                return d.strftime('%Y-%m-%d')
            else:
                return str(int(d.timestamp()))
        elif self is DateTimeType.Iso8601:
            return d.isoformat()
        elif self is DateTimeType.Epoch:
            return str(int(d.timestamp()))
        logging.warning('Failed to stringify %s' % value)

    def datetimeify(self, key, value):
        '''Convert an Enphase timestamp or time string to a datetime'''

        if self is DateTimeType.Enphase:
            if '_date' in key:
                return dt.datetime.strptime(value,'%Y-%m-%d')
            else:
                return dt.datetime.fromtimestamp(value)
        elif self is DateTimeType.Iso8601:
            return dp.parser.parse(value)
        elif self is DateTimeType.Epoch:
            return dt.datetime.fromtimestamp(value)
        logging.warning('Failed to datetimeify %s' % value)

    def sanatizeTimes(self, query):
        '''Make sure the datetime values are sane'''

        if 'start_at' in query and 'end_at' in query:
            if query['start_at'] > query['end_at']:
                logging.error('The value for start_at is after end_at')
                raise ValueError('start_at is after end_at')
        elif 'start_date' in query and 'end_date' in query:
            if query['start_date'] > query['end_date']:
                logging.error('The value for start_date is after end_date')
                raise ValueError('start_date is after end_date')

        for k,v in query.items():
            if '_at' in k or '_date' in k:
                if v > dt.datetime.now():
                    logging.error('The value for %s is set to the future' % k)
                    raise ValueError('A query with a future time is malformed')
                query[k] = self.stringify(k,v)

class RawEnphaseInterface(object):
    '''Interfaces with the Enphase api and returns the raw json
        It expects all dates and times to be in a child of a datetime type'''

    def __init__(self, userId, max_wait=DEFAULT_MAX_WAIT,
            useragent='Mozilla/5.0', datetimeType=DateTimeType.Enphase,
            errorhandler=None):

        if errorhandler==None:
            errorhandler=EnphaseErrorHandler(datetimeType,max_wait)

        self.userId = userId

        self.dtt = datetimeType
        self.handler = errorhandler

        self.opener = r.build_opener(self.handler)
        self.opener.addheaders = [('User-agent',useragent)]
        self.apiDest = APIV2

    def _execQuery(self, system_id, command, extraParams = dict()):
        '''Generates a request url for the Enphase API'''

        if system_id is not '':
            system_id = '/' + str(system_id)
        if command is not '':
            command = '/' + command

        try:
            query = {'user_id':self.userId,'key':APIKEYRING[0]}
        except IndexError:
            raise ValueError('Must register at least one key with APIKEYRING')
        query.update(extraParams)

        self.dtt.sanatizeTimes(query)

        q = p.urlencode(query)

        query = self.apiDest + '/systems' + system_id + command + '?' + q
        req = r.Request(query, headers={'Content-Type':'application/json'})

        logging.debug('GET %s' % query)
        response = self.opener.open(req).read()
        logging.debug(response.decode('UTF-8'))
        return response

    def _filterAttributes(self,attrs,kwargs):
        globalAttrs = ('datetime_format','callback','user_id','key')
        valids = [ (k,v) for k,v in kwargs.items() if k in attrs+globalAttrs ]
        return dict(valids)

    def setDateTimeType(self, dtt):
        '''Set the timestamp type for the Enphase API'''

        self.parameters['datetime_format'] = dtt.value
        self.handler.setDateTimeType(dtt)

        if dtt is DateTimeType.Enphase:
            self.parameters.pop('datetime_format',None)

    @staticmethod
    def _processPage(request):
        logging.debug(request.geturl())

        root = et.HTML(request.read().decode(encoding='UTF-8'))
        form = root.find('.//form[@action]')

        payload = {}
        for node in root.findall('.//input[@type="hidden"]'):
            payload[node.attrib['name']] = node.attrib['value']

        return (form.attrib['action'],payload)

    @staticmethod
    def authorizeApplication(app_id, username, password):
        '''Authorize an application to access a systems data
            and get the user_id
            The userid auth value appears to be binascii.hexlify(base64.b64encode(str(usernumber).encode())'''

        scheme = 'https'
        base_url = 'enlighten.enphaseenergy.com'
        action = 'app_user_auth/new'
        query = p.urlencode({'app_id':app_id})

        request1 = p.urlunsplit((scheme,base_url,action,query,''))
        logging.debug(request1)

        opener = r.build_opener(r.HTTPCookieProcessor())
        opener.addheaders = [('User-agent','Mozilla/5.0')]
        r1 = opener.open(request1)

        action,hiddens = EnphaseInterface._processPage(r1)

        payload = {'user[email]':username,'user[password]':password}
        hiddens.update(payload)

        request2 = p.urlunsplit((scheme,base_url,action,query,''))
        r2 = opener.open(request2,p.urlencode(hiddens).encode(encoding='UTF-8'))
        action, hiddens = EnphaseInterface._processPage(r2)

        request3 = p.urlunsplit((scheme,base_url,action,query,''))
        r3 = opener.open(request3,p.urlencode(hiddens).encode(encoding='UTF-8'))

        if 'enlighten-api-user-id' not in r3.info():
            logging.critical('Failed to aquire user_id')

        logging.debug(r3.info()['enlighten-api-user-id'])
        return r3.info()['enlighten-api-user-id']

    def energy_lifetime(self, system_id, **kwargs):
        '''Get the lifetime energy produced by the system'''

        validArgs = self._filterAttributes(('start_date','end_date'),kwargs)
        return self._execQuery(system_id, 'energy_lifetime', validArgs)

    def envoys(self, system_id, **kwargs):
        '''List the envoys associated with the system'''

        validArgs = self._filterAttributes(tuple(),kwargs)
        return self._execQuery(system_id, 'envoys', validArgs)

    def index(self, **kwargs):
        '''List the systems available by this API key'''

        sysAttributes = ['system_id', 'system_name', 'status', 'reference',
                            'installer', 'connection_type']
        validArgs = self._filterAttributes(tuple(sysAttributes),kwargs)

        uset = set(validArgs.keys()) & set(sysAttributes)
        if len(uset) > 1:
            for x in uset:
                validArgs[x+'[]'] = validArgs.pop(x)

        return self._execQuery('', '', validArgs)

    def inventory(self, system_id, **kwargs):
        '''List the inverters associated with this system'''

        validArgs = self._filterAttributes(tuple(),kwargs)
        return self._execQuery(system_id, 'inventory', validArgs)

    def monthly_production(self, system_id, **kwargs):
        '''List the energy produced in the last month'''

        validArgs = self._filterAttributes(('start_date',),kwargs)

        if 'start_date' not in validArgs:
            raise AttributeError('start_date required parameter')
        return self._execQuery(system_id, 'monthly_production', validArgs)

    def rgm_stats(self, system_id, **kwargs):
        '''List the Revenue Grade Meter stats'''

        validArgs = self._filterAttributes(('start_at','end_at'),kwargs)
        return self._execQuery(system_id, 'rgm_stats', validArgs)

    def stats(self, system_id, **kwargs):
        '''Get the 5 minute interval data for the given day'''


        validArgs = self._filterAttributes(('start_at','end_at'),kwargs)
        return self._execQuery(system_id, 'stats', validArgs)

    def summary(self, system_id, **kwargs):
        '''Get the system summary'''

        validArgs = self._filterAttributes(('summary_date',),kwargs)
        return self._execQuery(system_id, 'summary', validArgs)

class JsonEnphaseInterface(RawEnphaseInterface):
    def _execQuery(self, system_id, command, extraParams = dict()):
        data = super(JsonEnphaseInterface,self)._execQuery(system_id,
            command, extraParams)
        return json.loads(data.decode('UTF-8'))

class PandasEnphaseInterface(JsonEnphaseInterface):
    def _execQuery(self, system_id, command, extraParams = dict()):

        data = super(PandasEnphaseInterface,self)._execQuery(system_id,
            command, extraParams)
        logging.debug(data)

        if command == 'energy_lifetime':
            output = self._energy_lifetime(data)
        elif command == 'envoys':
            output = self._envoys(data)
        elif command == 'index' or command == '':
            output = self._index(data)
        elif command == 'inventory':
            output = self._inventory(data)
        elif command == 'monthly_production':
            output = self._monthly_production(data)
        elif command == 'rgm_stats':
            output = self._stats(data)
        elif command == 'stats':
            output = self._stats(data)
        elif command == 'summary':
            output = self._summary(data)
        else:
            raise ValueError('datatype parameter not supported')

        indexes = output.index.names
        return self._datetimeify(output).set_index(indexes)

    def _energy_lifetime(self,data):
        d = json_normalize(data, 'production',['start_date','system_id'])
        ts = to_timedelta(Series(d.index),unit='D')
        d['start_date'] = to_datetime(d['start_date'],unit='s') + ts
        d['start_date'] = d['start_date'].apply(
                lambda x:self.dtt.stringify('start_date',x))
        d.rename(columns={0:'production'},inplace=True)

        return d.set_index(['system_id','start_date'])

    def _envoys(self,data):
        return json_normalize(data, 'envoys',
            ['system_id']).set_index(['system_id','serial_number'])

    def _index(self,data):
        return json_normalize(data,'systems').set_index('system_id')

    def _inventory(self,data):
        cl = []
        for key in ['inverters','envoys','meters']:
            if key in data:
                cl.append(json_normalize(data,key,['system_id']))
            #this assumes only the envoys don't return the model type
        tmp = concat(cl).fillna('Envoy').set_index(['system_id','sn'])
        #normalize the index
        tmp.index.name = ['system_id','serial_number']
        return tmp

    def _monthly_production(self,data):
        if len(data['meter_readings']) > 0:
            output = json_normalize(data,'meter_readings',
                ['start_date','system_id','end_date','production_wh'])
        else:
            output = json_normalize(data,meta=
                    ['start_date','system_id','end_date','production_wh'])
        return output.set_index(['system_id','start_date','end_date'])

    def _stats(self,data):
        if len(data['intervals']) > 0:
            output = json_normalize(data,'intervals',
                ['system_id','total_devices']).set_index(['system_id',
                    'end_at'])
        else:
            output = json_normalize(data).set_index('system_id')
        return output

    def _summary(self,data):
        return json_normalize(data).set_index(['system_id','summary_date'])


    def _datetimeify(self,output):
        output.reset_index(inplace=True)
        for col in output.columns:
            if '_at' in col or '_date' in col:
                output[col] = output[col].apply(
                    lambda x:self.dtt.datetimeify(col,x))
        return output

class CachingEnphaseInterface(PandasEnphaseInterface):
    def __init__(self, userId, max_wait=DEFAULT_MAX_WAIT,
            engine = create_engine('sqlite://')):
        super(CachingEnphaseInterface,self).__init__(
                userId, max_wait)
        self.engine = engine

        self.createTables()

    def createTables(self):

        t = {}

        t['stats']      = '''CREATE TABLE stats (
                            [system_id] INTEGER,
                            [end_at] TEXT UNIQUE ON CONFLICT IGNORE,
                            [devices_reporting] INTEGER,
                            [enwh] INTEGER,
                            [powr] INTEGER,
                            [total_devices] INTEGER)'''
        t['rgm_stats']  = '''CREATE TABLE rgm_stats (
                            [system_id] INTEGER,
                            [end_at] TEXT UNIQUE ON CONFLICT IGNORE,
                            [devices_reporting] INTEGER,
                            [wh_del] INTEGER,
                            [total_devices] INTEGER)'''
        t['summary']    = '''CREATE TABLE summary (
                            [system_id] INTEGER,
                            [summary_date] TEXT UNIQUE ON CONFLICT IGNORE,
                            [current_power] INTEGER,
                            [energy_lifetime] INTEGER,
                            [energy_today] INTEGER,
                            [last_report_at] TEXT,
                            [modules] INTEGER,
                            [operational_at] TEXT,
                            [size_w] INTEGER,
                            [source] TEXT,
                            [status] TEXT)'''
        t['envoys']     = '''CREATE TABLE envoys (
                            [system_id] INTEGER,
                            [serial_number] TEXT,
                            [envoy_id] INTEGER,
                            [last_report_at] TEXT,
                            [name] TEXT,
                            [part_number] TEXT,
                            [status] TEXT)'''
        t['metastats']  = '''CREATE TABLE metastats (
                            [system_id] INT,
                            [obs_date] TEXT UNIQUE ON CONFLICT REPLACE,
                            [obs_type] TEXT)'''
        t['metargm_stats']='''CREATE TABLE metargm_stats (
                            [system_id] INT,
                            [obs_date] TEXT UNIQUE ON CONFLICT REPLACE,
                            [obs_type] TEXT)'''

        with self.engine.connect() as con:
            for k,v in t.items():
                if not self.engine.has_table(k):
                    con.execute(v)

    def summary(self, system_id, no_cache = False, **kwargs):
        '''Get the system summary'''

        if no_cache is True:
            summary = super(CachingEnphaseInterface,self)._execQuery(
                system_id,'summary',kwargs)
        else:
            q = 'select * from summary where system_id = ? and summary_date = ?'

            #summary_date defaults to midnight local time today
            default_date = dt.datetime.combine(dt.date.today(),dt.time(0))
            summary_date = kwargs.get('summary_date',default_date)
            params = (system_id,summary_date.isoformat())

            with self.engine.connect() as con:
                summary = pd.read_sql(
                        q, 
                        con.connection, 
                        index_col=['system_id','summary_date'], 
                        parse_dates=['summary_date'],
                        params = params)

                if len(summary) < 1:
                    summary = super(CachingEnphaseInterface,self)._execQuery(
                        system_id,'summary',kwargs)

                    summary.to_sql('summary',con.connection, if_exists='append')

        return summary

    def _istats(self, system_id, table, kwargs):

        midnight = dt.datetime.combine(dt.date.today(),dt.time(0))
        start_at = kwargs.get('start_at',midnight)
        end_at   = kwargs.get('end_at',dt.datetime.now())
        params = (system_id,start_at.date().isoformat(),end_at.date().isoformat())

        no_cache = kwargs.get('no_cache',False)

        if no_cache == True:
            return super(CachingEnphaseInterface,self)._execQuery(
                system_id,table,kwargs)

        q = '''select * from %s where system_id = ? and 
                end_at between ? and ?''' % table

        logging.debug(q)
        logging.debug(params)

        with self.engine.connect() as con:
            stats = pd.read_sql(
                    q, 
                    con.connection, 
                    params = params,
                    index_col=['system_id','end_at'],
                    parse_dates=['end_at'])

        logging.debug('Stats in database')
        logging.debug(stats)

        q = '''select * from %s where system_id = ?''' % ('meta'+table)
        with self.engine.connect() as con:
            result = con.execute(q, (system_id,)).fetchall()

        condition = lambda x:x[2] == 'full' and x[0] == system_id
        observedDates = set([x[1] for x in result if condition(x)])

        datetimes = pd.DatetimeIndex(start=start_at,end=end_at,freq='D')
        requestedDates = set([x.date().isoformat() for x in datetimes])

        daysToFetch = requestedDates - observedDates

        logging.debug(daysToFetch)

        if len(daysToFetch) > 0:
            kwargs.pop('end_at',0)
            results = [stats]
            for day in daysToFetch:
                start_at = dt.datetime.combine(pd.Timestamp(day),dt.time(0))
                logging.debug('Fetching %s'%start_at.isoformat())
                kwargs['start_at'] = start_at

                tstats = super(CachingEnphaseInterface,self)._execQuery(
                    system_id,table,kwargs)

                if start_at >= midnight:
                    params = (system_id, start_at.date().isoformat(),'partial')
                else:
                    params = (system_id, start_at.date().isoformat(),'full')

                with self.engine.connect() as con:
                    q = '''insert into %s values (?,?,?)'''%('meta'+table)
                    con.execute(q,params)
                    if 'intervals' in tstats.columns:
                        continue
                    tstats.to_sql(table,con.connection, if_exists='append')

                results.append(tstats)
            stats = pd.concat(results).drop_duplicates()
        return stats

    def stats(self, system_id, **kwargs):
        '''Get the 5 minute interval data for the given day'''

        return self._istats(system_id, 'stats', kwargs)

    def rgm_stats(self, system_id, **kwargs):

        return self._istats(system_id, 'rgm_stats', kwargs)

    def getAllStats(self, system_id):
        summary = self.summary(system_id,no_cache=True)
        return self.stats(system_id,
            start_at=summary['operational_at'].iloc[0],
            end_at = summary['last_report_at'].iloc[0])

    def envoys(self,system_id, no_cache=False, **kwargs):
        if no_cache is True:
            envoys = super(CachingEnphaseInterface,self)._execQuery(
                system_id,'envoys', kwargs)
        else:
            q = 'select * from envoys where system_id = ?'

            with self.engine.connect() as con:
                envoys = pd.read_sql(
                        q, 
                        con.connection, 
                        params = (system_id,),
                        index_col=['system_id','serial_number'],
                        parse_dates=['last_report_at'])

                if len(envoys) < 1:
                    envoys = super(CachingEnphaseInterface,self)._execQuery(
                        system_id,'envoys',kwargs)

                envoys.to_sql('envoys',con.connection, if_exists='append')

        return envoys

