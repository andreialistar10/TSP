'''
Created on Mar 9, 2019

@author: Andrei
'''
from pip._vendor.pyparsing import _MAX_INT

class Arbore:
    
    #reprezentarea in memorie a arborelui
    __reprezentare_arbore={}
    
    def __init__(self,radacina,nrNoduri):
        
        """
        Constructorul Clasei Arbore
        radacina - int (radacina arborelui)
        nrNoduri - int (numarul de noduri din graf)
        """
        
        self.__radacina=(radacina,)
        self.__permutari(self.__radacina, nrNoduri)
    
    def __adauga_fiu(self,parinte,fiu):
        
        """
        Adauga in arbore, pentru nodul "parinte" fiul "fiu"
        parinte - tuplu de numere intregi
        fiu - tuplu de numere intregi
        """
        
        if parinte in self.__reprezentare_arbore:
            if fiu not in self.__reprezentare_arbore[parinte]:
                self.__reprezentare_arbore[parinte].append(fiu)
        else:
            self.__reprezentare_arbore[parinte]=[fiu]
        
    def __permutari(self,permutare,n):
        
        """
        Genereaza toate permutarile de (n - len(permutare))!
        permutare - tuplu de numere intregi (reprezinta permutarea intermediara)
        n - int (simbolizeaza lungimea permutarii finale, ce trebuie sa fie generata de metoda)
        Metoda va actualiza arborele cu solutiile intermediare si finale (solutiile finale vor fi frunze in arbore)
        """
        
        if len(permutare)==n:
            return
        for i in range(1,n+1):
            if not i in permutare:
                permutare_fiu=permutare+(i,)
                self.__adauga_fiu(permutare,permutare_fiu )
                self.__permutari(permutare_fiu, n)
    
    def getSolutionWithDFS(self,proprietate,optim_de_minim=True):
        
        """
        Calculeaza drumul optim si costul acestuia folosind DFS, in functie de proprietatile date.
        Utilizeaza un algortim determinist.
        
        proprietate - referinta la o metoda ce calculeaza costul unei solutii finale si il returneaza
                    - antetul: proprietate(tuplu: Tuplu): int 
        optim_de_minim - boolean ce indica daca se doreste a se determina o solutie de optim de minim sau de maxim
        
        Returneaza drumul optim si costul acestuia, in conformitate cu proprietatile date
        """
        
        radacina=self.__radacina
        stiva=[]
        stiva.append(radacina)
        solutie=()
        cost_optim= (optim_de_minim==True) and _MAX_INT or -_MAX_INT
        while stiva:
            nod_actual=stiva.pop()
            if nod_actual not in self.__reprezentare_arbore:
                cost_actual=proprietate(nod_actual)
                solutie,cost_optim= (solutie==() or (cost_actual<cost_optim and optim_de_minim==True) or (cost_actual>cost_optim and optim_de_minim==False)) and (nod_actual,cost_actual) or (solutie,cost_optim)
            else:
                stiva += self.__reprezentare_arbore[nod_actual][::-1]         
        return solutie,cost_optim
    
    def get_solution_with_greedy(self,euristica_greedy,optim_de_minim=True):
        
        """
        Calculeaza drumul optim si costul acestuia folosind GREEDY, in functie de proprietatile date.
        Utilizeaza un algortim euristic, ce indica optimul local
        
        euristica_greedy - referinta la o metoda ce modeleaza euristica folosita pentru metoda
                         - antetul: euristica_greedy(tuplu: Tuplu): int   
        optim_de_minim - boolean ce indica daca se doreste a se determina o solutie de optim de minim sau de maxim
        
        Returneaza drumul optim local si costul acestuia, in conformitate cu proprietatile date
        """
        
        nod_actual=self.__radacina
        while nod_actual in self.__reprezentare_arbore:
            nod_actual=euristica_greedy(self.__reprezentare_arbore[nod_actual])
        return nod_actual