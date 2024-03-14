When you clone the repo, you will need to download a few zip files for the I3D model to work.

[archived](https://drive.google.com/file/d/1edscHp48Co5DAJKla3UO_gITCBKh0VU2/view?usp=sharing){:target="_blank"} - Put this folder inside the I3D folder. It has the weights for asl10 to asl2000.

[weights](https://drive.google.com/file/d/1cHsbj_FnhkQQrcy_hYSn3UHNf2eifAAt/view?usp=sharing){:target="_blank"} - These are the "I3D weights pre-trained Kinetics" in the original README file. It's referenced in the `def ensemble` function in the predict, test, and train I3D files, but according to the README its used for training. 