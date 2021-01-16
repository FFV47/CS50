#include "helpers.h"
#include <math.h>
#include <stdlib.h>

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

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed, sepiaGreen, sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaRed = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            sepiaGreen = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            sepiaBlue = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtBlue = round(sepiaBlue);
            image[i][j].rgbtGreen = round(sepiaGreen);
            image[i][j].rgbtRed = round(sepiaRed);
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