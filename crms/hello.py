import c_two as cc
from icrms.ihello import IHello

@cc.iicrm
class Hello(IHello):

    def hello(self) -> str:
        return 'hello'
