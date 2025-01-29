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
- Hips size in cm
- Dress size (EU)
- Shoes size (EU)
- Color of the hair
- Color of the eyes

For example, this is the vector corresponding to [Monica Bellucci](https://www.fashionmodeldirectory.com/models/monica_bellucci/) (🇮🇹):
```
Monica Bellucci,https://www.fashionmodeldirectory.com/models/monica_bellucci/,Italian,September 30 1964,175.0,90.0,61.0,90.0,36,40,Dark brown,Brown
```

In the dataset men and women are mixed. Differences in size and proportions between male and female body have been studied [2], hence we have been trying to distinguish the sexes of the models looking at the distribution of the collected data.

## Results
![Histograms](histograms.png)

|   | Minimum | Maximum | Average | Standard deviation |
| - |-------- | ------- | ------- | ------------------ |
| **Height** | [155 cm](https://www.fashionmodeldirectory.com/models/celine_joiris/)  | [198 cm](https://www.fashionmodeldirectory.com/models/dusty_lachowicz/) | 177.85 cm | 3.76 |
| **Bust** | [70 cm](https://www.fashionmodeldirectory.com/models/li_fuyao/)          | [120.5 cm](https://www.fashionmodeldirectory.com/models/lovisa_lager/)  | 83.45 cm  | 4.65 |
| **Waist** | [50 cm](https://www.fashionmodeldirectory.com/models/gabriella_buhlin/) | [111.0 cm](https://www.fashionmodeldirectory.com/models/ceval_omar/)    | 61.89 cm  | 4.55 |
| **Hips** | [74 cm](https://www.fashionmodeldirectory.com/models/luis_liranzo/)      | [138.5 cm](https://www.fashionmodeldirectory.com/models/lovisa_lager/)  | 88.60 cm  | 3.06 |
| **Bust to waist ratio** | [75/83 = 0.90](https://www.fashionmodeldirectory.com/models/baye_mor+seye/)   | [85/50 = 1.70](https://www.fashionmodeldirectory.com/models/gabriella_buhlin/) | 1.35 | 0.07 |
| **Hips to waist ratio** | [84/86 = 0.98](https://www.fashionmodeldirectory.com/models/dakota_martinez/) | [88/50 = 1.76](https://www.fashionmodeldirectory.com/models/gabriella_buhlin/) | 1.44 | 0.08 |

![Heatmap](heatmap.png)

## References
1. Topirceanu, A., & Udrescu, M. (2015, September). *FMNet: Physical Trait Patterns in the Fashion World*. In Network Intelligence Conference (ENIC), 2015 Second European (pp. 25-32). IEEE.
2. Robinette, K.M., Churchill, T., & Mcconville, J.T. (1979). [*A Comparison of Male and Female Body Sizes and Proportions*](https://apps.dtic.mil/sti/pdfs/ADA074807.pdf).
