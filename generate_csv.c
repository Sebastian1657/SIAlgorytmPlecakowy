#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


//zmienne globalne
FILE *file;
char buf[255] = "id,nazwa,kategoria,slot,waga_kg,stackowalny,pancerz,zdrowie,mana,obrazenia,charyzma\n\0";
int amount = 500;
int id=1;
float armor_prc=0.2, weapon_prc=0.4, item_prc=0.4;


int check_args(int argc, char* argv[])
{
	if(argc == 1)
		return 0;
	if(argc == 2)
	{
		int temp = atoi(argv[1]);
		if(temp <= 0)
		{
			printf("BLAD: Podaj liczbe calkowita wieksza od 0.");
			return 1;
		}
		else
		{
			amount = temp;
			return 0;
		}
	}
	if(argc == 5)
	{
		if(atoi(argv[2]) + atoi(argv[3]) + atoi(argv[4]) == 100)
		{
			armor_prc = atoi(argv[2]);
			armor_prc /= 100;
			weapon_prc = atoi(argv[3]);
			weapon_prc /= 100;
			item_prc = atoi(argv[4]);
			item_prc /= 100;
			return 0;
		}
		else
		{
			printf("BLAD: Suma procentow wszystkich kategorii nie rowna sie 100.");
			return 1;
		}
	}
	else
	{
		printf("Nieprawidlowa ilosc argumentow.");
		return 1;
	}
}


