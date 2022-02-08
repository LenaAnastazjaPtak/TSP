#include <iostream>
#include <cmath>
#include <fstream>
#include <cstdlib>
#include <bits/stdc++.h>
using namespace std;

char filename[50];  
bool print = false;


void randomowa(){
    int n;
    srand((unsigned int)time(NULL));    //tworzenie seeda, aby random dobrze dzialal
    ofstream myfile("tsp.txt");
    n = rand() % 20 + 5;
    if(myfile.is_open()) {
        myfile << n << endl;
        for(int i=1; i<=n; i++) myfile << i << " " << rand() % 1900 + 100 << " " << rand() % 1900 + 100 << endl;
        myfile.close();
        strncpy(filename, "tsp.txt", 50);
    }   
    else {
        perror("Blad tworzenia pliku tsp.txt");
        exit(1);
    }
}   

int main() {

    int test_case;
    cout << "Uzywam wlasnego pliku --> 1\nWygeneruj plik z instancjami --> 0\n\n";
    cin >> test_case;
    if(test_case == 1){
        printf("\nWpisz nazwe pliku z instancja: " ); fflush(stdin); fflush(stdout);
        cin.getline(filename, 50);
    }
    else randomowa();

    ifstream file;  //utworzenie obiektu do plików
    file.open(filename);

    if(!file.is_open()) { perror("Blad podczas otwierania pliku z instancja"); exit(1); }
    
    int total;
    file >> total;
    int newtotal = total;

    int **dane = new int * [total]; 
    for(int i=0; i<total; i++) {
        dane[i] = new int [4];
    } 
    
    int count = 0;
    while(file.good() && count != total) {
        file >> dane[count][0]; //numer
        file >> dane[count][1]; //x
        file >> dane[count][2]; //y
        dane[count++][3] = 0; //visited  
    }

    if(print) {
        cout << "\n\nDane wczytane z pliku\n\n";
        cout << "Laczna liczba wierzcholkow: " << total << endl;
        for(int i=0; i<total; i++){
            printf("nr.%2d  x=%5f   y=%5f   visited= %d\n", (int) dane[i][0], dane[i][1], dane[i][2], (int) dane[i][3]);
        }
    }

    double **distance = new double * [total];
    for(int i=0; i<total; i++) {
        distance[i] = new double [total];
    }

    for(int i=0; i<total; i++){
        for(int j=0; j<total; j++){
            if (i==j) distance[i][j] = 0.0;
            else {
                distance[i][j] = sqrt(pow((dane[i][1] - dane[j][1]), 2) + pow((dane[i][2] - dane[j][2]), 2));
            }
        }
    }
    if(print) {
        printf("\n\nMacierz sasiedztwa z dystansami miedzy punktami\n");

        for(int i=0; i<total; i++){
            cout << endl;
        for(int j=0; j<total; j++){
                printf("%-10.2f", distance[i][j]);
            }
        }
    }
    
    double suma;
    double najblizej;
    int obecny;
    int obecny_tymczasowo;
    int *ptr;
    double best_suma = 99999999.9999999999;
    int best_wierzcholek;
    int **tab = new int * [total];
        for(int i=0; i<total; i++){
            tab[i] = new int [total + 1];   //tablica na wszystkie przejscia (total + 1 bo musi wrocic do startowego)
        }

    printf("\n\n");

    for(int w_start=0; w_start<total; w_start++){ //wierzcholek startowy
       
        for(int zero=0; zero<total; zero++){    

            dane[zero][3] = 0;      //zerowanie odwiedzonych wierzcholkow, zeby moc zaczac od nowego wierzcholka startowego

        }

        suma = 0.0;
        najblizej = 9999999.0;
        obecny = w_start;
        dane[obecny][3] = 1;
        ptr = tab[obecny];  
        

        for(int przejscia=0; przejscia<total; przejscia++){ //liczba przejsc lacznie
            
            *(ptr + przejscia) = obecny + 1;

            if(przejscia == total-1) {
                
                *(ptr + przejscia + 1) = w_start + 1;
                suma += distance[obecny][w_start];
                
                if(suma < best_suma){

                    best_suma = suma;
                    best_wierzcholek = w_start + 1;

                } 
                if(print) {
                    cout << "\n\nDystans przebyty przez komiwojazera z punktu startowego nr " << w_start + 1 << ": " << suma << endl;
                    for(int i=0; i<=total; i++) cout << *(ptr+i) << " ";
                }
                break;

            }

            for(int droga=0; droga<total; droga++){ //najbliszy punkt 

                if(dane[droga][3] != 1) {   //jezeli punkt sposrod dostepnych nie byl odwiedzony

                    if(distance[obecny][droga] < najblizej){   //i jezeli jego droga jest mniejsza od poprzedniej zapisanej
                        
                        najblizej = distance[obecny][droga]; //to zapisz ten najblizszy                        //zmiana z  najblizej = distance[w_start][droga]
                        obecny_tymczasowo = droga; //i zapisz ten wierzcholek
                    }
                }
            }
            obecny = obecny_tymczasowo; //nowy obecny wierzcholek do ktorego idziemy
            dane[obecny][3] = 1;    //idziemy do najblizszego znalezionego wierzcholka i oznaczamy go jako odwiedzony
            suma += najblizej;
            najblizej = 9999999.0;
        }
    }
    //cout << "\n\nNajlepszym wyborem bedzie start z wierzcholka nr " << best_wierzcholek << endl;
    ptr = tab[best_wierzcholek-1];
    // for(int i=0; i<=total; i++) cout << *(ptr+i) << " ";
	for(int i=0; i<=total; i++) cout << dane[*(ptr+i)-1][1] << " ";
	cout << endl;
    for(int i=0; i<=total; i++) cout << dane[*(ptr+i)-1][2] << " ";

    //cout << "\nDroga wyzej to laczny dystans " << best_suma << " i jest to najbardziej optymalny wynik.";
	cout << endl << "GREEDY OPTIMUM: " << best_suma << endl;
	cout << "OPTIMUM: " << "???" << endl;

   
    for(int i=0; i<newtotal; i++) {
        delete [] tab[i];
        delete [] distance[i];
        delete [] dane[i];
    }
    delete [] tab;
    delete [] distance;
    delete [] dane;

	
	getchar();
	return 0;
}

