#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>
#include <sys/stat.h>

/*
[CAUTION] Compile this file with this command:
gcc -g mlite.c -lsqlite3 -o bin/mlite
*/
void get_line_number(char *mlocate_db, char *target, char* line);
void fill_txt_file(char *mlocate_db, char *target, char *text_file);
void human_readable_size(double size, char *output);
void create_db(sqlite3 *db);
char *get_filename_ext(const char *filename);
int main()
{
    // Define variables -> will be auto fetched from argv[]
    char *target     = "/home/amr";
    char *mlocate_db = "mlocate.db";
    char *mlocate_txt= "mlocate.txt";
    char *araneus_db = "araneus.db";

    // Generate text
    fill_txt_file(mlocate_db,target,mlocate_txt);

    // Read text line by line
    FILE *fp;
    char *line;
    size_t len = 0;
    ssize_t read;
    fp = fopen(mlocate_txt, "r");
    if (fp == NULL)
    {
        printf("Couldn't open %s\n", mlocate_txt);
        exit(EXIT_FAILURE);
    }

    // Setting file variables
    char last_directory[1024];
    char file_path[1024];
    char file_name[1024];
    // Setting file stats variable [to get size, modification and access time]
    struct stat st;

    // Setting file-details variables
    char file_size[32];

    // SQLite
    sqlite3 *db;
    sqlite3_stmt *sql_result;
    int rv = 0;
    char *err_msg = NULL;

	rv = sqlite3_open(araneus_db, &db);

	if (rv != SQLITE_OK)
	{
		printf("Failed to create/open Database: %s\n",araneus_db);
        sqlite3_close(db);
		exit(EXIT_FAILURE);
	}

    // Timestamp to be used by sqlite engine
    const char *timestamp = "DD-MM-YYYY HH:MM";

    // Insert statement:
    char command[4096] = "INSERT OR IGNORE INTO `files` (`name`,`path`,`size`,`mtime`,`atime`,`type`)"
    "VALUES(?,?,?,datetime(?,'unixepoch'),datetime(?,'unixepoch'),?);";
    // Create database / Empty current database
    create_db(db);

    // Setting optimisations
    rv = sqlite3_exec(db,"PRAGMA synchronous = OFF",0,0,&err_msg);
    rv = sqlite3_exec(db,"PRAGMA journal_mode = OFF",0,0,&err_msg);
    rv = sqlite3_exec(db,"PRAGMA temp_store = MEMORY",0,0,&err_msg);
    rv = sqlite3_exec(db,"PRAGMA page_size = 4096",0,0,&err_msg);
    rv = sqlite3_exec(db,"PRAGMA cache_size = 16384",0,0,&err_msg);
    rv = sqlite3_exec(db,"PRAGMA locking_mode = EXCLUSIVE",0,0,&err_msg);
	rv = sqlite3_exec(db,"BEGIN TRANSACTION",0,0,&err_msg);
    if (rv != SQLITE_OK)
    {
        printf("Failed to set optimisations\n");
        sqlite3_close(db);
		exit(EXIT_FAILURE);
    }
    // Looooooooooooooooop
    while((read = getline(&line,&len,fp)) != 0)
    {
        strtok(line,"\n"); // Remove \n from every line
        strcpy(file_name,line);
        if (line[0] == '/') // Directory
        {
            strcpy(last_directory,line); // copy this line to last directory
            strcpy(file_path,line); // copy this line to file_name
        }
        else
        {
            strcpy(file_path,last_directory);
            strcat(strcat(file_path,"/"),file_name); // Generate file path
        }
        stat(file_path,&st); // Get size, modification time and access time
        human_readable_size(st.st_size, file_size);
        rv = sqlite3_prepare_v2(db, command, -1, &sql_result, NULL);
        // Bind parameteres
        sqlite3_bind_text(sql_result,1,file_name,-1,NULL);
        sqlite3_bind_text(sql_result,2,file_path,-1,NULL);
        sqlite3_bind_text(sql_result,3,file_size,-1,NULL);
        sqlite3_bind_int64(sql_result,4,st.st_mtime);
        sqlite3_bind_int64(sql_result,5,st.st_atime);
        switch(st.st_mode & S_IFMT){
        case S_IFREG:
            sqlite3_bind_text(sql_result,6,get_filename_ext(file_name),-1,NULL);
            break;
        case S_IFDIR:
            sqlite3_bind_text(sql_result,6,"Directory",-1,NULL);
            break;
        default:
            sqlite3_bind_text(sql_result,6,"Unknown type",-1,NULL);
            break;
        }
        // Execute statement
        sqlite3_step(sql_result);
    }
    sqlite3_exec(db,"END TRANSACTION",0,0,&err_msg);
    sqlite3_close(db);
    fclose(fp);
    // Experimental 
    // remove(araneus_db);
    // remove(mlocate_txt);
    return 1;
}
void get_line_number(char *mlocate_db, char *target, char* line)
{
    const char *template_cmd = "strings %s | grep -n -m 2 %s | tail -n1 | cut -f1 -d:";
    char cmd_line[1024];
    sprintf(cmd_line,template_cmd,mlocate_db,target);
    
    FILE *fp = NULL;
    fp = popen(cmd_line, "r");
    if (fp == NULL)
    {
        printf("Sorry couldn't execute command %s\n", cmd_line);
        exit(EXIT_FAILURE);
    }
    fgets(line,sizeof(line)-5,fp);
    if (strlen(line) > 3)
    {
        printf("Coundn't get line number!\nCheck mlocate conifgurations.\n");
        exit(EXIT_FAILURE);
    }
    pclose(fp);
}
void fill_txt_file(char *mlocate_db, char *target, char *text_file)
{
    // Convert mlocate.db to mlocate.txt after sanitising headers
    char line_number[8];
    get_line_number(mlocate_db, target,line_number);
    // Create empty text file
    FILE *empty_file = NULL;
    empty_file = fopen(text_file, "w");
    if (empty_file == NULL)
    {
        printf("Couldn't create a new file!");
        exit(EXIT_FAILURE);
    }
    // Now it's time to fetch data from mlocate.db to text file
    char template_tail[128] = "strings %s | tail -n +%s > %s";
    char cmd_line[1024];
    sprintf(cmd_line,template_tail,mlocate_db,line_number,text_file);
    FILE *terminal = NULL;
    terminal = popen(cmd_line,"r");
    if (terminal == NULL)
    {
        printf("Sorry couldn't execute command %s\n", cmd_line);
        exit(EXIT_FAILURE);
    }
    fclose(empty_file);
    fclose(terminal);
}
void human_readable_size(double size, char *output) 
{
    if (size < 1024)
    {
        sprintf(output, "%g B", size);
    }
    else
    {
        int i = 0;
        const char* units[] = {"B", "kB", "MB", "GB", "TB"};
        while (size >= 1024) {
            size /= 1024;
            i++;
        }
        sprintf(output, "%.2f %s", size, units[i]);
    }
}
void create_db(sqlite3 *db)
{
    char *err_msg = 0;
    int rv;
    char *sql_statement = "DROP TABLE IF EXISTS `files`;"
    "CREATE TABLE IF NOT EXISTS `files`"
    "(`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
    "`name` TEXT, "
    "`path` TEXT UNIQUE,"
    "`size` TEXT,"
    "`mtime` TEXT, "
    "`atime` TEXT, "
    "`type` TEXT);";
	rv = sqlite3_exec(db,sql_statement,0,0,&err_msg);
	if (rv != SQLITE_OK)
    {
        printf("Couldn't execute sql:\n%s\n", sql_statement);
        sqlite3_close(db);
        exit(EXIT_FAILURE);
    }
}
char *get_filename_ext(const char *filename)
{
    char *dot = strrchr(filename, '.');
    if(!dot || dot == filename)
    {
        return "Unknown file type";
    }
    return dot + 1;
}
/*
References:
Concatenate strings in C https://stackoverflow.com/a/308712/7301680
Getting line number with grep https://stackoverflow.com/a/6958981/7301680
Getting file size https://stackoverflow.com/a/238609/7301680
Getting file Type https://stackoverflow.com/a/5309508/7301680
Convert size to human readable http://programanddesign.com/cpp/human-readable-file-size-in-c/
SQLite example : https://gist.github.com/jsok/2936764
Correct way to bind values in SQLite: http://www.adp-gmbh.ch/sqlite/bind_insert.html
SQLite optimisations expirement: https://stackoverflow.com/q/1711631/
SQLite quick Optimisations: https://forum.qt.io/post/106577
Force GCC to link libraries https://stackoverflow.com/a/32377586/7301680
*/