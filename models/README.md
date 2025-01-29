# Models

We have implemented a python3 script based on our humble scraping library to retrieve informations from the [Fashion Model Directory](https://www.fashionmodeldirectory.com/) (FMD). A similar work have been made in [1].

## Methodology
To run the script:
```
python3 fashionmodeldirectory.py
```

It will retrieve data from more than 15 thousand personal records (as of 2025) and look for simple inconsistencies. When values are unavailable or wrong, `NA` is written. On our machine it run for about 4 hours.

The retrieved data are saved in .csv form. They are:

- Name and surname of the model
- FMD page
- Nationality
- Birth date
- Height in cm
- Bust size in cm
- Waist size in cm
- Hip size in cm
- Dress size (EU)
- Shoes size (EU)
- Color of the hair
- Color of the eyes

For example, this is the vector corresponding to [Monica Bellucci](https://www.fashionmodeldirectory.com/models/monica_bellucci/) (🇮🇹):
```
Monica Bellucci,https://www.fashionmodeldirectory.com/models/monica_bellucci/,Italian,September 30 1964,175.0,90.0,61.0,90.0,36,40,Dark brown,Brown
```

In the dataset men and women are mixed. Differences in size and proportions between male and female body have been studied [2], hence we have been trying to distinguish the sexes of the models looking at the distribution of the collected data.

## References
1. Topirceanu, A., & Udrescu, M. (2015, September). *FMNet: Physical Trait Patterns in the Fashion World*. In Network Intelligence Conference (ENIC), 2015 Second European (pp. 25-32). IEEE.
2. Robinette, K.M., Churchill, T., & Mcconville, J.T. (1979). [*A Comparison of Male and Female Body Sizes and Proportions*](https://apps.dtic.mil/sti/pdfs/ADA074807.pdf).
