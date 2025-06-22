# /!\ Generated content. Do not edit!
class MyClass(GeneratedClass):
    def __init__(self):
        try: # disable autoBind
          GeneratedClass.__init__(self, False)
        except TypeError: # if NAOqi < 1.14
          GeneratedClass.__init__( self )

    def onInput_onStart(self, p):
        p = self.typeConversion(p)
        if(p == self.typeConversion("yes")):
            self.output_1(p)
        elif(p == self.typeConversion("no")):
            self.output_2(p)
        else:
            self.onDefault()

    def typeConversion(self, p):
        try:
            p = float(p)
            pint = int(p)
            if( p == pint ):
                p = pint
        except:
            p = str(p)
        return p
