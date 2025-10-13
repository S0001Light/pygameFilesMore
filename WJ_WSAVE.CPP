#include <stdio.h>
#include <stdlib.h>

FILE * fileA;
FILE * fileB;


int main()
{
    char zaa[80] = "";
    char zab[80] = "";
    char zac[80] = "";
    char zad[80] = "";
    char zae[80] = "";
    char zaf[80] = "";
    char zag[80] = "";
    char zah[80] = "";
    char zai[80] = "";
    char zaj[80] = "";

    printf("\nEnter 10 lines of word, no more than 80 each NO SPACES.\n\n");
    scanf("%s", zaa);
    scanf("%s", zab);
    scanf("%s", zac);
    scanf("%s", zad);
    scanf("%s", zae);
    scanf("%s", zaf);
    scanf("%s", zag);
    scanf("%s", zah);
    scanf("%s", zai);
    scanf("%s", zaj);

    printf("\nYou Typed:\n\n");
    printf("Line_1 : ");
    printf(zaa);
    printf("\n");
    printf("Line_2 : ");
    printf(zab);
    printf("\n");
    printf("Line_3 : ");
    printf(zac);
    printf("\n");
    printf("Line_4 : ");
    printf(zad);
    printf("\n");
    printf("Line_5 : ");
    printf(zae);
    printf("\n");
    printf("Line_6 : ");
    printf(zaf);
    printf("\n");
    printf("Line_7 : ");
    printf(zag);
    printf("\n");
    printf("Line_8 : ");
    printf(zah);
    printf("\n");
    printf("Line_9 : ");
    printf(zai);
    printf("\n");
    printf("Line_10 : ");
    printf(zaj);
    printf("\n\n");
    printf("The Machine Saved what you typed C:wjFILE1\n\nAPPENDS Jumbled to C:wjFILE2:\n\n");
    fileA = fopen("C:\WJFILE1.TXT", "w");
    fprintf(fileA, "\nYou Typed:\n\n");
    fprintf(fileA, "Line_1 : ");
    fprintf(fileA, zaa);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_2 : ");
    fprintf(fileA, zab);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_3 : ");
    fprintf(fileA, zac);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_4 : ");
    fprintf(fileA, zad);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_5 : ");
    fprintf(fileA, zae);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_6 : ");
    fprintf(fileA, zaf);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_7 : ");
    fprintf(fileA, zag);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_8 : ");
    fprintf(fileA, zah);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_9 : ");
    fprintf(fileA, zai);
    fprintf(fileA, "\n");
    fprintf(fileA, "Line_10 : ");
    fprintf(fileA, zaj);
    fprintf(fileA, "\n\n");
    fclose(fileA);
    fileB = fopen("C:\WJFILE2.TXT", "a");
    if(fileB == 0)
    {exit (0);}
    int i;
    for(i = 0; i < 100; i++)
    {
	if(i == 100);
            { break; }
	}
        int value1;
    	value1 = (rand() % 10) + 1;
    	int value2;
        value2 = (rand() % 10) + 1;
	int value3;
	value3 = (rand() % 10) + 1;
	int value4;
	value4 = (rand() % 10) + 1;
	int value5;
	value5 = (rand() % 10) + 1;
	int value6;
	value6 = (rand() % 10) + 1;
	int value7;
	value7 = (rand() % 10) + 1;
	int value8;
	value8 = (rand() % 10) + 1;
	int value9;
	value9 = (rand() % 10) + 1;
	int value10;
	value10 = (rand() % 10) + 1;

	int numeraL1;
	numeraL1 = 1;
	int numeral2;
	numeral2 = 2;
	int numeral3;
	numeral3 = 3;
	int numeral4;
	numeral4 = 4;
	int numeral5;
	numeral5 = 5;
	int numeral6;
	numeral6 = 6;
	int numeral7;
	numeral7 = 8;
	int numeral8;
	numeral8 = 8;
	int numeral9;
	numeral9 = 9;
	int numeral10;
	numeral10 = 10;
	fprintf(fileB, "----\n\n");
	if(value1 == numeraL1){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeraL1){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeraL1){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeraL1){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeraL1){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeraL1){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeraL1){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeraL1){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeraL1){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeraL1){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral2){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral2){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral2){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral2){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral2){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral2){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral2){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral2){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral2){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeral2){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral3){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral3){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral3){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral3){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral3){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral3){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral3){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral3){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral3){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeral3){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral4){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral4){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral4){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral4){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral4){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral4){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral4){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral4){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral4){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeral4){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral5){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral5){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral5){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral5){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral5){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral5){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral5){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral5){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral5){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeral5){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral6){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral6){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral6){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral6){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral6){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral6){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral6){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral6){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral6){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeral6){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral7){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral7){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral7){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral7){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral7){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral7){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral7){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral7){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral7){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeral7){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral8){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral8){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral8){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral8){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral8){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral8){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral8){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral8){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral8){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeral8){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral9){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral9){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral9){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral9){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral9){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral9){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral9){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral9){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral9){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");
	};
	if(value10 == numeral9){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};

	if(value1 == numeral10){
		fprintf(fileB, zaa);
		fprintf(fileB, "\n");
	};
	if(value2 == numeral10){
		fprintf(fileB, zab);
		fprintf(fileB, "\n");
	};
	if(value3 == numeral10){
		fprintf(fileB, zac);
		fprintf(fileB, "\n");
	};
	if(value4 == numeral10){
		fprintf(fileB, zad);
		fprintf(fileB, "\n");
	};
	if(value5 == numeral10){
		fprintf(fileB, zae);
		fprintf(fileB, "\n");
	};
	if(value6 == numeral10){
		fprintf(fileB, zaf);
		fprintf(fileB, "\n");
	};
	if(value7 == numeral10){
		fprintf(fileB, zag);
		fprintf(fileB, "\n");
	};
	if(value8 == numeral10){
		fprintf(fileB, zah);
		fprintf(fileB, "\n");
	};
	if(value9 == numeral10){
		fprintf(fileB, zai);
		fprintf(fileB, "\n");                         
	};
	if(value10 == numeral10){
		fprintf(fileB, zaj);
		fprintf(fileB, "\n");
	};                                                     
	
	printf("Finished.\n\n");
    	fclose(fileB);
        printf("FINISHED SUPPOSEDLY 100 TIMES OVER, and that all it prints, questionmark symbol, In one file");
        return 0;
	
}
       
