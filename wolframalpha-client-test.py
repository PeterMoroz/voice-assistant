import wolframalpha

client = wolframalpha.Client('######-##########')
query = 'calculate 5 + 3'
print('query: ' + str(query))
idx = query.lower().split().index('calculate')
print('idx: ' + str(idx))
query = query.split()[idx + 1:]
print('query: ' + str(query))
request = ' '.join(query)
print('request: ' + str(request))
response = client.query(request)
# print('response: ' + str(response))


file = open('calculate.txt', 'w')
file.write('request: ' + str(request) + '\n')
file.write('response: ' + str(response) + '\n')
file.close()

# answer = next(response.results).text
answer = next(response.results, None)
if answer:
    print('answer: ' + answer.text)
else:
    print('could not get answer')
print('---------------------------')


query = 'what is engine'
print('query: ' + str(query))
print('request: ' + str(query))
response = client.query(query)
# print('response: ' + str(response))


file = open('what_is.txt', 'w')
file.write('request: ' + str(request) + '\n')
file.write('response: ' + str(response) + '\n')
file.close()

# answer = next(response.results).text
answer = next(response.results, None)
if answer:
    print('answer: ' + answer.text)
else:
    print('could not get answer')
# print('answer: ' + str(answer))
print('---------------------------')



query = 'who is Edison'
print('query: ' + str(query))
print('request: ' + str(query))
response = client.query(query)
# print('response: ' + str(response))


file = open('who_is.txt', 'w')
file.write('request: ' + str(request) + '\n')
file.write('response: ' + str(response) + '\n')
file.close()

# answer = next(response.results).text
answer = next(response.results, None)
if answer:
    print('answer: ' + answer.text)
else:
    print('could not get answer')
# print('answer: ' + str(answer))
