class Gsearch_python:
    def __init__(self, name_search):
        self.name = name_search
    def Gsearch(self):
        count = 0
        try:
            from googlesearch import search
        except ImportError:
            print("No Module named 'google' Found")
        for i in search(query=self.name,tld='co.in',num=10,stop=10,pause=2):
            count += 1
            print (count)
            print(i + '\n')
search = input()

if __name__=='__main__':
    gs = Gsearch_python(search)
    gs.Gsearch()
