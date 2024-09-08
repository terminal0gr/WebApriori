class A():
    V1=1
    class B():
        V2=2
	
        def abc(self):
            print(A.V1)

b_instance = A.B()
b_instance.abc()
