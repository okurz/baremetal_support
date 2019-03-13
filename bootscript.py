
class BootscriptNotFound(Exception):
    """Raised when the address is invalid"""
    pass

class Bootscript:
    def __init__(self):
        self.bootscript = {}
    
    def set(self, ip, script):
        """ set the bootscript in the dict """
        self.bootscript.update({ip: script})

    def get(self, ip):
        """ return specific bootscript """
        try:
            return self.bootscript[ip]
        except KeyError:
            raise BootscriptNotFound("no script found for " + ip)
