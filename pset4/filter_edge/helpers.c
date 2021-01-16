#include "helpers.h"
#include <math.h>
#include <stdlib.h>

int *box_edge(int i, int j, int height, int width, RGBTRIPLE image[height][width]);
float *box_blur(int lin, int col, int height, int width, RGBTRIPLE image[height][width]);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float mean;
    BYTE byte_mean;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            mean = (float)(image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3;
            byte_mean  = round(mean);
            image[i][j].rgbtBlue = byte_mean;
            image[i][j].rgbtGreen = byte_mean;
            image[i][j].rgbtRed = byte_mean;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE swap[height][width];
    for (int j = 0, gap = width - 1; j < width / 2; j++, gap--)
    {
        for (int i = 0; i < height; i++)
        {
            swap[i][j] = image[i][gap];
            image[i][gap] = image[i][j];
            image[i][j] = swap[i][j];
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Another 2D array must be created with all blurred pixels from original image
    // After all pixels have been processed, then it can replace the original pixels
    // on [image]
    RGBTRIPLE blurred_image[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float *blur = box_blur(i, j, height, width, image);
            blurred_image[i][j].rgbtBlue = round(blur[0] / blur[3]);
            blurred_image[i][j].rgbtGreen = round(blur[1] / blur[3]);
            blurred_image[i][j].rgbtRed = round(blur[2] / blur[3]);
            free(blur);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blurred_image[i][j];
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE edge_image[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int *edge = box_edge(i, j, height, width, image);
            edge_image[i][j].rgbtBlue = edge[0];
            edge_image[i][j].rgbtGreen = edge[1];
            edge_image[i][j].rgbtRed = edge[2];
            free(edge);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = edge_image[i][j];
        }
    }
    return;
}

int *box_edge(int i, int j, int height, int width, RGBTRIPLE image[height][width])
{
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    float *sum_x = calloc(1, 3 * sizeof(float));
    float *sum_y = calloc(1, 3 * sizeof(float));

    for (int h = 0, lin = -1; lin < 2; lin++, h++)
    {
        for (int w = 0, col = -1; col < 2; col++, w++)
        {
            if (i + lin >= 0 && i + lin < height && j + col >= 0 && j + col < width)
            {
                sum_x[0] += image[i + lin][j + col].rgbtBlue * Gx[h][w];
                sum_x[1] += image[i + lin][j + col].rgbtGreen * Gx[h][w];
                sum_x[2] += image[i + lin][j + col].rgbtRed * Gx[h][w];

                sum_y[0] += image[i + lin][j + col].rgbtBlue * Gy[h][w];
                sum_y[1] += image[i + lin][j + col].rgbtGreen * Gy[h][w];
                sum_y[2] += image[i + lin][j + col].rgbtRed * Gy[h][w];
            }
            else
            {
                sum_x[0] += 0 * Gx[h][w];
                sum_x[1] += 0 * Gx[h][w];
                sum_x[2] += 0 * Gx[h][w];

                sum_y[0] += 0 * Gy[h][w];
                sum_y[1] += 0 * Gy[h][w];
                sum_y[2] += 0 * Gy[h][w];
            }
        }
    }

    int *sobel_array = malloc(3 * sizeof(float));
    float sobel;

    for (int k = 0; k < 3; k++)
    {
        sobel = sqrt(pow(sum_x[k], 2) + pow(sum_y[k], 2));
        if (sobel > 255)
        {
            sobel_array[k] = 255;
        }
        else
        {
            sobel_array[k] = round(sobel);
        }
    }

    free(sum_x);
    free(sum_y);
    return sobel_array;
}


// the last element of [sum] stores how many sums were realized,
// so it can be used to calculate the mean
float *box_blur(int i, int j, int height, int width, RGBTRIPLE image[height][width])
{
    float *sum = calloc(1, 4 * sizeof(float));
    for (int lin = -1; lin < 2; lin++)
    {
        for (int col = -1; col < 2; col++)
        {
            if (i + lin >= 0 && i + lin < height && j + col >= 0 && j + col < width)
            {
                sum[0] += image[i + lin][j + col].rgbtBlue;
                sum[1] += image[i + lin][j + col].rgbtGreen;
                sum[2] += image[i + lin][j + col].rgbtRed;
                sum[3]++;
            }
        }
    }
    return sum;
}