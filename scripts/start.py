import helpers as h

def main():
    output = h.do(['ps', '-eo', 'user,pid,comm'])
    h.show(output)

if __name__ == "__main__":
    main()
