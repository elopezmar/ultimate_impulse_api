from schemas.common.exceptions import BusinessError

class Roles():
    ADMIN = 'admin'
    COLLABORATOR = 'collaborator'
    USER = 'user'
    ANONYMOUS = 'anonymous'


class Methods():
    POST = 'post'
    GET = 'get'
    PUT = 'put'
    DELETE = 'delete'


class Ownerships():
    SELF = 'self'
    ALL = 'all'
    

class Security():
    def __init__(self, enable=True):
        self.roles = {
            Roles.ADMIN: {
                'privileges': {
                    Methods.POST: {'ownership': Ownerships.ALL}, 
                    Methods.GET: {'ownership': Ownerships.ALL}, 
                    Methods.PUT: {'ownership': Ownerships.ALL}, 
                    Methods.DELETE: {'ownership': Ownerships.ALL}
                }
            },
            Roles.COLLABORATOR: {
                'privileges': {
                    Methods.POST: {'ownership': Ownerships.SELF}, 
                    Methods.GET: {'ownership': Ownerships.ALL}, 
                    Methods.PUT: {'ownership': Ownerships.SELF}, 
                    Methods.DELETE: {'ownership': Ownerships.SELF}
                }
            },
            Roles.USER: {
                'privileges': {
                    Methods.POST: {'ownership': Ownerships.SELF}, 
                    Methods.GET: {'ownership': Ownerships.ALL}, 
                    Methods.PUT: {'ownership': Ownerships.SELF}, 
                    Methods.DELETE: {'ownership': Ownerships.SELF}
                }
            },
            Roles.ANONYMOUS: {
                'privileges': {
                    Methods.GET: {'ownership': Ownerships.ALL}
                }
            }
        }

        self.enable = enable
        self.method = None
        self.requestor = {
            'id': None,
            'role': self.roles[Roles.ANONYMOUS]
        }
        
    def set_requestor(self, requestor: dict):
        self.requestor = requestor
        self.requestor['role'] = self.roles[requestor.get('role', Roles.ANONYMOUS)]

    def set_privilege(self, role: str, mehtod: str, ownership: str):
        self.roles[role]['privileges'][mehtod] = {'ownership': ownership}

    def remove_privilege(self, role: str, privilege: str):
        self.roles[role]['privileges'].pop(privilege)

    def verify_privilege(self):
        if self.enable:
            try:
                self.requestor['role']['privileges'][self.method]
            except KeyError:
                raise BusinessError(f"User doesn't have {self.method} privilege.", 400)
    
    def verify_ownership(self, owner_id: str):
        if self.enable:
            try:
                ownership = self.requestor['role']['privileges'][self.method]['ownership']
                if owner_id != self.requestor['id'] and ownership != Ownerships.ALL:
                    raise BusinessError(f"User can't execute {self.method} privilege on the resource.", 400)
            except KeyError:
                raise BusinessError('Security config error.', 500)



            




        
