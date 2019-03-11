'''
Created on Mar 9, 2019

@author: Andrei
'''
from comis.arbore import Arbore

class ComisVoiajor:
    def __init__(self,nume_fisier_intrare,nume_fisier_iesire_dfs,nume_fisier_iesire_greedy):
        
        """
        Constructorul clasei ComisVoiajor
        
        nume_fisier_intare - numele fisierului din care citeste matricea costurilor din graf
        nume_fisier_iesire_dfs - numele fisierului in care vom scrie solutia rezolvata cu dfs
        nume_fisier_iesire_greedy - numele fisierului in care vom scrie solutia rezolvata cu greedy
        
        In urma creeri unei instante, efectul va fi urmatorul:
            - se citeste matricea costurilor din fisierul dat ca fisier de input
            - se rezolva problema comisului voiajor utilizand DFS si se va scrie in fisierul de output pentru DFS numarul de noduri, drumul optim si costul acestuia
            - se rezolva problema comisului voiajor utilizand greedy si se va scrie in fisierul de output pentru greefy numarul de noduri, drumul optim obtinut si costul acestuia
        """
        self.__nume_fisier_intrare=nume_fisier_intrare
        self.__graf_costuri=[]
        self.__read_from_file()
        self.__write_in_file(nume_fisier_iesire_dfs, self.__get_solution_with_dfs)
        self.__write_in_file(nume_fisier_iesire_greedy, self.__get_solution_with_greedy)
    
    def __convert_strings_to_ints(self,lista):
        
        """
        Converteste o lista de string-uri intr-o lista de int-uri 
        
        lista - lista de string-uri
        
        Returneaza lista convertita
        """
        for index in range (0,len(lista)):
            lista[index]=int(lista[index])
        return lista
    
    def __read_from_file(self):
        
        """
        Citeste din fisierul de intrare specificat la crearea obiectului si creeaza graf-ul costurilor dintre orase astfel:
            - structura de date va fi o lista de lungime n (numarul de noduri), unde pe pozitia (i-1) va fi o alta lista ce indica costul de la nodul i la celelalte noduri
            - construieste arborele cu solutii intermediare si finale pentru numarul de noduri indicate la citirea din fisier
        
        In cazul in care nu se poate deschide fisierul, va afisa mesajul: "Nu exista fisierul specificat!"
        """
        try:
            with open(self.__nume_fisier_intrare,"r") as descriptor_fisier_input:
                linie=descriptor_fisier_input.readline().strip()
                self.__arbore=Arbore(1,int(linie))
                linie=descriptor_fisier_input.readline().strip()
                while linie!="":
                    self.__graf_costuri.append(self.__convert_strings_to_ints(linie.split(",")))
                    linie=descriptor_fisier_input.readline().strip()
        except IOError:
            print("Nu exista fisierul specificat!")
            
    def __cost_drum(self,drum):
        
        """
        Calculeaza costul unui drum in graf, privit ca ciclu
        
        drum - tuplu de int-uri ce indica un ciclu in graf
        
        Returneaza costul ciclului specificat
        """
        cost=0
        for index in range(0,len(drum)-1):
            extremitate_stanga=drum[index]-1
            extremitate_dreapta=drum[index+1]-1
            cost+=self.__graf_costuri[extremitate_stanga][extremitate_dreapta]
        extremitate_stanga=drum[0]-1
        extremitate_dreapta=drum[-1]-1
        cost+=self.__graf_costuri[extremitate_stanga][extremitate_dreapta]
        return cost

    def __euristica_greedy(self,drumuri_partiale):
        
        """
        Calculeaza pentru arborele solutiilor, care este "calea" cea mai buna, la un moment dat, pentru rezolvarea problemei
        
        drumuri_partiale - lista de tupluri de int-uri ce indica variantele posibile ale problemei la momentul actual de timp
        
        Returneaza euristic drumul partial pentru pasul urmator, cu sansa cea mai mare de a indica optimul problemei Comisului Voiajor 
        """
        
        drum_partial_ales=drumuri_partiale[0]
        extremitate_stanga=drum_partial_ales[-2]-1
        extremitate_dreapta=drum_partial_ales[-1]-1
        cost_minim=self.__graf_costuri[extremitate_stanga][extremitate_dreapta]
        for drum_partial in drumuri_partiale:
            extremitate_dreapta=drum_partial[-1]-1
            if self.__graf_costuri[extremitate_stanga][extremitate_dreapta] < cost_minim:
                drum_partial_ales=drum_partial
                cost_minim=self.__graf_costuri[extremitate_stanga][extremitate_dreapta]
        return drum_partial_ales
            
    def __get_solution_with_dfs(self):
        
        """
        Calculeaza drumul optim si costul acestuia utilizand parcurgerea cu DFS a arborelui cu solutii intermediare si finale 
        
        Returneaza drumul minim si costul acestuia
        """
        
        return self.__arbore.getSolutionWithDFS(self.__cost_drum)
    
    def __get_solution_with_greedy(self):
        
        """
        Calculeaza drumul optim local si costul acestuia utilizand un algoritm greedy cu euristica definita in functia __euristica_greedy
        
        Returneaza optimul local obtinut cu euristica aleasa si costul acestuia
        """
        
        drum=self.__arbore.get_solution_with_greedy(self.__euristica_greedy)
        return drum,self.__cost_drum(drum)
            
    def __write_in_file(self,nume_fisier,metoda_de_rezolvare):
        
        """
        Scrie in fisierul specificat rezultatul obtinut pentru problema Comisului Voiajor, conform metodei de rezolvare aleasa, in formatul:
                prima linie: numarul de noduri din graf
                a II-a linie: drumul optim determinat, in care nodurile sunt delimitate prin virgula
                a III-a linie: costul drumului determinat anterior
        
        nume_fisier - string ce reprezinta numele fisierului in care dorim sa tiparim rezultatul obtinut
        metoda_de_rezolvare - referinta la metoda ce va indica metoda de rezolvare pe care o folosim in determinarea solutie problemei (dfs sau greedy)
        
        In cazul in care nu se poate scrie in fisierul specificat, se va tipari mesajul "Eroare la scriere in fisierul nume_fisier!"
        """
        
        try:
            with open(nume_fisier,"w") as descriptor_fisier:
                descriptor_fisier.write(len(self.__graf_costuri).__str__()+"\n")
                drum,cost=metoda_de_rezolvare()
                for index in range(0,len(drum)-1):
                    descriptor_fisier.write(drum[index].__str__()+",")
                descriptor_fisier.write(drum[-1].__str__()+"\n")
                descriptor_fisier.write(cost.__str__())
        except IOError:
            print("Eroare la scriere in fisierul "+nume_fisier+"!")