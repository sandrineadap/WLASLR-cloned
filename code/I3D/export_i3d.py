########################################################################################
# Exports i3d model to a file called i3d_small.ptl
# Exported file is to be placed in the appropriate directory of the aslmala app project.
# From playtorch docs: https://playtorch.dev/docs/tutorials/prepare-custom-model/
########################################################################################

import torch
import torchvision 
from torch.utils.mobile_optimizer import optimize_for_mobile

model = 