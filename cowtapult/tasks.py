from celery import Celery
celery = Celery()
celery.config_from_object('celeryconfig')

from salesforce import sf

# from https://gist.github.com/mrluanma/1480728
flatten = lambda lst: reduce(lambda l, i: l + flatten(i) if isinstance(i, (list, tuple)) else l + [i], lst, [])

def sf_safe_string(string):
    return string.replace("'","\'")

@celery.task
def upsert(*args, **kwargs):

    flat_args = flatten(args)
    # Handle canvas prepending args to child task's args
    # last arg = stype_name
    stype_name = flat_args[-1]
    # second to last = data
    data = flat_args[-2]
    # everything else is history, may be empty
    # also, ignore the last item as it is the stype_name from parent task
    history = flat_args[:-3]

    # Handle data being a tuple if called in a canvas
    if isinstance(data, tuple):
        history = data[1:]
        data = data[0]

    action = 'update'
    success = False
    object_id = data.get('Id', None)

    match = kwargs.get('match', None)
    if match is not None and object_id is None:
        # For now, assume match is a string value with the name of a single field
        # Also, matching is done synchronously.  It may be good to support async
        # to allow for batching of match queries under high load situations.
        match_id = SingleFieldMatch(stype_name, data, field=match)()

        if match_id:
            data['Id'] = match_id

    stype = getattr(sf, stype_name)

    # Merge values from history into data, useful for Ids in reference fields
    # Merge path is a tuple of two indexes to traverse the history tuple
    merge = kwargs.get('merge', None)
    if merge is not None:
        for field, path in merge.items():
            try:
                data[field] = history[path[0]][path[1]]
            except IndexError:
                data[field] = None

    # Create a copy of Data without the Id
    if data.has_key('Id'):
        data_no_id = data.copy()
        del data_no_id['Id']
        try:
            res = stype.upsert(data['Id'], data_no_id)
        except Exception, exc:
            raise upsert.retry(exc=exc)
        if res == 204:
            success = True
    else:
        try:
            res = stype.create(data)
        except Exception, exc:
            raise upsert.retry(exc=exc)
        success = res[u'success']

    if success is not True:
        pass
        # FIXME - Handle errors

    # If there was no Id passed or found through a match, action was create
    if data.get('Id',None) is None:
        data.update({'Id': res[u'id']})
        action = 'create'

    if len(history) != 0:
        r_data = list(history)
        r_data.append(data)
        return tuple(r_data), stype_name

    return data, stype_name

class SingleFieldMatch(object):
    def __init__(self, stype_name, data, **kwargs):
        self.stype_name = stype_name
        self.data = data
        self.field = kwargs.get('field')
        self.data_value = self.data.get(self.field, None)

    def __call__(self):
        if self.data_value:
            soql = "select Id from %s where %s = '%s' limit 1" % (
                sf_safe_string(self.stype_name),
                sf_safe_string(self.field),
                sf_safe_string(self.data_value)
            )

        res = sf.query(soql)             
        if res[u'totalSize'] > 0:
            return res[u'records'][0]['Id']


