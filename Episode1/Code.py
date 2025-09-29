# #Programming for the Puzzled -- Srini Devadas
# #You Will All Conform
# #Input is a vector of F's and B's, in terms of forwards and backwards caps
# #Output is a set of commands (printed out) to get either all F's or all B's
# #Fewest commands are the goal
caps = ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'B', 'F' ]
# cap2 = ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'F', 'F' ]
# def pleaseConformOpt(caps):
#     #Initialization
#     start = 0
#     forward = 0
#     backward = 0
#     intervals = []
#     caps = caps + ['END']
#     #Determine intervals where caps are on in the same direction
#     for i in range(1, len(caps)):
#         if caps[start] != caps[i]:
#             # each interval is a tuple with 3 elements (start, end, type)
#             intervals.append((start, i - 1, caps[start]))
#             if caps[start] == 'F':
#                 forward += 1
#             else:
#                 backward += 1
#             start = i
#     if forward < backward:
#         flip = 'F'
#     else:
#         flip = 'B'
#     for t in intervals:
#         if t[2] == flip:
#             #Exercise: if t[0] == t[1] change the printing!
#             print ('People in positions', t[0], 'through', t[1], 'flip your caps!')
# def pleaseConformOnepass(caps):
#     caps = caps + [caps[0]]
#     for i in range(1, len(caps)):
#         if caps[i] != caps[i-1]:
#             if caps[i] != caps[0]:
#                 print('People in positions', i, end='')
#             else:
#                 print(' through', i-1, 'flip your caps!
# pleaseConformOpt(caps)
# pleaseConformOnepass(caps)
#After this I will provide the solution which is written by me
def caps_solution(caps):
    groupValue=0
    flip=''
    for cap in caps:
        if cap == 'F':
            groupValue+=1
        else:
            groupValue-=1
    if groupValue>0:
        flip='B'
    else:
        flip='F'
    for i in range(len(caps)):
        if caps[i]!=flip and (i==0 or caps[i-1]==flip):
            print('People in positions', i, end='')
        if caps[i]!=flip and (i==len(caps)-1 or caps[i+1]==flip):
            print(' through', i, 'flip your caps!')
caps_solution(caps)
