#include <stdio.h>
#include <stdlib.h>
#define PI 3.14159265358979323846
#include <math.h>
#include <string.h>

struct applicant{
    char name[64];
    float score;
    char pref[64];
    int date;
    struct applicant* next; 
    char *assignment;
};

struct org{
    char name[64];
    int index;
    int *spots;
};

struct applicant* newapplicant(char name[], float score, char pref[], int date){
    struct applicant* piz = (struct applicant*) malloc (sizeof(struct applicant));
    piz->next=NULL;
    strcpy(piz->name, name);
    piz->score=score;
    strcpy(piz->pref, pref);
    piz->date=date;
    piz->assignment=NULL;
    return piz;
}

struct org* neworg(char name[], int index, int *spots){
    struct org* piz = (struct org*) malloc (sizeof(struct org));
    strcpy(piz->name, name);
    piz->index=index;
    piz->spots=spots;
    return piz;
}

struct applicant* applicantlist(char file[]){
    FILE *pizfile;
    
    char open[64];
    pizfile=fopen(file, "r");

    char line[64];
    int recentnum;
    int count=0;
    int head=0;
    struct applicant* first = NULL;
    struct applicant* pront;
    int loop=1;

    while (loop==1){
        struct applicant* current;
        struct applicant* hop;
        struct applicant* temp;
        char name[64];
        float score;
        char pref[64];
        char *token;
        int date;
        count++;
        if (fgets(line, 64, pizfile) == NULL){
            break;
        }
        
        

        token = strtok(line, ",");
        if (strcmp(token, "END")==0){
            break;
        }

        strcpy(name, token);
        token = strtok(NULL, ",");
        score = atof(token);
        token = strtok(NULL, ",");
        date = atoi(token);
        token = strtok(NULL, ",");
        strcpy(pref, token);
        
        if (head==0){
            first = newapplicant(name, score, pref, date);
            current=first;
            head=1;
        }
        else{
            temp=first;
            while (temp->next!=NULL){
                temp=temp->next;
            }

            struct applicant* newapplicant = (struct applicant*) malloc(sizeof(struct applicant));
            if (newapplicant == NULL){
                // Handle the error gracefully
                printf("Not enough memory to allocate new applicant\n");
                return NULL;
            }

            strcpy(newapplicant->name, name);
            newapplicant->score=score;
            strcpy(newapplicant->pref, pref);
            newapplicant->date=date;

            (*temp).next=newapplicant;
        }
    }
    fclose(pizfile);
    return first;
}

float appcmp(struct applicant* a, struct applicant* b){
    if (a->score!=b->score){
        return (a->score-b->score);
    }
    else{
        return (a->date-b->date);
    }
}

void remove(struct applicant* head, struct applicant* rem) { 
    struct applicant* current = head;
    while (current->next!=rem){
        current=current->next;
    }
    struct applicant* temp = rem->next;
    current->next=temp;
}


int main(int argc, char* argv[]){ //might have numbers assigned with each org, number of candidates. As we assign subtract from until zero. 2 csv's inputted
    char file[64];
    char orgz[64];
    int numorgs;
    /*
    if (argc!=2 || sscanf(argv[1], "%s", file)==0){
        printf("SYNTAX: ApplicantFile <FILE_NAME>\n");
        return EXIT_SUCCESS;
    }
    */
    
    sscanf(argv[1], "%s", file);
    sscanf(argv[2], "%s", orgz);
    sscanf(argv[3], "%d", &numorgs);

    FILE *orgfile;
    char open[64];
    orgfile=fopen(orgz, "r");
    char line[64];
    int spots[numorgs];

    struct org* orgarray[8*numorgs];
    for (int i=0; i<numorgs; i++){
        char *token;
        char name[64];
        
        if (fgets(line, 64, orgfile) == NULL){
            break;
        }

        token = strtok(line, ",");
        if (strcmp(token, "END")==0){
            break;
        }

        strcpy(name, token);
        token = strtok(NULL, ",");
        spots[i] = atof(token);
        orgarray[i]=neworg(name, i, spots+i);
        //printf("%s %d\n", orgarray[i]->name, *(orgarray[i]->spots));

    }
    char waitlist[]="waitlist";





    struct applicant* head = applicantlist(file);

    //in sorting, assess if the values of each int is 0

    struct applicant* temp = head;
    
    while (temp!=NULL){
        struct applicant* max = head;
        struct applicant* current = head;
        char *preftok;
        int choice;
        int match=0;
        while (current!=NULL){
            if (appcmp(max, current)<0){
                max=current;
            }
            current=current->next;
            
        }
        if (max==head && head->next!=NULL){
            head=head->next;
            
            preftok = strtok(max->pref, ";");
            while (preftok!=NULL){
                choice = atoi(preftok);
                
                if (*(orgarray[choice]->spots)!=0){
                    //printf("%s spots: %d\n", orgarray[choice]->name, *(orgarray[choice]->spots));
                    max->assignment=orgarray[choice]->name;
                    *(orgarray[choice]->spots)+=(-1);
                    match=1;
                    break;
                    
                }
                preftok = strtok(NULL, ";");
            }
            if (match==0){
                max->assignment=waitlist;
            }
            printf("Name: %7s Date Submitted: %7d Score: %7f Assignment: %7s\n", max->name, max->date, max->score, max->assignment);

            
        }
        else if (max==head && head->next==NULL){
            
            preftok = strtok(max->pref, ";");
            while (preftok!=NULL){
                
                choice = atoi(preftok);
                
                if (*(orgarray[choice]->spots)!=0){
                    //printf("%s spots: %d\n", orgarray[choice]->name, *(orgarray[choice]->spots));
                    max->assignment=orgarray[choice]->name;
                    *(orgarray[choice]->spots)+=(-1);
                    match=1;
                    break;
                    
                }
                preftok = strtok(NULL, ";");
            }
            if (match==0){
                max->assignment=waitlist;
            }
            printf("Name: %7s Date Submitted: %7d Score: %7f Assignment: %7s\n", max->name, max->date, max->score, max->assignment);
            break;
        }
        else{
            
            
            preftok = strtok(max->pref, ";");
            while (preftok!=NULL){
                choice = atoi(preftok);
                
                if (*(orgarray[choice]->spots)!=0){
                    //printf("%s spots: %d\n", orgarray[choice]->name, *(orgarray[choice]->spots));
                    max->assignment=orgarray[choice]->name;
                    *(orgarray[choice]->spots)+=(-1);
                    match=1;
                    
                    break;
                    
                }
                preftok = strtok(NULL, ";");
            }
            if (match==0){
                max->assignment=waitlist;
            }
            printf("Name: %7s Date Submitted: %7d Score: %7f Assignment: %7s\n", max->name, max->date, max->score, max->assignment);
            remove(head, max);
        }
        
        
    }
    
    
    return EXIT_SUCCESS;

}
