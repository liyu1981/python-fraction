"""
Linear Algebra Tool by Yu LI (liyu1981@gmail.com)
Usage: Follow the instructions. :)
"""

useage = """[What is your action]:
1. add one row to another row
2. change a row
3. add one column to another column
4. change a column
5. print gnuplot drawing cmds
8. set display column width
9. write matrix to result.txt
0. exit
: """

display_col_width = 6

"""
Fraction - a Python class
Copyright 2000 by Mike Hostetler
taken from here http://users.binary.net/thehaas/fractionpy.shtml
modified a little by Yu LI
"""

def gcd(a,b):
## the gcd function is used by Fraction.reduce(), but it is significant
## in it's own right
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

class Fraction:
    def __init__ (self,num=0,denom=1):
        self.numerator = 0
        self.denominator = 1
        if denom > 0:
            self.numerator = num
            self.denominator = denom
        elif denom < 0:
            self.numerator = -num
            self.denominator = -denom
        else:
            print "### the denominator must not be zero -",
            print "%d is " %(denom)
            

    def toString(self):
        if abs(self.denominator) == 1:
            return "%d" %(int(self.numerator) * int(self.denominator))
        return "%s/%s" %(self.numerator,self.denominator)

    def toDecimal(self):
        return float(self.numerator)/self.denominator

    def mixedNumber(self):
        return (self.numerator/self.denominator,(self-Fraction(self.numerator/self.denominator)))
        
    def reduce(self):
        divisor= gcd(self.numerator,self.denominator)
        if divisor> 1:
            self.numerator = self.numerator/divisor
            self.denominator= self.denominator/divisor

    def __add__(self,fract2):
        sum = Fraction()
        sum.numerator = (self.numerator*fract2.denominator)+(fract2.numerator*self.denominator)
        sum.denominator = (self.denominator*fract2.denominator)
        if sum.numerator > 0:
            sum.reduce()
        else:
            sum.numerator = -1*sum.numerator
            sum.reduce()
            sum.numerator = -1*sum.numerator
        return sum

    def __sub__(self,fract2):
        negative= Fraction(-1*fract2.numerator,fract2.denominator)
        return self + negative

    def __mul__(self,fract2):
        product = Fraction()
        product.numerator = self.numerator*fract2.numerator
        product.denominator = self.denominator*fract2.denominator
        if product.denominator < 0:
            product.denominator = -1*product.denominator
            product.reduce()
            product.numerator = -1*product.numerator
        elif product.numerator < 0:
            product.numerator = -1*product.numerator
            product.reduce()
            product.numerator = -1*product.numerator
        else:
            product.reduce()
        return product

    def __div__(self,fract2):
        recip = Fraction(fract2.denominator,fract2.numerator)
        return self * recip

    def __iadd__(self,fract2):
        return self + fract2

    def __isub__(self,fract2):
        return self - fract2

    def __imul__(self,fract2):
        return self * fract2

    def __idiv__(self,fract2):
        return self / fract2

def readMatrix(file):
    lines = file.readlines()
    file.close()
    matrix = []
    for line in lines:
        numbers = line.split()
        row = []
        for number in numbers:
            row.append(parseFraction(number))
        matrix.append(row)
    return matrix

def matrixString(matrix, p):
    r = ""
    formatstr = '%'+str(display_col_width)+'s '
    if p:
        s = ""
        for i in range(len(matrix[0])):
            s += formatstr % (i)
        r += s + "\n"
    for i in range(len(matrix)):
        row = matrix[i]
        s = ""
        for col in row:
            s += formatstr % (col.toString())
        if p:
            r += str(i) + ": " + s + "\n"
        else:
            r += s + "\n"
    return r

def printMatrix(matrix):
    print "======The Matrix======"
    print matrixString(matrix, 1),

def parseFraction(str):
    ts = str.split("/")
    if len(ts) == 1:
        return Fraction(int(ts[0]),1);
    else:
        return Fraction(int(ts[0]), int(ts[1]))

def rowTransform(m, pars):
    row = m[pars[0]]
    target_row = m[pars[2]]
    times = pars[1]
    for i in range(len(target_row)):
        target_row[i] = target_row[i] + times * row[i]

def changeRow(m, pars):
    target_row = m[pars[0]]
    par = pars[1]
    for i in range(len(target_row)):
        target_row[i] = par * target_row[i]

def colTransform(m, pars):
    col_index = pars[0]
    target_col_index = pars[2]
    times = pars[1]
    for row in m:
        row[target_col_index] = row[target_col_index] + times * row[col_index]

def changeCol(m, pars):
    target_col_index = pars[0]
    par = pars[1]
    for row in m:
        row[target_col_index] = par * row[target_col_index]

def printDrawCmds(matrix):
    cmd = "plot \\"
    for i in range(1, len(matrix)):
        row = matrix[i]
        const_num = row[0] / row[2]
        a = (Fraction() - row[1]) / row[2]
        cmd += "\n%f*x+(%f) title '(%s)x+(%s)', \\" % (a.toDecimal(), const_num.toDecimal(), a.toString(), const_num.toString())
    cmd = cmd[:-3]
    print cmd

if __name__ == "__main__":
    mfile = raw_input("Where is your matrix? [default is m.txt in same directory]: ")
    if len(mfile.strip()) == 0:
        m = readMatrix(open("m.txt","r"))
    else:
        m = readMatrix(open(mfile, "r"))
    printMatrix(m)
    while(1):
        i = input(useage);
        if i == 1:
            instr = raw_input("[row times target-row]: ")
            pars = instr.split()
            rowTransform(m, (int(pars[0]), parseFraction(pars[1]), int(pars[2])))
            printMatrix(m)
        elif i == 2:
            instr = raw_input("[row par]: ")
            pars = instr.split()
            changeRow(m, (int(pars[0]), parseFraction(pars[1])))
            printMatrix(m)
        elif i == 3:
            instr = raw_input("[column times target-column]:")
            pars = instr.split()
            colTransform(m, (int(pars[0]), parseFraction(pars[1]), int(pars[2])))
            printMatrix(m)
        elif i == 4:
            instr = raw_input("[column par]: ")
            pars = instr.split()
            changeCol(m, (int(pars[0]), parseFraction(pars[1])))
            printMatrix(m)
        elif i == 5:
            printDrawCmds(m)
        elif i == 8:
            display_col_width = input("[display_col_width=]: ")
            printMatrix(m)
        elif i == 9:
            f = open("result.txt", "a")
            f.write("=========================\n")
            f.write(matrixString(m, 0))
            f.write("\n")
            f.close()
            print "matrix outputed!"
        elif i == 0:
            break
