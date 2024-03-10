# A polynomial object can be created from a string that represents a polynomial
# as sums or differences of monomials.
# - Monomials are ordered from highest to lowest powers.
# - All factors are strictly positive, except possibly for the leading factor
# - For nonzero powers, factors of 1 are only implicit.
# A single space surrounds + and - signs between monomials.

# Written by *** and Eric Martin for COMP9021


import re # split() suffices though
from collections import defaultdict
from copy import deepcopy


class Polynomial:
    def __init__(self, polynomial = None):
        monomials_dict = defaultdict()
        character = {'-':-1,'+':1}
        fuhao = 1
        if polynomial :
            monomials = polynomial.split(' ') #得到每一个单项式，目标，储存每一个单项式的倍数和次方数
            for monomial in monomials:
                if monomial in character:
                    fuhao = character[monomial]
                    continue
                monomial = monomial.replace('^', '')
                numbers = monomial.split('x')
                if len(numbers)==1:
                    monomials_dict[0] = fuhao * int(numbers[0])
                if len(numbers)==2:
                    if (numbers[1] == '')&(numbers[0] == ''):
                        numbers[1] = 1
                        numbers[0] = 1
                        monomials_dict[int(numbers[1])] = fuhao * int(numbers[0])
                    elif numbers[1] == '':
                        numbers[1] = 1
                        monomials_dict[int(numbers[1])] = fuhao * int(numbers[0])#0号位储存的是倍数，1号位储存的是power数
                    elif numbers[0] == '':
                        numbers[0] = 1
                        monomials_dict[int(numbers[1])] = fuhao * int(numbers[0])
                    else:
                        monomials_dict[int(numbers[1])] = fuhao * int(numbers[0])
        self.polynomial = monomials_dict
        self.maxpower = 0
        if monomials_dict.keys():
            self.maxpower = max(monomials_dict.keys())



    def __add__(self, other):
        max_power = max(self.maxpower,other.maxpower)
        new_equation = defaultdict()
        final_monominal = 0
        for i in range(max_power + 1):
            if (i not in self.polynomial.keys()) & (i not in other.polynomial.keys()):
                continue
            elif i not in self.polynomial.keys():
                final_monominal = other.polynomial[i]
            elif i not in other.polynomial.keys():
                final_monominal = self.polynomial[i]
            else:
                final_monominal = self.polynomial[i] + other.polynomial[i]
            if final_monominal != 0:
                new_equation[i] = final_monominal

        new_polynomial = Polynomial()
        new_polynomial.polynomial = new_equation
        return new_polynomial


    def __mul__(self, other):
        max_power = max(self.maxpower,other.maxpower)
        new_equation = defaultdict()
        final_monominal = 0
        for m in range(max_power + 1):
            for n in range(max_power + 1):
                key = m + n
                final_monominal = self.polynomial.get(m,0)*other.polynomial.get(n,0)
                if final_monominal != 0:
                    if key in new_equation.keys():
                        new_equation[key] = new_equation[key] + final_monominal
                    else:
                        new_equation[key] = final_monominal

        new_polynomial = Polynomial()
        new_polynomial.polynomial = new_equation
        return new_polynomial



    def __str__(self):
        if self.polynomial:
            diaplay_dict = deepcopy(self.polynomial)
            keys = list(reversed(sorted(diaplay_dict.keys())))
            equation = ''
            for i in range(len(keys)):
                if i == 0:
                    if keys[i] == 0:
                        if diaplay_dict[keys[i]] > 0:
                            equation += f'{diaplay_dict[keys[i]]}'
                        if diaplay_dict[keys[i]] < 0:
                            equation += f'-{-diaplay_dict[keys[i]]}'
                        continue
                    if keys[i] == 1:
                        if diaplay_dict[keys[i]] == 1:
                            equation += 'x'
                        if diaplay_dict[keys[i]] == -1:
                            equation += '-x'
                        if diaplay_dict[keys[i]] > 1:
                            equation += f'{diaplay_dict[keys[i]]}x'
                        if diaplay_dict[keys[i]] < 0:
                            equation += f'-{-diaplay_dict[keys[i]]}x'
                        continue
                    if keys[i] > 1:
                        if diaplay_dict[keys[i]] == 1:
                            equation += f'x^{keys[i]}'
                        if diaplay_dict[keys[i]] == -1:
                            equation += f'-x^{keys[i]}'
                        if diaplay_dict[keys[i]] > 1:
                            equation += f'{diaplay_dict[keys[i]]}x^{keys[i]}'
                        if diaplay_dict[keys[i]] < 0:
                            equation += f'-{-diaplay_dict[keys[i]]}x^{keys[i]}'
                        continue
                else:
                    if keys[i] == 0 :
                        if diaplay_dict[keys[i]] > 0:
                            equation += f' + {diaplay_dict[keys[i]]}'
                        if diaplay_dict[keys[i]] < 0:
                            equation += f' - {-diaplay_dict[keys[i]]}'
                        continue
                    if keys[i] == 1 :
                        if diaplay_dict[keys[i]] == 1:
                            equation += f' + x'
                        if diaplay_dict[keys[i]] == -1:
                            equation += f' - x'
                        if diaplay_dict[keys[i]] > 1:
                            equation += f' + {diaplay_dict[keys[i]]}x'
                        if diaplay_dict[keys[i]] < -1:
                            equation += f' - {-diaplay_dict[keys[i]]}x'
                        continue
                    if keys[i] > 1 :
                        if diaplay_dict[keys[i]] == 1:
                            equation += f' + x^{keys[i]}'
                        if diaplay_dict[keys[i]] == -1:
                            equation += f' - x^{keys[i]}'
                        if diaplay_dict[keys[i]] > 1:
                            equation += f' + {diaplay_dict[keys[i]]}x^{keys[i]}'
                        if diaplay_dict[keys[i]] < -1:
                            equation += f' - {-diaplay_dict[keys[i]]}x^{keys[i]}'
                        continue
            return equation
        else:
            return '0'
        # REPLACE pass ABOVE WITH YOUR CODE

    # DEFINE OTHER METHODS

