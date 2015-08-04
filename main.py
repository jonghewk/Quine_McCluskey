__author__ = 'jonghewk park'

'''
<Logic Design>
This is a program that implements Quine-McCluskey Method.

Written By: JongHewk Park 
Last Edit : June 2, 2015

Here is the algorithm
1. Find the prime implicants
2. Make Prime implicant chart
3. Find essential prime implicants
4. Use Petrick's Method to find all solutions


'''


import itertools


#compare two binary strings, check where there is one difference
def compBinary(s1,s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count+=1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None


#compare if the number is same as implicant term
#s1 should be the term
def compBinarySame(term,number):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != number[i]:
                return False

    return True


#combine pairs and make new group
def combinePairs(group, unchecked):
    #define length
    l = len(group) -1

    #check list
    check_list = []

    #create next group
    next_group = [[] for x in range(l)]

    #go through the groups
    for i in range(l):
        #first selected group
        for elem1 in group[i]:
            #next selected group
            for elem2 in group[i+1]:
                b, pos = compBinary(elem1, elem2)
                if b == True:
                    #append the ones used in check list
                    check_list.append(elem1)
                    check_list.append(elem2)
                    #replace the different bit with '-'
                    new_elem = list(elem1)
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)
                    next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked


#remove redundant lists in 2d list
def remove_redundant(group):
    new_group = []
    for j in group:
        new=[]
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group


#remove redundant in 1d list
def remove_redundant_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list


#return True if empty
def check_empty(group):

    if len(group) == 0:
        return True

    else:
        count = 0
        for i in group:
            if i:
                count+=1
        if count == 0:
            return True
    return False


#find essential prime implicants ( col num of ones = 1)
def find_prime(Chart):
    prime = []
    for col in range(len(Chart[0])):
        count = 0
        pos = 0
        for row in range(len(Chart)):
            #find essential
            if Chart[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)

    return prime

def check_all_zero(Chart):
    for i in Chart:
        for j in i:
            if j != 0:
                return False
    return True

#find max value in list
def find_max(l):
    max = -1
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index

#multiply two terms (ex. (p1 + p2)(p1+p4+p5) )..it returns the product
def multiplication(list1, list2):
    list_result = []
    #if empty
    if len(list1) == 0 and len(list2)== 0:
        return list_result
    #if one is empty
    elif len(list1)==0:
        return list2
    #if another is empty
    elif len(list2)==0:
        return list1

    #both not empty
    else:
        for i in list1:
            for j in list2:
                #if two term same
                if i == j:
                    #list_result.append(sorted(i))
                    list_result.append(i)
                else:
                    #list_result.append(sorted(list(set(i+j))))
                    list_result.append(list(set(i+j)))

        #sort and remove redundant lists and return this list
        list_result.sort()
        return list(list_result for list_result,_ in itertools.groupby(list_result))

#petrick's method
def petrick_method(Chart):
    #initial P
    P = []
    for col in range(len(Chart[0])):
        p =[]
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                p.append([row])
        P.append(p)
    #do multiplication
    for l in range(len(P)-1):
        P[l+1] = multiplication(P[l],P[l+1])

    P = sorted(P[len(P)-1],key=len)
    final = []
    #find the terms with min length = this is the one with lowest cost (optimized result)
    min=len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
        else:
            break
    #final is the result of petrick's method
    return final

#chart = n*n list
def find_minimum_cost(Chart, unchecked):
    P_final = []
    #essential_prime = list with terms with only one 1 (Essential Prime Implicants)
    essential_prime = find_prime(Chart)
    essential_prime = remove_redundant_list(essential_prime)

    #print out the essential primes
    if len(essential_prime)>0:
        s = "\nEssential Prime Implicants :\n"
        for i in range(len(unchecked)):
            for j in essential_prime:
                if j == i:
                    s= s+binary_to_letter(unchecked[i])+' , '
        print s[:(len(s)-3)]

    #modifiy the chart to exclude the covered terms
    for i in range(len(essential_prime)):
        for col in range(len(Chart[0])):
            if Chart[essential_prime[i]][col] == 1:
                for row in range(len(Chart)):
                    Chart[row][col] = 0

    #if all zero, no need for petrick method
    if check_all_zero(Chart) == True:
        P_final = [essential_prime]
    else:
        #petrick's method
        P = petrick_method(Chart)

        #find the one with minimum cost
        #see "Introduction to Logic Design" - Alan B.Marcovitz Example 4.6 pg 213
        '''
        Although Petrick's method gives the minimum terms that cover all,
        it does not mean that it is the solution for minimum cost!
        '''

        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unchecked)):
                for j in prime:
                    if j == i:
                        count = count+ cal_efficient(unchecked[i])
            P_cost.append(count)


        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])

        #append prime implicants to the solution of Petrick's method
        for i in P_final:
            for j in essential_prime:
                if j not in i:
                    i.append(j)

    return P_final

#calculate the number of literals
def cal_efficient(s):
    count = 0
    for i in range(len(s)):
        if s[i] != '-':
            count+=1

    return count

#print the binary code to letter
def binary_to_letter(s):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        #if it is a range a-zA-Z
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c+'\''

        if more == True:
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + '\''
            n+=1
        #conditions for next operations
        if c=='z' and more == False:
            c = 'A'
        elif c=='Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c)+1)
    return out



#main function
def main():
    #get the num of variables (bits) as input
    n_var = int(raw_input("Enter the number of variables(bits): "))
    #get the minterms as input
    minterms = raw_input("Enter the minterms (ex. 0 1 2 5 9 10) : ")
    a = minterms.split()
    #put the numbers in list in int form
    a = map(int, a)

    #make a group list
    group = [[] for x in range(n_var+1)]

    for i in range(len(a)):
        #convert to binary
        a[i] = bin(a[i])[2:]
        if len(a[i]) < n_var:
            #add zeros to fill the n-bits
            for j in range(n_var - len(a[i])):
                a[i] = '0'+ a[i]
        #if incorrect input
        elif len(a[i]) > n_var:
            print '\nError : Choose the correct number of variables(bits)\n'
            return
        #count the num of 1
        index = a[i].count('1')
        #group by num of 1 separately
        group[index].append(a[i])


    all_group=[]
    unchecked = []
    #combine the pairs in series until nothing new can be combined
    while check_empty(group) == False:
        all_group.append(group)
        next_group, unchecked = combinePairs(group,unchecked)
        group = remove_redundant(next_group)

    s = "\nPrime Implicants :\n"
    for i in unchecked:
        s= s + binary_to_letter(i) + " , "
    print s[:(len(s)-3)]

    #make the prime implicant chart
    Chart = [[0 for x in range(len(a))] for x in range(len(unchecked))]

    for i in range(len(a)):
        for j in range (len(unchecked)):
            #term is same as number
            if compBinarySame(unchecked[j], a[i]):
               Chart[j][i] = 1

    #prime contains the index of the prime implicant terms
    #prime = remove_redundant_list(find_minimum_cost(Chart))
    primes = find_minimum_cost(Chart, unchecked)
    primes = remove_redundant(primes)


    print "\n--  Answers --\n"

    for prime in primes:
        s=''
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    s= s+binary_to_letter(unchecked[i])+' + '
        print s[:(len(s)-3)]



if __name__ == "__main__":
    main()
    A = raw_input("\nPress Enter to Quit")