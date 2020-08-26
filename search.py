from googlesearch import search

for i, result in enumerate(search(input("What are we looking for? "), lang='ru', stop=10, extra_params={"filetype": "txt"})):
    print(i, result)