void generate_armor(int armor_amount)
{
	int item_amount = armor_amount; //20% przedmiotów to zbroja
	while(id<=item_amount)
	{
		int rand_type = rand()%5; //losowanie typu zbroi
		int rand_atr; //zmienna dla wybierania rodzaju atrybutu zbroi
		float waga = 0.0;
		int pancerz = 0, zdrowie=0, mana=0, obrazenia=0, charyzma=0;
		char converted_int[16];
		itoa(id,converted_int,10);
		strcpy(buf,converted_int); //dodawanie id do bufora
		strcat(buf,",");
		
		switch(rand_type)
		{
			//TODO: czasem wychodzi 0.0 waga xddddd
			case 0: //dodawanie nazwy he³mu i modyfikacja wartoœci
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (waga)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Lekki"
						strcat(buf, "Lekki ");
						waga -= 0.2 + (float)((rand()%2)/10.0); //-(0.2 - 0.3)
						pancerz -= 2; //-2
						break;
					case 2: //"Ciê¿ki"
						strcat(buf, "Ciê¿ki ");
						waga += 0.2 + (float)((rand()%2)/10.0); //+(0.2 - 0.3)
						pancerz += 2; //+2
						break;
				}
				
				rand_atr = rand()%2; //losowanie drugiego atrybutu (typ)
				if(rand_atr == 0)
				{
					waga += 0.5 + (-0.1 + (float)((rand()%3)/10.0)); //0.4 - 0.6
					pancerz += 6+rand()%3; //6-8
					strcat(buf, "Skórzany ");
				}
				else
				{
					waga += 2.0 + (-0.2 + (float)((rand()%5)/10.0)); //1.8 - 2.2
					pancerz += 7+rand()%3; //7-9
					strcat(buf, "Stalowy ");
				}
					
				strcat(buf, "He³m");
					
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 3+rand()%10; //3-12
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 3+rand()%10; //3-12
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 3+rand()%10; //3-12
						strcat(buf, " Charyzmy");
						break;
				}
				break;
				
			case 1: //dodawanie nazwy napierœnika i modyfikacja wartoœci
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (waga)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Lekki"
						strcat(buf, "Lekki ");
						waga -= 0.3 + (float)((rand()%3)/10.0); //-(0.3 - 0.5)
						pancerz -= 2-rand()%2; //-(2 - 3)
						break;
					case 2: //"Ciê¿ki"
						strcat(buf, "Ciê¿ki ");
						waga += 0.3 + (float)((rand()%3)/10.0); //+(0.3 - 0.5)
						pancerz += 2+rand()%2; //+(2 - 3)
						break;
				}
				
				rand_atr = rand()%2; //losowanie drugiego atrybutu (typ)
				if(rand_atr == 0)
				{
					waga += 2.0 + (-0.2 + (float)((rand()%5)/10.0)); //1.8 - 2.2
					pancerz += 9+rand()%2; //9-11
					strcat(buf, "Skórzany ");
				}
				else
				{
					waga += 7.5 + (-0.5 + (float)((rand()%10)/10.0)); //7.0 - 7.9
					pancerz += 12+rand()%2; //12-14
					strcat(buf, "Stalowy ");
				}
					
				strcat(buf, "Napierœnik");
					
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 3+rand()%10; //3-12
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 3+rand()%10; //3-12
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 3+rand()%10; //3-12
						strcat(buf, " Charyzmy");
						break;
				}
				break;
				
			case 2: //dodawanie nazwy rêkawic i modyfikacja wartoœci
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (waga)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Lekkie"
						strcat(buf, "Lekkie ");
						waga -= 0.1; //-0.1
						pancerz -= 1+rand()%2; //-(1 - 2)
						break;
					case 2: //"Ciê¿kie"
						strcat(buf, "Ciê¿kie ");
						waga += 0.1 + (float)((rand()%2)/10.0); //+(0.1 - 0.2)
						pancerz += 1+rand()%2; //+(1 - 2)
						break;
				}
				
				rand_atr = rand()%2; //losowanie drugiego atrybutu (typ)
				if(rand_atr == 0)
				{
					waga += 0.3 + (-(float)((rand()%2)/10.0)); //0.2 - 0.3
					pancerz += 3+rand()%2; //3-4
					strcat(buf, "Skórzane ");
				}
				else
				{
					waga += 1.6 + (-(float)((rand()%3)/10.0)); //1.4 - 1.6
					pancerz += 4+rand()%3; //4-6
					strcat(buf, "Stalowe ");
				}
					
				strcat(buf, "Rêkawice");
					
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 3+rand()%10; //3-12
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 3+rand()%10; //3-12
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 3+rand()%10; //3-12
						strcat(buf, " Charyzmy");
						break;
				}
				break;
				
			case 3: //dodawanie nazwy nogawic i modyfikacja wartoœci
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (waga)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Lekkie"
						strcat(buf, "Lekkie ");
						waga -= 0.2 + (float)((rand()%3)/10.0); //-(0.2 - 0.4)
						pancerz -= 2; //-2
						break;
					case 2: //"Ciê¿kie"
						strcat(buf, "Ciê¿kie ");
						waga += 0.2 + (float)((rand()%3)/10.0); //+(0.2 - 0.4)
						pancerz += 2+rand()%2; //+(2 - 3)
						break;
				}
				
				rand_atr = rand()%2; //losowanie drugiego atrybutu (typ)
				if(rand_atr == 0)
				{
					waga += 1.6 + (-0.1 + (float)((rand()%3)/10.0)); //1.5 - 1.7
					pancerz += 7+rand()%3; //7-9
					strcat(buf, "Skórzane ");
				}
				else
				{
					waga += 5.0 + (-0.2 + (float)((rand()%5)/10.0)); //4.8 - 5.2
					pancerz += 8+rand()%3; //8-10
					strcat(buf, "Stalowe ");
				}
					
				strcat(buf, "Nogawice");
					
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 3+rand()%10; //3-12
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 3+rand()%10; //3-12
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 3+rand()%10; //3-12
						strcat(buf, " Charyzmy");
						break;
				}
				break;
				
			case 4: //dodawanie nazwy butów i modyfikacja wartoœci
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (waga)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Lekkie"
						strcat(buf, "Lekkie ");
						waga -= 0.2 + (float)((rand()%2)/10.0); //-(0.2 - 0.3)
						pancerz -= 1; //-1
						break;
					case 2: //"Ciê¿kie"
						strcat(buf, "Ciê¿kie ");
						waga += 0.2 + (float)((rand()%2)/10.0); //+(0.2 - 0.3)
						pancerz += 2; //+2
						break;
				}
				
				rand_atr = rand()%2; //losowanie drugiego atrybutu (typ)
				if(rand_atr == 0)
				{
					waga += 0.5 + (-(float)((rand()%2)/10.0)); //0.4 - 0.5
					pancerz += 4+rand()%3; //4-6
					strcat(buf, "Skórzane ");
				}
				else
				{
					waga += 1.7 + (-0.2 + (float)((rand()%4)/10.0)); //1.5 - 1.8
					pancerz += 5+rand()%3; //5-7
					strcat(buf, "Stalowe ");
				}
					
				strcat(buf, "Buty");
					
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 3+rand()%10; //3-12
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 3+rand()%10; //3-12
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 3+rand()%10; //3-12
						strcat(buf, " Charyzmy");
						break;
				}
				break;
		}
		
		//dodawanie kategorii przedmiotu
		strcat(buf, ",Zbroja,");
		
		//dodawanie slotu przedmiotu
		switch(rand_type)
		{
			case 0: //he³m - "G³owa"
				strcat(buf,"Glowa,");
				break;
			case 1: //napierœnik - "Korpus"
				strcat(buf,"Korpus,");
				break;
			case 2: //rêkawice - "Rêkawice"
				strcat(buf,"Rekawice,");
				break;
			case 3: //nogawice - "Nogi"
				strcat(buf,"Nogi,");
				break;
			case 4: //buty - "Buty"
				strcat(buf,"Buty,");
				break;
		}
		
		//dodawanie wagi przedmiotu
		sprintf(converted_int,"%.1f,", waga);
		strcat(buf, converted_int);
		
		//dodawanie stackowalnoœci przedmiotu
		strcat(buf,"False,");
		
		//dodawanie punktów pancerza przedmiotu
		itoa(pancerz,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów zdrowia przedmiotu
		itoa(zdrowie,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów many przedmiotu
		itoa(mana,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów obra¿eñ przedmiotu
		itoa(obrazenia,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów charyzmy przedmiotu
		itoa(charyzma,converted_int,10);
		strcat(buf,converted_int);
		
		//zakoñczenie linii i zapisanie przedmiotu do pliku
		strcat(buf,"\n\0");
		fwrite(&buf, strlen(buf), 1, file);
		
		id++;
	}
}


void generate_weapons(int armor_prc, int weapon_prc)
{
	int item_amount = armor_prc + weapon_prc; //40% przedmiotów to bronie
	while(id<=item_amount)
	{
		int rand_type = rand()%3; //losowanie typu broni
		int rand_atr; //zmienna dla wybierania rodzaju atrybutu broni
		float waga = 0.0;
		int pancerz = 0, zdrowie=0, mana=0, obrazenia=0, charyzma=0;
		char converted_int[16];
		itoa(id,converted_int,10);
		strcpy(buf,converted_int); //dodawanie id do bufora
		strcat(buf,",");
		switch(rand_type)
		{
			case 0: //dodawanie nazwy miecza i modyfikacja wartoœci
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (Naostrzenie)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Têpy"
						strcat(buf, "Têpy ");
						obrazenia -= 1+rand()%2; //-(1 - 2)
						break;
					case 2: //"Ostry"
						strcat(buf, "Ostry ");
						obrazenia += 1+rand()%2; //+(1 - 2)
						break;
				}
				
				rand_atr = rand()%2; //losowanie drugiego atrybutu (typ)
				if(rand_atr == 0)
				{
					waga += 0.7 + (-0.1 + (float)((rand()%3)/10.0)); //0.6 - 0.8
					obrazenia += 6+rand()%3; //6-8
					strcat(buf, "Drewniany ");
				}
				else
				{
					waga += 1.3 + (-0.1 + (float)((rand()%3)/10.0)); //1.2 - 1.4
					obrazenia += 11+rand()%3; //11-13
					strcat(buf, "Stalowy ");
				}
					
				strcat(buf, "Miecz");
					
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 3+rand()%10; //3-12
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 3+rand()%10; //3-12
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 3+rand()%10; //3-12
						strcat(buf, " Charyzmy");
						break;
				}
				break;
			case 1: //dodawanie nazwy toporu i modyfikacja wartoœci
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (Naostrzenie)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Têpy"
						strcat(buf, "Têpy ");
						obrazenia -= 2+rand()%2; //-(2 - 3)
						break;
					case 2: //"Ostry"
						strcat(buf, "Ostry ");
						obrazenia += 2+rand()%2; //+(2 - 3)
						break;
				}
				
				rand_atr = rand()%2; //losowanie drugiego atrybutu (typ)
				if(rand_atr == 0)
				{
					waga += 0.8 + (-0.1 + (float)((rand()%3)/10.0)); //0.7 - 0.9
					obrazenia += 8+rand()%3; //8-10
					strcat(buf, "Drewniany ");
				}
				else
				{
					waga += 1.5 + (-0.1 + (float)((rand()%3)/10.0)); //1.4 - 1.6
					obrazenia += 14+rand()%3; //14-16
					strcat(buf, "Stalowy ");
				}
					
				strcat(buf, "Topór");
					
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 3+rand()%10; //3-12
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 3+rand()%10; //3-12
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 3+rand()%10; //3-12
						strcat(buf, " Charyzmy");
						break;
				}
				break;
			case 2: //dodawanie nazwy ³uku i modyfikacja wartoœci
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (Naostrzenie)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zu¿yty"
						strcat(buf, "Zu¿yty ");
						obrazenia -= 2+rand()%2; //-(2 - 3)
						break;
					case 2: //"Elastyczny"
						strcat(buf, "Elastyczny ");
						obrazenia += 2+rand()%2; //+(2 - 3)
						break;
				}
				
				//nie ma tu drugiego atrybutu
				waga += 0.6 + (-0.1 + (float)((rand()%3)/10.0)); //0.5 - 0.7
				obrazenia = 7+rand()%3; //7-9
				
				strcat(buf, "£uk");
					
				rand_atr = rand()%4; //losowanie drugiego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 3+rand()%10; //3-12
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 3+rand()%10; //3-12
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 3+rand()%10; //3-12
						strcat(buf, " Charyzmy");
						break;
				}
				break;
		}
		
		//dodawanie kategorii przedmiotu
		strcat(buf, ",Bron,");
		
		//dodawanie slotu przedmiotu
		strcat(buf, "Bron,");
		
		//dodawanie wagi przedmiotu
		sprintf(converted_int,"%.1f,", waga);
		strcat(buf, converted_int);
		
		//dodawanie stackowalnoœci przedmiotu
		strcat(buf,"False,");
		
		//dodawanie punktów pancerza przedmiotu
		itoa(pancerz,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów zdrowia przedmiotu
		itoa(zdrowie,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów many przedmiotu
		itoa(mana,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów obra¿eñ przedmiotu
		itoa(obrazenia,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów charyzmy przedmiotu
		itoa(charyzma,converted_int,10);
		strcat(buf,converted_int);
		
		//zakoñczenie linii i zapisanie przedmiotu do pliku
		strcat(buf,"\n\0");
		fwrite(&buf, strlen(buf), 1, file);
		
		id++;
	}
}


void generate_items()
{
	int item_amount = amount; //40% przedmiotów to zbroja
	while(id<=item_amount)
	{
		int rand_type = rand()%2; //losowanie typu przedmiotu u¿ytkowego
		int rand_atr; //zmienna dla wybierania rodzaju atrybutu przedmiotu u¿ytkowego
		float waga = 0.0;
		int pancerz = 0, zdrowie=0, mana=0, obrazenia=0, charyzma=0;
		char converted_int[16];
		itoa(id,converted_int,10);
		strcpy(buf,converted_int); //dodawanie id do bufora
		strcat(buf,",");
		switch(rand_type)
		{
			case 0: //mikstura
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (Wielkoœæ)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Ma³a"
						strcat(buf, "Ma³a ");
						waga -= 0.1;
						obrazenia -= 5 + rand()%3; //-(5 - 7)
						//to samo ka¿da inna statystyka, jako ¿e nie wiadomo jeszcze jaka to mikstura
						zdrowie = mana = charyzma = obrazenia;
						break;
					case 2: //"Du¿a"
						strcat(buf, "Du¿a ");
						waga += 0.1;
						obrazenia += 10 - rand()%3; //+(8 - 10)
						//to samo ka¿da inna statystyka, jako ¿e nie wiadomo jeszcze jaka to mikstura
						zdrowie = mana = charyzma = obrazenia;
						break;
				}
					
				//nie ma tu drugiego atrybutu
				waga += 0.2;
						
				strcat(buf, "Mikstura");
						
				rand_atr = rand()%5; //losowanie drugiego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //"Pancerza"
						pancerz += 9+rand()%3; //9-11
						zdrowie = mana = obrazenia = charyzma = 0; //wyzerowanie poprzednio zmniejszonych atrybutów niedotycz¹cych danej mikstury
						strcat(buf, " Pancerza");
						break;
					case 1: //"Zdrowia"
						zdrowie += 9+rand()%3; //9-11
						pancerz = mana = obrazenia = charyzma = 0; //wyzerowanie poprzednio zmniejszonych atrybutów niedotycz¹cych danej mikstury
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 9+rand()%3; //9-11
						pancerz = zdrowie = obrazenia = charyzma = 0; //wyzerowanie poprzednio zmniejszonych atrybutów niedotycz¹cych danej mikstury
						strcat(buf, " Many");
						break;
					case 3: //"Si³y"
						obrazenia += 9+rand()%3; //9-11
						pancerz = zdrowie = mana = charyzma = 0; //wyzerowanie poprzednio zmniejszonych atrybutów niedotycz¹cych danej mikstury
						strcat(buf, " Si³y");
						break;
					case 4: //"Charyzmy"
						charyzma += 9+rand()%3; //9-11
						pancerz = zdrowie = mana = obrazenia = 0; //wyzerowanie poprzednio zmniejszonych atrybutów niedotycz¹cych danej mikstury
						strcat(buf, " Charyzmy");
						break;
				}
				break;
			case 1: //strza³a
				rand_atr = rand()%3; //losowanie pierwszego atrybutu (Naostrzenie)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Têpa"
						strcat(buf, "Têpa ");
						obrazenia -= 2+rand()%2; //-(2 - 3)
						break;
					case 2: //"Naostrzona"
						strcat(buf, "Naostrzona ");
						obrazenia += 4+rand()%2; //+(4 - 5)
						break;
				}
					
				//nie ma drugiego atrybutu	
				waga = 0.1;
				obrazenia += 4+rand()%3; //4-6	
				strcat(buf, "Strza³a");
						
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 4+rand()%3; //4-6
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 4+rand()%3; //4-6
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 4+rand()%3; //4-6
						strcat(buf, " Charyzmy");
						break;
				}
				break;
			case 2: //olejek
				rand_atr = rand()%2; //losowanie pierwszego atrybutu (Naostrzenie)
				switch(rand_atr)
				{
					case 0: //brak
						break;
					case 1: //"Ulepszony"
						strcat(buf, "Ulepszony ");
						obrazenia += 5+rand()%2; //+(5 - 6)
						zdrowie = mana = charyzma = obrazenia; //to samo ka¿da inna statystyka, jako ¿e nie wiadomo jeszcze jaki to olejek
						waga += 0.1;
						break;
				}
					
				//nie ma drugiego atrybutu	
				waga += 0.1;	
				strcat(buf, "Olejek");
						
				rand_atr = rand()%4; //losowanie trzeciego atrybutu ("modyfikator")
				switch(rand_atr)
				{ //TODO: wartoœci pozmieniaæ
					case 0: //brak
						break;
					case 1: //"Zdrowia"
						zdrowie += 4+rand()%3; //4-6
						strcat(buf, " Zdrowia");
						break;
					case 2: //"Many"
						mana += 4+rand()%3; //4-6
						strcat(buf, " Many");
						break;
					case 3: //"Charyzmy"
						charyzma += 4+rand()%3; //4-6
						strcat(buf, " Charyzmy");
						break;
				}
				break;
		}
		
		//dodawanie kategorii przedmiotu
		strcat(buf, ",Przedmiot_Uzytkowy,");
		
		//dodawanie slotu przedmiotu
		strcat(buf, "Brak,");
		
		//dodawanie wagi przedmiotu
		sprintf(converted_int,"%.1f,", waga);
		strcat(buf, converted_int);
		
		//dodawanie stackowalnoœci przedmiotu
		strcat(buf,"True,");
		
		//dodawanie punktów pancerza przedmiotu
		itoa(pancerz,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów zdrowia przedmiotu
		itoa(zdrowie,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów many przedmiotu
		itoa(mana,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów obra¿eñ przedmiotu
		itoa(obrazenia,converted_int,10);
		strcat(buf,converted_int);
		strcat(buf,",");
		
		//dodawanie punktów charyzmy przedmiotu
		itoa(charyzma,converted_int,10);
		strcat(buf,converted_int);
		
		//zakoñczenie linii i zapisanie przedmiotu do pliku
		strcat(buf,"\n\0");
		fwrite(&buf, strlen(buf), 1, file);
		
		id++;
	}
}


int main(int argc, char* argv[])
{
	if(check_args(argc, argv)==0)
	{
		srand(time(NULL));
		int armor_amount = amount * armor_prc;
		int weapon_amount = amount * weapon_prc;
		int item_amount = amount * item_prc;
		file = fopen("przedmioty.csv", "wb");
		fwrite(&buf, strlen(buf), 1, file); //zapis pierwszej linijki
		generate_armor(armor_amount);
		generate_weapons(armor_amount, weapon_amount);
		generate_items();
		fclose(file);
	}
	return 0;
}
