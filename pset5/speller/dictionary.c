// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table (between 1.5 and 2 * [size of dictionary])
// N = 143091 or 214637
const unsigned int N = 214637;

/* Nearest prime number close and bigger than 2 * N

Doubling N and choosing a prime number bigger than that
provide better hash value distribution, reducing collision
and lookup time in the table
*/
const unsigned int mod = 214639; // mod = 143093 or 214639

// Hash table
node *table[N];

// Recursive function to free nodes in the hashtable
void freelink(node *word_node)
{
    if (word_node == NULL)
        ;
    else
    {
        freelink(word_node->next);
        free(word_node);
    }
}

// Hashes word to a number
/*
    hash function obtained from: http://www.cse.yorku.ca/~oz/hash.html
    Author: Dan Bernstein (aka djb2)
    I chose this function cause it's short and seems fast according to some posts found below
    https://stackoverflow.com/questions/7700400/whats-a-good-hash-function-for-english-words
    https://stackoverflow.com/questions/7666509/hash-function-for-string
    I made a adjustment in the return value, since it must return a hash based in the size of the hash table
*/
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return (hash % mod);
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // convert word to lowercase
    char word_lowercase[LENGTH + 1];
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        word_lowercase[i] = tolower(word[i]);
    }
    // add the null character to set as string
    word_lowercase[len] = '\0';

    // check if word hash matches a empty bucket
    int hash_value = hash(word_lowercase);
    if (table[hash_value] == NULL)
    {
        return false;
    }

    // if is a non-empty bucket, perform linear search for the word on it

    /* It's possible that a word hash matches a dict hash, but the word
    is not in the dictionary. It's necessary to perform a linear search
    in the table chain to find it */
    node *lsearch = table[hash_value];

    // strcmp return 'false' for a match
    while (strcmp(word_lowercase, lsearch->word) && lsearch->next != NULL)
    {
        lsearch = lsearch->next;
    }

    //if no word is found the in bucket, compare != 0
    if (strcmp(word_lowercase, lsearch->word) == 0)
    {
        return true;
    }
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");

    if (dict == NULL)
    {
        return false;
    }

    node *new_word_node = NULL;
    char *str = NULL;
    unsigned int hash_value;
    while (1)
    {
        // create a 'node' to store words in the dictionary table
        new_word_node = malloc(sizeof(node));

        // check for available space for a 'node'
        if (new_word_node == NULL)
        {
            printf("Could not create a node.\n");
            return false;
        }

        // assign a word from 'dict' to 'new_word_node->word' and create a alias for it
        str = fgets(new_word_node->word, LENGTH + 1, dict);
        // when 'fgets' reaches EOF, str == NULL
        if (str == NULL)
        {
            // on the last run, a new node is allocated but never used, so it needs to be freed
            free(new_word_node);
            break;
        }

        // removes '\n' that 'fgets' adds as last character in 'new_word_node->word'
        if (str[strlen(str) - 1] == '\n')
        {
            str[strlen(str) - 1] = '\0';
        }

        // remove any address 'next' is pointing to
        new_word_node->next = NULL;

        // get a hash value from 'str'
        hash_value = hash(str);

        if (table[hash_value] == NULL)
        {
            // if hashtable is empty in that bucket, assign a 'node' to it
            table[hash_value] = new_word_node;
        }
        else
        {
            /* puts the new 'node' on the top of the bucket, and keep pushing
            old items to the end;
            */
            new_word_node->next = table[hash_value];
            table[hash_value] = new_word_node;
        }
    }

    // close file after filling the hash table
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    unsigned int words = 0;
    node *lsearch = NULL;

    for (int i = 0; i < N; i++)
    {
        lsearch = table[i];
        if (lsearch != NULL)
        {
            // count each word in the linked-list attached to a table[index]
            while (lsearch != NULL)
            {
                words++;
                lsearch = lsearch->next;
            }
        }
    }

    return words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        freelink(table[i]);
    }
    return true;
}
