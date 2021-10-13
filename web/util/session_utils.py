import json
from django.core.exceptions import ValidationError
from django.core.serializers import serialize

def add_data_to_session_as_dict(request, name, session, key, value):

    if str(key) not in session:
        try:
            session[str(key)] = serialize('json', [value])
            request.session[name] = json.dumps(session)
        except:
            raise ValidationError(f"Could not add data to {session}.{name} with values {{ {key}:{value} }}")

def read_session_data(request, name, default={}):
        session_data = request.session.get(name, default) 
        if isinstance(session_data, str):
            try:
                return json.loads(session_data)
            except:
                raise ValidationError(f"Could not load session data for: {name}")
        else:
            return session_data
