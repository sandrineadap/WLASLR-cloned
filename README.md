*This repository was cloned from Dongxu Li et al.'s [WLASL repository](https://github.com/dxli94/WLASL), whose dataset was made open source for research purposes. This project investigates the I3D model's usability for a mobile application. A demo of the mobile app we've developed so far, called Sign&#8226;a&#8226;Mander, can be found [here](https://drive.google.com/file/d/1EyIwe2gwZ9dp2kES_Tdl19bG3JTf5Vj1/view?usp=sharing).*

When you clone the repo, you will need to download a few zip files for the I3D model to work.

[archived](https://drive.google.com/file/d/1edscHp48Co5DAJKla3UO_gITCBKh0VU2/view?usp=sharing) - Put this folder inside the I3D folder. It has the weights for asl10 to asl2000.

[weights](https://drive.google.com/file/d/1cHsbj_FnhkQQrcy_hYSn3UHNf2eifAAt/view?usp=sharing) - Also put this folder inside the I3D folder. These are the "I3D weights pre-trained Kinetics" in the original README file. It's referenced in the `def ensemble` function in the predict, test, and train I3D files, but according to README-WLASL.md, it is used for training. 

I also downloaded the entire dataset via Kaggle: [https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed](https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed).

Please refer to the original repository's README, included in this repo as README-WLASL.md for additional instructions.
