s = input()
start = s.find('h')
finish = len(s) - s[::-1].find('h')
print(s[:start+1]+s[start+1:finish-1:].replace('h', 'H')+s[finish-1::])
