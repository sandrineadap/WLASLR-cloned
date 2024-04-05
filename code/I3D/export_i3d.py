########################################################################################
# Exports i3d model to a file called i3d_small.ptl
# Exported file is to be placed in the appropriate directory of the aslmala app project.
# From playtorch docs: https://playtorch.dev/docs/tutorials/prepare-custom-model/
########################################################################################

import torch
import torchvision 
from torch.utils.mobile_optimizer import optimize_for_mobile
from pytorch_i3d_torchOps import InceptionI3d
# from pytorch_i3d import InceptionI3d


model = InceptionI3d(400, in_channels=3)
# model = torchvision.models.mobilenet_v3_small(pretrained=True)
model.eval()

scripted_model = torch.jit.script(model)
optimized_model = optimize_for_mobile(scripted_model)
optimized_model._save_for_lite_interpreter("i3d_small.ptl")
# optimized_model._save_for_lite_interpreter("mobilenet_v3_small.ptl")

print("model successfully exported")