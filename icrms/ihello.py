import c_two as cc
# Define ICRM ###########################################################
@cc.icrm
class IHello:
    def hello(self) -> str:
        ...